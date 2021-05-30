# Copyright (C) 2021 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov, Christian Menard

import time

from mocasin.simulate.application import RuntimeDataflowApplication
from mocasin.simulate.manager import RuntimeManager
from mocasin.tetris.job_request import JobRequestStatus


class RuntimeTetrisManager(RuntimeManager):
    """Runtime Tetris Manager.

    The runtime tetris manager is used in the multi-application simulations, it
    manages the (real-time) applications and distribute resource among them.
    To start the applications, the method `start_applications` should be called.
    Tetris attempts to generate the schedule, and if successful, the
    applications are accepted, otherwise they are rejected.

    The generated schedule could be inaccurate due to system contentions. In
    this case the manager tracks the state of the started applications, and
    update the Tetris's internal state. If the application finished earlier than
    expected, the generated schedule is adjusted. If the application's execution
    time was underestimated, the runtime manager keeps it running assuming it
    needs a short time to finish.

    Args:
        resource_manager (ResourceManager): the resource manager
        system (System): the system
    """

    def __init__(self, resource_manager, system):
        super().__init__(system)
        self.resource_manager = resource_manager

        # New applications
        self._new_applications = []

        # keep track of runtime applications
        # {(request: RuntimeDataflowApplication)}
        self._runtime_applications = {}
        # keep track of all finished events
        self._finished_events = []

        # an event indicating that new schedule need to be generated
        self._request_generate_schedule = self.env.event()

    @property
    def name(self):
        """The runtime manager name."""
        return "Tetris Manager"

    def run(self):
        """Start a simpy process modelling the actual resource manager."""
        self._log.info("Starting up")

        while True:
            # wait until there are mapping segments or we should shut down
            yield self.env.any_of(
                [self._request_generate_schedule, self._request_shutdown]
            )

            # break out of the loop if we are supposed to shutdown
            if self._request_shutdown.triggered:
                break

            # otherwise, new schedule is requested to generate
            assert self._request_generate_schedule.triggered
            # reinitialize the event
            self._request_generate_schedule = self.env.event()

            # Generate new schedule
            self._generate_schedule()

            # Note: We probably should also model delays here which Tetris
            # needs to actually find mappings.

            # while schedule is active
            while self.resource_manager.schedule:
                # apply mappings as specified in the first schedule's segment
                self._handle_mapping_segment()
                segment = self.resource_manager.schedule.segments()[0]
                # wait until the end of the segment or until we are interrupted
                # by new segments
                yield self.env.any_of(
                    [
                        self.env.timeout(segment.duration * 1000000000),
                        self._request_generate_schedule,
                    ]
                )

                # break out of the for loop if new segments where provided and
                # continue in the top of the while loop
                if self._request_generate_schedule.triggered:
                    break

                # Update the state of resource manager
                self.resource_manager.advance_segment()

                # Check if any application was finished before it is expected
                self._clean_finished_applications()

        # wait for all applications to terminate
        yield self.env.all_of(self._finished_events)

        self._log.info("Shutting down")

    def start_applications(self, graphs, traces, pareto_fronts, timeouts):
        """Start new applications.

        The runtime manager expects arguments graphs, traces, pareto fronts and
        timeouts  be lists of the equal size.
        """
        self._log.debug(f"Starting {len(graphs)} application")

        for tup in zip(graphs, traces, pareto_fronts, timeouts):
            self._new_applications.append(tup)

        assert not self._request_generate_schedule.triggered
        self._request_generate_schedule.succeed()

    def _generate_schedule(self):
        self.resource_manager.advance_to_time(self.env.now / 1000000000.0)
        self._clean_finished_applications()
        num_prev = len(self._runtime_applications)

        # Register new requests at the resource manager
        requests = []
        for tup in self._new_applications:
            graph, trace, pareto, timeout = tup
            request = self.resource_manager.new_request(
                graph, pareto, timeout=timeout
            )
            requests.append((request, trace))

        # Reset the list of new applications
        self._new_applications.clear()

        # Generate the schedule
        start = time.process_time()
        self.resource_manager.generate_schedule()
        scheduling_time = time.process_time() - start

        new_apps = {}
        for request, trace in requests:
            graph = request.app
            entry = self.statistics.new_application(
                graph, arrival=self.env.now, deadline=request.deadline
            )
            if request.status == JobRequestStatus.ACCEPTED:
                self._log.debug(f"Application {graph.name} is accepted")
                app = self._create_runtime_application(request, trace)
                new_apps.update({request: app})
                entry.accepted = True
            elif request.status == JobRequestStatus.REFUSED:
                self._log.debug(f"Application {graph.name} is rejected")
                entry.accepted = False
            else:
                raise ValueError(f"Unexpected status {request.status}")

        self._runtime_applications.update(new_apps)

        # Save the information about the applications and activations
        self._update_statistics()
        self.statistics.new_activation(
            self.env.now,
            len(requests),
            len(new_apps),
            num_prev,
            scheduling_time,
        )

    def _create_runtime_application(self, request, trace):
        # TODO: Deadlines are not supported, support them.
        # See Issue #109
        graph = request.app
        return RuntimeDataflowApplication(
            name=graph.name, graph=graph, app_trace=trace, system=self.system
        )

    def _clean_finished_applications(self):
        """Clean finished applications."""
        for request, app in list(self._runtime_applications.items()):
            if app.is_finished():
                if request.status != JobRequestStatus.FINISHED:
                    self._log.debug(
                        f"Application {request.app.name} was already finished, "
                        f"modeled current cratio "
                        f"{self.resource_manager.requests[request].cratio:.4f}"
                    )
                    self.resource_manager.finish_request(request)
                self._runtime_applications.pop(request)

    def _get_modeled_active_requests(self):
        """Get active requests from the resource manager."""
        return list(
            filter(
                lambda r: r.status != JobRequestStatus.FINISHED,
                self._runtime_applications.keys(),
            )
        )

    def _get_actual_active_requests(self):
        """Return the requests of running applications in the system.

        Unlike `_get_modeled_active_requests()`, this function only checks thei
        current status of the runtime applications.

        Returns: a list of requests.
        """
        # TODO: remove this function
        result = []
        for request, app in self._runtime_applications.items():
            assert not app.is_finished()
            result.append(request)
        return result

    def _handle_mapping_segment(self):
        self._log.debug("Start processing a new segment")
        # Start all new apps and keep events indicating when the app finished
        assert self.resource_manager.schedule
        segment = self.resource_manager.schedule.segments()[0]
        self._log.debug(segment.to_str())
        remaining_modeled = set(self._get_modeled_active_requests())
        remaining_actual = set(self._get_actual_active_requests())

        # Handle the jobs scheduled in the segment
        for job_segment in segment.jobs():
            request = job_segment.request
            remaining_modeled.remove(request)
            remaining_actual.remove(request)
            app = self._runtime_applications[request]
            if app.is_new():
                # the application is not yet started
                finished = self.env.process(app.run(job_segment.mapping))
                self._finished_events.append(finished)
            elif app.is_running():
                # the application is  running
                app.update_mapping(job_segment.mapping)
            elif app.is_paused():
                # the applcation is paused
                app.resume(mapping=job_segment.mapping)
            else:
                raise RuntimeError(
                    f"Unexpected state of the application {app.graph.name}"
                )

        # Handle the case when the active request is not in the schedule
        for request in remaining_modeled:
            remaining_actual.remove(request)
            app = self._runtime_applications[request]
            if app.is_new() or app.is_paused():
                # the application is paused or not yet started, do nothing
                continue
            # pause the application
            app.pause()

        # TODO: Handle the case when the job's execution time was underestimated
        for request in remaining_actual:
            app = self._runtime_applications[request]
            cratio = app.get_progress()
            self._log.warning(
                f"Application {request.app.name} is modeled as finished, but "
                f"it is still running (cratio = {cratio:.4f})"
            )

    def _update_statistics(self):
        """Update application statistics.

        Update the expected end time of the applications. The method should be
        called after new schedule is generated.
        """
        schedule = self.resource_manager.schedule
        # Update accepted tasks
        if schedule:
            for request, segments in schedule.per_requests().items():
                assert segments[-1].finished
                expected_end_time = segments[-1].end_time
                entry = self.statistics.find_application(request.app.name)
                assert entry.accepted
                entry.expected_end_time = expected_end_time * 1000000000.0

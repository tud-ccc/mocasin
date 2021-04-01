# Copyright (C) 2021 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov, Christian Menard

import logging

from mocasin.simulate.adapter import SimulateLoggerAdapter
from mocasin.tetris.job_request import JobRequestStatus


log = logging.getLogger(__name__)


class RuntimeResourceManager:
    def __init__(self, resource_manager, system):
        self.resource_manager = resource_manager
        self.system = system

        # a special logger that allows printing timestamped messages
        self._log = SimulateLoggerAdapter(
            log, "Runtime Resource Manager", self.env
        )

        # New applications
        self._new_applications = []

        # keep track of runtime applications
        # {(request: RuntimeDataflowApplication)}
        self._runtime_applications = {}
        # keep track of all events indicating when an app finished
        # {(request: event)}
        self._finished_events = {}

        # an event indicating that new schedule need to be generated
        self._request_generate_schedule = self.env.event()
        # an event indicating that tetris should shut down
        self._request_shutdown = self.env.event()

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
                self._check_finished_applications()

        # wait for all applications to terminate
        yield self.env.all_of(self._finished_events.values())

        self._log.info("Shutting down")

    def _check_finished_applications(self):
        """Check whether any application was finished."""
        requests = self._get_modeled_active_requests()
        for request in requests:
            if request not in self._finished_events:
                continue
            finished = self._finished_events[request]
            if finished.triggered:
                self._log.debug(
                    f"Application {request.app.name} was already finished, "
                    f"modeled current cratio "
                    f"{self.resource_manager.requests[request].cratio:.4f}"
                )
                self.resource_manager.finish_request(request)

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
        result = []
        for request, app in self._runtime_applications.items():
            if app.is_new():
                result.append(request)
                continue
            # for uknown to me reason, the application might already finish, but
            # app.is_finished will be false, checking finished event
            finished = self._finished_events[request]
            if not finished.triggered:
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
                self._finished_events.update({request: finished})
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

    def shutdown(self):
        """Terminate Tetris.

        Tetris will not stop immediately but wait until all currently running
        applications terminate.
        """
        self._log.debug("Shutdown was requested")
        self._request_shutdown.succeed()

    @property
    def env(self):
        """The simpy environment."""
        return self.system.env

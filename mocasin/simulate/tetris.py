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

        # keep track of all running applications
        # keys = request, values = RuntimeDataflowApplication
        self._running_applications = {}

        # a special logger that allows printing timestamped messages
        self._log = SimulateLoggerAdapter(
            log, "Runtime Resource Manager", self.env
        )

        # an event indicating that tetris should shut down
        self._request_shutdown = self.env.event()
        # an event indicating that there are new mapping segments
        self._updated_segments = self.env.event()

        # a dict to keep track of all events indicating when an app finished
        self._finished_events = {}

    def run(self):
        """Start a simpy process modelling the actual resource manager."""
        self._log.info("Starting up")

        while True:
            # wait until there are mapping segments or we should shut down
            yield self.env.any_of(
                [self._updated_segments, self._request_shutdown]
            )

            # break out of the loop if we are supposed to shutdown
            if self._request_shutdown.triggered:
                break

            # otherwise, there are some new segments to run
            assert self._updated_segments.triggered
            # reinitialize the event
            self._updated_segments = self.env.event()

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
                        self._updated_segments,
                    ]
                )

                # TODO: Handle the case when the job should finish by the end of
                # the segment but it is not yet finished. Not trivial.

                # break out of the for loop if new segments where provided and
                # continue in the top of the while loop
                if self._updated_segments.triggered:
                    break
                # Update the state of resource manager
                self.resource_manager.advance_segment()

        # wait for all applications to terminate
        yield self.env.all_of(self._finished_events.values())

        self._log.info("Shutting down")

    def _handle_mapping_segment(self):
        self._log.debug("Start processing a new segment")
        # Start all new apps and keep events indicating when the app finished
        assert self.resource_manager.schedule
        segment = self.resource_manager.schedule.segments()[0]
        remaining = set(self._running_applications.keys())
        for job_segment in segment.jobs():
            remaining.remove(job_segment.request)
            app = self._running_applications[job_segment.request]
            if job_segment.request not in self._finished_events:
                finished = self.env.process(app.run(job_segment.mapping))
                self._finished_events.update({job_segment.request: finished})
            else:
                app.update_mapping(job_segment.mapping)

        # TODO: Handle the case when the job is suspended
        for r in remaining:
            if r.status != JobRequestStatus.FINISHED:
                print(r.to_str())
                print(segment.to_str())
                raise NotImplementedError()

        # TODO: Handle the case when the job's execution time was underestimated

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

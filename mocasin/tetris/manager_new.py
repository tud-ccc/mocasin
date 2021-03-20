# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import logging
import time

from mocasin.tetris.job_request import JobRequestStatus
from mocasin.tetris.job_state import Job
from mocasin.tetris.schedule import Schedule, TIME_EPS

log = logging.getLogger(__name__)


class ResourceManager:
    def __init__(self, platform, scheduler):
        self.platform = platform
        self.scheduler = scheduler

        # Dict: job requests -> job states
        self.requests = {}
        self.schedule = None

        # Time corresponding to the current internal state of resource manager
        self._state_time = 0.0

    def _log_info(self, message):
        log.info(f"t:{self.state_time:.2f}  {message}")

    def _log_debug(self, message):
        log.debug(f"t:{self.state_time:.2f}  {message}")

    @property
    def state_time(self):
        return self._state_time

    def accepted_requests(self):
        """Returns the list of tuples of active requests and job states."""
        res = []
        for request, job in self.requests.items():
            if request.status == JobRequestStatus.ACCEPTED:
                res.append((request, job))
        return res

    def _schedule_new_request(self, request):
        # Create a copy of the current job list with the new request
        # Ensure that jobs are immutable
        jobs = [j for _, j in self.accepted_requests()]
        jobs.append(Job.from_request(request))

        # Generate scheduling with the new job
        st = time.time()
        schedule = self.scheduler.schedule(
            jobs, scheduling_start_time=self.state_time
        )
        et = time.time()
        log.debug("Time to find the schedule: {}".format(et - st))
        return schedule

    def new_request(self, request):
        """Handle new request."""
        if request.status != JobRequestStatus.NEW:
            raise RuntimeError(
                f"A request must have the status NEW, but this request has "
                f"the status {request.status.name}"
            )

        if request in self.requests:
            raise RuntimeError(
                f"Request {request.app.name} is already registered by "
                "the resource manager"
            )

        # TODO: Consider assigning request.arrival in this function
        if request.arrival is not None:
            if request.arrival != self.state_time:
                raise RuntimeError(
                    f"The request's arrival ({request.arrival}) does not match "
                    f"the current state time ({self.state_time})"
                )
        else:
            request.arrival = self.state_time

        app = request.app
        deadline = request.deadline

        # Add a new request into request list
        self.requests.update({request: None})
        self._log_info(f"New request {app.name}, deadline = {deadline}")

        schedule = self._schedule_new_request(request)

        if not schedule:
            self._log_info(f"Request {app.name} is rejected")
            request.status = JobRequestStatus.REFUSED
            return False

        self._log_info(f"Request {app.name} is accepted")
        self._log_debug(schedule.to_str(verbose=True))
        # Update job list and active scheduling
        job = Job.from_request(request).dispatch()
        self.requests.update({request: job})
        self.schedule = schedule
        request.status = JobRequestStatus.ACCEPTED
        return True

    def update_request_state(self, request, state):
        raise NotImplementedError()

    def _advance_segment(self, segment, till_time=None):
        """Advance an internal state by the schedule segment.

        This method advances the internal state by a single segment. If
        `till_time` is not None, then the segment is advanced till this
        specified time within a segment.

        If `till_time` is None, the function returns None, otherwise it returns
        the remaining part of the segment
        """
        # the state time must equal to start time of the segment
        if abs(self.state_time - segment.start_time) > 0.0001:
            raise RuntimeError(
                f"The current state time ({self.state_time}) does not equal "
                f"the start time of the segment ({segment.start_time})"
            )

        rest = None
        if till_time:
            if not segment.start_time <= till_time <= segment.end_time:
                raise RuntimeError(
                    f"The end time ({till_time}) must be within the segment "
                    f"({segment.start_time}..{segment.end_time})"
                )
            segment, rest = segment.split(till_time)

        jobs = [j for _, j in self.accepted_requests()]
        schedule = Schedule(self.platform, [segment])
        # FIXME: Remove this constructor, create method in
        # SingleJobMappingSegment class
        end_jobs = Job.from_schedule(schedule, init_jobs=jobs)

        for job in end_jobs:
            request = job.request
            if job.is_terminated():
                # FIXME: application might have finished earlier,
                # write a correct finish time
                self._log_info(f"job {job.app.name} finished")
                # update request
                request.status = JobRequestStatus.FINISHED
                self.requests.update({request: None})
            else:
                self.requests.update({request: job})

        self._state_time = segment.end_time

        return rest

    def advance_segment(self):
        """Advance an internal state by the schedule segment."""
        if not self.schedule:
            raise RuntimeError("No active schedule")
        self._advance_segment(self.schedule.first)
        self.schedule.remove_segment(0)
        if len(self.schedule) == 0:
            self.schedule = None

    def advance_to_time(self, new_time):
        """Advance an internal state till `new_time`."""
        if new_time < self.state_time:
            raise RuntimeError(
                f"The resource manager cannot be moved backwards {self.state_time} -> {new_time}."
            )

        # No action if time is not changed
        if new_time == self.state_time:
            return

        # Simply update state time if there are no currently running jobs
        if not self.schedule:
            if self.accepted_requests():
                raise RuntimeError(
                    "The resource manager must have an active schedule "
                    "for still running requests"
                )
            self._state_time = new_time
            return

        new_schedule = Schedule(self.platform)
        for segment in self.schedule.segments():
            # advance by the whole segment
            if new_time >= segment.end_time:
                self._advance_segment(segment)
            # tne new_time is in the middle of the segment
            if segment.start_time <= new_time < segment.end_time:
                rest = self._advance_segment(segment, new_time)
                new_schedule.append_segment(rest)
            # the segments after new_time
            if new_time < segment.start_time:
                new_schedule.append_segment(segment)

        self.schedule = new_schedule
        if len(self.schedule) == 0:
            self.schedule = None
            self._state_time = new_time

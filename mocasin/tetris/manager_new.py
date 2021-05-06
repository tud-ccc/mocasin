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

    def active_requests(self):
        raise NotImplementedError()

    def active_jobs(self):
        """Returns the list of active jobs."""
        jobs = []
        for request, job in self.requests.items():
            if (
                request.status == JobRequestStatus.ARRIVED
                or request.status == JobRequestStatus.ACCEPTED
            ):
                jobs.append(job)
        return jobs

    def updated_request_state(self, request, state):
        raise NotImplementedError()

    def update_states_to_time(self, new_time):
        raise NotImplementedError()

    def _schedule_new_request(self, request):
        # Create a copy of the current job list with the new request
        # Ensure that jobs are immutable
        jobs = self.active_jobs()
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

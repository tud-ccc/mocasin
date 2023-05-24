# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import logging
import time

from mocasin.tetris.job_request import JobRequestInfo, JobRequestStatus
from mocasin.tetris.job_state import Job
from mocasin.tetris.schedule import (
    Schedule,
    MultiJobSegmentMapping,
    SingleJobSegmentMapping,
)

log = logging.getLogger(__name__)

EPS = 0.0001


class ResourceManager:
    def __init__(
        self,
        platform,
        scheduler,
        schedule_iteratively=True,
    ):
        self.platform = platform
        self.scheduler = scheduler

        # Parameters
        self._schedule_iteratively = schedule_iteratively

        # Time corresponding to the current internal state of resource manager
        self._state_time = 0.0
        self._dynamic_energy = 0.0

        # Dict: job requests -> job states
        self.requests = {}
        self._schedule = None

    @property
    def state_time(self):
        return self._state_time

    @property
    def dynamic_energy(self):
        return self._dynamic_energy

    @property
    def schedule(self):
        return self._schedule

    def _set_schedule(self, new_schedule):
        """Set the schedule.

        If the schedule is empty, set None.
        """
        if new_schedule.is_empty():
            self._schedule = None
        else:
            self._schedule = new_schedule
            log.debug("Current active schedule:")
            log.debug(new_schedule.to_str(verbose=True))

    def _is_schedule_adjusted(self, schedule):
        EPS = 1e-5
        current_time = self.state_time
        for segment in schedule.segments():
            if abs(segment.start_time - current_time) > EPS:
                return False
            current_time = segment.end_time
        return True

    def _adjust_schedule(self, schedule):
        """Adjust the schedule.

        If some segments were removed in the schedule, we need to adjust by
        correcting the segment's start_time and end_time.
        """
        current_time = self.state_time
        new_schedule = Schedule(self.platform)
        for segment in schedule.segments():
            new_segment = MultiJobSegmentMapping(self.platform)
            for job in segment.jobs():
                new_job = SingleJobSegmentMapping(
                    job.request,
                    job.mapping,
                    start_time=current_time,
                    start_cratio=job.start_cratio,
                    end_time=current_time + job.duration,
                )
                new_segment.append_job(new_job)
            new_schedule.add_segment(new_segment)
            current_time = new_segment.end_time
        return new_schedule

    def new_request(self, graph, mappings, timeout=None):
        """Handle new request.

        Handle a new request to start application `graph` with a relative
        deadline `timeout`. This method register a new request, and put it in
        the queue of new applcations to handle.

        Args:
            graph (DataflowGraph): an input application
            mappings (list of Mapping): operating points
            timeout (float or None): timeout in ms

        Returns: request
        """
        deadline = None
        if timeout:
            deadline = self.state_time + timeout
        request = JobRequestInfo(
            graph, mappings, arrival=self.state_time, deadline=deadline
        )

        # Add a new request into request list
        self.requests.update({request: None})
        log.debug(
            f"New request {graph.name}, "
            f"timeout [deadline] = {timeout} [{deadline}]"
        )
        return request

    def _finish_request(self, request):
        """Mark request as completed.

        Args:
            request (JobRequestInfo): the request
        """
        assert request in self.requests
        log.debug(f"Request {request.app.name} finished")
        # update request
        request.status = JobRequestStatus.FINISHED
        self._remove_request(request)

    def finish_request(self, request):
        """Mark request as completed, and remove request from the schedule.

        Args:
            request (JobRequestInfo): the request
        """
        self._finish_request(request)
        new_schedule = self.schedule.copy()
        segments = new_schedule.segments()
        for segment in segments:
            jobs = segment.jobs()
            for job in jobs:
                if job.request == request:
                    segment.remove_job(job)
            if len(segment.jobs()) == 0:
                new_schedule.remove_segment(segment)
        if not self._is_schedule_adjusted(new_schedule):
            log.debug("Schedule is not adjusted. Adjusting..")
            new_schedule = self._adjust_schedule(new_schedule)
        self._set_schedule(new_schedule)

    def _generate_schedule(
        self, new_requests=None, allow_partial_solution=False
    ):
        """Generate a schedule with new requests.

        Internal method to generate a schedule. The schedule is not applied in
        the resource manager.
        """
        # Create a copy of the current job list with the new request
        # Ensure that jobs are immutable
        jobs = [j for _, j in self.requests.items() if j]

        if new_requests:
            for request in new_requests:
                jobs.append(Job.from_request(request).dispatch())

        # Generate scheduling with the new job
        st = time.time()
        if allow_partial_solution:
            schedule = self.scheduler.schedule(
                jobs,
                scheduling_start_time=self.state_time,
                allow_partial_solution=True,
                current_schedule=self.schedule,
            )
        else:
            schedule = self.scheduler.schedule(
                jobs,
                scheduling_start_time=self.state_time,
                current_schedule=self.schedule,
            )

        et = time.time()
        scheduling_time = et - st
        log.debug(
            f"Schedule found = {schedule is not None}. "
            f"Time to find the schedule: {scheduling_time}"
        )
        return schedule, scheduling_time

    def _generate_schedule_iteratively(self):
        """Generate schedule for multiple requests iteratively."""
        new_requests = [
            r for r in self.requests.keys() if r.status == JobRequestStatus.NEW
        ]
        new_schedule = None
        total_sched_time = 0
        for request in new_requests:
            schedule, sched_time = self._generate_schedule([request])
            total_sched_time += sched_time
            if schedule:
                log.debug(f"Request {request.app.name} is accepted")
                request.status = JobRequestStatus.ACCEPTED
                job = Job.from_request(request).dispatch()
                self.requests.update({request: job})
                new_schedule = schedule
            else:
                log.debug(f"Request {request.app.name} is rejected")
                request.status = JobRequestStatus.REFUSED
                self._remove_request(request)
        return new_schedule, total_sched_time

    def _generate_schedule_jointly(self):
        """Generate schedule for multiple requests jointly."""
        # Schedule all jobs in once
        new_requests = [
            r for r in self.requests.keys() if r.status == JobRequestStatus.NEW
        ]
        schedule, sched_time = self._generate_schedule(
            new_requests, allow_partial_solution=True
        )
        if not schedule:
            log.debug(f"Schedule was not generated")
            for request in new_requests:
                log.debug(f"Request {request.app.name} is rejected")
                request.status = JobRequestStatus.REFUSED
                self._remove_request(request)
            return None, sched_time

        scheduled_requests = schedule.get_requests()
        for request in list(self.requests.keys()):
            if request.status == JobRequestStatus.ACCEPTED:
                if request not in scheduled_requests:
                    raise RuntimeError(
                        f"The earlier accepted request {request.app.name} "
                        "was not scheduled"
                    )
                continue
            assert request.status == JobRequestStatus.NEW
            if request in scheduled_requests:
                log.debug(f"Request {request.app.name} is accepted")
                request.status = JobRequestStatus.ACCEPTED
                job = Job.from_request(request).dispatch()
                self.requests.update({request: job})
            else:
                log.debug(f"Request {request.app.name} is rejected")
                request.status = JobRequestStatus.REFUSED
                self._remove_request(request)
        return schedule, sched_time

    def generate_schedule(self, force=False):
        """Generate a new schedule.

        If there are new requests in the queue, they are attempted to be
        scheduled in the order the request were created. If the resource manager
        can schedule the request, its status is changed to "accepted", otherwise
        it is changed to "refused". If the request is accepted, it will be
        included in the generated schedule.

        The parameter `force` indicates whether the schedule should be
        re-generated even if no new request is accepted. This is useful in case
        if some jobs were manually marked as finished, we let the user decide if
        new schedule should be generated at the expense of the runtime overhead.

        Args:
            force(bool): force re-generation of the schedule if no new request
                is accepted.

        Returns: a new schedule if the new schedule was generated, otherwise
            None
        """
        schedule = None
        new_requests = [
            r for r in self.requests.keys() if r.status == JobRequestStatus.NEW
        ]
        if self._schedule_iteratively:
            schedule, sched_time = self._generate_schedule_iteratively()
        else:
            schedule, sched_time = self._generate_schedule_jointly()

        if not schedule and force:
            schedule, sched_time = self._generate_schedule()
            assert schedule

        if schedule:
            self._set_schedule(schedule)
            return self.schedule, sched_time

        return None, sched_time

    def _remove_request(self, request):
        """Remove finished or refused request."""
        assert (
            request.status == JobRequestStatus.REFUSED
            or request.status == JobRequestStatus.FINISHED
        )
        self.requests.pop(request)
        self.scheduler.orbit_lookup_manager.remove_graph_orbit_entries(
            request.app
        )

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
            if abs(segment.start_time - till_time) < EPS:
                return segment
            elif abs(segment.end_time - till_time) < EPS:
                rest = None
            else:
                segment, rest = segment.split(till_time)

        jobs = [j for _, j in self.requests.items() if j]
        schedule = Schedule(self.platform, [segment])
        # FIXME: Remove this constructor, create method in
        # SingleJobMappingSegment class
        end_jobs = Job.from_schedule(schedule, init_jobs=jobs)

        for job in end_jobs:
            request = job.request
            if job.is_terminated():
                self._finish_request(request)
            else:
                self.requests.update({request: job})

        self._state_time = segment.end_time
        self._dynamic_energy += segment.energy
        return rest

    def advance_segment(self):
        """Advance an internal state by the schedule segment."""
        if any(r.status == JobRequestStatus.NEW for r in self.requests):
            raise RuntimeError(
                "New requests must be scheduled when advancing "
                "the resource manager"
            )
        if not self.schedule:
            raise RuntimeError("No active schedule")
        segment = self.schedule.pop_front()
        self._advance_segment(segment)
        self._set_schedule(self.schedule)

    def advance_to_time(self, new_time):
        """Advance an internal state till `new_time`."""
        if any(r.status == JobRequestStatus.NEW for r in self.requests):
            raise RuntimeError(
                "New requests must be scheduled when advancing "
                "the resource manager"
            )
        if new_time < self.state_time:
            raise RuntimeError(
                f"The resource manager cannot be moved backwards "
                f"{self.state_time} -> {new_time}."
            )

        # No action if time is not changed
        if new_time == self.state_time:
            return

        # Simply update state time if there are no currently running jobs
        if not self.schedule:
            if self.requests:
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
                continue
            # tne new_time is in the middle of the segment
            if segment.start_time < new_time < segment.end_time:
                rest = self._advance_segment(segment, new_time)
                if rest is not None:
                    new_schedule.add_segment(rest)
                continue
            # the segments after new_time
            if new_time <= segment.start_time:
                new_schedule.add_segment(segment)
                continue

        self._set_schedule(new_schedule)
        if not self.schedule:
            self._state_time = new_time

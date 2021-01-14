# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from mocasin.tetris.job_request import JobRequestInfo
from mocasin.tetris.schedule import CRATIO_EPS

from mocasin.common.mapping import Mapping

import copy
from enum import Enum
import logging

log = logging.getLogger(__name__)


class JobStates(Enum):
    NEW = 1
    BLOCKED = 2
    READY = 3
    RUNNING = 4
    TERMINATED = 5

    def __str__(self):
        return self.name


class Job:
    """Job state.

    Job is defined by a JobRequestInfo object, a mapping, a state and
    a completion state. The objects of this class are supplied to scheduler.

    Args:
        request (JobRequestInfo): a reference to job request
        mapping (Mapping): a current mapping
        state (JobStates): a current state
        cratio (float): a completion ratio
        completed (bool): a completed flag
    """
    def __init__(self, request, mapping=None, state=JobStates.NEW, cratio=0.0,
                 completed=False):
        assert isinstance(request, JobRequestInfo)
        assert isinstance(mapping, (Mapping, type(None)))
        assert isinstance(cratio, float)
        self.__request = request
        self.__mapping = mapping
        self.__last_mapping = mapping

        self.__state = state
        self.__cratio = cratio
        # Flag specifies whether the job was successfully completed
        self.__completed = completed

        # Check that the job in a sane state
        self.__verify()

    @property
    def request(self):
        return self.__request

    @property
    def mapping(self):
        return self.__mapping

    @property
    def last_mapping(self):
        return self.__last_mapping

    @property
    def deadline(self):
        return self.__request.deadline

    @property
    def cratio(self):
        return self.__cratio

    @cratio.setter
    # TODO: Consider removing this function
    def cratio(self, val):
        if val < self.cratio:
            log.warning("Job state is going to be degrade")
        self.__cratio = val

    @property
    def app(self):
        """Application."""
        return self.__request.app

    # States properties
    @property
    def state(self):
        return self.__state

    def is_new(self):
        return self.__state == JobStates.NEW

    def is_ready(self):
        return self.__state == JobStates.READY

    def is_blocked(self):
        return self.__state == JobStates.BLOCKED

    def is_running(self):
        return self.__state == JobStates.RUNNING

    def is_terminated(self):
        return self.__state == JobStates.TERMINATED

    @property
    def completed(self):
        return self.__completed

    def __verify(self):
        """ Verify that the object in a sane state.
        """
        failed = False
        # Mapping should be assigned only when the job in running state
        if self.is_running():
            if self.mapping is None or self.last_mapping is None:
                log.error(
                    "There must be a [last] mapping in a {} state".format(
                        self.state))
                failed = True
        else:
            if self.mapping is not None:
                log.error("There must be no mapping in a {} state".format(
                    self.state))
                failed = True

        # Correspondence of values: state, cratio and completed
        if self.is_new():
            if self.cratio != self.request.start_cratio:
                log.error(
                    "In a {} state, a cratio must equal a start cratio of the request"
                    .format(self.state))
                failed = True
            if self.completed:
                log.error(
                    "In a {} state, a job cannot be in completed state".format(
                        self.state))
                failed = True
        else:
            if self.cratio < self.request.start_cratio:
                log.error("In a {} state, a cratio must be greater than or "
                          "equal to a start cratio of the request".format(
                              self.state))
                failed = True

            if self.cratio > 1.0:
                log.error("In a {} state, a cratio must be less than or "
                          "equal to 1.0".format(self.state))
                failed = True

            if self.is_terminated:
                if self.completed and self.cratio < 1.0:
                    log.error("In a completed state, a cratio must equal 1.0")
                    failed = True
            else:
                if self.completed:
                    log.error(
                        "In a {} state, a job cannot be in completed state"
                        .format(self.state))
                    failed = True

        if failed:
            log.error(
                "Some errors occured, see messages above.\n{}\n{}".format(
                    self.to_str(), self.request.to_str()))
            assert False

    def to_str(self):
        completed_str = ""
        if self.completed:
            completed_str = "[F]"
        res = "(Job app={} deadline={} mapping={} state={} cratio={:.3f}{})".format(
            self.app.name, self.deadline, self.mapping, self.state,
            self.cratio, completed_str)
        return res

    @staticmethod
    def from_request(req):
        """ Generate job states from the job request

        Args:
            req (JobRequestInfo): a job request
        """
        return Job(req, cratio=req.start_cratio)

    @staticmethod
    # TODO: remove
    def from_requests(reqs):
        """ Generate job states from job requests

        Args:
            reqs (list): a list of JobRequestInfo objects
        """
        jobs = []
        for req in reqs:
            job = Job(req, cratio=req.start_cratio)
            jobs.append(job)
        return jobs

    def can_meet_deadline(self, ctime):
        """ Returns whether the job can meet a deadline.

        If a job in a TERMINATED state, the function returns true if the job is
        completed, otherwise it returns false.

        Args:
            ctime (float): current time
        """
        rratio = 1.0 - self.cratio
        rtime = self.request.deadline - ctime

        if self.is_terminated():
            return self.completed

        return (self.request.get_min_exec_time() * rratio <= rtime)

    def dispatch(self):
        """ Dispatch the job, that it could execute.

        Returns: the object itself (to allow chaining).
        """
        assert self.is_new()
        self.__state = JobStates.READY
        self.__verify()
        return self

    def advance(self, job_segment):
        """ Advance the JobState by a job segment mapping.

        Args:
            job_segment (JobSegmentMapping): a job segment mapping

        Returns: the object itself (to allow chaining).
        """
        # Checking prerequisities
        assert self.request == job_segment.request
        assert abs(self.cratio - job_segment.start_cratio) < CRATIO_EPS, (
            "Cannot apply job to a job segment:\n"
            "job: {}\n"
            "segment: {}".format(self.to_str(), job_segment.to_str()))
        assert self.is_ready() or self.is_running(), (
            "Cannot advance the job with a state {}".format(self.state))

        # Advance the job state
        self.__mapping = job_segment.mapping
        self.__last_mapping = job_segment.mapping
        self.__cratio = job_segment.end_cratio
        self.__state = JobStates.RUNNING
        if job_segment.finished:
            self.__mapping = None
            self.__state = JobStates.TERMINATED
            self.__completed = True
        self.__verify()
        return self

    def idle(self):
        """ Put job in an idle state

        Returns: the object itself to allow chaining.
        """
        if self.is_running():
            self.__state = JobStates.READY
            self.__mapping = None
        assert self.mapping is None
        self.__verify()
        return self

    @staticmethod
    def from_schedule(schedule, init_jobs=None):
        """ Generate jobs from a schedule

        If 'init_jobs' is None, then this list is constructed with job requests
        present in the schedule and their start_cratio at first segment related
        to the correspoding job request.

        Args:
            schedule (Schedule): a schedule
            init_jobs (list): a list of Job objects

        Returns: a list of Job objects after applying a schedule
        """
        req_schedules = schedule.per_requests(none_as_idle=True)
        if init_jobs is None:
            # Construct the init job states
            init_jobs = []
            for r, ml in req_schedules.items():
                m = next(m for m in ml if m is not None)
                js = JobState(r, cratio=m.start_cratio)
                init_jobs.append(js)

        assert isinstance(init_jobs, list)

        res = []
        for j in init_jobs:
            j_after = copy.copy(j)
            for segment in req_schedules.get(j.request, [None]):
                if segment is None:
                    j_after.idle()
                else:
                    j_after.advance(segment)
            res.append(j_after)
        return res

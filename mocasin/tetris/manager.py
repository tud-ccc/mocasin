# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.tetris.job_request import JobRequestStatus
from mocasin.tetris.job_state import Job
from mocasin.tetris.schedule import Schedule, TIME_EPS

from mocasin.common.platform import Platform

import logging

log = logging.getLogger(__name__)

import time


class ResourceManager:
    def __init__(self, platform, scheduler, migrations=True, start_time=0.0):
        self.scheduler = scheduler
        self.platform = platform
        self.__migrations = migrations

        self.__ctime = start_time
        self.__job_state_table = None  # active_job_table

        self.__requests = []
        self.__jobs = None
        self.__active_mapping = None
        self.__history_mapping = None

    @property
    def ctime(self):
        return self.__ctime

    @property
    def migrations(self):
        return self.__migrations

    def start(self):
        self.__jobs = []
        self.__active_mapping = Schedule(self.platform)
        self.__history_mapping = Schedule(self.platform)

    def __simulate_segment(self, segment):
        """Simulare the RM by a mapping segment."""
        if len(self.__history_mapping) > 0:
            # Assert no gaps in the actual scheduling
            assert (
                abs(self.__history_mapping.end_time - segment.start_time)
                < TIME_EPS
            )

        self.__history_mapping.append_segment(segment)

        new_jobs = Job.from_schedule(
            Schedule(self.platform, [segment]), init_jobs=self.__jobs
        )

        for job in new_jobs:
            if job.is_terminated():
                log.info(
                    "t:{:.2f}, job {} finished".format(
                        segment.end_time, job.app.name
                    )
                )

        new_jobs = [x for x in new_jobs if not x.is_terminated()]

        self.__jobs = new_jobs

    def simulate_to(self, new_time):
        assert isinstance(new_time, (int, float))
        assert new_time > self.ctime
        assert self.__active_mapping is not None

        log.debug("Advancing the simulation time to t:{:.2f}".format(new_time))

        new_active_scheduling = Schedule(self.platform)

        # If there is an active mapping, then update the states by segments
        for segment in self.__active_mapping:
            assert segment.start_time > self.ctime - TIME_EPS, (
                "The start of the segment ({}) in the past"
                " (current time is {})".format(segment.start_time, self.ctime)
            )

            if segment.start_time < new_time - TIME_EPS:
                # If the segment starts before the new time
                if segment.end_time - TIME_EPS < new_time:
                    # Easy case, the whole segment
                    self.__simulate_segment(segment)
                else:
                    # If the new time in the middle of the segment, then split
                    s1, s2 = segment.split(new_time)
                    self.__simulate_segment(s1)
                    new_active_scheduling.append_segment(s2)
            else:
                # If the segment is in the future
                new_active_scheduling.append_segment(segment)

        self.__active_mapping = new_active_scheduling
        self.__ctime = new_time

    def finish(self):
        """Finish the current scheduling."""
        if len(self.__active_mapping) > 0:
            finish_time = self.__active_mapping.end_time
            self.simulate_to(finish_time)
        return self.ctime

    def new_request(self, request):
        arrival = request.arrival
        app = request.app
        deadline = request.deadline
        assert self.ctime == arrival

        # Add a new request into request list
        self.__requests.append(request)
        log.info(
            "t:{:.2f}  New request {}, deadline = {}".format(
                arrival, app.name, deadline
            )
        )

        # Create a copy of the current job list with the new request
        new_job_list = self.__jobs.copy()
        new_job_list.append(Job.from_request(request))

        # Generate scheduling with the new job
        st = time.time()
        schedule = self.scheduler.schedule(
            new_job_list, scheduling_start_time=self.ctime
        )
        et = time.time()
        log.debug("Time to find the schedule: {}".format(et - st))

        if schedule:
            log.info(
                "t:{:.2f}  Request {} is accepted".format(self.ctime, app.name)
            )
            log.debug(
                "t:{:.2f}  {}".format(self.ctime, schedule.to_str(verbose=True))
            )
            # Update job list and active scheduling
            job = Job.from_request(request).dispatch()
            self.__jobs.append(job)
            self.__active_mapping = schedule
            request.status = JobRequestStatus.ACCEPTED
        else:
            log.info(
                "t:{:.2f}  Request {} is rejected".format(
                    self.ctime, request.app.name
                )
            )
            request.status = JobRequestStatus.REFUSED

    def stats(self):
        res = {}
        res["requests"] = len(self.__requests)
        res["accepted"] = sum(
            x.status == JobRequestStatus.ACCEPTED for x in self.__requests
        )
        res["energy"] = self.__history_mapping.energy
        res["scheduler"] = self.scheduler.name
        return res

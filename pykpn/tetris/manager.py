# This file implements classes of Application tables
#
# Author: Robert Khasanov

from pykpn.tetris.scheduler.base import SchedulerBase
from pykpn.common.platform import Platform
from pykpn.tetris.apptable import AppTable
from pykpn.tetris.mapping import Mapping
from pykpn.tetris.context import Context
from pykpn.tetris.job import JobTable
from pykpn.tetris.reqtable import RequestStatus

import logging
log = logging.getLogger(__name__)

import time

EPS = 0.00001


class ResourceManager:
    def __init__(self, app_table, platform, scheduler, allow_migration=True,
                 start_time=0.0):
        assert isinstance(app_table, AppTable)
        assert isinstance(scheduler, SchedulerBase)
        assert isinstance(platform, Platform)
        self.__app_table = app_table
        self.__scheduler = scheduler
        self.__platform = platform
        self.__allow_migration = allow_migration

        self.__ctime = start_time
        self.__job_state_table = None # active_job_table

        self.__jobs = None
        self.__active_mapping = None
        self.__history_mapping = None

    @property
    def ctime(self):
        return self.__ctime

    @property
    def app_table(self):
        return self.__app_table

    @property
    def scheduler(self):
        return self.__scheduler

    @property
    def platform(self):
        return self.__platform

    @property
    def allow_migration(self):
        return self.__allow_migration


    def start(self):
        self.__jobs = JobTable(time=self.ctime)
        self.__active_mapping = Mapping()
        self.__history_mapping = Mapping()

    def __simulate_segment(self, segment):
        """Simulare the RM by a mapping segment."""
        if len(self.__history_mapping) > 0:
            # Assert no gaps in the actual scheduling
            assert abs(self.__history_mapping.end_time -
                       segment.start_time) < EPS

        self.__history_mapping.append_segment(segment)

        for job in segment:
            j = self.__jobs.find_by_rid(job.rid)
            j.cratio = job.end_cratio
            if job.finished:
                log.info("t:{:.2f}, job (rid={}) finished".format(
                    segment.end_time, job.rid))
                self.__jobs.remove(job.rid)
        self.__jobs.time = segment.end_time

    def simulate_to(self, new_time):
        assert isinstance(new_time, (int, float))
        assert new_time > self.ctime
        assert self.__active_mapping is not None

        log.debug("Advancing the simulation time to t:{:.2f}".format(new_time))

        new_active_scheduling = Mapping()

        # If there is an active mapping, then update the states by segments
        for segment in self.__active_mapping:
            assert segment.start_time > self.ctime - EPS, (
                "The start of the segment ({}) in the past"
                " (current time is {})".format(segment.start_time, self.ctime))

            if segment.start_time < new_time - EPS:
                # If the segment starts before the new time
                if segment.end_time - EPS < new_time:
                    # Easy case, the whole segment
                    self.__simulate_segment(segment)
                else:
                    # If the new time in the middle of the segment, then split
                    s1, s2 = segment.split_at_time(new_time)
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

    def new_request(self, arrival, app, deadline):
        assert self.ctime == arrival

        # Add a new request into request table
        rid = Context().req_table.add(app, arrival, deadline)
        log.info(
            "t:{:.2f}  New request {}, application = {}, deadline = {}".format(
                arrival, rid, app, deadline))

        # Create a copy of the current job list with the new request
        new_job_list = self.__jobs.copy()
        new_job_list.add(rid)

        # Generate scheduling with the new job
        st = time.time()
        res, scheduling, _ = self.scheduler.schedule(new_job_list)
        et = time.time()
        log.debug("Time to find a scheduling: {}".format(et - st))

        if res:
            log.info("t:{:.2f}  Request {} is accepted".format(
                self.ctime, rid))
            log.debug("t:{:.2f}  {}".format(self.ctime, scheduling))
            # scheduling.dump_jobs_info()
            # Update job list and active scheduling
            self.__jobs.add(rid)
            self.__active_mapping = scheduling
            Context().req_table[rid].status = RequestStatus.ACCEPTED
        else:
            log.info("t:{:.2f}  Request {} is rejected".format(
                self.ctime, rid))
            Context().req_table[rid].status = RequestStatus.REFUSED

    def stats(self):
        res = {}
        res['requests'] = len(Context().req_table)
        res['accepted'] = Context().req_table.count_accepted_and_finished()
        res['energy'] = self.__history_mapping.energy
        res['scheduler'] = self.scheduler.name
        return res

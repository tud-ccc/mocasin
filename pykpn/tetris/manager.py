from pykpn.tetris.scheduler.base import SchedulerBase
from pykpn.common.platform import Platform
from pykpn.tetris.mapping import Mapping
from pykpn.tetris.context import Context
from pykpn.tetris.job import JobTable
from pykpn.tetris.reqtable import RequestStatus

import logging
log = logging.getLogger(__name__)

import time

EPS = 0.00001

class ResourceManager:
    def __init__(self, scheduler, platform):
        assert isinstance(scheduler, SchedulerBase)
        assert isinstance(platform, Platform)
        self.__scheduler = scheduler
        self.__platform = platform

        self.__time = None
        self.__jobs = None
        self.__active_mapping = None
        self.__history_mapping = None

    def start(self):
        self.__time = 0.0
        self.__jobs = JobTable(time = self.__time)
        self.__active_mapping = Mapping()
        self.__history_mapping = Mapping()

    def __simulate_segment(self, segment):
        """Simulare the RM by a mapping segment."""
        if len(self.__history_mapping) > 0:
            # Assert no gaps in the actual scheduling
            assert abs(self.__history_mapping.end_time - segment.start_time) < EPS

        self.__history_mapping.append_segment(segment)

        for job in segment:
            j = self.__jobs.find_by_rid(job.rid)
            j.cratio = job.end_cratio
            if job.finished:
                log.info("t:{:.2f}, job (rid={}) finished".format(segment.end_time, job.rid))
                self.__jobs.remove(job.rid)
        self.__jobs.time = segment.end_time

    def simulate_to(self, new_time):
        assert isinstance(new_time, (int, float))
        assert new_time > self.__time
        assert self.__active_mapping is not None

        log.debug("Advancing the simulation time to t:{:.2f}".format(new_time))

        new_active_scheduling = Mapping()

        # If there is an active mapping, then update the states by segments
        for segment in self.__active_mapping:
            assert segment.start_time > self.__time - EPS, "The start of the segment ({}) in the past (current time is {})".format(segment.start_time, self.__time)
            if segment.start_time < new_time - EPS:
                # If the segment starts before the new time
                if segment.end_time - EPS < new_time:
                    # Easy case, the whole segment
                    self.__simulate_segment(segment)
                else:
                    # If the new time in the middle of the segment, then split it
                    s1,s2 = segment.split_at_time(new_time)
                    self.__simulate_segment(s1)
                    new_active_scheduling.append_segment(s2)
            else:
                # If the segment is in the future
                new_active_scheduling.append_segment(segment)

        self.__active_mapping = new_active_scheduling
        self.__time = new_time

    def finish(self):
        """Finish the current scheduling."""
        if len(self.__active_mapping) > 0:
            finish_time = self.__active_mapping.end_time
            self.simulate_to(finish_time)
        return self.__time

    def new_request(self, arrival, app, deadline):
        assert self.__time == arrival

	# Add a new request into request table
        rid = Context().req_table.add(app, arrival, deadline)
        log.info("t:{:.2f}  New request {}, application = {}, deadline = {}".format(arrival, rid, app, deadline))

        # Create a copy of the current job list with the new request
        new_job_list = self.__jobs.copy()
        new_job_list.add(rid)

        # Generate scheduling with the new job
        st = time.time()
        res, scheduling, _ = self.__scheduler.schedule(new_job_list)
        et = time.time()
        log.debug("Time to find a scheduling: {}".format(et-st))

        if res:
            log.info("t:{:.2f}  Request {} is accepted".format(self.__time, rid))
            log.debug("t:{:.2f}  {}".format(self.__time, scheduling))
            # scheduling.dump_jobs_info()
            # Update job list and active scheduling
            self.__jobs.add(rid)
            self.__active_mapping = scheduling
            Context().req_table[rid].status = RequestStatus.ACCEPTED
        else:
            log.info("t:{:.2f}  Request {} is rejected".format(self.__time, rid))
            Context().req_table[rid].status = RequestStatus.REFUSED

    def stats(self):
        res = {}
        res['requests'] = len(Context().req_table)
        res['accepted'] = Context().req_table.count_accepted_and_finished()
        res['energy'] = self.__history_mapping.energy
        res['scheduler'] = self.__scheduler.name
        return res 

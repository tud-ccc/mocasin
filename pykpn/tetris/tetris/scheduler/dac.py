
from pykpn.tetris.tetris.job import JobTable, Job
import math
import logging

from pykpn.tetris.tetris.mapping import Mapping, SegmentMapping, JobSegmentMapping
from pykpn.tetris.tetris.scheduler.base import SchedulerBase

from pykpn.tetris.tetris.tplatform import Platform

log = logging.getLogger(__name__)

EPS = 0.00001

class DacScheduler(SchedulerBase):

    def __init__(self, platform, version = "original"):
        assert isinstance(platform, Platform)
        self.__platform = platform
        self.__start_energy = 0.0
        self.__start_time = 0.0
        self.__version = version

    @property
    def name(self):
        return "NUEP19'"

    def __select_app_mappings_fit_jars(self, app, deadline, core_type_jars, completion = 0.0):
        res = []
        for mid, mapping in app.mappings.items():
            if mid == '__idle__':
                continue
            rem_time = mapping.time(start_cratio = completion)
            if rem_time > deadline:
                continue

            if not (mapping.core_types * rem_time <= core_type_jars):
                continue

            rem_energy = mapping.energy(start_cratio = completion)
            res.append((mid, rem_energy))
        res.sort(key=lambda tup: tup[1])
        return res

    @staticmethod
    def __add_job_to_scheduling(scheduling, job, mid, start_time, platform):
        """Add job to the scheduling.

        Args:
            scheduling (Mapping): Current scheduling
            job (Job): A job to add
            mid: The mapping id
            start_time (float): A start time of scheduling (used if scheduling is empty)
            platform (Platform): Target platform
        """
        assert scheduling is not None
        assert isinstance(scheduling, Mapping)
        assert isinstance(job, Job)
        assert isinstance(mid, int)

        cur_cratio = job.cratio
        mapping = job.app.mappings[mid]
        cur_rem_time = mapping.time(start_cratio = cur_cratio)
        finished = False
        finish_time = None

        # First try to put the job into segments
        for index, segment in enumerate(scheduling):
            if segment.used_core_types + mapping.core_types <= platform.core_types():
                # This segment has enough resource available for the mapping
                duration = segment.duration
                if cur_rem_time >= duration - EPS:
                    # This segment is small to finish the job.
                    # Schedule here, the rest will be scheduled in the next segments.
                    jm = JobSegmentMapping(job.rid, mid,
                        start_time = segment.start_time,
                        start_cratio = cur_cratio,
                        end_time = segment.end_time)
                    segment.append_job(jm)
                    if jm.finished:
                        # If the segment is a right fit for a job
                        finished = True
                        finish_time = jm.end_time
                    # Update current values
                    cur_cratio = jm.end_cratio
                    cur_rem_time = mapping.time(start_cratio = cur_cratio)
                else:
                    # This segment is larger than the remaining time.
                    # Split the segment into two parts
                    s1, s2 = segment.split_at_time(segment.start_time + cur_rem_time)
                    jm = JobSegmentMapping(job.rid, mid,
                        start_time = s1.start_time,
                        start_cratio = cur_cratio,
                        end_time = s1.end_time)
                    s1.append_job(jm)

                    #Remove old segment, insert new two segments
                    scheduling.remove_segment(index)
                    scheduling.insert_segment(index, s2)
                    scheduling.insert_segment(index, s1)

                    # Update current values
                    assert jm.finished
                    cur_ratio = jm.end_cratio
                    cur_rem_time = 0.0
                    finished = True
                    finish_time = jm.end_time
                if finished:
                    # Go out of loop if finished
                    break
            else:
                # If not enough resources, insert `idle` mappings
                idle_mapping = JobSegmentMapping(job.rid, '__idle__',
                    start_time = segment.start_time,
                    start_cratio = cur_cratio,
                    end_time = segment.end_time)
                segment.append_job(idle_mapping)

        if not finished:
            # Create new segment with a job.
            if len(scheduling) == 0:
                segment_start = start_time
            else:
                segment_start = scheduling.end_time
            jm = JobSegmentMapping(job.rid, mid, start_time = segment_start,
                    start_cratio = cur_cratio, finished = True)
            new_segment = SegmentMapping(platform, jobs = [jm])
            scheduling.append_segment(new_segment)
            finished = True
            finish_time = jm.end_time

        # Check deadline
        assert finished
        abs_deadline = job.abs_deadline
        res = (finish_time <= abs_deadline)

        return res

    def __schedule_mapping(self, mapping):
        to_schedule = [(ts, m) for ts, m in zip(self.__job_table, mapping) if m is not None]
        to_schedule.sort(key=lambda x: x[0].deadline)

        scheduling = Mapping()

        for ts, m in to_schedule:
            schedulable = DacScheduler.__add_job_to_scheduling(scheduling, ts, m, self.__job_table.time, self.__platform)
            assert scheduling is not None
            if not schedulable:
                return None
        return scheduling

    def __map_infinite_jobs(self):
        tt = self.__job_table
        mapping = [None] * len(tt)
        # Assign task with infinite deadlines to one with minimal energy
        for i, t in enumerate(tt):
            if t.deadline == math.inf:
                e = math.inf
                mid = None
                for k, m in t.app.mappings.items():
                    if k != "__idle__" and  m.energy() < e:
                        e = m.energy()
                        mid = k
                assert mid is not None
                mapping[i] = mid
        return mapping

    def __schedule_original(self):
        tt = self.__job_table
        mapping = self.__map_infinite_jobs()

        if None not in mapping:
            res_scheduling = self.__schedule_mapping(mapping)
            assert res_scheduling is not None
            return res_scheduling


        to_be_scheduled = set([i for i, x in enumerate(tt) if x.deadline != math.inf])
        max_deadline = max([tt[x].deadline for x in to_be_scheduled])
        core_type_jars = self.__platform.core_types() * max_deadline
        log.debug(to_be_scheduled)

        while len(to_be_scheduled) != 0:
            log.debug("Jars: {}".format(core_type_jars))
            # List of mappings to finish the applications
            to_finish = {}
            i_md, diff = None, -math.inf
            for tid in to_be_scheduled:
                ts = tt[tid]
                d = ts.deadline
                c = ts.cratio
                app = ts.app
                to_finish[tid] = self.__select_app_mappings_fit_jars(app, d, core_type_jars, completion = c)
                log.debug("{}: {}".format(tid, to_finish[tid]))
                if len(to_finish[tid]) == 0:
                    continue
                if len(to_finish[tid]) == 1:
                    diff = math.inf
                    i_md = tid
                    continue
                cdiff = to_finish[tid][1][1] - to_finish[tid][0][1]
                if cdiff > diff:
                    diff = cdiff
                    i_md = tid
            log.debug("Choose {}".format(i_md))
            if i_md is None:
                return None

            while mapping[i_md] is None:
                new_mapping = mapping.copy()
                new_mapping[i_md] = to_finish[i_md][0][0]
                res_scheduling = self.__schedule_mapping(new_mapping)
                if res_scheduling is None:
                    to_finish[i_md].pop(0)
                    if len(to_finish[i_md]) == 0:
                        return None
                else:
                    mapping = new_mapping
                    log.debug("New mapping: {}".format(mapping))
                    log.debug(res_scheduling.legacy_dump_str())
                    ts = self.__job_table[i_md]
                    cm = ts.app.mappings[mapping[i_md]]
                    rem_time = cm.time(start_cratio=ts.cratio)
                    core_type_jars -= cm.core_types * rem_time
                    to_be_scheduled.remove(i_md)

        return res_scheduling

    def __schedule_2(self):
        tt = self.__job_table
        mapping = self.__map_infinite_jobs()

        if None not in mapping:
            res_scheduling = self.__schedule_mapping(mapping)
            assert res_scheduling is not None
            return res_scheduling


        to_be_scheduled = set([i for i, x in enumerate(tt) if x.deadline != math.inf])
        max_deadline = max([tt[x].deadline for x in to_be_scheduled])
        core_type_jars = self.__platform.core_types() * max_deadline
        log.debug(to_be_scheduled)

        while len(to_be_scheduled) != 0:
            log.debug("Jars: {}".format(core_type_jars))
            # List of mappings to finish the applications
            to_finish = {}
            for tid in to_be_scheduled:
                ts = tt[tid]
                d = ts.deadline
                c = ts.cratio
                app = ts.app
                to_finish[tid] = self.__select_app_mappings_fit_jars(app, d, core_type_jars, completion = c)
                log.debug("{}: {}".format(tid, to_finish[tid]))

            while True:
                i_md, diff = None, -math.inf
                for tid in to_be_scheduled:
                    log.debug("Canonical mappings in list (to_finish), job {}: {}".format(tid, to_finish[tid]))
                    if len(to_finish[tid]) == 0:
                        continue
                    if len(to_finish[tid]) == 1:
                        diff = math.inf
                        i_md = tid
                        continue
                    cdiff = to_finish[tid][1][1] - to_finish[tid][0][1]
                    if cdiff > diff:
                        diff = cdiff
                        i_md = tid
                log.debug("Choose {}".format(i_md))
                if i_md is None:
                    return None

                assert mapping[i_md] is None
                new_mapping = mapping.copy()
                new_mapping[i_md] = to_finish[i_md][0][0]
                res_scheduling = self.__schedule_mapping(new_mapping)
                if res_scheduling is None:
                    to_finish[i_md].pop(0)
                else:
                    mapping = new_mapping
                    log.debug("New mapping: {}".format(mapping))
                    log.debug(res_scheduling.legacy_dump_str())
                    ts = self.__job_table[i_md]
                    cm = ts.app.mappings[mapping[i_md]]
                    rem_time = cm.time(start_cratio=ts.cratio)
                    core_type_jars -= cm.core_types * rem_time
                    to_be_scheduled.remove(i_md)
                    break
        return res_scheduling

    def schedule(self, jobs):
        assert isinstance(jobs, JobTable)
        self.__job_table = jobs
        if self.__version == "original":
            scheduling = self.__schedule_original()
        elif self.__version == "2":
            scheduling = self.__schedule_2()
        return scheduling is not None, scheduling, True

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

# from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import (Schedule, ScheduleSegment,
                                   JobSegmentMapping, TIME_EPS)
from pykpn.tetris.scheduler.base import SchedulerBase

from collections import Counter
import logging
import math

log = logging.getLogger(__name__)


def get_mapping_time_core_product(mapping, cratio=0.0):
    rtime = mapping.metadata.exec_time * (1.0-cratio)
    return Counter(
        {k: v * rtime
         for k, v in mapping.get_used_processor_types().items()})


class DacScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        super().__init__(platform)
        self.__start_energy = 0.0
        self.__start_time = 0.0
        self.__version = kwargs['dac_version']

    @property
    def name(self):
        return "NUEP19'"

    def _filter_job_mappings_by_deadline_jars(self, job, time_core_jars):
        """ Filters mappings which can feet core jars and deadlines.

        Args:
            job (Job): a job
            core_jars (Counter): available core jars volume

        Returns: a list of mappings satisfying deadline and jars consditions.
        """
        res = []
        for m in job.request.mappings:
            rtime = m.metadata.exec_time * (1.0 - job.cratio)
            if rtime > job.request.deadline - self.__scheduling_start_time:
                continue
            m_time_core_prod = get_mapping_time_core_product(m, job.cratio)
            if (m_time_core_prod | time_core_jars) != time_core_jars:
                continue

            res.append(m)
        return res

    def _add_schedule_job_mapping(self, schedule, job, mapping):
        """Add a job mappings to a schedule

        Args:
            schedule (Schedule): a currently constructing schedule
            job (Job): a job
            mapping (Mapping): a mapping

        Returns: whether a job was added without violating deadlines.
        """
        cur_cratio = job.cratio
        cur_rtime = mapping.metadata.exec_time * (1.0-cur_cratio)
        job_finish_time = None

        platform_cores = self.platform.get_processor_types()
        mapping_cores = mapping.get_used_processor_types()

        # First try to put the job into segments
        for index, segment in enumerate(schedule):
            added_segment_cores = (segment.get_used_processor_types() +
                                   mapping_cores)
            if ((added_segment_cores | platform_cores) != platform_cores):
                # This segment has no enough resources
                continue
            if cur_rtime < segment.duration - TIME_EPS:
                s1, s2 = segment.split(segment.start_time + cur_rtime)
                #Remove old segment, insert new two segments
                schedule.remove_segment(index)
                schedule.insert_segment(index, s2)
                schedule.insert_segment(index, s1)
                segment_to_add = s1
            else:
                segment_to_add = segment

            jm = JobSegmentMapping(job.request, mapping,
                                   start_time=segment_to_add.start_time,
                                   start_cratio=cur_cratio,
                                   end_time=segment_to_add.end_time)
            segment_to_add.append_job(jm)
            cur_cratio = jm.end_cratio
            cur_rtime = mapping.metadata.exec_time * (1.0-cur_cratio)
            if jm.finished:
                # If the segment is a right fit for a job
                job_finish_time = jm.end_time
                break

        # If the job is still not finished, create a new segment
        if job_finish_time is None:
            # Create new segment with a job.
            segment_start_time = self.__scheduling_start_time
            if len(schedule) != 0:
                segment_start_time = schedule.end_time

            jm = JobSegmentMapping(job.request, mapping,
                                   start_time=segment_start_time,
                                   start_cratio=cur_cratio, finished=True)
            new_segment = ScheduleSegment(self.platform, jobs=[jm])
            schedule.append_segment(new_segment)
            job_finish_time = jm.end_time

        # Check deadline
        res = (job_finish_time <= job.request.deadline)

        return res

    def _form_schedule(self, job_mappings):
        ordered_job_mappings = sorted(job_mappings.items(),
                                      key=lambda kv: kv[0].request.deadline)

        schedule = Schedule(self.platform)

        for j, m in ordered_job_mappings:
            successful = self._add_schedule_job_mapping(schedule, j, m)
            if not successful:
                return None
        return schedule

    def __map_infinite_jobs(self):
        """ Map jobs without deadlines.

        Since the algorithm uses an internal data structures "jars" initialized
        with the max deadline, we want to choose the mappings for infinite
        jobs outside the main part of the algorithm.

        Returns: a dict of job mappings
        """
        jobs = self.__jobs
        job_mappings = {
            j: min(j.request.mappings, key=lambda m: m.metadata.energy)
            for j in jobs if j.request.deadline == math.inf
        }
        # print({j.to_str(): m.energy for j,m in job_mappings.items()})
        return job_mappings

    def __schedule_original(self):
        jobs = self.__jobs
        job_mappings = self.__map_infinite_jobs()
        schedule = self._form_schedule(job_mappings)

        max_deadline = max([
            j.request.deadline for j in jobs if j.request.deadline != math.inf
        ], default=0)

        time_core_jars = Counter({
            k: v * max_deadline
            for k, v in self.platform.get_processor_types().items()
        })

        while any(j not in job_mappings for j in jobs):
            log.debug("Jars: {}".format(time_core_jars))
            # List of mappings to finish the applications
            to_finish = {}
            diff = (-math.inf, None)
            for job in (j for j in jobs if j not in job_mappings):
                to_finish[job] = (self._filter_job_mappings_by_deadline_jars(
                    job, time_core_jars))
                to_finish[job].sort(key=lambda m: m.metadata.energy)
                log.debug("to_finish[{}]: {}".format(job.to_str(), [
                    m.metadata.energy * (1.0 - job.cratio)
                    for m in to_finish[job]
                ]))
                if len(to_finish[job]) == 0:
                    continue
                if len(to_finish[job]) == 1:
                    diff = (math.inf, job)
                    continue
                # Check energy difference between first two mappings
                cdiff = (1.0 -
                         job.cratio) * (to_finish[job][1].metadata.energy -
                                        to_finish[job][0].metadata.energy)
                if cdiff > diff[0]:
                    diff = (cdiff, job)
            _, job_d = diff
            if job_d is None:
                return None
            log.debug("Choose {}".format(job_d.to_str()))

            while job_d not in job_mappings:
                current_mapping = to_finish[job_d][0]
                job_mappings[job_d] = current_mapping
                schedule = self._form_schedule(job_mappings)
                if schedule is None:
                    to_finish[job_d].pop(0)
                    del job_mappings[job_d]
                    if len(to_finish[job_d]) == 0:
                        return None
                else:
                    log.debug(schedule.to_str())

                    # update time_core_jars
                    m_time_core_prod = get_mapping_time_core_product(
                        current_mapping, job_d.cratio)
                    time_core_jars -= m_time_core_prod
                    log.debug('Job_mappings: {}'.format([
                        (j.to_str(), m.get_used_processor_types(),
                         m.metadata.energy * (1.0 - j.cratio))
                        for j, m in job_mappings.items()
                    ]))

        return schedule

    def __schedule_2(self):
        tt = self.__job_table
        mapping = self.__map_infinite_jobs()

        if None not in mapping:
            res_scheduling = self.__schedule_mapping(mapping)
            assert res_scheduling is not None
            return res_scheduling

        to_be_scheduled = set(
            [i for i, x in enumerate(tt) if x.deadline != math.inf])
        max_deadline = max([tt[x].deadline for x in to_be_scheduled])
        core_type_jars = NamedDimensionalNumber(
            dict(self.__platform.get_processor_types())) * max_deadline
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
                to_finish[tid] = self.__select_app_mappings_fit_jars(
                    app, d, core_type_jars, completion=c)
                log.debug("{}: {}".format(tid, to_finish[tid]))

            while True:
                i_md, diff = None, -math.inf
                for tid in to_be_scheduled:
                    log.debug(
                        "Canonical mappings in list (to_finish), job {}: {}"
                        .format(tid, to_finish[tid]))
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

    def schedule(self, jobs, scheduling_start_time=0.0):
        self.__jobs = jobs
        self.__scheduling_start_time = scheduling_start_time
        # TODO: Consider to remove version 2
        if self.__version == "original":
            schedule = self.__schedule_original()
        elif self.__version == "2":
            schedule = self.__schedule_2()
        else:
            assert False
        return schedule

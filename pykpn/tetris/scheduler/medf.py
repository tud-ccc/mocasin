# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.schedule import (Schedule, MultiJobSegmentMapping,
                                   SingleJobSegmentMapping, TIME_EPS)
from pykpn.tetris.scheduler.base import SchedulerBase

from collections import Counter
import copy
import logging
import math

log = logging.getLogger(__name__)


def get_mapping_time_core_product(mapping, cratio=0.0):
    rtime = mapping.metadata.exec_time * (1.0-cratio)
    return Counter(
        {k: v * rtime
         for k, v in mapping.get_used_processor_types().items()})


class MedfScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        """ Maximum Energy Difference First Scheduler. """
        super().__init__(platform, **kwargs)

        if not self.preemptions:
            raise RuntimeError(
                "MedfScheduler only generates schedules with preemtpions")

    @property
    def name(self):
        return "MEDF"

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

    def _append_job_mapping_to_schedule(self, schedule, job, mapping,
                                        check_only_counters=False):
        """Add a job mappings to a schedule

        Args:
            schedule (Schedule): a currently constructing schedule
            job (Job): a job
            mapping (Mapping): a mapping
            check_only_counters (bool): whether we check only processor counters
                instead of exact processors

        Returns: a tuple (successful, job_finish_time), where
            successful (bool): whether a job was added without violating
                deadlines
            job_finish_time (float): finish time of the job
        """
        cur_cratio = job.cratio
        cur_rtime = mapping.metadata.exec_time * (1.0-cur_cratio)
        job_finish_time = None

        platform_proc_types = self.platform.get_processor_types()
        mapping_procs = mapping.get_used_processors()
        mapping_proc_types = mapping.get_used_processor_types()

        # First try to put the job into segments
        for index, segment in enumerate(schedule):
            if check_only_counters:
                # Check only the counters
                added_segment_proc_types = (
                    segment.get_used_processor_types() + mapping_proc_types)
                if ((added_segment_proc_types | platform_proc_types) !=
                        platform_proc_types):
                    # This segment has no enough resources
                    continue
            else:
                # Check that the mapping can fit the processors
                segment_procs = segment.get_used_processors()
                overlap_procs = segment_procs.intersection(mapping_procs)
                if overlap_procs:
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

            jm = SingleJobSegmentMapping(job.request, mapping,
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

            jm = SingleJobSegmentMapping(job.request, mapping,
                                         start_time=segment_start_time,
                                         start_cratio=cur_cratio,
                                         finished=True)
            new_segment = MultiJobSegmentMapping(self.platform, jobs=[jm])
            schedule.append_segment(new_segment)
            job_finish_time = jm.end_time

        # Check deadline
        res = (job_finish_time <= job.request.deadline)
        return (res, job_finish_time)

    def _form_schedule_with_job_mapping(self, schedule, job, mapping):
        """ Form a schedule with a job mapping.

        If rotations are allowed, the scheduler choose the variant, which
        minimizes finish time of the new job.

        Args:
            schedule (Schedule): a current schedule
            job (Job): a job
            mapping (Mapping): a mapping

        Returns: a new schedule object if the job was added successfully,
        otherwise returns None.
        """
        counter_schedule = schedule.copy()
        counter_result = self._append_job_mapping_to_schedule(
            counter_schedule, job, mapping, check_only_counters=True)
        successful, counter_end_time = counter_result
        if self.rotations:
            if not successful:
                return None
            equivalent_mappings = self.orbit_lookup_manager.get_orbit(
                job.app, mapping)
            best_result = math.inf, None
            for m in equivalent_mappings:
                m_schedule = schedule.copy()
                m_result = self._append_job_mapping_to_schedule(
                    m_schedule, job, m)
                m_successful, m_end_time = m_result
                if not m_successful:
                    continue
                if m_end_time - counter_end_time < TIME_EPS:
                    # Found best schedule
                    return m_schedule
                if m_end_time < best_result[0]:
                    best_result = m_end_time, m_schedule
            return best_result[1]
        else:
            return counter_schedule if successful else None

    def _form_schedule(self, job_mappings):
        ordered_job_mappings = sorted(job_mappings.items(),
                                      key=lambda kv: kv[0].request.deadline)

        schedule = Schedule(self.platform)

        for j, m in ordered_job_mappings:
            schedule = self._form_schedule_with_job_mapping(schedule, j, m)
            if schedule is None:
                return None
        return schedule

    def _map_infinite_jobs(self):
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
        return job_mappings

    def schedule(self, jobs, scheduling_start_time=0.0):
        self.__jobs = jobs
        self.__scheduling_start_time = scheduling_start_time
        job_mappings = self._map_infinite_jobs()
        schedule = self._form_schedule(job_mappings)

        max_deadline = max([
            j.request.deadline - scheduling_start_time
            for j in jobs if j.request.deadline != math.inf
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
                log.debug(
                    f"Checking mapping e:{current_mapping.metadata.energy*(1.0-job_d.cratio)}"
                )
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

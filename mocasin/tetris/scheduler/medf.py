# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from collections import Counter
import copy
import logging
import math

from mocasin.tetris.job_request import JobRequestStatus
from mocasin.tetris.schedule import (
    Schedule,
    MultiJobSegmentMapping,
    SingleJobSegmentMapping,
    TIME_EPS,
)
from mocasin.tetris.scheduler import SchedulerBase

log = logging.getLogger(__name__)


def get_mapping_time_core_product(mapping, cratio=0.0):
    rtime = mapping.metadata.exec_time * (1.0 - cratio)
    return Counter(
        {k: v * rtime for k, v in mapping.get_used_processor_types().items()}
    )


class MedfScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        """Maximum Energy Difference First Scheduler."""
        super().__init__(platform, **kwargs)

        if not self.preemptions:
            raise RuntimeError(
                "MedfScheduler only generates schedules with preemtpions"
            )

    @property
    def name(self):
        return "MEDF"

    def _update_filtered_mappings(self, filtered, jobs, time_core_jars):
        """Filters mappings which can feet core jars and deadlines.

        Args:
            filtered (List): a list of mappings to be filtered
            jobs (List): a list of remaining jobs
            core_jars (Counter): available core jars volume

        Returns: a list of mappings satisfying deadline and jars conditions.
        """
        for job in filtered.copy():
            if job not in jobs:
                filtered.pop(job)
                continue
            renergies = []
            for m in filtered[job].copy():
                rtime = m.metadata.exec_time * (1.0 - job.cratio)
                if rtime > job.request.deadline - self.__scheduling_start_time:
                    filtered[job].remove(m)
                    continue
                m_time_core_prod = get_mapping_time_core_product(m, job.cratio)
                if (m_time_core_prod | time_core_jars) != time_core_jars:
                    filtered[job].remove(m)
                    continue
                renergies.append(m.metadata.energy * (1.0 - job.cratio))
            log.debug("filtered[{}]: {}".format(job.to_str(), renergies))
        return filtered

    def _append_job_mapping_to_schedule(
        self, schedule, job, mapping, check_only_counters=False
    ):
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
        cur_rtime = mapping.metadata.exec_time * (1.0 - cur_cratio)
        job_finish_time = None

        platform_proc_types = self.platform.get_processor_types()
        mapping_procs = mapping.get_used_processors()
        mapping_proc_types = mapping.get_used_processor_types()

        # First try to put the job into segments
        for segment in schedule.segments():
            if check_only_counters:
                # Check only the counters
                added_segment_proc_types = (
                    segment.get_used_processor_types() + mapping_proc_types
                )
                if (
                    added_segment_proc_types | platform_proc_types
                ) != platform_proc_types:
                    # This segment has no enough resources
                    continue
            else:
                assert False, "NYI"

            if cur_rtime < segment.duration - TIME_EPS:
                s1, s2 = segment.split(segment.start_time + cur_rtime)
                # Remove old segment, insert new two segments
                schedule.remove_segment(segment)
                schedule.add_segment(s2)
                schedule.add_segment(s1)
                segment_to_add = s1
            else:
                segment_to_add = segment

            jm = SingleJobSegmentMapping(
                job.request,
                mapping,
                start_time=segment_to_add.start_time,
                start_cratio=cur_cratio,
                end_time=segment_to_add.end_time,
            )
            segment_to_add.append_job(jm)
            cur_cratio = jm.end_cratio
            cur_rtime = mapping.metadata.exec_time * (1.0 - cur_cratio)
            if jm.finished:
                # If the segment is a right fit for a job
                job_finish_time = jm.end_time
                break

        # If the job is still not finished, create a new segment
        if job_finish_time is None:
            # Create new segment with a job.
            segment_start_time = self.__scheduling_start_time
            if not schedule.is_empty():
                segment_start_time = schedule.end_time

            jm = SingleJobSegmentMapping(
                job.request,
                mapping,
                start_time=segment_start_time,
                start_cratio=cur_cratio,
                finished=True,
            )
            new_segment = MultiJobSegmentMapping(self.platform, jobs=[jm])
            schedule.add_segment(new_segment)
            job_finish_time = jm.end_time

        # Check deadline
        res = job_finish_time <= job.request.deadline
        return (res, job_finish_time)

    def _form_schedule_with_job_mapping(self, schedule, job, mapping):
        """Form a schedule with a job mapping.

        Args:
            schedule (Schedule): a current schedule
            job (Job): a job
            mapping (Mapping): a mapping

        Returns: a new schedule object if the job was added successfully,
        otherwise returns None.
        """
        counter_schedule = schedule.copy()
        counter_result = self._append_job_mapping_to_schedule(
            counter_schedule, job, mapping, check_only_counters=True
        )
        successful, counter_end_time = counter_result
        return counter_schedule if successful else None

    def _form_schedule(self, job_mappings):
        ordered_job_mappings = sorted(
            job_mappings.items(), key=lambda kv: kv[0].request.deadline
        )

        schedule = Schedule(self.platform)

        for j, m in ordered_job_mappings:
            if not m:
                continue
            schedule = self._form_schedule_with_job_mapping(schedule, j, m)
            if schedule is None:
                return None
        return schedule

    def _map_infinite_jobs(self, jobs):
        """Map jobs without deadlines.

        Since the algorithm uses an internal data structures "jars" initialized
        with the max deadline, we want to choose the mappings for infinite
        jobs outside the main part of the algorithm.

        Returns: a dict of job mappings
        """
        assert all(job.request.deadline == math.inf for job in jobs)

        job_mappings = {
            j: min(j.request.mappings, key=lambda m: m.metadata.energy)
            for j in jobs
        }
        return job_mappings

    def _initialize_filtered_mappings(self, jobs):
        res = {}
        for job in jobs:
            mappings = job.request.mappings.copy()
            mappings.sort(key=lambda m: m.metadata.energy)
            res[job] = mappings
        return res

    def _schedule_job_set(self, job_mappings, job_set, time_window):
        """Schedule a job set

        The function returns the schedule, as well as the `job_mappings` object
        is updated.
        """
        # Initialize time_core_jars
        time_core_jars = Counter(
            {
                k: v * time_window
                for k, v in self.platform.get_processor_types().items()
            }
        )
        for job, mapping in job_mappings.items():
            m_time_core_prod = get_mapping_time_core_product(
                mapping, job.cratio
            )
            time_core_jars -= m_time_core_prod

        remaining_jobs = job_set.copy()

        filtered = self._initialize_filtered_mappings(remaining_jobs)
        resultant_schedule = None

        while remaining_jobs:
            log.debug("Jars: {}".format(time_core_jars))
            # List of mappings to finish the applications
            filtered = self._update_filtered_mappings(
                filtered, remaining_jobs, time_core_jars
            )
            # Find the job with the maximum energy difference between first two
            # mappings
            diff = (-math.inf, None)
            for job in remaining_jobs:
                if len(filtered[job]) == 0:
                    continue
                if len(filtered[job]) == 1:
                    diff = (math.inf, job)
                    continue
                # Check energy difference between first two mappings
                cdiff = (1.0 - job.cratio) * (
                    filtered[job][1].metadata.energy
                    - filtered[job][0].metadata.energy
                )
                if cdiff > diff[0]:
                    diff = (cdiff, job)

            # Select the job to schedule
            _, job_d = diff
            if job_d is None:
                # There are still jobs, but no mappings could be assigned
                for job in remaining_jobs:
                    job_mappings[job] = None
                break
            log.debug("Choose {}".format(job_d.to_str()))

            while job_d not in job_mappings:
                current_mapping = filtered[job_d].pop(0)
                job_mappings[job_d] = current_mapping
                log.debug(
                    "Checking mapping e:{}".format(
                        current_mapping.metadata.energy * (1.0 - job_d.cratio)
                    )
                )
                schedule = self._form_schedule(job_mappings)
                if schedule is None:
                    del job_mappings[job_d]
                    if len(filtered[job_d]) == 0:
                        job_mappings[job_d] = None
                else:
                    log.debug(schedule.to_str())

                    # update time_core_jars
                    m_time_core_prod = get_mapping_time_core_product(
                        current_mapping, job_d.cratio
                    )
                    time_core_jars -= m_time_core_prod
                    resultant_schedule = schedule
                    log.debug(
                        "Job_mappings: {}".format(
                            [
                                (
                                    j.to_str(),
                                    m.get_used_processor_types(),
                                    m.metadata.energy * (1.0 - j.cratio),
                                )
                                if m
                                else (j.to_str(), None)
                                for j, m in job_mappings.items()
                            ]
                        )
                    )
            assert job_d in job_mappings
            remaining_jobs.remove(job_d)
        return resultant_schedule

    def schedule(
        self,
        jobs,
        scheduling_start_time=0.0,
        allow_partial_solution=False,
        current_schedule=None,
    ):
        """Schedule the jobs.

        If `allow_partial_solution` is True, the scheduler could schedule only
        the part of the jobs if it cannot schedule all jobs. Otherwise, it
        schedules all jobs or returns None.

        if `current_schedule` is not None, the scheduler tries to reuse the
        previously generated schedule.
        """
        self.__scheduling_start_time = scheduling_start_time

        # Schedule jobs with infinite deadline
        infinite_jobs = [
            job for job in jobs if job.request.deadline == math.inf
        ]
        job_mappings = self._map_infinite_jobs(infinite_jobs)
        resultant_schedule = self._form_schedule(job_mappings)

        # Calculate time window
        remaining_jobs = [j for j in jobs if j not in job_mappings]
        time_window = 0
        if remaining_jobs:
            max_deadline = max([j.request.deadline for j in remaining_jobs])
            time_window = max_deadline - scheduling_start_time

        # Reuse the job mappings from the previous schedule
        if self.schedule_reuse and current_schedule:
            current_schedule_requests = current_schedule.get_requests()
            for job in remaining_jobs:
                request = job.request
                if request not in current_schedule_requests:
                    continue
                mapping_list = current_schedule.find_request_segments(request)
                job_mappings[job] = mapping_list[-1].mapping
            resultant_schedule = current_schedule

        remaining_jobs = [j for j in jobs if j not in job_mappings]

        # Map the remaining jobs
        if self.schedule_reuse and current_schedule:
            # if current schedule is supplied, all remaining jobs should be new
            assert all(
                job.request.status == JobRequestStatus.NEW
                for job in remaining_jobs
            )

        schedule = self._schedule_job_set(
            job_mappings, remaining_jobs, time_window
        )
        if schedule:
            resultant_schedule = schedule

        if not allow_partial_solution:
            # If any previously accepted job was refused, return None
            if any(job_mappings[j] is None for j in jobs):
                return None

        rotated_schedule = self.variant_selector.finalize_schedule(
            resultant_schedule
        )
        return rotated_schedule

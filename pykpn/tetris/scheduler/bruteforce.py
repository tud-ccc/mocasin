# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import (Schedule, ScheduleSegment,
                                   JobSegmentMapping, MAX_END_GAP)
from pykpn.tetris.scheduler.base import SchedulerBase

from collections import Counter
import heapq
import logging
import math

EPS = 0.00001

log = logging.getLogger(__name__)


def _is_better_eu(a, b):
    """ Compare two schedules in terms of Energy-Utility Functions.
    """
    if b is None:
        return True
    if a.energy < b.energy - EPS:
        return True
    if a.energy > b.energy + EPS:
        return False
    if a.end_time < b.end_time + EPS:
        return True
    return False


class _BfSchedule(Schedule):
    """Inheritted schedule class for Bruteforce scheduler.

    This class is used to store intermediate mapping object with
    additional metadata.
    """
    def __init__(self, segments=[], best_case_energy=None):
        Schedule.__init__(self, segments=segments)
        assert best_case_energy is not None
        self.__best_case_energy = best_case_energy

    def copy(self):
        """_BfSchedule: returns a shallow copy of the mapping"""
        return _BfSchedule(self.segments(), self.__best_case_energy)

    @property
    def best_case_energy(self):
        return self.__best_case_energy

    @best_case_energy.setter
    def best_case_energy(self, val):
        self.__best_case_energy = val

    def __lt__(self, other):
        if self.count_non_finished_jobs() != other.count_non_finished_jobs():
            return (self.count_non_finished_jobs() <
                    other.count_non_finished_jobs())
        if self.best_case_energy != other.best_case_energy:
            return self.best_case_energy < other.best_case_energy
        if self.end_time != other.end_time:
            return self.end_time > other.end_time
        if len(self) > 0 and len(other) > 0:
            if self.last.energy != other.last.energy:
                return self.last.energy < other.last.energy
        if self.energy != other.energy:
            return self.energy < other.energy
        return id(self) < id(other)

    def count_non_finished_jobs(self):
        return sum([
            1 for _, ms in self.per_requests().items() if not ms[-1].finished
        ])


class BruteforceSegmentScheduler:
    def __init__(self, parent_scheduler):
        self.__parent = parent_scheduler

        # Initialize variables used during the scheduling to None
        self.__jobs = None
        self.__step_best_energy = None
        self.__segment_start_time = None
        self.__accumulated_energy = None
        self.__results = None

    def __eval_min_segment_duration(self):
        """Evaluate minimal segment duration.
        """
        return min([
            mapping.metadata.exec_time * (1.0 - job.cratio)
            for job in self.__jobs for mapping in job.request.mappings
        ])

    def __eval_core_energy_usage(self, current_mappings):
        """Evaluate the energy and used processors types of assigned mappings.

        The length of 'current_mappings' equals to the number of already
        assigned jobs. The energy consumption is evaluated assuming minimal
        duration of the segment '__min_segment_duration'.

        Args:
            current_mappings (list of Mapping): The list of mappings

        Returns: a tuple (core_types (Counter), energy (float))
        """
        # Initialize the variables to zero values
        energy = 0
        core_types = Counter()

        for job, mapping in zip(self.__jobs, current_mappings):
            cratio = job.cratio
            if mapping is not None:
                rratio = 1.0 - cratio
                config_rem_time = mapping.metadata.exec_time * rratio
                assert config_rem_time > self.__min_segment_duration - EPS
                energy += (mapping.metadata.energy *
                           self.__min_segment_duration /
                           mapping.metadata.exec_time)
                core_types.update(mapping.get_used_processor_types())
        return (core_types, energy)

    def __form_schedule_segment(self, job_mappings):
        """ Construct a schedule segment out of job mappings.

        Args:
            job_mappings (list of Mapping): The list of job mappings.

        Returns: a ScheduleSegment object
        """
        # TODO: Return only a schedule segment
        res = []
        full_mapping_list = []

        # Calculate segment end time
        jobs_rem_time = [
            m.metadata.exec_time * (1.0 - j.cratio)
            for j, m in zip(self.__jobs, job_mappings) if m is not None
        ]
        segment_duration = max(
            [t for t in jobs_rem_time if t < min(jobs_rem_time) + MAX_END_GAP])
        segment_end_time = segment_duration + self.__segment_start_time
        assert segment_duration > self.__min_segment_duration - EPS

        segment_mapping_list = []
        for j, m in zip(self.__jobs, job_mappings):
            if m is not None:
                ssm = JobSegmentMapping(j.request, m,
                                        start_time=self.__segment_start_time,
                                        start_cratio=j.cratio,
                                        end_time=segment_end_time)
                segment_mapping_list.append(ssm)

        # Check if all jobs might meet deadlines given the current mapping
        # TODO: Check idle jobs
        segment_meets_deadline = True
        finished = True
        for sm in segment_mapping_list:
            d = sm.request.deadline
            if not sm.finished:
                finished = False
            if sm.end_time > d:
                segment_meets_deadline = False
            min_time_left = sm.request.get_min_exec_time() * (1.0 -
                                                              sm.end_cratio)
            if min_time_left + sm.end_time > d:
                segment_meets_deadline = False

        if segment_meets_deadline:
            # Evaluate best-case energy consumption
            cur_energy = sum([x.energy for x in segment_mapping_list])
            total_energy = cur_energy + self.__accumulated_energy
            best_case_energy = total_energy
            for sm in segment_mapping_list:
                bc_energy = sm.request.get_min_energy() * (1.0 - sm.end_cratio)
                best_case_energy += bc_energy

            new_schedule = self.__prev_schedule.copy()
            new_segment = ScheduleSegment(
                self.__parent.platform, segment_mapping_list,
                time_range=(self.__segment_start_time, segment_end_time))
            new_segment.verify()
            new_schedule.append_segment(new_segment)
            new_schedule.best_case_energy = total_energy
            res.append((segment_meets_deadline, total_energy, new_schedule))
        return res

    def __schedule_step(self, current_mappings):
        """ Perform a single step of the bruteforce algorithm.

        Args:
            current_mappings (list): list of the chosen mappings for jobs.
        """
        (used_cores, e) = self.__eval_core_energy_usage(current_mappings)
        total_cores = self.__parent.platform.get_processor_types()

        # Check whether the current used cores do not exceed available cores
        if (used_cores | total_cores) != total_cores:
            return

        # Whether all jobs are mapped
        if len(current_mappings) == len(self.__jobs):
            # Skip mappings with all idle jobs
            only_idle = all(m is None for m in current_mappings)
            if only_idle:
                return

            results = self.__form_schedule_segment(current_mappings)
            for r, energy, m in results:
                if r:
                    self.__results.append(m)
            return

        next_job = self.__jobs[len(current_mappings)]
        for mapping in next_job.request.mappings + [None]:
            self.__schedule_step(current_mappings + [mapping])

    def schedule(self, jobs, segment_start_time=0.0, accumulated_energy=0.0,
                 prev_schedule=None):
        """ Schedule the jobs.

        Args:
            jobs (list of JobState): a list of jobs
        """
        # TODO: Remove prev_schedule
        assert prev_schedule is not None

        assert self.__jobs is None

        # Check that all jobs are in ready state
        _jobs = []
        for j in jobs:
            if j.is_ready() or j.is_running():
                _jobs.append(j)
                continue
            log.warning(
                "Removing job with a state {} from a job list: {}".format(
                    j.state, j.to_str()))

        if len(_jobs) == 0:
            log.warning("No job to schedule")
            return []

        # Initialize variables
        self.__jobs = _jobs
        self.__min_segment_duration = self.__eval_min_segment_duration()
        self.__step_best_energy = math.inf
        self.__segment_start_time = segment_start_time
        self.__results = []
        self.__accumulated_energy = accumulated_energy
        self.__prev_schedule = prev_schedule

        # Run step scheduler
        self.__schedule_step([])
        results = self.__results

        # Deinitialize variables
        self.__jobs = None
        self.__min_segment_duration = None
        self.__step_best_energy = None
        self.__results = None
        self.__segment_start_time = None
        self.__accumulated_energy = None
        self.__prev_schedule = None

        return results


class BruteforceScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        super().__init__(platform)

        self.__dump_steps = kwargs["bf_dump_steps"]
        # Initialize a step scheduler
        self.__segment_scheduler = BruteforceSegmentScheduler(self)

    @property
    def name(self):
        return "Exact"

    def __register_best_scheduling(self, m):
        self.__best_scheduling = m
        self.__best_energy = m.energy
        log.debug("Found new best scheduling: energy = {}".format(
            self.__best_energy))
        log.debug("New scheduling: \n" + self.__best_scheduling.to_str() +
                  '\n')
        pass

    def _energy_limit(self):
        return self.__best_energy + EPS

    def __hq_best_est_energy(self):
        hq_bc_list = [x.best_case_energy for x in self.__hq]
        if len(hq_bc_list) > 0:
            return min(hq_bc_list)
        else:
            return math.inf

    def __calc_distribution_by_finished(self):
        # FIXME: count_non_finished_jobs might be incorrect because the schedule
        # does not include idle jobs
        num_tasks = len(self.__jobs)

        res = [0] * (num_tasks+1)
        for s in self.__hq:
            res[num_tasks - s.count_non_finished_jobs()] += 1
        return res

    def __clear(self):
        self.__best_scheduling = None
        self.__best_energy = math.inf
        self._wc_energy = math.inf
        self.__hq = []

    def schedule(self, jobs, scheduling_start_time=0.0):
        """Find the optimal scheduling.

        Args:
            jobs (list[JobState]): jobs to schedule
            scheduling_start_time (float): a start time

        Returns:
            a tuple (successful, list of configurations)
        """
        self.__clear()
        self.__jobs = jobs
        self.__scheduling_start_time = scheduling_start_time

        # Generate the empty mapping
        m = None

        heapq.heappush(self.__hq, m)

        finished = []
        step_counter = 0

        while self.__hq:
            l = len(self.__hq)
            m = heapq.heappop(self.__hq)
            if m is None:
                # First iteration
                current_jobs = self.__jobs.copy()
                m = _BfSchedule(segments=[], best_case_energy=-1)
                segment_start_time = self.__scheduling_start_time
            else:
                # Create a list of remained jobs
                current_jobs = [
                    x for x in Job.from_schedule(m, self.__jobs)
                    if not x.is_terminated()
                ]
                segment_start_time = m.end_time

            e = m.energy
            bc = m.best_case_energy
            if e > self._energy_limit():
                continue

            if bc > self._energy_limit():
                continue
            step_counter += 1

            # print("current_jobs", [j.to_str() for j in current_jobs])
            results = self.__segment_scheduler.schedule(
                current_jobs, segment_start_time=segment_start_time,
                accumulated_energy=e, prev_schedule=m)
            # print("#results:", len(results))
            results.sort()

            for m in results:
                e = m.energy
                if e > self._energy_limit():
                    continue
                if m.best_case_energy > self._energy_limit():
                    continue
                # Check that all jobs are finished
                req_schedules = m.per_requests()
                all_jobs_finished = True
                for j in self.__jobs:
                    if j.request not in req_schedules:
                        all_jobs_finished = False
                        break
                    if not req_schedules[j.request][-1].finished:
                        all_jobs_finished = False
                        break
                if all_jobs_finished:
                    if _is_better_eu(m, self.__best_scheduling):
                        self.__register_best_scheduling(m)
                    continue
                heapq.heappush(self.__hq, m)

            if step_counter % self.__dump_steps == 0:
                distr_finished = self.__calc_distribution_by_finished()
                log.debug("step_counter = {}, queue_size = {}, "
                          "found_best_energy = {}, hq_best_est_energy = {}, "
                          "distr_by_finished = {}".format(
                              step_counter, len(self.__hq), self.__best_energy,
                              self.__hq_best_est_energy(), distr_finished))

        return self.__best_scheduling

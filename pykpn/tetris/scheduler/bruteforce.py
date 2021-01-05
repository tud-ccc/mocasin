# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import (Schedule, ScheduleSegment,
                                   JobSegmentMapping, MAX_END_GAP, ENERGY_EPS,
                                   TIME_EPS)
from pykpn.tetris.scheduler.base import SegmentSchedulerBase, SchedulerBase

from collections import Counter
import heapq
import logging
import math

log = logging.getLogger(__name__)


def _is_better_eu(a, b):
    """ Compare two schedules in terms of Energy-Utility Functions.
    """
    if b is None:
        return True
    if a.energy < b.energy - ENERGY_EPS:
        return True
    if a.energy > b.energy + ENERGY_EPS:
        return False
    if a.end_time < b.end_time + TIME_EPS:
        return True
    return False


def get_jobs_bc_energy(jobs):
    """ Returns the best energy of job lists.
    """
    return sum([(1.0 - j.cratio) * j.request.get_min_energy() for j in jobs
                if not j.is_terminated()])


class BruteforceSegmentScheduler(SegmentSchedulerBase):
    def __init__(self, scheduler):
        super().__init__(scheduler, scheduler.platform)

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
                assert config_rem_time > self.__min_segment_duration - TIME_EPS
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
        # Skip mappings with all idle jobs
        only_idle = all(m is None for m in job_mappings)
        if only_idle:
            return None

        # Calculate segment end time
        jobs_rem_time = [
            m.metadata.exec_time * (1.0 - j.cratio)
            for j, m in zip(self.__jobs, job_mappings) if m is not None
        ]
        segment_duration = max(
            [t for t in jobs_rem_time if t < min(jobs_rem_time) + MAX_END_GAP])
        segment_end_time = segment_duration + self.__segment_start_time
        assert segment_duration > self.__min_segment_duration - TIME_EPS

        # Construct JobSegmentMapping objects
        job_segments = []
        for j, m in zip(self.__jobs, job_mappings):
            if m is not None:
                ssm = JobSegmentMapping(j.request, m,
                                        start_time=self.__segment_start_time,
                                        start_cratio=j.cratio,
                                        end_time=segment_end_time)
                job_segments.append(ssm)

        # Construct a schedule segment
        new_segment = ScheduleSegment(self.scheduler.platform, job_segments)
        new_segment.verify()
        return new_segment

    def __schedule_step(self, current_mappings):
        """ Perform a single step of the bruteforce algorithm.

        Args:
            current_mappings (list): list of the chosen mappings for jobs.
        """
        (used_cores, e) = self.__eval_core_energy_usage(current_mappings)
        total_cores = self.scheduler.platform.get_processor_types()

        # Check whether the current used cores do not exceed available cores
        if (used_cores | total_cores) != total_cores:
            return

        # Whether all jobs are mapped
        if len(current_mappings) == len(self.__jobs):
            segment = self.__form_schedule_segment(current_mappings)
            if segment is None:
                return

            # Check that all jobs meet dealines
            for js in segment:
                if js.end_time > js.request.deadline:
                    return

            # Generate the job states at the end of the segment
            new_jobs = [
                x for x in Job.from_schedule(Schedule(self.platform, segment),
                                             self.__jobs)
                if not x.is_terminated()
            ]

            # Check whether all remaining jobs still meet deadlines
            if not all(
                    j.can_meet_deadline(segment.end_time) for j in new_jobs):
                return

            new_schedule = self.__prev_schedule.copy()
            new_schedule.append_segment(segment)
            self.__results.append((new_schedule, new_jobs))
            return

        next_job = self.__jobs[len(current_mappings)]
        for mapping in next_job.request.mappings + [None]:
            self.__schedule_step(current_mappings + [mapping])

    # TODO: Remove prev_schedule
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


class ScheduleHeap:
    def __init__(self):
        self._index = 0
        self._data = []

    @staticmethod
    def _key(schedule, jobs):
        """ Returns a tuple: (-#finished_jobs, bc_energy, -end_time).
        """
        f = schedule.count_finished_jobs()
        full_bc_energy = schedule.energy + get_jobs_bc_energy(jobs)
        end_time = schedule.end_time
        if end_time is None:
            end_time = -math.inf
        return (-f, full_bc_energy, -end_time)

    def __len__(self):
        return len(self._data)

    def empty(self):
        return len(self._data) == 0

    def push(self, schedule, jobs):
        key = self._key(schedule, jobs)
        heapq.heappush(self._data, (key, self._index, (schedule, jobs)))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._data)[2]

    def _get_finished_distr(self):
        res = []
        for item in self._data:
            s, _ = item[2]
            f = s.count_finished_jobs()
            while len(res) <= f:
                res.append(0)
            res[f] += 1
        return res

    def _get_min_bc_energy(self):
        return min([
            schedule.energy + get_jobs_bc_energy(jobs)
            for _, _, (schedule, jobs) in self._data
        ])


class BruteforceScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        super().__init__(platform)

        self.__dump_steps = kwargs["bf_dump_steps"]
        # Initialize a segment scheduler
        self.__segment_scheduler = BruteforceSegmentScheduler(self)

    @property
    def name(self):
        return "Exact"

    def __register_best_schedule(self, m):
        self.__best_schedule = m
        self.__best_energy = m.energy
        log.debug("Found new best schedule: energy = {}".format(
            self.__best_energy))
        log.debug("New schedule: \n" + self.__best_schedule.to_str() + '\n')
        pass

    def _energy_limit(self):
        return self.__best_energy + ENERGY_EPS

    def __clear(self):
        self.__best_schedule = None
        self.__best_energy = math.inf

    def schedule(self, jobs, scheduling_start_time=0.0):
        """Find the optimal scheduling.

        Args:
            jobs (list[JobState]): jobs to schedule
            scheduling_start_time (float): a start time

        Returns:
            a tuple (successful, list of configurations)
        """
        # Initialization
        self.__clear()
        self.__jobs = jobs
        self.__scheduling_start_time = scheduling_start_time

        # Create ScheduleHeap, push a starting point
        schedule_heap = ScheduleHeap()
        schedule_heap.push(Schedule(self.platform, []), self.__jobs)

        step_counter = 0

        while not schedule_heap.empty():
            if step_counter % self.__dump_steps == 0:
                finished_distr = schedule_heap._get_finished_distr()
                log.debug(
                    "step_cnt = {}, heap_size = {}, "
                    "found_best_energy = {:.3f}, heap_bc_energy = {:.3f}, "
                    "distr_by_finished = {}".format(
                        step_counter, len(schedule_heap), self.__best_energy,
                        schedule_heap._get_min_bc_energy(), finished_distr))
            step_counter += 1

            cschedule, cjobs = schedule_heap.pop()
            cstart_time = self.__scheduling_start_time
            if len(cschedule.segments()) > 0:
                cstart_time = cschedule.end_time

            full_bc_energy = cschedule.energy + get_jobs_bc_energy(cjobs)
            if full_bc_energy > self._energy_limit():
                continue

            # print("current_jobs", [j.to_str() for j in current_jobs])
            results = self.__segment_scheduler.schedule(
                cjobs, segment_start_time=cstart_time,
                accumulated_energy=cschedule.energy, prev_schedule=cschedule)
            # print("#segments:", len(segments))

            for nsegment, njobs in results:
                # Check whether all jobs are finished
                all_jobs_finished = all(
                    nsegment.is_request_completed(j.request)
                    for j in self.__jobs)
                if all_jobs_finished:
                    if _is_better_eu(nsegment, self.__best_schedule):
                        self.__register_best_schedule(nsegment)
                    continue

                # otherwise push the new state into the heap
                schedule_heap.push(nsegment, njobs)

        return self.__best_schedule

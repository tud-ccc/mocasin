# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

# TODO:
# [ ] Separate Memoization code into another class/file
# [ ] Remove pruning in memoization
# [ ] Remove time limits

from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import Schedule, ScheduleSegment, JobSegmentMapping
from pykpn.tetris.scheduler.base import SchedulerBase

from collections import Counter
import heapq
import logging
import math
import time

EPS = 0.00001
FINISH_MAX_DIFF = 0.5

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
    def __init__(self, parent_scheduler, all_combinations=False):
        self.__parent = parent_scheduler
        self.__all_combinations = all_combinations

        # Initialize variables used during the scheduling to None
        self.__jobs = None
        self.__step_best_energy = None
        self.__segment_start_time = None
        self.__accumulated_energy = None
        self.__force_return = None
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

        # Calculate estimated end time
        for job, mapping in zip(self.__jobs, job_mappings):
            if mapping is not None:
                single_job_mapping = JobSegmentMapping(
                    job.request, mapping, start_time=self.__segment_start_time,
                    start_cratio=job.cratio, finished=True)
                full_mapping_list.append(single_job_mapping)

        # Check if the scheduling meets deadlines
        full_meets_deadline = True
        for sm in full_mapping_list:
            d = sm.request.deadline
            if sm.end_time > d:
                full_meets_deadline = False
            # if sm.idle:
            #     full_meets_deadline = False

        if full_meets_deadline and False:
            # TODO: This branch constructs the mapping where all jobs meet
            # deadlines. This step optimizes the bruteforce algorithm, however
            # I doubt that it significantly reduces the search time, maybe
            # I remove it later
            cur_energy = sum([x.energy for x in full_mapping_list])
            total_energy = cur_energy + self.__accumulated_energy
            if self.__step_best_energy > total_energy:
                self.__step_best_energy = total_energy

            full_finish_time = max([x.end_time for x in full_mapping_list])
            new_segment = ScheduleSegment(
                self.__parent.platform, full_mapping_list,
                time_range=(self.__segment_start_time, full_finish_time))
            new_schedule = _BfSchedule(segments=[new_segment],
                                       best_case_energy=total_energy)
            res.append((full_meets_deadline, total_energy, new_schedule))

        segment_mapping_list = []
        min_finish_time = min([x.end_time for x in full_mapping_list])
        stop_jobs = [
            x for x in full_mapping_list
            if x.end_time < min_finish_time + FINISH_MAX_DIFF
        ]
        segment_end_time = max([x.end_time for x in stop_jobs])
        segment_duration = segment_end_time - self.__segment_start_time
        assert segment_duration > self.__min_segment_duration - EPS
        for fsm in full_mapping_list:
            ssm = JobSegmentMapping(fsm.request, fsm.mapping,
                                    start_time=fsm.start_time,
                                    start_cratio=fsm.start_cratio,
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
        if self.__force_return:
            return

        (used_cores, e) = self.__eval_core_energy_usage(current_mappings)
        total_cores = self.__parent.platform.get_processor_types()

        # Check whether the current used cores do not exceed available cores
        if (used_cores | total_cores) != total_cores:
            return

        # Check current energy
        if not self.__all_combinations:
            if e + self.__accumulated_energy > self.__parent._energy_limit():
                return

            # Check current energy
            if e + self.__accumulated_energy > self.__step_best_energy:
                return

        # Whether all jobs are mapped
        if len(current_mappings) == len(self.__jobs):
            # Skip mappings with all idle jobs
            only_idle = all(m is None for m in current_mappings)
            if only_idle:
                return

            results = self.__form_schedule_segment(current_mappings)
            # print("results", results)
            for r, energy, m in results:
                if r:
                    self.__results.append(m)

            if not self.__parent._within_time_limit():
                self.__force_return = True
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
        self.__force_return = False
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
        self.__force_return = None
        self.__results = None
        self.__segment_start_time = None
        self.__accumulated_energy = None
        self.__prev_schedule = None

        return results


class StateMemoryTable:

    COMP_STEP = 0.01
    TIME_STEP = 0.1

    def __init__(self, num_apps, prune_mem_table=False):
        self.__num_apps = num_apps
        self.__table = []
        self.__prune_mem_table = prune_mem_table
        self.__added_cnt = 0

    def find_min_energy_from_state(self, task_comp, time, exclude_list=[]):
        max_energy = 0
        found = False
        for idx, s in enumerate(self.__table):
            if idx in exclude_list:
                continue
            if s['time'] > time + EPS:
                continue
            rs = True
            for msc, tc in zip(s['task_comp'], task_comp):
                if msc + EPS < tc:
                    rs = False
                    break
            if not rs:
                continue
            found = True
            if max_energy < s['min_energy']:
                max_energy = s['min_energy']
        if found:
            return max_energy
        else:
            return None

    def __prune(self):
        log.debug("Pruning the memory table. Current size = {}".format(
            len(self.__table)))
        to_exclude = []
        for idx, item in enumerate(self.__table):
            found_energy = self.find_min_energy_from_state(
                item['task_comp'], item['time'], to_exclude + [idx])
            if found_energy is None:
                continue
            if found_energy + EPS > item['min_energy']:
                to_exclude.append(idx)
        log.debug("Items to remove: {}".format(to_exclude))
        self.__table = [
            v for k, v in enumerate(self.__table) if k not in to_exclude
        ]
        log.debug("New size = {}".format(len(self.__table)))

    def size(self):
        return len(self.__table)

    def add_state(self, task_comp, time, min_energy):
        assert len(task_comp) == self.__num_apps
        current_e = self.find_min_energy_from_state(task_comp, time)
        if current_e is not None:
            # assert min_energy + EPS > current_e,
            # "For task_comp = {}, time = {}, found current_e = {},"
            # " new min_energy = {}".format(
            # task_comp, time, current_e, min_energy)
            if abs(min_energy - current_e) < EPS:
                return
            if min_energy < current_e + EPS:
                return
        if self.__prune_mem_table and False:
            task_comp = [
                math.floor(x / StateMemoryTable.COMP_STEP) *
                StateMemoryTable.COMP_STEP for x in task_comp
            ]
            time = math.ceil(
                time / StateMemoryTable.TIME_STEP) * StateMemoryTable.TIME_STEP
        s = {}
        s['task_comp'] = task_comp
        s['time'] = time
        s['min_energy'] = min_energy
        self.__table.append(s)

        if self.__prune_mem_table:
            self.__added_cnt += 1
            if self.__added_cnt % 100 == 0:
                self.__prune()

    def dump_str(self):
        res = "StateMemoryTable:\n"
        for idx, item in enumerate(self.__table):
            res += "{}: time = {}, task states = {}, min energy = {}\n".format(
                idx, item['time'], item['task_comp'], item['min_energy'])
        return res


class BruteforceScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        super().__init__(platform)

        self.__dump_steps = kwargs["bf_dump_steps"]

        self.__time_limit = kwargs["time_limit"]

        self.__scheduled_on_time = True
        self.__memoization = kwargs["memoization"]
        self.__dump_mem_table = kwargs["dump_mem_table"]
        self.__prune_mem_table = kwargs["prune_mem_table"]

        # Initialize a step scheduler
        self.__step_scheduler = BruteforceSegmentScheduler(
            self, all_combinations=self.__memoization)

    @property
    def name(self):
        if not self.__memoization:
            res = "Exact"
        else:
            res = "Exact-Memo"
        if self.__time_limit:
            res += "-TL{:.1f}".format(self.__time_limit)
        return res

    def _within_time_limit(self):
        if self.__time_limit is None:
            return True
        if time.time() - self.__start_time > self.__time_limit:
            self.__scheduled_on_time = False
            return False
        return True

    def __register_best_scheduling(self, m):
        self.__best_scheduling = m
        self.__best_energy = m.energy
        self.__filter_queue()
        log.debug("Found new best scheduling: energy = {}".format(
            self.__best_energy))
        log.debug("New scheduling: \n" + self.__best_scheduling.to_str() +
                  '\n')
        pass

    def _energy_limit(self):
        return self.__best_energy + EPS

    def __filter_queue(self):
        energy_limit = self._energy_limit()
        filtered = [x for x in self.__hq if x.best_case_energy < energy_limit]
        heapq.heapify(filtered)
        self.__hq = filtered
        pass

    def __hq_best_est_energy(self):
        hq_bc_list = [x.best_case_energy for x in self.__hq]
        if len(hq_bc_list) > 0:
            return min(hq_bc_list)
        else:
            return math.inf

    def __filter_step_results(self, res):
        energy_limit = self._energy_limit()
        new_res = [
            x for x in res
            if x.energy < energy_limit and x.best_case_energy < energy_limit
        ]
        return new_res

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
        if self.__time_limit is not None:
            self.__start_time = time.time()

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

        if self.__memoization:
            return self.__schedule_memoization()

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
                nf = -1  # TODO: What is it? Probably needs to be removed
                segment_start_time = self.__scheduling_start_time
            else:
                # Create a list of remained jobs
                current_jobs = [
                    x for x in Job.from_schedule(m, self.__jobs)
                    if not x.is_terminated()
                ]
                segment_start_time = m.end_time
                nf = m.count_non_finished_jobs()

            e = m.energy
            bc = m.best_case_energy
            if e > self._energy_limit():
                continue

            if bc > self._energy_limit():
                continue
            step_counter += 1

            # print("current_jobs", [j.to_str() for j in current_jobs])
            results = self.__step_scheduler.schedule(
                current_jobs, segment_start_time=segment_start_time,
                accumulated_energy=e, prev_schedule=m)
            # print("#results:", len(results))
            results = self.__filter_step_results(results)
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

            if not self._within_time_limit():
                log.debug("Reached time limit, returning")
                break

        return (self.__best_energy != math.inf, self.__best_scheduling,
                self.__scheduled_on_time)

    # Run scheduler with memoization
    def __schedule_memoization(self):
        self.__mem_step_counter = 0
        self.__mem_state_table = StateMemoryTable(len(self.__jobs),
                                                  self.__prune_mem_table)
        self.__force_return = False
        self.__schedule_memoization_step(None)
        return (self.__best_energy != math.inf, self.__best_scheduling,
                self.__scheduled_on_time)

    # Returns (min energy to finish)
    def __schedule_memoization_step(self, mapping):
        if not self._within_time_limit():
            self.__force_return = True
            log.debug("Reached time limit, returning")
            return math.inf
        self.__mem_step_counter += 1
        if mapping is None:
            prev_e = 0.0
            bc = -1
            nf = -1
        else:
            prev_e = mapping.energy
            bc = mapping.best_case_energy
            nf = mapping.count_non_finished_jobs()
        if bc > self._energy_limit():
            return (bc - e)

        if self.__mem_step_counter % self.__dump_steps == 0:
            log.debug("step_counter = {}, found_best_energy = {},"
                      " size(mem_table) = {}".format(
                          self.__mem_step_counter, self.__best_energy,
                          self.__mem_state_table.size()))

        if mapping is not None:
            req_schedules = mapping.per_requests()
            cratio_list = [
                req_schedules[j.request][-1].end_cratio
                if j.request in req_schedules else j.cratio
                for j in self.__jobs
            ]
            mem_e = self.__mem_state_table.find_min_energy_from_state(
                cratio_list, mapping.end_time)
            if self.__dump_mem_table:
                log.debug(self.__mem_state_table.dump_str())
                log.debug(
                    "Check mem table: comp = {}, time = {}, found energy = {}"
                    .format(cratio_list, mapping.end_time(), mem_e))
            if mem_e is not None:
                if self.__dump_mem_table:
                    log.debug("prev_energy = {}".format(prev_e))
                if mem_e == math.inf:
                    if self.__dump_mem_table:
                        log.debug("Returning")
                    return math.inf
                if mem_e + prev_e > self._energy_limit():
                    if self.__dump_mem_table:
                        log.debug("Returning")
                    return mem_e

        if mapping is None:
            jobs = self.__jobs.copy()
            passed_schedule = _BfSchedule([], -1)
            segment_start_time = self.__scheduling_start_time
        else:
            jobs = [
                x for x in Job.from_schedule(mapping, self.__jobs)
                if not x.is_terminated()
            ]
            passed_schedule = mapping
            segment_start_time = mapping.end_time

        results = self.__step_scheduler.schedule(
            jobs, segment_start_time=segment_start_time,
            accumulated_energy=prev_e, prev_schedule=passed_schedule)
        # results = self.__filter_step_results(results)
        results.sort()

        best_mapping = None
        child_min_energy = math.inf

        for m in results:
            if self.__force_return:
                return child_min_energy
            e = m.energy
            if m.best_case_energy > self._energy_limit():
                if m.best_case_energy - prev_e < child_min_energy:
                    child_min_energy = m.best_case_energy - prev_e
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
                best_mapping = m
                if e - prev_e < child_min_energy:
                    child_min_energy = e - prev_e
                continue
            (child_e) = self.__schedule_memoization_step(m)
            if e + child_e - prev_e < child_min_energy:
                child_min_energy = e + child_e - prev_e

        if mapping is not None:
            self.__mem_state_table.add_state(cratio_list, mapping.end_time,
                                             child_min_energy)

        return child_min_energy

    def total_energy(self):
        return self.__best_energy

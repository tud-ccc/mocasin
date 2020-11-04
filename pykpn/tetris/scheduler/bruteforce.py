#!/usr/bin/env python3

import math
import heapq
import time

import copy

from pykpn.tetris.scheduler.base import SchedulerBase
from pykpn.tetris.context import Context
from pykpn.tetris.mapping import Mapping, SegmentMapping, JobSegmentMapping
from pykpn.tetris.job import JobTable
from pykpn.tetris.extra import NamedDimensionalNumber

EPS = 0.00001

FINISH_MAX_DIFF = 0.5

import logging
log = logging.getLogger(__name__)


class _BfMapping(Mapping):
    """Mapping class for Bruteforce scheduler.

    This class is used to store intermediate mapping object with
    additional data.
    """
    def __init__(self, segments=[], best_case_energy=None):
        Mapping.__init__(self, segments=segments)
        assert best_case_energy is not None
        self.__best_case_energy = best_case_energy

    def copy(self):
        """_BfMapping: returns a shallow copy of the mapping"""
        return _BfMapping(self.segments(), self.__best_case_energy)

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
        if len(self) == 0:
            return 0
        return sum([1 for m in self.last if not m.finished])


class BruteforceStepScheduler:
    def __init__(self, parent_scheduler, job_table, prev_mapping=None,
                 rescheduling=True, all_combinations=False):
        assert len(job_table) != 0
        self.__parent = parent_scheduler
        self.__job_table = job_table
        self.__rescheduling = rescheduling
        self.__prev_mapping = prev_mapping
        self.__step_best_energy = math.inf
        self.__force_return = False
        self.__results = []
        self.__all_combinations = all_combinations

        self.__start_time = job_table.time

        if prev_mapping.last is not None:
            self.__start_energy = prev_mapping.energy
        else:
            self.__start_energy = 0.0

        self.__min_segment_time = self.__calc_min_segment_time()

    def __calc_min_segment_time(self):
        res = [
            x.app.best_case_time(start_cratio=x.cratio)
            for x in self.__job_table
        ]
        return min(res)

    def __schedule_calc_values(self, clist):
        energy = 0
        core_types = NamedDimensionalNumber(
            self.__parent._platform.core_types(), init_only_names=True)
        for ts, m in zip(self.__job_table, clist):
            cratio = ts.cratio
            app = ts.app
            config = app.mappings[m]
            if m != "__idle__":
                config_rem_time = config.time(start_cratio=cratio)
                assert config_rem_time > self.__min_segment_time - EPS
                energy += (config.energy() * self.__min_segment_time /
                           config.time())
            core_types += config.core_types
        return (core_types, energy)

    def __create_mapping_from_list(self, clist):
        res = []
        full_mapping_list = []

        # Calculate estimated end time
        for ts, m in zip(self.__job_table, clist):
            single_job_mapping = JobSegmentMapping(
                ts.rid, m, start_time=self.__start_time,
                start_cratio=ts.cratio, finished=True)
            full_mapping_list.append(single_job_mapping)

        # Check if the scheduling meets deadlines
        full_meets_deadline = True
        for sm in full_mapping_list:
            rid = sm.rid
            ts = self.__job_table.find_by_rid(rid)
            d = ts.abs_deadline
            if sm.end_time > d:
                full_meets_deadline = False
            if sm.idle:
                full_meets_deadline = False

        if full_meets_deadline:
            cur_energy = sum([x.energy for x in full_mapping_list])
            total_energy = cur_energy + self.__start_energy
            if self.__step_best_energy > total_energy:
                self.__step_best_energy = total_energy

            full_finish_time = max([x.end_time for x in full_mapping_list])
            new_segment = SegmentMapping(
                self.__parent._platform, full_mapping_list,
                time_range=(self.__start_time, full_finish_time))
            new_mapping = self.__prev_mapping.copy()
            new_mapping.append_segment(new_segment)
            new_mapping.best_case_energy = total_energy
            res.append((full_meets_deadline, total_energy, new_mapping))

        if self.__rescheduling:
            segment_mapping_list = []
            min_finish_time = min([x.end_time for x in full_mapping_list])
            stop_jobs = [
                x for x in full_mapping_list
                if x.end_time < min_finish_time + FINISH_MAX_DIFF
            ]
            segment_end_time = max([x.end_time for x in stop_jobs])
            segment_time = segment_end_time - self.__start_time
            assert segment_time > self.__min_segment_time - EPS
            for fsm in full_mapping_list:
                ssm = JobSegmentMapping(fsm.rid, fsm.can_mapping_id,
                                        start_time=fsm.start_time,
                                        start_cratio=fsm.start_cratio,
                                        end_time=segment_end_time)
                segment_mapping_list.append(ssm)

            # Check if the scheduling meets deadlines
            segment_meets_deadline = True
            finished = True
            for sm in segment_mapping_list:
                rid = sm.rid
                ts = self.__job_table.find_by_rid(rid)
                d = ts.abs_deadline
                if not sm.finished:
                    finished = False
                if sm.end_time > d:
                    segment_meets_deadline = False
                app = ts.app
                min_time_left = app.best_case_time(start_cratio=sm.end_cratio)
                if min_time_left + sm.end_time > d:
                    segment_meets_deadline = False

            if segment_meets_deadline:
                # Evaluate best-case energy consumption
                cur_energy = sum([x.energy for x in segment_mapping_list])
                total_energy = cur_energy + self.__start_energy
                best_case_energy = total_energy
                for sm in segment_mapping_list:
                    rid = sm.rid
                    ts = self.__job_table.find_by_rid(rid)
                    app = ts.app
                    bc_energy = app.best_case_energy(
                        start_cratio=sm.end_cratio)
                    best_case_energy += bc_energy

                new_segment = SegmentMapping(
                    self.__parent._platform, segment_mapping_list,
                    time_range=(self.__start_time, segment_end_time))
                new_mapping = self.__prev_mapping.copy()
                new_mapping.append_segment(new_segment)
                new_mapping.best_case_energy = best_case_energy
                res.append((segment_meets_deadline, total_energy, new_mapping))
        return res

    def __schedule_step(self, clist):
        if self.__force_return:
            return

        (core_types, e) = self.__schedule_calc_values(clist)

        if not (core_types <= NamedDimensionalNumber(
                self.__parent._platform.core_types())):
            return

        # Check current energy
        if not self.__all_combinations:
            if e + self.__start_energy > self.__parent._energy_limit():
                return

            # Check current energy
            if e + self.__start_energy > self.__step_best_energy:
                return

        if len(clist) == len(self.__job_table):
            only_idle = True
            for x in clist:
                if x != "__idle__":
                    only_idle = False
            if only_idle:
                return

            results = self.__create_mapping_from_list(clist)
            for r, energy, m in results:
                if r:
                    self.__results.append(m)

            if not self.__parent._within_time_limit():
                self.__force_return = True
            return

        next_app = self.__job_table[len(clist)].app
        for config in next_app.mappings.keys():
            if not self.__rescheduling and config == "__idle__":
                continue
            self.__schedule_step(clist + [config])

    def schedule(self):
        self.__schedule_step([])
        return self.__results


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
    def __init__(self, app_table, platform, **kwargs):
        super().__init__(app_table, platform)
        self._platform = platform
        self.__rescheduling = kwargs['reschedule']
        self.__drop_high = kwargs["bf_drop"]
        self.__dump_steps = kwargs["bf_dump_steps"]

        self.__time_limit = kwargs["time_limit"]

        self.__scheduled_on_time = True
        self.__memoization = kwargs["memoization"]
        self.__dump_mem_table = kwargs["dump_mem_table"]
        self.__prune_mem_table = kwargs["prune_mem_table"]

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
        log.debug("New scheduling: \n" +
                  self.__best_scheduling.legacy_dump_str() + '\n')
        pass

    def _energy_limit(self):
        return self.__best_energy * (1.0 - self.__drop_high) - EPS

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
        num_tasks = len(self.__jobs)

        res = [0] * (num_tasks+1)
        for i, r in enumerate(res):
            res[i] = sum(1 for s in self.__hq
                         if num_tasks - s.count_non_finished_jobs() == i)
        return res

    def __clear(self):
        self.__best_scheduling = None
        self.__best_energy = math.inf
        self._wc_energy = math.inf
        self.__hq = []
        if self.__time_limit is not None:
            self.__start_time = time.time()

    def schedule(self, jobs_start):
        """Find the optimal scheduling.
        
        Args:
            jobs_start (JobTable): jobs to schedule

        Returns:
            a tuple (successful, list of configurations)
        """
        self.__clear()
        self.__jobs = jobs_start

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
                jobs = self.__jobs.copy()
                m = _BfMapping(segments=[], best_case_energy=-1)
                nf = -1
            else:
                jobs = JobTable.from_mapping(m)
                nf = m.count_non_finished_jobs()

            e = m.energy
            bc = m.best_case_energy
            if e > self._energy_limit():
                continue

            if bc > self._energy_limit():
                continue
            step_counter += 1
            # print("len(hq) = {}, e = {:.3f}, bc_energy = {:.3f},"
            # " self._wc_energy = {:.3f}, non_finished = {},"
            # " #full_schedulin: {}".format(
            # l, e, bc, self._wc_energy, nf, len(finished)))

            step_scheduler = BruteforceStepScheduler(
                self, jobs, m, rescheduling=self.__rescheduling)
            results = step_scheduler.schedule()
            results = self.__filter_step_results(results)
            results.sort()

            for m in results:
                e = m.energy
                if e > self._energy_limit():
                    continue
                if m.best_case_energy > self._energy_limit():
                    continue
                if m.last.finished:
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
            cratio_list = [
                mapping.get_job_end_cratio(x.rid) for x in self.__jobs
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
            passed_mapping = _BfMapping([], -1)
        else:
            jobs = JobTable.from_mapping(mapping)
            passed_mapping = mapping

        step_scheduler = BruteforceStepScheduler(
            self, jobs, prev_mapping=passed_mapping,
            rescheduling=self.__rescheduling, all_combinations=True)
        results = step_scheduler.schedule()
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
            if m.last.finished:
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

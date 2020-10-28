# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import Schedule
from pykpn.tetris.scheduler.base import SchedulerBase
from pykpn.tetris.scheduler.bruteforce import (BruteforceSegmentScheduler,
                                               _is_better_eu)

import logging
import math

EPS = 0.00001

log = logging.getLogger(__name__)


class StateMemoryTable:

    COMP_STEP = 0.01
    TIME_STEP = 0.1

    def __init__(self, num_apps):
        self.__num_apps = num_apps
        self.__table = []

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

    def size(self):
        return len(self.__table)

    def add_state(self, task_comp, time, min_energy):
        assert len(task_comp) == self.__num_apps
        current_e = self.find_min_energy_from_state(task_comp, time)
        if current_e is not None:
            if abs(min_energy - current_e) < EPS:
                return
            if min_energy < current_e + EPS:
                return
        s = {}
        s['task_comp'] = task_comp
        s['time'] = time
        s['min_energy'] = min_energy
        self.__table.append(s)

    def dump_str(self):
        res = "StateMemoryTable:\n"
        for idx, item in enumerate(self.__table):
            res += "{}: time = {}, task states = {}, min energy = {}\n".format(
                idx, item['time'], item['task_comp'], item['min_energy'])
        return res


class BruteforceMemoScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        super().__init__(platform)

        self.__dump_steps = kwargs["bf_dump_steps"]
        self.__dump_mem_table = kwargs["dump_mem_table"]

        # Initialize a step scheduler
        self.__segment_scheduler = BruteforceSegmentScheduler(self)

    @property
    def name(self):
        return "Exact-Memo"

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

    def __clear(self):
        self.__best_scheduling = None
        self.__best_energy = math.inf

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

        self.__mem_step_counter = 0
        self.__mem_state_table = StateMemoryTable(len(self.__jobs))
        self.__schedule_step(None)
        return self.__best_scheduling

    # Returns (min energy to finish)
    def __schedule_step(self, mapping):
        self.__mem_step_counter += 1
        if mapping is None:
            prev_e = 0.0
            bc = -1
        else:
            prev_e = mapping.energy
            bc = mapping.best_case_energy
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
            passed_schedule = Schedule([])
            segment_start_time = self.__scheduling_start_time
        else:
            jobs = [
                x for x in Job.from_schedule(mapping, self.__jobs)
                if not x.is_terminated()
            ]
            passed_schedule = mapping
            segment_start_time = mapping.end_time

        results = self.__segment_scheduler.schedule(
            jobs, segment_start_time=segment_start_time,
            accumulated_energy=prev_e, prev_schedule=passed_schedule)

        best_mapping = None
        child_min_energy = math.inf

        for m in results:
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
            (child_e) = self.__schedule_step(m)
            if e + child_e - prev_e < child_min_energy:
                child_min_energy = e + child_e - prev_e

        if mapping is not None:
            self.__mem_state_table.add_state(cratio_list, mapping.end_time,
                                             child_min_energy)

        return child_min_energy

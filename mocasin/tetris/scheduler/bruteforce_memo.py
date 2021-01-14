# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from mocasin.tetris.schedule import Schedule, ENERGY_EPS, TIME_EPS
from mocasin.tetris.scheduler import SchedulerBase
from mocasin.tetris.scheduler.bruteforce import (
    BruteforceSegmentGenerator,
    get_jobs_bc_energy,
    _is_better_eu,
)

import logging
import math

log = logging.getLogger(__name__)


class StateMemoryTable:
    def __init__(self, num_apps):
        self.__num_apps = num_apps
        self.__table = []

    def find_min_energy_from_state(self, task_comp, time, exclude_list=[]):
        max_energy = 0
        found = False
        for idx, s in enumerate(self.__table):
            if idx in exclude_list:
                continue
            if s["time"] > time + TIME_EPS:
                continue
            rs = True
            for msc, tc in zip(s["task_comp"], task_comp):
                if msc + TIME_EPS < tc:
                    rs = False
                    break
            if not rs:
                continue
            found = True
            if max_energy < s["min_energy"]:
                max_energy = s["min_energy"]
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
            if abs(min_energy - current_e) < ENERGY_EPS:
                return
            if min_energy < current_e + ENERGY_EPS:
                return
        s = {}
        s["task_comp"] = task_comp
        s["time"] = time
        s["min_energy"] = min_energy
        self.__table.append(s)

    def dump_str(self):
        res = "StateMemoryTable:\n"
        for idx, item in enumerate(self.__table):
            res += "{}: time = {}, task states = {}, min energy = {}\n".format(
                idx, item["time"], item["task_comp"], item["min_energy"]
            )
        return res


class BruteforceMemoScheduler(SchedulerBase):
    def __init__(self, platform, **kwargs):
        super().__init__(platform, **kwargs)

        self.__dump_steps = kwargs["bf_dump_steps"]
        self.__dump_mem_table = kwargs["dump_mem_table"]

        # Initialize a step scheduler
        self.__segment_generator = BruteforceSegmentGenerator(self)

        if self.rotations:
            raise RuntimeError(
                "Rotations are not yet supported by bruteforce-memo scheduler"
            )

        if not self.migrations:
            raise RuntimeError(
                "Non-migratable workload is not yet supported by bruteforce-memo scheduler"
            )

        if not self.preemptions:
            raise RuntimeError(
                "Non-preemptable workload is not yet supported by bruteforce-memo scheduler"
            )

    @property
    def name(self):
        return "Exact-Memo"

    def __register_best_schedule(self, m):
        self.__best_schedule = m
        self.__best_energy = m.energy
        log.debug(
            "Found new best schedule: energy = {}".format(self.__best_energy)
        )
        log.debug("New schedule: \n" + self.__best_schedule.to_str() + "\n")
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
        self.__clear()
        self.__jobs = jobs
        self.__scheduling_start_time = scheduling_start_time

        self.__mem_step_counter = 0
        self.__mem_state_table = StateMemoryTable(len(self.__jobs))
        self.__schedule_step(Schedule(self.platform, []), jobs)
        return self.__best_schedule

    # Returns (min energy to finish)
    def __schedule_step(self, cschedule, cjobs):
        if self.__mem_step_counter % self.__dump_steps == 0:
            log.debug(
                "step_counter = {}, found_best_energy = {},"
                " size(mem_table) = {}".format(
                    self.__mem_step_counter,
                    self.__best_energy,
                    self.__mem_state_table.size(),
                )
            )

        self.__mem_step_counter += 1

        cstart_time = self.__scheduling_start_time
        if len(cschedule.segments()) > 0:
            cstart_time = cschedule.end_time

        # If bc_energy exceeds the energy of the current solution, skip it
        jobs_bc_energy = get_jobs_bc_energy(cjobs)
        full_bc_energy = cschedule.energy + jobs_bc_energy
        if full_bc_energy > self._energy_limit():
            return jobs_bc_energy

        # Look up in the mem_state_table
        req_schedules = cschedule.per_requests()
        cratio_list = [
            req_schedules[j.request][-1].end_cratio
            if j.request in req_schedules
            else j.cratio
            for j in self.__jobs
        ]

        mem_e = self.__mem_state_table.find_min_energy_from_state(
            cratio_list, cstart_time
        )
        if self.__dump_mem_table:
            log.debug(self.__mem_state_table.dump_str())
            log.debug(
                "Checking mem table: comp = {}, time = {}, found energy = {}".format(
                    cratio_list, cstart_time, mem_e
                )
            )

        # Check with a cached energy whether we can improve energy efficiency
        if mem_e is not None:
            if mem_e + cschedule.energy >= self._energy_limit():
                if self.__dump_mem_table:
                    log.debug("Returning")
                return mem_e

        # Get child segments
        results = self.__segment_generator.generate_segments(
            cjobs,
            segment_start_time=cstart_time,
            accumulated_energy=cschedule.energy,
            prev_schedule=cschedule,
        )

        min_child_energy = math.inf

        for nsegment, njobs in results:
            # Check if all jobs are finished
            all_jobs_finished = all(
                nsegment.is_request_completed(j.request) for j in self.__jobs
            )
            if all_jobs_finished:
                if _is_better_eu(nsegment, self.__best_schedule):
                    self.__register_best_schedule(nsegment)
                current_child_energy = nsegment.energy - cschedule.energy
                min_child_energy = min(current_child_energy, min_child_energy)
                continue

            # If non-finished jobs exist
            (child_e) = self.__schedule_step(nsegment, njobs)
            current_child_energy = nsegment.energy + child_e - cschedule.energy
            min_child_energy = min(current_child_energy, min_child_energy)

        self.__mem_state_table.add_state(
            cratio_list, cstart_time, min_child_energy
        )

        return min_child_energy

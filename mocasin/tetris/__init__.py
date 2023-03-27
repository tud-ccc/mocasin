# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.tetris.job_state import Job
from mocasin.tetris.manager import ResourceManager
from mocasin.tetris.tracer import TracePlayer
from mocasin.tetris.tetris_reader import read_applications, read_requests

import csv
from dataclasses import dataclass, field, fields
import hydra
import logging
import sys

from hydra.utils import to_absolute_path

log = logging.getLogger(__name__)


class TetrisScheduling:
    """Class for handling tetris scheduling.

    This class serves for handling the scheduling for a given job table,
    platform. While this class is called from hydra tasks, we dedicate a static
    method to handle hydra configuration object.
    """

    def __init__(self, scheduler, reqs):
        self.scheduler = scheduler
        self.requests = reqs

        # Job table
        # TODO: no need in a method which generates the whole list, switch to
        # a single object constructor
        self.jobs = list(
            map(lambda x: x.dispatch(), Job.from_requests(self.requests))
        )
        log.info("Jobs: {}".format(",".join(x.to_str() for x in self.jobs)))

        # Scheduling results
        self.found_schedule = None
        self.schedule = None

    def check_solution(self):
        if self.schedule is None:
            return

        # Verify that a schedule object in a valid state
        self.schedule.verify(only_counters=not self.scheduler.rotations)

        failed = False

        # Check whether all jobs finish
        fjobs = Job.from_schedule(self.schedule, self.jobs)
        for sj, fj in zip(self.jobs, fjobs):
            if fj.completed:
                continue
            log.error(
                "Job {} is not completed at the end of the schedule: ".format(
                    sj.to_str(), fj.to_str()
                )
            )
            failed = True

        # Check all jobs meet deadlines
        for j, js in self.schedule.per_requests().items():
            if j.deadline >= js[-1].end_time:
                continue
            log.error(
                "Job {} does not meet deadline, finished={:.3f}".format(
                    j.to_str(), js[-1].end_time
                )
            )
            failed = True

        if failed:
            log.error("The error occured in the generated schedule:\n")
            for s in self.schedule:
                log.error("{}".format(s.to_str()))
            sys.exit(1)

    def precalculate_orbits(self):
        """Precalculate all orbits before running the scheduler.

        The calculation of the mapping orbit is implemented in strict way, which
        is time-consuming. For some tests, it takes up to 99% of the overall
        scheduling time. Until the lazy computation of the orbit is implemented,
        we estimate the scalability of the algorithm by pre-calculation of the
        orbits and excluding the precalculation time from the overall scheduling
        time.
        """
        orbit_manager = self.scheduler.orbit_lookup_manager
        for job in self.jobs:
            mappings = job.request.mappings
            for mapping in mappings:
                entry = orbit_manager.get_orbit_entry(job.app, mapping)
                gen = entry.get_generator()
                list(gen)

    def run(self):
        self.schedule = self.scheduler.schedule(
            self.jobs, scheduling_start_time=0.0
        )
        self.check_solution()
        self.found_schedule = self.schedule is not None

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`TetrisScheduling` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        # Set the platform
        platform = hydra.utils.instantiate(cfg["platform"])

        # Read applications and mappings
        base_apps_dir = to_absolute_path(cfg["tetris_apps_dir"])
        apps = read_applications(base_apps_dir, platform)

        # Read jobs file
        reqs = read_requests(to_absolute_path(cfg["job_table"]), apps)

        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg["resource_manager"], platform)

        scheduling = TetrisScheduling(scheduler, reqs)
        return scheduling


@dataclass
class TetrisManagementSummary:
    input_trace: str
    scheduler: str
    total_requests: int
    accepted_requests: int
    rejected_requests: int = field(init=False)
    total_activations: int = field(default=None, init=False)
    active_requests_mean: float = field(default=None, init=False)
    active_requests_std: float = field(default=None, init=False)
    dynamic_energy: float = field(default=None, init=False)
    scheduling_time_mean: float = field(default=None, init=False)
    scheduling_time_std: float = field(default=None, init=False)

    def __post_init__(self):
        self.rejected_requests = self.total_requests - self.accepted_requests

    def print(self):
        accepted_ratio = 0
        rejected_ratio = 0
        if self.total_requests:
            accepted_ratio = self.accepted_requests / self.total_requests
            rejected_ratio = self.rejected_requests / self.total_requests
        print(f"Input trace: {self.input_trace}")
        print(f"Scheduler: {self.scheduler}")
        print(f"Total requests: {self.total_requests}")
        print(
            f"Accepted requests: {self.accepted_requests} "
            f"({accepted_ratio * 100:.2f} %)"
        )
        print(
            f"Rejected requests: {self.rejected_requests} "
            f"({rejected_ratio * 100:.2f} %)"
        )
        print(f"Total runtime manager activations: {self.total_activations}")
        print(
            f"Average active requests: {self.active_requests_mean} "
            f"(std={self.active_requests_std:.2f})"
        )
        print(f"Dynamic energy: {self.dynamic_energy:.3f} J")
        print(
            f"Average scheduling time: {self.scheduling_time_mean * 1000:.6f} ms "
            f"(std={self.scheduling_time_std * 1000:.6f} ms)"
        )

    def to_csv(self, file_name):
        field_names = [f.name for f in fields(self)]
        field_values = [getattr(self, f.name) for f in fields(self)]

        with open(file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            writer.writerow(field_values)


class TetrisManagement:
    """Class for handling tetris management.

    This class serves for handling the runtime resource management for a given
    input job request trace and platform. While this class is called from hydra
    tasks, we dedicate a static method to handle hydra configuration object.
    """

    def __init__(self, manager, tracer, reqs, input_trace=None):
        self.manager = manager
        self.tracer = tracer
        self.requests = reqs
        self.input_trace = input_trace
        self.stats = None
        self.summary = None

    def run(self):
        self.tracer.run()
        self.stats = self.tracer.stats
        self.build_summary()

    def build_summary(self):
        """Build simulation summary."""
        assert self.stats
        total_reqs = self.stats.total_applications()
        accepted = self.stats.total_accepted()
        summary = TetrisManagementSummary(
            self.input_trace, self.manager.scheduler.name, total_reqs, accepted
        )
        summary.total_activations = self.stats.total_activations()
        ar_mean, ar_std = self.stats.active_requests_stats()
        summary.active_requests_mean = ar_mean
        summary.active_requests_std = ar_std
        summary.dynamic_energy = self.manager.dynamic_energy
        st_mean, st_std = self.stats.scheduling_time_stats()
        summary.scheduling_time_mean = st_mean
        summary.scheduling_time_std = st_std
        self.summary = summary

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`TetrisScheduling` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        # Set the platform
        platform = hydra.utils.instantiate(cfg["platform"])

        # Read applications and mappings
        base_apps_dir = to_absolute_path(cfg["tetris_apps_dir"])
        apps = read_applications(base_apps_dir, platform)

        # Read jobs file
        trace_filename = cfg["input_jobs"]
        reqs = read_requests(to_absolute_path(trace_filename), apps)

        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg["resource_manager"], platform)

        # TODO: add a flag to the config: "schedule_iteratively"
        manager = ResourceManager(platform, scheduler)

        tracer = TracePlayer(manager, reqs)

        management = TetrisManagement(
            manager, tracer, reqs, input_trace=trace_filename
        )
        return management

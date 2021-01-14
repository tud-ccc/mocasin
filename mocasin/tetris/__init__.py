# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from mocasin.tetris.job_state import Job
from mocasin.tetris.manager import ResourceManager
from mocasin.tetris.tracer import TracePlayer
from mocasin.tetris.tetris_reader import read_applications, read_requests

import hydra
import logging
import sys

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
            map(lambda x: x.dispatch(), Job.from_requests(self.requests)))
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
                    sj.to_str(), fj.to_str()))
            failed = True

        # Check all jobs meet deadlines
        for j, js in self.schedule.per_requests().items():
            if j.deadline >= js[-1].end_time:
                continue
            log.error("Job {} does not meet deadline, finished={:.3f}".format(
                j.to_str(), js[-1].end_time))
            failed = True

        if failed:
            log.error("The error occured in the generated schedule:\n")
            for s in self.schedule:
                log.error("{}".format(s.to_str()))
            sys.exit(1)

    def run(self):
        self.schedule = self.scheduler.schedule(self.jobs,
                                                scheduling_start_time=0.0)
        self.check_solution()
        self.found_schedule = (self.schedule is not None)

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`TetrisScheduling` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        # Set the platform
        platform = hydra.utils.instantiate(cfg['platform'])

        # Read applications and mappings
        base_apps_dir = cfg['tetris_apps_dir']
        apps = read_applications(base_apps_dir, platform)

        # Read jobs file
        reqs = read_requests(cfg['job_table'], apps)

        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg['resource_manager'], platform)

        scheduling = TetrisScheduling(scheduler, reqs)
        return scheduling


class TetrisManagement:
    """Class for handling tetris management.

    This class serves for handling the runtime resource management for a given
    input job request trace and platform. While this class is called from hydra
    tasks, we dedicate a static method to handle hydra configuration object.
    """
    def __init__(self, manager, tracer, reqs):
        self.manager = manager
        self.tracer = tracer
        self.requests = reqs

    def run(self):
        self.tracer.run()

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`TetrisScheduling` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        # Set the platform
        platform = hydra.utils.instantiate(cfg['platform'])

        # Read applications and mappings
        base_apps_dir = cfg['tetris_apps_dir']
        apps = read_applications(base_apps_dir, platform)

        # Read jobs file
        reqs = read_requests(cfg['input_jobs'], apps)

        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg['resource_manager'], platform)

        manager = ResourceManager(platform, scheduler, cfg['allow_migration'])

        tracer = TracePlayer(manager, reqs)

        management = TetrisManagement(manager, tracer, reqs)
        return management

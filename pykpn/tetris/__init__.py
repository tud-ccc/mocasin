# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

import hydra

from pykpn.tetris.apptable import AppTable
from pykpn.tetris.context import Context
from pykpn.tetris.job import JobTable
from pykpn.tetris.manager import ResourceManager
from pykpn.tetris.reqtable import ReqTable
from pykpn.tetris.tracer import TracePlayer


class TetrisScheduling:
    """Class for handling tetris scheduling.

    This class serves for handling the scheduling for a given job table,
    platform. While this class is called from hydra tasks, we dedicate a static
    method to handle hydra configuration object.
    """
    def __init__(self, scheduler, req_table):
        self.scheduler = scheduler
        self.req_table = req_table
        Context().req_table = self.req_table

        # Job table
        self.job_table = JobTable()
        self.job_table.init_by_req_table(self.req_table)

        # Scheduling results
        self.found_schedule = None
        self.schedule = None
        self.within_time_limit = None

    def run(self):
        (self.found_schedule, self.schedule,
         self.within_time_limit) = self.scheduler.schedule(self.job_table)
        pass

    @staticmethod
    def from_hydra(cfg):
        """Factory method.

        Instantiates :class:`TetrisScheduling` from a hydra configuration object.

        Args:
            cfg: a hydra configuration object
        """
        # Set the platform
        platform = hydra.utils.instantiate(cfg['platform'])

        # Initialize application table
        base_apps_dir = cfg['tetris_apps_dir']
        app_table = AppTable(platform, base_apps_dir)

        # Initialize a job table, and fill it by job infos from the file
        req_table = ReqTable(app_table)
        req_table.read_from_file(cfg['job_table'])

        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg['resource_manager'], app_table,
                                            platform)

        scheduling = TetrisScheduling(scheduler, req_table)
        return scheduling


class TetrisManagement:
    """Class for handling tetris management.

    This class serves for handling the runtime resource management for a given
    input job request trace and platform. While this class is called from hydra
    tasks, we dedicate a static method to handle hydra configuration object.
    """
    def __init__(self, manager, tracer, req_table):
        self.manager = manager
        self.tracer = tracer
        self.req_table = req_table
        Context().req_table = self.req_table

        # Scheduling results

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

        # Initialize application table
        base_apps_dir = cfg['tetris_apps_dir']
        app_table = AppTable(platform, base_apps_dir)

        # Initialize a job table, and fill it by job infos from the file
        req_table = ReqTable(app_table)

        scenario = cfg['input_jobs']

        # Initialize tetris scheduler
        scheduler = hydra.utils.instantiate(cfg['resource_manager'], app_table,
                                            platform)

        manager = ResourceManager(app_table, platform, scheduler,
                                  cfg['allow_migration'])

        tracer = TracePlayer(manager, scenario)

        management = TetrisManagement(manager, tracer, req_table)
        return management

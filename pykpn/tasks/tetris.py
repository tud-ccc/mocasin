# The main file of the project which is called from command line.
#
# Author: Robert Khasanov

import sys, os
import argparse
import re
import time
import logging
import hydra

from pykpn.tetris.context import Context
from pykpn.tetris.reqtable import ReqTable
from pykpn.tetris.apptable import AppTable
from pykpn.tetris.job import JobTable

from pykpn.common.platform import Platform

from pykpn.tetris.scheduler.bruteforce import BruteforceScheduler
from pykpn.tetris.scheduler.fast import FastScheduler
from pykpn.tetris.scheduler.dac import DacScheduler
from pykpn.tetris.scheduler.wwt15 import (
    WWT15Scheduler,
    WWT15SortingKey,
    WWT15ExploreMode,
)
from pykpn.tetris.scheduler.lr_solver import LRConstraint

from pykpn.tetris.manager import ResourceManager
from pykpn.tetris.tracer import TracePlayer

log = logging.getLogger(__name__)


def init_logging():
    logging.getLogger("pykpn.slx.platform.convert_2017_04").setLevel(
        logging.ERROR)
    logging.getLogger("pykpn.slx.platform").setLevel(logging.WARNING)
    logging.getLogger("pykpn.slx.kpn").setLevel(logging.WARNING)


def print_summary(scenario, res, scheduling, schedule_time, within_time,
                  opt_summary, scheduler, opt_reschedule):
    # TODO: Take the name of scheduler from scheduler
    summary_file = opt_summary
    if summary_file is None:
        return
    outf = open(summary_file, "w")
    print(
        "input_state,scheduler,reschedule,search_time,scheduled"
        ",energy,longest_time,time_segments,within_TL",
        file=outf,
    )

    scheduler_str = scheduler.name

    if res:
        energy = scheduling.energy
        longest_time = scheduling.end_time
        num_segments = len(scheduling)
    else:
        energy = None
        longest_time = None
        num_segments = None

    print(
        "{},{},{},{},{},{},{},{},{}".format(
            scenario,
            scheduler_str,
            opt_reschedule,
            schedule_time,
            res,
            energy,
            longest_time,
            num_segments,
            within_time,
        ),
        file=outf,
    )


def single_mode_scheduler(scheduler, scenario):
    """Schedule all applications at once.

    The scheduler takes all requests and attempts to schedule them.

    Args:
        scheduler (SchedulerBase): Scheduler instance
    """
    Context().req_table.read_from_file(scenario)
    log.info("Read requests from the file")
    log.info(Context().req_table.dump_str().rstrip())

    # Job table
    job_table = JobTable()
    job_table.init_by_req_table()

    log.info("Starting scheduling")
    start_time = time.time()
    res, scheduling, within_time = scheduler.schedule(job_table)
    stop_time = time.time()
    log.info("Finished scheduling")
    schedule_time = stop_time - start_time
    return res, scheduling, schedule_time


@hydra.main(config_path='../conf', config_name='tetris_scheduler')
def tetris_scheduler(cfg):
    """Tetris scheduler

    This task runs tetris scheduler for a single request table.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        TODO: Write down 
    """
    if os.path.isabs(cfg["job_table"]):
        scenario = cfg["job_table"]
    else:
        scenario = os.path.abspath(
            os.path.join(os.getcwd(), "..", "..", "..", cfg["job_table"]))

    out_fn = cfg["output_schedule"]
    if out_fn != None:
        outf = open(out_fn, mode="w")
    else:
        outf = sys.stdout

    # Suppress logs from pykpn module
    init_logging()

    tetris_base = cfg['tetris_base']

    # Set the platform
    platform = hydra.utils.instantiate(cfg['platform'])

    # Initialize application table
    app_table = AppTable(platform, os.path.join(tetris_base, "apps"))

    # Initialize request table, and fill it by requests from the file
    req_table = ReqTable(app_table)

    # Save reference to table in Context
    Context().req_table = req_table

    # Initialize scheduler
    scheduler = hydra.utils.instantiate(cfg['resource_manager'], app_table, platform)

    opt_summary = cfg["summary_csv"]
    opt_time_limit = cfg.get("time_limit", 'None')
    opt_reschedule = cfg.get("reschedule", True)
    res, scheduling, schedule_time = single_mode_scheduler(scheduler, scenario)
    if res:
        scheduling.legacy_dump(outf=outf)
        # scheduling.legacy_dump_jobs_info(outf=outf)
    if opt_time_limit != 'None':
        within_time = schedule_time <= opt_time_limit
    else:
        within_time = True
    print_summary(
        scenario,
        res,
        scheduling,
        schedule_time,
        within_time,
        opt_summary,
        scheduler,
        opt_reschedule,
    )


@hydra.main(config_path='../conf', config_name='tetris_manager')
def tetris_manager(cfg):
    """Tetris manager

    This task runs tetris manager for the input trace of jobs

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        TODO: Write down 
    """
    if os.path.isabs(cfg["input_jobs"]):
        scenario = cfg["input_jobs"]
    else:
        scenario = os.path.abspath(
            os.path.join(os.getcwd(), "..", "..", "..", cfg["input_jobs"]))

    out_fn = cfg["output_trace"]
    if out_fn != None:
        outf = open(out_fn, mode="w")
    else:
        outf = sys.stdout

    # Suppress logs from pykpn module
    init_logging()

    tetris_base = cfg['tetris_base']

    # Set the platform
    platform = hydra.utils.instantiate(cfg['platform'])

    # Initialize application table
    app_table = AppTable(platform, os.path.join(tetris_base, "apps"))

    # Initialize request table, and fill it by requests from the file
    req_table = ReqTable(app_table)

    # Save reference to table in Context
    Context().req_table = req_table

    # Initialize scheduler
    scheduler = hydra.utils.instantiate(cfg['resource_manager'], app_table,
                                        platform, cfg)

    opt_summary = cfg["summary_csv"]
    opt_time_limit = cfg.get("time_limit", 'None')
    opt_reschedule = cfg.get("reschedule", True)
    dump_summary = False
    dump_path = ""
    if opt_summary is not None:
        dump_summary = True
        dump_path = opt_summary

    manager = ResourceManager(scheduler, platform)
    tracer = TracePlayer(manager, scenario, dump_summary, dump_path)
    tracer.run()

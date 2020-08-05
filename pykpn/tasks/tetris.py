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
                  opt_summary, opt_summary_append, scheduler, opt_reschedule,
                  opt_allow_idle):
    # TODO: Take the name of scheduler from scheduler
    summary_file = opt_summary
    if summary_file is None:
        outf = sys.stdout
        new_file = True
    else:
        if os.path.isfile(summary_file):
            new_file = False
        else:
            new_file = True
        if opt_summary_append:
            outf = open(summary_file, "a+")
        else:
            outf = open(summary_file, "w")
            new_file = True
    if new_file:
        print(
            "input_state,scheduler,reschedule,allow_idle,search_time,scheduled"
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
        "{},{},{},{},{},{},{},{},{},{}".format(
            scenario,
            scheduler_str,
            opt_reschedule,
            opt_allow_idle,
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


@hydra.main(config_path="conf/tetris.yaml")
def tetris(cfg):
    """TETRiS

    This task runs tetris scheduler using the table of operating points.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        TODO: Write down 
    """
    print(cfg.pretty())

    if os.path.isabs(cfg["scenario"]):
        scenario = cfg["scenario"]
    else:
        scenario = os.path.abspath(
            os.path.join(os.getcwd(), "..", "..", "..", cfg["scenario"]))

    mapping_dir = cfg["mapping_dir"]
    idle = cfg["allow_idle_job_segments"]
    out_fn = cfg["output"]
    if out_fn != None:
        outf = open(out_fn, mode="w")
    else:
        outf = sys.stdout
    scheduler_name = cfg["scheduler"]
    mode = cfg["mode"]

    # Suppress logs from pykpn module
    init_logging()

    tetris_base = cfg['tetris_base']

    # Set the platform
    platform = hydra.utils.instantiate(cfg['platform'])

    # Initialize application table
    app_table = AppTable(platform, os.path.join(tetris_base, "apps"),
                         allow_idle=idle)

    # Initialize request table, and fill it by requests from the file
    req_table = ReqTable(app_table)

    # Save reference to table in Context
    Context().req_table = req_table

    # Initialize scheduler
    opt_bf_drop = cfg["bf_drop"]
    opt_reschedule = cfg["reschedule"]
    opt_bf_dump_steps = cfg["bf_dump_steps"]
    opt_time_limit = cfg["time_limit"]
    opt_dump_mem_table = cfg["dump_mem_table"]
    opt_prune_mem_table = cfg["prune_mem_table"]
    if scheduler_name == "BF" or scheduler_name == "BF-MEM":
        drop_high = opt_bf_drop
        if scheduler_name == "BF-MEM":
            memorization = True
        else:
            memorization = False
        scheduler = BruteforceScheduler(
            app_table,
            platform,
            rescheduling=opt_reschedule,
            drop_high=drop_high,
            dump_steps=opt_bf_dump_steps,
            time_limit=opt_time_limit,
            memorization=memorization,
            dump_mem_table=opt_dump_mem_table,
            prune_mem_table=opt_prune_mem_table,
        )
    elif scheduler_name == "FAST":
        scheduler = FastScheduler(app_table, platform)
    elif scheduler_name.startswith("DAC"):
        if scheduler_name == "DAC":
            scheduler = DacScheduler(app_table, platform)
        else:
            v = scheduler_name[4:]
            scheduler = DacScheduler(app_table, platform, version=v)
    elif scheduler_name.startswith("WWT15"):
        # Parse WWT15 related arguments
        scheduler_type = cfg["wwt15_type"]

        sorting_arg = cfg["wwt15_sorting"]
        if sorting_arg == "COST":
            sorting_key = WWT15SortingKey.MINCOST
        elif sorting_arg == "DEADLINE":
            sorting_key = WWT15SortingKey.DEADLINE
        elif sorting_arg == "CDP":
            sorting_key = WWT15SortingKey.CDP
        else:
            assert False, "Unknown sorting key"

        explore_arg = cfg["wwt15_seg_explore"]
        if explore_arg == "ALL":
            explore_mode = WWT15ExploreMode.ALL
        elif explore_arg == "BEST":
            explore_mode = WWT15ExploreMode.BEST
        else:
            assert False, "Unknown explore mode"

        lr_constraints_arg = cfg["wwt15_lr"]
        if len(lr_constraints_arg) == 0:
            lr_constraints_arg.append("R")
        lr_constraints = LRConstraint.NULL
        if "R" in lr_constraints_arg:
            lr_constraints |= LRConstraint.RESOURCE
        if "D" in lr_constraints_arg:
            lr_constraints |= LRConstraint.DELAY
        if "RDP" in lr_constraints_arg:
            lr_constraints |= LRConstraint.RDP

        lr_rounds = cfg["wwt15_lr_rounds"]

        # Instantiate scheduler
        if scheduler_type == "SEG":
            # Using segmentized scheduler
            scheduler = WWT15Scheduler(
                app_table,
                platform,
                sorting=sorting_key,
                explore_mode=explore_mode,
                lr_constraints=lr_constraints,
                lr_rounds=lr_rounds,
            )
        else:
            assert False, "NYI"
    else:
        assert False, "Unknown scheduler"

    opt_summary = cfg["summary"]
    opt_summary_append = cfg["summary_append"]
    if mode == "single":
        res, scheduling, schedule_time = single_mode_scheduler(
            scheduler, scenario)
        if res:
            scheduling.legacy_dump(outf=outf)
            # scheduling.legacy_dump_jobs_info(outf=outf)
        if opt_time_limit is not None:
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
            opt_summary_append,
            scheduler,
            opt_reschedule,
            idle,
        )
    elif mode == "trace":
        dump_summary = False
        dump_path = ""
        if opt_summary is not None:
            dump_summary = True
            dump_path = opt_summary

        manager = ResourceManager(scheduler, platform)
        tracer = TracePlayer(manager, scenario, dump_summary, dump_path)
        tracer.run()
    else:
        assert False, "Unknown scheduler"

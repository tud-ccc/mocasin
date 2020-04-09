# The main file of the project which is called from command line.
#
# Author: Robert Khasanov

import sys, os
import argparse
import re
import time
import logging
import hydra

from pykpn.tetris.tetris.context import Context
from pykpn.tetris.tetris.reqtable import ReqTable
from pykpn.tetris.tetris.apptable import AppTable
from pykpn.tetris.tetris.job import JobTable

from pykpn.slx.platform import SlxPlatform
from pykpn.tetris.tetris.tplatform import Platform

from pykpn.tetris.tetris.scheduler.bruteforce import BruteforceScheduler
from pykpn.tetris.tetris.scheduler.fast import FastScheduler
from pykpn.tetris.tetris.scheduler.dac import DacScheduler
from pykpn.tetris.tetris.scheduler.wwt15 import (
    WWT15Scheduler,
    WWT15SortingKey,
    WWT15ExploreMode,
)
from pykpn.tetris.tetris.scheduler.lr_solver import LRConstraint

from pykpn.tetris.tetris.manager import ResourceManager
from pykpn.tetris.tetris.tracer import TracePlayer


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
    logging.info("Read requests from the file")
    logging.info(Context().req_table.dump_str().rstrip())

    # Job table
    job_table = JobTable()
    job_table.init_by_req_table()

    logging.info("Starting scheduling")
    start_time = time.time()
    res, scheduling, within_time = scheduler.schedule(job_table)
    stop_time = time.time()
    logging.info("Finished scheduling")
    schedule_time = stop_time - start_time
    return res, scheduling, schedule_time


@hydra.main(config_path="conf/tetris.yaml")
def tetris(cfg):
    """TETRiS

    This task runs tetris scheduler using the table of operating points.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
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
    # TODO: How to use platform from pykpn?
    platform_name = cfg["platform"]
    mode = cfg["mode"]

    loglevel_opt = cfg["loglevel"]
    logout = cfg["logout"]

    # TODO: Use pykpn infra for logging
    if loglevel_opt is not None:
        loglevel = getattr(logging, loglevel_opt)

        if logout is None:
            logging.basicConfig(
                level=loglevel,
                format="[%(asctime)s %(levelname)s] %(message)s")
        else:
            logging.basicConfig(
                level=loglevel,
                format="[%(asctime)s %(levelname)s] %(message)s",
                filename=logout,
            )

    # Suppress logs from pykpn module
    logging.getLogger("pykpn.slx.platform.convert_2017_04").setLevel(
        logging.ERROR)
    logging.getLogger("pykpn.slx.platform").setLevel(logging.ERROR)
    logging.getLogger("pykpn.slx.kpn").setLevel(logging.ERROR)

    logging.getLogger("pykpn.tetris.tetris.apptable").setLevel(logging.ERROR)
    logging.getLogger("pykpn.common.mapping").setLevel(logging.ERROR)

    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "../tetris/tetris")

    # Set the platform
    # TODO: Remove this "1"
    if platform_name == "exynos" or True:
        platform = Platform(
            "exynos",
            SlxPlatform(
                "SlxPlatform",
                os.path.join(BASE_DIR, "platforms/exynos.platform"),
                "2017.04",
            ),
        )
    else:
        assert False

    # Initialize request table, and fill it by requests from the file
    req_table = ReqTable()

    # Initialize application table
    app_table = AppTable(platform, allow_idle=idle)
    app_table.read_applications(os.path.join(BASE_DIR, "apps"))

    # Save reference to table in Context
    Context().req_table = req_table
    Context().app_table = app_table

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
        scheduler = FastScheduler(platform)
    elif scheduler_name.startswith("DAC"):
        if scheduler_name == "DAC":
            scheduler = DacScheduler(platform)
        else:
            v = scheduler_name[4:]
            scheduler = DacScheduler(platform, version=v)
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

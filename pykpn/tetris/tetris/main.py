#The main file of the project which is called from command line.
#
#Author: Robert Khasanov

import sys, os
import argparse
import re
import time
import logging

from pykpn.tetris.tetris.context import Context
from pykpn.tetris.tetris.reqtable import ReqTable
from pykpn.tetris.tetris.apptable import AppTable
from pykpn.tetris.tetris.job import JobTable

from pykpn.slx.platform import SlxPlatform
from pykpn.tetris.tetris.tplatform import Platform

from pykpn.tetris.tetris.scheduler.bruteforce import BruteforceScheduler
from pykpn.tetris.tetris.scheduler.fast import FastScheduler
from pykpn.tetris.tetris.scheduler.dac import DacScheduler
from pykpn.tetris.tetris.scheduler.wwt15 import WWT15Scheduler, WWT15SortingKey, WWT15ExploreMode
from pykpn.tetris.tetris.scheduler.lr_solver import LRConstraint

from pykpn.tetris.tetris.manager import ResourceManager
from pykpn.tetris.tetris.tracer import TracePlayer

def parse_resource(s):
    pattern = re.compile(r"""(?P<big>\d+)b(?P<little>\d+)l""", re.VERBOSE)
    match = pattern.match(s)

    return int(match.group('big')), int(match.group('little'))

def print_summary(parsed_args, res, scheduling, schedule_time, within_time):
    # TODO: Take the name of scheduler from scheduler
    summary_file = parsed_args.summary
    if summary_file == '':
        outf = sys.stdout
        new_file = True
    else:
        if os.path.isfile(summary_file):
            new_file = False
        else:
            new_file = True
        if parsed_args.summary_append:
            outf = open(summary_file, "a+")
        else:
            outf = open(summary_file, "w")
            new_file = True
    if new_file:
        print("input_state,scheduler,reschedule,allow_idle,search_time,scheduled,energy,longest_time,time_segments,within_TL", file=outf)
   
    scheduler = parsed_args.scheduler
    if parsed_args.scheduler == "BF":
        scheduler += "-hd{:02.0f}".format(parsed_args.bf_drop*100)

    if parsed_args.time_limit is not None:
        scheduler += "-tl{:.0f}".format(parsed_args.time_limit)

    if res:
        energy = scheduling.energy
        longest_time = scheduling.end_time
        num_segments = len(scheduling)
    else:
        energy = None
        longest_time = None
        num_segments = None

    print("{},{},{},{},{},{},{},{},{},{}".format(
        parsed_args.scenario,scheduler,parsed_args.reschedule,parsed_args.idle,
        schedule_time,res,energy, longest_time,num_segments, within_time), file=outf)

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

def main():
    ## Argument parser
    ## TODO: Reorder and hide some options.
    args = argparse.ArgumentParser()

    args.add_argument('--scenario', dest='scenario', action='store', required=True,
                      help='Scenario to schedule')
    args.add_argument('--mapping-dir', dest='mapping_dir', action='store', default='mappings',
                      help='Folder contanings pareto configurations of all applications')
    args.add_argument('--resources', dest='resources', action='store', default='4b4l',
                      metavar='XbYl', help='Number of big and little cores')
    args.add_argument('--output', dest='output', action='store', default="",
                      help='Output file for scheduling')
    args.add_argument("--platform", "-p", dest="platform", choices=['exynos'], default="exynos",
                      help="Set the platform")
    args.add_argument("--mode", dest="mode", choices=['single', 'trace'], default='trace',
                      help="""Set the mode. In single mode a scheduler is run only once to schedule all requests in scenario (all requests start arrive at time=0.0).
                      In trace mode, the tool evaluates each request at the time of their arrival.""")
    args.add_argument("--scheduler", "-s", dest="scheduler", choices=['BF', 'BF-MEM', 'FAST', 'DAC', 'DAC-2', 'FAST-2', 'WWT15'], default="BF",
                      help="Set the scheduler")
    args.add_argument('--reschedule', dest='reschedule', action='store_true')
    args.add_argument('--no-reschedule', dest='reschedule', action='store_false')
    args.set_defaults(reschedule=True)
    args.add_argument('--idle', '-i', dest='idle', action='store_true')
    args.add_argument('--no-idle', dest='idle', action='store_false')
    args.set_defaults(idle=True)
    args.add_argument('--summary', dest='summary', action='store', default='',
                      help='Output file for summary')
    args.add_argument('--summary-append', dest='summary_append', action='store_true',
                      help='Append to existing summary file (do not print a header)')
    args.set_defaults(summary_append=False)
    args.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      help="Set the logging level")
    args.add_argument("--logout", dest="logout", action='store', default='', help="Output log to the file")
    args.add_argument("--bf-drop", dest="bf_drop", type=float, default=0.0,
                      help="Drop schedulings close to current best by bf_drop")
    args.add_argument("--bf-dump-steps", dest="bf_dump_steps", type=int, default=1000,
                      help="Dump the status of the queue every N steps")
    args.add_argument("--time-limit", dest="time_limit", type=float,
                      help="Set a time limit")
    args.add_argument("--dump-mem-table", dest="dump_mem_table", action='store_true',
                      help="Dump the mem table")
    args.add_argument("--prune-mem-table", dest="prune_mem_table", action='store_true',
                      help="Enable pruning the mem table")
    args.add_argument("--wwt15-type", dest="wwt15_type", choices=['SEG', 'JF', 'JD'], default="SEG",
                      help="A high-level mapper algorithm: segmentized (SEG), joint-fixed (JF), joint-dynamic (JD)")
    args.add_argument("--wwt15-sorting", dest="wwt15_sorting", choices=['COST', 'DEADLINE', 'CDP'], default="COST",
                      help="Determines an order, in which applications are mapped")
    args.add_argument("--wwt15-seg-explore", dest="wwt15_seg_explore", choices=['BEST', 'ALL'], default="ALL",
                      help="In segmentizes version, which points might form the segment: all points (ALL), or only best (if possible, not to violate deadlines) (BEST)")
    args.add_argument("--wwt15-lr-r", dest="wwt15_lr", action='append_const', const='R', default=[],
                      help="Use constraint on resources in Lagrangian relaxation solver")
    args.add_argument("--wwt15-lr-d", dest="wwt15_lr", action='append_const', const='D',
                      help="Use constraint on delay in Lagrangian relaxation solver")
    args.add_argument("--wwt15-lr-rdp", dest="wwt15_lr", action='append_const', const='RDP',
                      help="Use constraint on resource-delay-product (RDP) in Lagrangian relaxation solver")
    args.add_argument("--wwt15-lr-rounds", dest="wwt15_lr_rounds", type=int, default=1000,
                      help="Number of iterations (rounds) in Lagrangian relaxation")

    parsed_args = args.parse_args()

    scenario = parsed_args.scenario
    mapping_dir = parsed_args.mapping_dir
    idle = parsed_args.idle
    (big, little) = parse_resource(parsed_args.resources) # TODO: Remove big, littles
    out_fn = parsed_args.output
    if out_fn != "":
        outf = open(out_fn, mode='w')
    else:
        outf = sys.stdout
    scheduler_name = parsed_args.scheduler
    platform_name = parsed_args.platform
    mode = parsed_args.mode

    if parsed_args.logLevel:
        loglevel = getattr(logging, parsed_args.logLevel)

        if parsed_args.logout == "":
            logging.basicConfig(level=getattr(logging, parsed_args.logLevel),
                                format='[%(asctime)s %(levelname)s] %(message)s')
        else:
            logging.basicConfig(level=getattr(logging, parsed_args.logLevel),
                                format='[%(asctime)s %(levelname)s] %(message)s',
                                filename=parsed_args.logout)

    # Suppress logs from pykpn module
    logging.getLogger('pykpn.slx.platform.convert_2017_04').setLevel(logging.ERROR)
    logging.getLogger('pykpn.slx.platform').setLevel(logging.ERROR)
    logging.getLogger('pykpn.slx.kpn').setLevel(logging.ERROR)

    logging.getLogger('pykpn.tetris.tetris.apptable').setLevel(logging.ERROR)
    logging.getLogger('pykpn.common.mapping').setLevel(logging.ERROR)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Set the platform
    if platform_name == 'exynos':
        platform = Platform(platform_name, SlxPlatform("SlxPlatform", os.path.join(BASE_DIR, "platforms/exynos.platform"), "2017.04"))
    else:
        assert False

    # Initialize request table, and fill it by requests from the file
    req_table = ReqTable()

    # Initialize application table
    app_table = AppTable(platform, allow_idle = idle)
    app_table.read_applications(os.path.join(BASE_DIR, 'apps'))

    # Save reference to table in Context
    Context().req_table = req_table
    Context().app_table = app_table

    # Initialize scheduler
    if scheduler_name == "BF" or scheduler_name == "BF-MEM":
        drop_high = parsed_args.bf_drop
        if scheduler_name == "BF-MEM":
            memorization = True
        else:
            memorization = False
        scheduler = BruteforceScheduler(platform,
                rescheduling = parsed_args.reschedule, drop_high = drop_high,
                dump_steps = parsed_args.bf_dump_steps,
                time_limit = parsed_args.time_limit,
                memorization = memorization,
                dump_mem_table = parsed_args.dump_mem_table,
                prune_mem_table = parsed_args.prune_mem_table)
    elif scheduler_name.startswith("FAST"):
        if scheduler_name == "FAST":
            scheduler = FastScheduler(platform)
        else:
            v = scheduler_name[5:]
            scheduler = FastScheduler(platform, version=v)
    elif scheduler_name.startswith("DAC"):
        if scheduler_name == "DAC":
            scheduler  = DacScheduler(platform)
        else:
            v = scheduler_name[4:]
            scheduler = DacScheduler(platform, version = v)
    elif scheduler_name.startswith("WWT15"):
        # Parse WWT15 related arguments
        scheduler_type = parsed_args.wwt15_type

        sorting_arg = parsed_args.wwt15_sorting
        if sorting_arg == "COST":
            sorting_key = WWT15SortingKey.MINCOST
        elif sorting_arg == "DEADLINE":
            sorting_key = WWT15SortingKey.DEADLINE
        elif sorting_arg == "CDP":
            sorting_key = WWT15SortingKey.CDP
        else:
            assert False, "Unknown sorting key"

        explore_arg = parsed_args.wwt15_seg_explore
        if explore_arg == "ALL":
            explore_mode = WWT15ExploreMode.ALL
        elif explore_arg == "BEST":
            explore_mode = WWT15ExploreMode.BEST
        else:
            assert False, "Unknown explore mode"

        lr_constraints_arg = parsed_args.wwt15_lr
        if len(lr_constraints_arg) == 0:
            lr_constraints_arg.append("R")
        lr_constraints = LRConstraint.NULL
        if "R" in lr_constraints_arg:
            lr_constraints |= LRConstraint.RESOURCE
        if "D" in lr_constraints_arg:
            lr_constraints |= LRConstraint.DELAY
        if "RDP" in lr_constraints_arg:
            lr_constraints |= LRConstraint.RDP

        lr_rounds = parsed_args.wwt15_lr_rounds

        # Instantiate scheduler
        if scheduler_type == "SEG":
            # Using segmentized scheduler
            scheduler = WWT15Scheduler(platform, sorting = sorting_key, explore_mode = explore_mode,
                                       lr_constraints = lr_constraints, lr_rounds = lr_rounds)
        else:
            assert False, "NYI"
    else:
        assert False, "Unknown scheduler"

    if mode == "single":
        res, scheduling, schedule_time = single_mode_scheduler(scheduler, scenario)
        if res:
            scheduling.legacy_dump(outf=outf)
            # scheduling.legacy_dump_jobs_info(outf=outf)
        if parsed_args.time_limit is not None:
            within_time = schedule_time <= parsed_args.time_limit
        else:
            within_time = True
        print_summary(parsed_args, res, scheduling, schedule_time, within_time)
    elif mode == "trace":
        dump_summary = False
        dump_path = ""
        if parsed_args.summary != '':
            dump_summary=True
            dump_path = parsed_args.summary

        manager = ResourceManager(scheduler, platform)
        tracer = TracePlayer(manager, scenario, dump_summary, dump_path)
        tracer.run()
    else:
        assert False, "Unknown scheduler"


if __name__ == "__main__":
    main()

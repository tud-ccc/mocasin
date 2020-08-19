# The main file of the project which is called from command line.
#
# Author: Robert Khasanov

import sys, os
import time
import timeit
import logging
import hydra

from pykpn.tetris.context import Context
from pykpn.tetris.reqtable import ReqTable
from pykpn.tetris.apptable import AppTable
from pykpn.tetris.job import JobTable

from pykpn.common.platform import Platform

from pykpn.tetris.manager import ResourceManager
from pykpn.tetris.tracer import TracePlayer

from pykpn.tetris import TetrisScheduling

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
    # Suppress logs from pykpn module
    init_logging()

    out_fn = cfg["output_schedule"]
    if out_fn != None:
        outf = open(out_fn, mode="w")
    else:
        outf = sys.stdout

    scheduling = TetrisScheduling.from_hydra(cfg)

    log.info('Start the scheduling')
    start = timeit.default_timer()
    scheduling.run()
    stop = timeit.default_timer()
    log.info('Scheduling done')

    opt_summary = cfg["summary_csv"]
    opt_time_limit = cfg.get("time_limit", 'None')
    opt_reschedule = cfg.get("reschedule", True)
    if scheduling.found_schedule:
        scheduling.schedule.legacy_dump(outf=outf)
        # scheduling.legacy_dump_jobs_info(outf=outf)
    if opt_time_limit != 'None':
        within_time = schedule_time <= opt_time_limit
    else:
        within_time = True
    print_summary(
        cfg['job_table'],
        scheduling.found_schedule,
        scheduling.schedule,
        stop - start,
        scheduling.within_time_limit,
        opt_summary,
        scheduling.scheduler,
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

    tetris_apps_dir = cfg['tetris_apps_dir']

    # Set the platform
    platform = hydra.utils.instantiate(cfg['platform'])

    # Initialize application table
    app_table = AppTable(platform, tetris_apps_dir)

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

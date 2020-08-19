# The main file of the project which is called from command line.
#
# Author: Robert Khasanov

import sys
import timeit
import logging
import hydra

from pykpn.tetris import (TetrisScheduling, TetrisManagement)

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
    # Suppress logs from pykpn module
    init_logging()

    management = TetrisManagement.from_hydra(cfg)

    log.info('Start the tetris management')
    start = timeit.default_timer()
    management.run()
    stop = timeit.default_timer()
    log.info('Tetris management done')

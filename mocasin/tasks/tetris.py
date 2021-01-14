# The main file of the project which is called from command line.
#
# Author: Robert Khasanov

import sys
import timeit
import logging
import hydra

from mocasin.tetris import TetrisScheduling, TetrisManagement

log = logging.getLogger(__name__)


def init_logging():
    logging.getLogger("mocasin.slx.platform.convert").setLevel(logging.ERROR)
    logging.getLogger("mocasin.slx.platform").setLevel(logging.WARNING)
    logging.getLogger("mocasin.slx.kpn").setLevel(logging.WARNING)
    logging.getLogger("mocasin.mapper.partial").setLevel(logging.WARNING)
    logging.getLogger("mocasin.common.mapping").setLevel(logging.WARNING)


@hydra.main(config_path="../conf", config_name="tetris_scheduler")
def tetris_scheduler(cfg):
    """Tetris scheduler

    This task runs tetris scheduler for a single request table.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **tetris_apps_dir:** the base directory with applications and mappings
          info
        * **job_table:** the job table
        * **output_schedule:** the output file with the generated schedule
    """
    # Suppress logs from mocasin module
    init_logging()

    scheduling = TetrisScheduling.from_hydra(cfg)

    log.info("Start the scheduling")
    start = timeit.default_timer()
    scheduling.run()
    stop = timeit.default_timer()
    log.info("Scheduling done")
    scheduling_time = stop - start

    print("Job table file: " + str(cfg["job_table"]))
    print("Scheduler: " + str(scheduling.scheduler.name))
    print("Scheduling time: {:.5f} s".format(scheduling_time))
    print("Found schedule: {}".format(scheduling.found_schedule))
    if scheduling.found_schedule:
        print("Schedule time: {:.5f} s".format(scheduling.schedule.end_time))
        print("Energy consumption: {:.5f} J".format(scheduling.schedule.energy))
        print("Number of segments: {}".format(len(scheduling.schedule)))
        if cfg["output_schedule"] is not None:
            with open(cfg["output_schedule"], mode="w") as f:
                print(scheduling.schedule.to_str(verbose=True), file=f)


@hydra.main(config_path="../conf", config_name="tetris_manager")
def tetris_manager(cfg):
    """Tetris manager

    This task runs tetris manager for the input trace of jobs

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        TODO: Write down
    """
    # Suppress logs from mocasin module
    init_logging()

    management = TetrisManagement.from_hydra(cfg)

    log.info("Start the tetris management")
    start = timeit.default_timer()
    management.run()
    stop = timeit.default_timer()
    log.info("Tetris management done")

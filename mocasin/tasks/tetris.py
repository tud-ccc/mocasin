# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# The main file of the project which is called from command line.
#
# Author: Robert Khasanov

import timeit
import logging
import hydra

from mocasin.tetris import TetrisScheduling, TetrisManagement

log = logging.getLogger(__name__)


def init_logging():
    logging.getLogger("mocasin.maps.platform.convert").setLevel(logging.ERROR)
    logging.getLogger("mocasin.maps.platform").setLevel(logging.WARNING)
    logging.getLogger("mocasin.maps.graph").setLevel(logging.WARNING)
    logging.getLogger("mocasin.mapper.partial").setLevel(logging.WARNING)
    logging.getLogger("mocasin.common.mapping").setLevel(logging.WARNING)


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
    if cfg["precalc_orbits"]:
        log.info("Start precalculation of all orbits")
        start = timeit.default_timer()
        scheduling.precalculate_orbits()
        stop = timeit.default_timer()
        log.info("Precalculation done")
        precalc_time = stop - start

    log.info("Start the scheduling")
    start = timeit.default_timer()
    scheduling.run()
    stop = timeit.default_timer()
    log.info("Scheduling done")
    scheduling_time = stop - start

    print("Job table file: " + str(cfg["job_table"]))
    print("Scheduler: " + str(scheduling.scheduler.name))

    if cfg["precalc_orbits"]:
        print("Orbit precalculation time: {:.5f} s".format(precalc_time))

    print("Scheduling time: {:.5f} s".format(scheduling_time))
    print("Found schedule: {}".format(scheduling.found_schedule))
    if scheduling.found_schedule:
        print("Makespan: {:.5f} s".format(scheduling.schedule.end_time))
        print("Energy consumption: {:.5f} J".format(scheduling.schedule.energy))
        print(f"Number of segments: {len(scheduling.schedule.segments())}")
        if cfg["output_schedule"] is not None:
            with open(cfg["output_schedule"], mode="w") as f:
                print(scheduling.schedule.to_str(verbose=True), file=f)


def tetris_manager(cfg):
    """Tetris manager

    This task simulates the scheduling of multiple applications with Tetris.
    The input trace is represented as a list of arrival events: arrival time,
    application and deadline.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **resource_manager:** the resource_manager.
        * **tetris_apps_dir:** the base directory with applications and mappings
          info
        * **input_jobs:** the input trace of jobs
        * **output_trace:** the output file with the generated trace
        * **stats_jobs:** the output file for job statistics
        * **stats_manager:** the output file for manager statistics
        * **summary:** the output file for the summary results
    """
    # TODO: Change the name to `input_trace`
    # TODO: Change the task name to `simulate_tetris`
    # TODO: Generate output trace

    # Suppress logs from mocasin module
    init_logging()

    management = TetrisManagement.from_hydra(cfg)

    log.info("Start the tetris management")
    start = timeit.default_timer()
    management.run()
    stop = timeit.default_timer()
    log.info("Tetris management done")

    stats = management.stats
    summary = management.summary

    print(f"Total simulation time: {stop - start} s")
    summary.print()

    stats.dump_applications(cfg["stats_jobs"])
    stats.dump_activations(cfg["stats_manager"])
    summary.to_csv(cfg["summary"])

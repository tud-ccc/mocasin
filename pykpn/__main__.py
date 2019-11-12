#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens


import hydra
import logging
import sys

from pykpn.tasks import kpn_to_dot
from pykpn.tasks import mapping_to_dot
from pykpn.tasks import platform_to_dot

from scripts.slx.dc import dc_task
from scripts.slx.enumerate_equivalent import enumerate_equivalent
from scripts.slx.simulate import simulate
from scripts.slx.random_walk import random_walk
from scripts.slx.csv_plot import csv_plot

from scripts.slx.platform_to_autgrp import platform_to_autgrp

log = logging.getLogger(__name__)


pykpn_tasks = {
    'csv_plot': csv_plot,
    'design_centering': dc_task,
    'enumerate_equivalent': enumerate_equivalent,
    'kpn_to_dot': kpn_to_dot,
    'mapping_to_dot': mapping_to_dot,
    'platform_to_autgrp': platform_to_autgrp,
    'platform_to_dot': platform_to_dot,
    'random_walk_mapping': random_walk,
    'simulate': simulate,
}


@hydra.main(config_path='../conf/default.yaml')
def pykpn(cfg):
    """
    This is script is the universal pykpn launcher, which replaces
    individual scripts for different tasks.

    The idea is for this script to manage different tasks that are
    available to do with the pykpn framework, using the different
    configuration capabilities allowed by the hydra framework.

    To add a new task, write a function in a script that executes
    that task and call it from here with the corresponding task
    descriptor, as done in the other examples. No direct
    functionality should be implemented here.

    :param cfg: Omniconf object created by hydra decorator
    :return:
    """

    # TODO: add check if app/platform combination works
    # (can we do this with hydra confs directly?)

    task = cfg['task']
    if task not in pykpn_tasks:
        log.error("Tried to run a task unknown to pykpn (%s)" % task)
        log.info("Choose one of %s" % list(pykpn_tasks.keys()))
        sys.exit(-1)

    # execute the task
    function = pykpn_tasks[task]
    function(cfg)


def main():
    # if the first argument is not an assignment, we treat it as a task
    if len(sys.argv) > 1 and '=' not in sys.argv[1]:
        sys.argv[1] = "task=%s" % sys.argv[1]
    pykpn()


if __name__ == "__main__":
    main()

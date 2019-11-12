# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""This module manages the executable tasks that are available within pykpn

To add a new task, write a function within this package and add an entry to the
:attr:`pykpn_tasks` dict pointing to this function. Each task function should
expect precisely one parameter, the Omniconf object as created by hydra.
"""


import hydra
import logging
import sys

from pykpn.tasks.csv_plot import csv_plot
from pykpn.tasks.enumerate_equivalent import enumerate_equivalent
from pykpn.tasks.platform_to_autgrp import platform_to_autgrp
from pykpn.tasks.random_walk import random_walk
from pykpn.tasks.simulate import simulate
from pykpn.tasks.to_dot import kpn_to_dot
from pykpn.tasks.to_dot import mapping_to_dot
from pykpn.tasks.to_dot import platform_to_dot

log = logging.getLogger(__name__)

pykpn_tasks = {
    'csv_plot': csv_plot,
    'enumerate_equivalent': enumerate_equivalent,
    'kpn_to_dot': kpn_to_dot,
    'mapping_to_dot': mapping_to_dot,
    'platform_to_autgrp': platform_to_autgrp,
    'platform_to_dot': platform_to_dot,
    'random_walk_mapping': random_walk,
    'simulate': simulate,
}
"""A dictionary that maps task names to a callable function."""


@hydra.main(config_path='../conf/default.yaml')
def execute_task(cfg):
    """Executes an individual task as specified in the configuration

    :param cfg: Omniconf object created by hydra decorator
    :return:
    """
    task = cfg['task']

    if task not in pykpn_tasks:
        log.error("Tried to run a task unknown to pykpn (%s)" % task)
        log.info("Choose one of %s" % list(pykpn_tasks.keys()))
        sys.exit(-1)

    # execute the task
    function = pykpn_tasks[task]
    function(cfg)

#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens
from scripts.slx.dc import dc_task
from scripts.slx.enumerate_equivalent import enumerate_equivalent
from scripts.slx.simulate import simulate
from scripts.slx.random_walk import random_walk
from scripts.slx.csv_plot import csv_plot
from scripts.slx.platform_to_dot import platform_to_dot
from scripts.slx.mapping_to_dot import mapping_to_dot
from scripts.slx.kpn_to_dot import kpn_to_dot
from scripts.slx.platform_to_autgrp import platform_to_autgrp

from pykpn.util import logging
log = logging.getLogger(__name__)

import hydra

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
    logging.setup_from_cfg_dict(cfg)
    #TODO: add check if app/platform combination works
    # (can we do this with hydra confs directly?)

    task = cfg['task']
    if task == 'simulate':
        simulate(config_dict=cfg)
    if task == 'random_walk_mapping':
        random_walk(cfg)
    if task == 'csv_plot':
        csv_plot(cfg)
    if task == 'platform_to_dot':
        platform_to_dot(cfg)
    if task == 'mapping_to_dot':
        mapping_to_dot(cfg)
    if task == 'kpn_to_dot':
        kpn_to_dot(cfg)
    if task == 'platform_to_autgrp':
        platform_to_autgrp(cfg)
    if task == 'enumerate_equivalent':
        enumerate_equivalent(cfg)
    if task == 'design_centering':
        dc_task(cfg)


if __name__ == "__main__":
    pykpn()

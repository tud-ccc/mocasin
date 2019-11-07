#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens
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
    logging.setup_from_cfg_dict(cfg)
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
        log.error("design centering not ported to pykpn_manager yet, use script for now.")


if __name__ == "__main__":
    pykpn()

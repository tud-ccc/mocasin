#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens


from scripts.slx.simulate import simulate
from scripts.slx.random_walk import random_walk

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


if __name__ == "__main__":
    pykpn()

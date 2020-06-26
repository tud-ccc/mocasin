#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra

from pykpn.representations.representations import RepresentationType

log = logging.getLogger(__name__)


@hydra.main(config_path='conf/enumerate_equivalent.yaml')
def enumerate_equivalent(cfg):
    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    mapping = hydra.utils.instantiate(cfg['mapper'], kpn, platform, cfg).generate_mapping()

    representation = RepresentationType['Symmetries'].getClassType()(kpn,platform)
    log.info(("calculating orbit for mapping:" + str(mapping.to_list())))
    orbit = representation.allEquivalent(mapping.to_list())
    log.info("orbit of size: " + str(len(orbit)))
    with open(cfg['output_file'],'w') as output_file:
        for i,elem in enumerate(orbit):
            output_file.write(f"\n mapping {i}:\n")
            output_file.write(mapping.to_string())

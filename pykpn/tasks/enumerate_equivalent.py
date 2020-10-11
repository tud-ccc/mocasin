#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra

from pykpn.representations import SymmetryRepresentation

log = logging.getLogger(__name__)


@hydra.main(config_path='../conf', config_name='enumerate_equivalent')
def enumerate_equivalent(cfg):
    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    trace = hydra.utils.instantiate(cfg['trace'])
    if cfg['representation']._target_ != 'pykpn.representations.SymmetryRepresentation':
        raise RuntimeError(f"The enumerate equvialent task needs to be called with the Symmetry representation. Called with {cfg['representation']._target_}")
    representation = hydra.utils.instantiate(cfg['representation'], kpn, platform)
    mapping = hydra.utils.instantiate(cfg['mapper'], kpn, platform, trace,representation).generate_mapping()

    log.info(("calculating orbit for mapping:" + str(mapping.to_list())))
    orbit = representation.allEquivalent(mapping.to_list())
    log.info("orbit of size: " + str(len(orbit)))
    with open(cfg['output_file'],'w') as output_file:
        for i,elem in enumerate(orbit):
            output_file.write(f"\n mapping {i}:\n")
            output_file.write(elem.to_string())

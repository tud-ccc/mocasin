#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Christian Menard

import logging
import hydra
import os
import pickle

from pykpn.tgff.tgffSimulation import TgffReferenceError
from pykpn.mapper.genetic import GeneticMapper

log = logging.getLogger(__name__)


@hydra.main(config_path='../conf/', config_name='pareto_front.yaml')
def pareto_front(cfg):
    """Pareto Front Task

    This task produces a pareto front of mappings using the genetic algorithms task


    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **export_all:** a flag indicating whether all mappings should be
          exported. If ``false`` only the best mapping will be exported.
        * **kpn:** the input kpn graph. The task expects a configuration dict
          that can be instantiated to a :class:`~pykpn.common.kpn.KpnGraph`
          object.
        * **outdir:** the output directory
        * **progress:** a flag indicating whether to show a progress bar with
          ETA
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~pykpn.common.trace.TraceGenerator` object.
"""
    try:
        kpn = hydra.utils.instantiate(cfg['kpn'])
        platform = hydra.utils.instantiate(cfg['platform'])
        mapper = hydra.utils.instantiate(cfg['mapper'], kpn, platform, cfg)
    except TgffReferenceError:
        # Special exception indicates a bad combination of tgff components
        # can be thrown during multiruns and should not stop the hydra
        # execution
        log.warning("Referenced non existing tgff component!")
        return

    #Run genetic algorithm
    results = mapper.generate_pareto_front()

    # export the best mapping
    outdir = cfg['outdir']
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for i,result in enumerate(results):
        with open(outdir + f"/mapping{i}.pickle" ,'wb') as f:
            p = pickle.Pickler(f)
            p.dump(result)

    for i,result in enumerate(results):
        with open(outdir + f"results{i}.txt",'w') as f:
            f.write(str(mapper.evaluate_mapping(mapper.representation.toRepresentation(result))))

    del mapper

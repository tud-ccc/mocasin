#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra
import os
import simpy
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem

from pykpn.slx.mapping import export_slx_mapping

log = logging.getLogger(__name__)

def generate_mapping(cfg):
    """Mapper Task

    This task produces a mapping using one of multiple possible mapping algorithms.


    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **mapper:** the mapper (mapping algorithm) to be used.
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
        * **plot_distribution:** a flag indicating whether to plot the
          distribution of simulated execution times over all mapping
        * **rep_type_str** the representation type for the mapping space
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~pykpn.common.trace.TraceGenerator` object.
        * **visualize:** a flag indicating whether to visualize the mapping
          space using t-SNE
        * **show_plots:** a flag indicating whether to open all plots or just
            write them to files.

    It is recommended to use the silent all logginf o (``-s``) to suppress all logging
    output from the individual simulations.
"""

    mapper = hydra.utils.instantiate(cfg['mapper'],cfg)
    #Run mapper
    result = mapper.generate_mapping()

    # export the best mapping
    outdir = cfg['outdir']
    if not os.path.exists(outdir):
        os.makedirs(outdir)



    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    trace = hydra.utils.instantiate(cfg['trace'])

    env = simpy.Environment()
    app = RuntimeKpnApplication(name=kpn.name,
                                kpn_graph=kpn,
                                mapping=result,
                                trace_generator=trace,
                                env=env,)
    system = RuntimeSystem(platform, [app], env)

    system.simulate()

    exec_time = float(env.now) / 1000000000.0
    log.info('Best mapping simulated time: ' + str(exec_time) + ' ms')


    export_slx_mapping(result,
                   os.path.join(outdir, 'generated_mapping'),
                   '2017.10')

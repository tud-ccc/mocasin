#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra
import os
import pickle

from pykpn.slx.mapping import export_slx_mapping
from pykpn.simulate import KpnSimulation
from pykpn.tgff.tgffSimulation import TgffReferenceError

log = logging.getLogger(__name__)

@hydra.main(config_path='../conf', config_name='generate_mapping')
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
    try:
        kpn = hydra.utils.instantiate(cfg['kpn'])
        platform = hydra.utils.instantiate(cfg['platform'])
        trace = hydra.utils.instantiate(cfg['trace'])
        representation = hydra.utils.instantiate(cfg['representation'],kpn,platform)
        mapper = hydra.utils.instantiate(cfg['mapper'], kpn, platform, trace, representation)
    except TgffReferenceError:
        # Special exception indicates a bad combination of tgff components
        # can be thrown during multiruns and should not stop the hydra
        # execution
        log.warning("Referenced non existing tgff component!")
        return

    #Run mapper
    result = mapper.generate_mapping()

    # export the best mapping
    outdir = cfg['outdir']
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        with open(outdir + "/mapping.pickle" ,'wb') as f:
            p = pickle.Pickler(f)
            p.dump(result)

    if cfg['simulate_best']:
        trace = hydra.utils.instantiate(cfg['trace'])
        simulation = KpnSimulation(result.platform, result.kpn, result, trace)
        with simulation as s:
            s.run()

        exec_time = float(simulation.exec_time) / 1000000000.0
        log.info('Best mapping simulated time: ' + str(exec_time) + ' ms')
        with open(outdir + 'best_time.txt','w') as f:
            f.write(str(exec_time))

    if not cfg['kpn']['_target_'] == 'pykpn.tgff.tgffSimulation.KpnGraphFromTgff':
        export_slx_mapping(result,
                           os.path.join(outdir, 'generated_mapping'))
    #moved this from random mapper. It should be part of the task, not the mapper.
    # export all mappings if requested
    # idx = 1
    #if self.export_all:
    #    for mapping in mappings:
    #        mapping_name = 'rnd_%08d.mapping' % idx
    #        #FIXME: We assume an slx output here, this should be configured
    #        export_slx_mapping(mapping, os.path.join(self.out_dir, mapping_name))
    #        idx += 1

    # plot result distribution
    #if self.plot_distribution:
    #    import matplotlib.pyplot as plt
    #    # exec time in milliseconds
    #    plt.hist(exec_times, bins=int(self.num_iterations / 20), density=True)
    #    plt.yscale('log', nonposy='clip')
    #    plt.title("Mapping Distribution")
    #    plt.xlabel("Execution Time [ms]")
    #    plt.ylabel("Probability")

    #    if self.show_plots:
    #        plt.show()

    #    plt.savefig("distribution.pdf")

    ## visualize searched space
    #if self.visualize:

    #    plot.visualize_mapping_space(mappings,
    #                                 exec_times,
    #                                 self.representation,
    #                                 show_plot=self.show_plots,
    #                                 tick=self.tick,
    #                                 history=self.history)


    del mapper

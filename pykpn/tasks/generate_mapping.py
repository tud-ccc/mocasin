#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra
import os

from pykpn.representations.representations import RepresentationType
from pykpn.slx.mapping import export_slx_mapping
from pykpn.util import plot

log = logging.getLogger(__name__)



def random_walk(cfg):
    """A Random Walk Mapper

    This task produces multiple random mappings and simulates each mapping in
    order to find the 'best' mapping. As outlined below, the script expects
    multiple configuration parameters to be available.


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
    rep_type_str = cfg['rep_type_str']
    num_iterations = cfg['num_iterations']

    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])

    if rep_type_str not in dir(RepresentationType):
        log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(dir(RepresentationType)))
        raise RuntimeError('Unrecognized representation.')
    rep_type = RepresentationType[rep_type_str]


    mapper = hydra.utils.instantiate(cfg['mapper'])

    #Run mapper

    # export the best mapping
    outdir = cfg['outdir']
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for ac in best_result.app_contexts:
        mapping_name = '%s.best.mapping' % (ac.name)
        # FIXME: We assume an slx output here, this should be configured
        export_slx_mapping(ac.mapping,
                           os.path.join(outdir, mapping_name),
                           '2017.10')

    # export all mappings if requested
    idx = 1
    if cfg['export_all']:
        for r in results:
            for ac in r.app_contexts:
                mapping_name = '%s.rnd_%08d.mapping' % (ac.name, idx)
                # FIXME: We assume an slx output here, this should be configured
                export_slx_mapping(ac.mapping,
                                   os.path.join(outdir, mapping_name),
                                   '2017.10')
            idx += 1

    # plot result distribution
    if cfg['plot_distribution']:
        import matplotlib.pyplot as plt
        # exec time in milliseconds
        plt.hist(exec_times, bins=int(num_iterations/20), density=True)
        plt.yscale('log', nonposy='clip')
        plt.title("Mapping Distribution")
        plt.xlabel("Execution Time [ms]")
        plt.ylabel("Probability")
        if cfg['show_plots']:
            plt.show()
        plt.savefig("distribution.pdf")

    # visualize searched space
    visualize = cfg['visualize']
    if cfg['visualize']:
        if len(results[0].app_contexts) > 1:
            raise RuntimeError('Search space visualization only works '
                               'for single application mappings')
        mappings = [r.app_contexts[0].mapping for r in results]
        plot.visualize_mapping_space(mappings,
                                     exec_times,
                                     representation_type=rep_type,
                                     show_plot=cfg['show_plots'],)



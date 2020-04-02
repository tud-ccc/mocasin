#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra
import multiprocessing as mp
import os
import simpy
import timeit
import csv

from pykpn.mapper.random import RandomMapping
from pykpn.representations.representations import RepresentationType
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
from pykpn.slx.mapping import export_slx_mapping
from pykpn.util import plot

log = logging.getLogger(__name__)


class ApplicationContext(object):

    def __init__(self, name=None, kpn=None, mapping=None, trace_reader=None,
                 start_time=None):
        self.name = name
        self.kpn = kpn
        self.mapping = mapping
        self.trace_reader = trace_reader
        self.start_time = start_time


class SimulationContext(object):

    def __init__(self, platform=None, app_contexts=None):
        self.platform = platform
        if app_contexts is None:
            self.app_contexts = []
        else:
            self.app_contexts = app_contexts
        self.exec_time = None


@hydra.main(config_path='conf/random_walk_mapping.yaml')
def random_walk(cfg):
    """A Random Walk Mapper

    This task produces multiple random mappings and simulates each mapping in
    order to find the 'best' mapping. As outlined below, the script expects
    multiple configuration parameters to be available.


    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **export_all:** a flag indicating whether all mappings should be
          exported. If ``false`` only the best mapping will be exported.
        * **jobs:** the number of parallel jobs
        * **kpn:** the input kpn graph. The task expects a configuration dict
          that can be instantiated to a :class:`~pykpn.common.kpn.KpnGraph`
          object.
        * **num_operations:** the total number of mappings to be generated
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

    start = timeit.default_timer()

    # Create a list of 'simulations'. These are later executed by multiple
    # worker processes.
    simulations = []
    for i in range(0, num_iterations):

        # create a simulation context
        sim_context = SimulationContext(platform)

        # create the application context
        name = kpn.name
        app_context = ApplicationContext(name, kpn)

        app_context.start_time = 0

        # generate a random mapping
        app_context.representation = RepresentationType[rep_type_str]
        app_context.mapping = RandomMapping(kpn, platform)

        # create the trace reader
        app_context.trace_reader = hydra.utils.instantiate(cfg['trace'])

        sim_context.app_contexts.append(app_context)

        simulations.append(sim_context)

    # run the simulations and search for the best mapping
    pool = mp.Pool(processes=cfg['jobs'])

    # execute the simulations in parallel
    if cfg['progress']:
        import tqdm
        results = list(tqdm.tqdm(pool.imap(run_simualtion, simulations,
                                           chunksize=10),
                                 total=num_iterations))
    else:
        results = list(pool.map(run_simualtion, simulations, chunksize=10))

    # calculate the execution times in milliseconds and look for the best
    # result
    best_result = results[0]
    exec_times = []  # keep a list of exec_times for later
    for r in results:
        exec_times.append(float(r.exec_time / 1000000000.0))
        if r.exec_time < best_result.exec_time:
            best_result = r

    # When we reach this point, all simulations completed

    stop = timeit.default_timer()
    log.info('Tried %d random mappings in %0.1fs' %
          (len(results), stop - start))
    exec_time = float(best_result.exec_time / 1000000000.0)
    log.info('Best simulated execution time: %0.1fms' % (exec_time))

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
        with open(os.path.join(outdir,'runtimes.csv'), 'w', newline='') as csvfile:
            result_writer = csv.writer(csvfile, delimiter=',')
            result_writer.writerow(['index', 'filename', 'runtime'])
            for r in results:
                for ac in r.app_contexts:
                    mapping_name = '%s.rnd_%08d.mapping' % (ac.name, idx)
                    result_writer.writerow([idx,mapping_name,exec_times[idx-1]])
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


def run_simualtion(sim_context):
    # Create simulation environment
    env = simpy.Environment()

    # create the applications
    applications = []
    mappings = {}
    for ac in sim_context.app_contexts:
        app = RuntimeKpnApplication(ac.name, ac.kpn, ac.mapping,
                                    ac.trace_reader, env, ac.start_time)
        applications.append(app)
        mappings[ac.name] = ac.mapping

    # Create the system
    system = RuntimeSystem(sim_context.platform, applications, env)

    # run the simulation
    system.simulate()
    system.check_errors()

    sim_context.exec_time = env.now

    return sim_context

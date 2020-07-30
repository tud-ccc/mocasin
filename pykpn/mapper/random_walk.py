# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import timeit
import multiprocessing as mp
import hydra
import random
import numpy as np
import os

from pykpn.mapper.utils import Statistics, ApplicationContext, SimulationContext, run_simulation
from pykpn.mapper.random import RandomMapper
from pykpn.util import logging, plot
from pykpn.slx.mapping import export_slx_mapping
from pykpn.representations.representations import RepresentationType
from pykpn.common.mapping import ChannelMappingInfo, Mapping, ProcessMappingInfo

log = logging.getLogger(__name__)

#TODO: Skip this cause representation object is needed?

class RandomWalkMapper(object):
    """Generates a full mapping via a random walk

    This class is used to generate a mapping for a given
    platform and KPN application, via a random walk through
    the mapping space.
    It produces multiple random mappings and simulates each mapping in
    order to find the 'best' mapping. As outlined below, the script expects
    multiple configuration parameters to be available.
    **Hydra Parameters**:
        * **jobs:** the number of parallel jobs
        * **num_operations:** the total number of mappings to be generated
    """

    def __init__(self, kpn, platform, config):
        """Generates a random mapping for a given platform and KPN application.
        Args:
           cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object
        """
        self.full_mapper = True
        self.kpn = kpn
        self.platform = platform
        self.random_mapper = RandomMapper(self.kpn, self.platform, random_seed=None)
        self.config = config
        self.statistics = Statistics(log, len(self.kpn.processes()), config['mapper']['record_statistics'])
        rep_type_str = config['representation']

        self.seed = config['mapper']['random_seed']
        if self.seed == 'None':
            self.seed = None
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " +
                          ", ".join(dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        self.rep_type = RepresentationType[rep_type_str]


    def generate_mapping(self):
        """ Generates a mapping via a random walk
        """
        cfg = self.config
        num_iterations = cfg['mapper']['num_iterations']

        start = timeit.default_timer()
        # Create a list of 'simulations'. These are later executed by multiple
        # worker processes.
        simulations = []

        for i in range(0, self.config['mapper']['num_iterations']):
            # create a simulation context
            sim_context = SimulationContext(self.platform)

            # create the application context
            name = self.kpn.name
            app_context = ApplicationContext(name, self.kpn)

            app_context.start_time = 0

            # generate a random mapping
            app_context.representation = self.rep_type
            app_context.mapping = self.random_mapper.generate_mapping()

            #since mappings are simulated in parallel, whole simulation time is added later as offset
            self.statistics.mapping_evaluated(0)

            # create the trace reader
            app_context.trace_reader = hydra.utils.instantiate(cfg['trace'])

            sim_context.app_contexts.append(app_context)

            simulations.append(sim_context)

        # run the simulations and search for the best mapping
        pool = mp.Pool(processes=cfg['mapper']['jobs'])

        # execute the simulations in parallel
        if cfg['mapper']['progress']:
            import tqdm
            results = list(tqdm.tqdm(pool.imap(run_simulation, simulations,
                                               chunksize=10),
                                     total=num_iterations))
        else:
            results = list(pool.map(run_simulation, simulations, chunksize=10))

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
        self.statistics.add_offset(stop - start)
        exec_time = float(best_result.exec_time / 1000000000.0)
        log.info('Best simulated execution time: %0.1fms' % (exec_time))
        # export all mappings if requested
        idx = 1
        outdir = cfg['outdir']

        if cfg['mapper']['export_all']:
            for r in results:
                for ac in r.app_contexts:
                    mapping_name = '%s.rnd_%08d.mapping' % (ac.name, idx)
                    # FIXME: We assume an slx output here, this should be configured
                    export_slx_mapping(ac.mapping,
                                       os.path.join(outdir, mapping_name))
                idx += 1

        # plot result distribution
        if cfg['mapper']['plot_distribution']:
            import matplotlib.pyplot as plt
            # exec time in milliseconds
            plt.hist(exec_times, bins=int(cfg['num_iterations'] / 20), density=True)
            plt.yscale('log', nonposy='clip')
            plt.title("Mapping Distribution")
            plt.xlabel("Execution Time [ms]")
            plt.ylabel("Probability")

            if cfg['mapper']['show_plots']:
                plt.show()

            plt.savefig("distribution.pdf")

        # visualize searched space
        if cfg['mapper']['visualize']:

            if len(results[0].app_contexts) > 1:
                raise RuntimeError('Search space visualization only works '
                                   'for single application mappings')

            mappings = [r.app_contexts[0].mapping for r in results]
            plot.visualize_mapping_space(mappings,
                                         exec_times,
                                         representation_type=self.rep_type,
                                         show_plot=cfg['mapper']['show_plots'], )

        self.statistics.to_file()
        return best_result.app_contexts[0].mapping

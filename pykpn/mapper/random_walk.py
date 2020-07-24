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

from pykpn.mapper.utils import Statistics, ApplicationContext, SimulationContext, run_simulation, SimulationManager
from pykpn.mapper.random import RandomMapper
from pykpn.util import logging, plot
from pykpn.slx.mapping import export_slx_mapping
from pykpn.representations.representations import RepresentationType
from pykpn.common.mapping import ChannelMappingInfo, Mapping, ProcessMappingInfo

log = logging.getLogger(__name__)


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
        self.kpn = hydra.utils.instantiate(config['kpn'])
        self.platform = hydra.utils.instantiate(config['platform'])
        self.random_mapper = RandomMapper(self.kpn,self.platform,config)
        self.config = config

        self.seed = config['random_seed']
        if self.seed == 'None':
            self.seed = None
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        rep_type_str = config['representation']
        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")
            self.rep_type = representation_type

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation

        self.simulation_manager = SimulationManager(representation, config)

    def generate_mapping(self):
        """ Generates a mapping via a random walk
        """
        cfg = self.config
        num_iterations = cfg['num_iterations']

        start = timeit.default_timer()
        # Create a list of 'simulations'. These are later executed by multiple
        # worker processes.
        mappings = []

        for i in range(0, self.config['num_iterations']):
            mapping = self.random_mapper.generate_mapping()
            mappings.append(mapping)

        if cfg['parallel']:
            simulations = []
            for mapping in mappings:
                # create a simulation context
                sim_context = SimulationContext(self.platform)

                # create the application context
                name = self.kpn.name
                app_context = ApplicationContext(name, self.kpn)
                app_context.start_time = 0

                # generate a random mapping
                app_context.representation = self.rep_type
                app_context.mapping = mapping

                # since mappings are simulated in parallel, whole simulation time is added later as offset
                self.simulation_manager.statistics.mapping_evaluated(0)

                # create the trace reader
                app_context.trace_reader = hydra.utils.instantiate(cfg['trace'])
                sim_context.app_contexts.append(app_context)
                simulations.append(sim_context)

            # run the simulations and search for the best mapping
            pool = mp.Pool(processes=cfg['jobs'])

            # execute the simulations in parallel
            if cfg['progress']:
                 import tqdm
                 results = list(tqdm.tqdm(pool.imap(run_simulation, simulations,
                                                    chunksize = 10), total = num_iterations))
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

            exec_time = float(best_result.exec_time / 1000000000.0)
            best_result = best_result.app_contexts[0].mapping
            # When we reach this point, all simulations completed

        else: #sequential
            exec_times = []
            exec_time = np.inf

            for mapping in mappings:
                m = self.representation.toRepresentation(mapping)
                cur_time = self.simulation_manager.simulate(m)
                if cur_time < exec_time:
                    exec_time = cur_time
                    best_result = mapping
                exec_times.append(cur_time)



        stop = timeit.default_timer()
        log.info('Tried %d random mappings in %0.1fs' %
                 (len(exec_times), stop - start))
        self.simulation_manager.statistics.add_offset(stop - start)
        log.info('Best simulated execution time: %0.1fms' % (exec_time))
        # export all mappings if requested
        idx = 1
        outdir = cfg['outdir']

        if cfg['export_all']:
            for mapping in mappings:
                 mapping_name = 'rnd_%08d.mapping' % idx
                  # FIXME: We assume an slx output here, this should be configured
                 export_slx_mapping(mapping,
                                    os.path.join(outdir, mapping_name))
                 idx += 1

        # plot result distribution
        if cfg['plot_distribution']:
            import matplotlib.pyplot as plt
            # exec time in milliseconds
            plt.hist(exec_times, bins=int(cfg['num_iterations'] / 20), density=True)
            plt.yscale('log', nonposy='clip')
            plt.title("Mapping Distribution")
            plt.xlabel("Execution Time [ms]")
            plt.ylabel("Probability")

            if cfg['show_plots']:
                plt.show()

            plt.savefig("distribution.pdf")

        # visualize searched space
        if cfg['visualize']:

            if cfg['parallel'] and len(results[0].app_contexts) > 1:
                raise RuntimeError('Search space visualization only works '
                                   'for single application mappings')

            plot.visualize_mapping_space(mappings,
                                         exec_times,
                                         representation_type=self.rep_type,
                                         show_plot=cfg['show_plots'], )

        self.simulation_manager.statistics.to_file()
        if self.config['dump_cache']:
            self.simulation_manager.dump('mapping_cache.csv')

        return best_result

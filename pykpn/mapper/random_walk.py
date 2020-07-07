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
        self.statistics = Statistics(log, len(self.kpn.processes()), config['record_statistics'])
        rep_type_str = config['representation']

        self.seed = config['random_seed']
        if self.seed == 'None':
            self.seed = None
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        self.rep_type = RepresentationType[rep_type_str]


    def generate_mapping(self):
        """ Generates a mapping via a random walk
        """
        cfg = self.config
        num_iterations = cfg['num_iterations']

        start = timeit.default_timer()
        # Create a list of 'simulations'. These are later executed by multiple
        # worker processes.
        simulations = []

        for i in range(0, self.config['num_iterations']):
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
        pool = mp.Pool(processes=cfg['jobs'])

        # execute the simulations in parallel
        if cfg['progress']:
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

            if len(results[0].app_contexts) > 1:
                raise RuntimeError('Search space visualization only works '
                                   'for single application mappings')

            mappings = [r.app_contexts[0].mapping for r in results]
            plot.visualize_mapping_space(mappings,
                                         exec_times,
                                         representation_type=self.rep_type,
                                         show_plot=cfg['show_plots'], )

        self.statistics.to_file()
        return best_result.app_contexts[0].mapping


class RandomPartialMapper(object):
    """Generates a random mapping

    This class is used to generate a random mapping for a given
    platform and KPN application.
    """

    def __init__(self, kpn, platform, config, seed=None):
        """Generates a random mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        """
        if seed is not None:
            random.seed(seed)
        self.seed = seed
        self.config = config
        self.full_mapper = True
        self.platform = platform
        self.kpn = kpn

    def generate_mapping(self, part_mapping = None):
        """ Generates a random mapping

        The generated mapping takes a partial mapping (that may also be empty)
        as starting point. All open mapping decissions were taken by generated
        randomness derived from the given seed.

        :param seed: initial seed for the random generator
        :type seed: integer
        :param part_mapping: partial mapping to start from
        :type part_mapping: Mapping
        """

        #generate new mapping if no partial mapping is given
        if not part_mapping:
            part_mapping = Mapping(self.kpn, self.platform)

        # check if the platform/kpn is equivalent
        if not part_mapping.platform is self.platform or not part_mapping.kpn is self.kpn:
            raise RuntimeError('rand_map: Try to map partial mapping of platform,KPN %s,%s to %s,%s',
                               part_mapping.platform.name, part_mapping.kpn.name,
                               self.platform.name, self.kpn.name)

        # map processes
        processes = part_mapping.get_unmapped_processes()
        #print("remaining process list: {}".format(processes))
        for p in processes:
            i = random.randrange(0, len(self.platform.schedulers()))
            scheduler = list(self.platform.schedulers())[i]
            i = random.randrange(0, len(scheduler.processors))
            affinity = scheduler.processors[i]
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            part_mapping.add_process_info(p, info)
            log.debug('rand_map: map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)

            # map channels
        channels = part_mapping.get_unmapped_channels()
        for c in channels:
            capacity = 4 # fixed channel bound this may cause problems
            suitable_primitives = []
            for p in part_mapping.platform.primitives():
                src = part_mapping.process_info(c.source).affinity
                sinks = [part_mapping.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError('rand_map: Mapping failed! No suitable primitive for '
                                   'communication from %s to %s found!' %
                                   (src.name, str(sinks)))
            i = random.randrange(0, len(suitable_primitives))
            primitive = suitable_primitives[i]
            info = ChannelMappingInfo(primitive, capacity)
            part_mapping.add_channel_info(c, info)
            log.debug('rand_map: map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity))


            # finally check if the mapping is fully specified
        assert not part_mapping.get_unmapped_processes()
        assert not part_mapping.get_unmapped_channels()
        return part_mapping

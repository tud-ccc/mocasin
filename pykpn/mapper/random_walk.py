# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import timeit
import random
import numpy as np
import tqdm
from hydra.utils import instantiate

from pykpn.mapper.utils import SimulationManager, Statistics
from pykpn.mapper.random import RandomMapper
from pykpn.util import logging
from pykpn.representations import MappingRepresentation

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

    def __init__(self, kpn, platform, trace, representation, num_iterations=100, progress=False,
                 radius=3.0,random_seed=42, record_statistics=False, parallel=False,
                 dump_cache=False, chunk_size=10, jobs=1):
        """Generates a random mapping for a given platform and KPN application.
        Args:
        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param random_seed: A random seed for the RNG
        :type random_seed: int
        :param record_statistics: Record statistics on mappings evaluated?
        :type record_statistics: bool
        :param num_iterations: Number of iterations (mappings) in random walk
        :type num_iterations: int
        :param rodius: Currently unused.
        :type radius: float
        :param dump_cache: Dump the mapping cache?
        :type dump_cache: bool
        :param chunk_size: Size of chunks for parallel simulation
        :type chunk_size: int
        :param progress: Display simulation progress visually?
        :type progress: bool
        :param parallel: Execute simulations in parallel?
        :type parallel: bool
        :param jobs: Number of jobs for parallel simulation
        :type jobs: int
        """
        self.full_mapper = True
        self.kpn = kpn
        self.platform = platform
        self.random_mapper = RandomMapper(self.kpn, self.platform, trace, representation, random_seed=None)
        self.num_iterations = num_iterations
        self.dump_cache = dump_cache
        self.seed = random_seed
        self.progress = progress
        if self.seed == 'None':
            self.seed = None
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not issubclass(type(type(representation)), MappingRepresentation):
            representation = instantiate(representation,kpn,platform)
        self.representation = representation

        self.simulation_manager = SimulationManager(self.representation, trace,jobs, parallel,
                                                    progress,chunk_size,record_statistics)

    def generate_mapping(self):
        """ Generates a mapping via a random walk
        """
        start = timeit.default_timer()
        # Create a list of 'simulations'. These are later executed by multiple
        # worker processes.
        mappings = []

        if self.progress:
            iterations_range = tqdm.tqdm(range(self.num_iterations))
        else:
            iterations_range = range(self.num_iterations)
        for i in iterations_range:
            mapping = self.random_mapper.generate_mapping()
            mappings.append(mapping)
        if hasattr(self.representation,'canonical_operations') and not self.representation.canonical_operations:
            tup = list(map(self.representation.toRepresentationNoncanonical, mappings))
        else:
            tup = list(map(self.representation.toRepresentation, mappings))
        exec_times = self.simulation_manager.simulate(tup)
        best_result_idx = exec_times.index(min(exec_times))
        best_result = mappings[best_result_idx]
        stop = timeit.default_timer()
        log.info('Tried %d random mappings in %0.1fs' %
                 (len(exec_times), stop - start))
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump('mapping_cache.csv')

        return best_result

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
from hydra.utils import instantiate
import numpy as np

from pykpn.util import logging
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.utils import SimulationManager
from pykpn.mapper.utils import Statistics
from pykpn.representations import MappingRepresentation

log = logging.getLogger(__name__)


class GradientDescentMapper(object):
    """Generates a full mapping by using a gradient descent on the mapping space.
    """
    def __init__(self, kpn, platform, trace, representation, gd_iterations=100,
                 stepsize=2, random_seed=42, record_statistics=False,
                 dump_cache=False, chunk_size=10, progress=False, parallel=False,
                 jobs=2):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param gd_iterations: Number of iterations for gradient descent
        :type gd_iterations: int
        :param stepsize: Size of gradient step
        :type stepsize: float
        :param random_seed: A random seed for the RNG
        :type random_seed: int
        :param record_statistics: Record statistics on mappings evaluated?
        :type record_statistics: bool
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
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = kpn
        self.platform = platform
        self.num_PEs = len(platform.processors())
        self.random_mapper = RandomPartialMapper(self.kpn, self.platform, seed=None)
        self.gd_iterations = gd_iterations
        self.stepsize = stepsize
        self.dump_cache = dump_cache
        self.statistics = Statistics(log, len(self.kpn.processes()), record_statistics)

        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not issubclass(type(type(representation)), MappingRepresentation):
            representation = instantiate(representation,kpn,platform)
        self.representation = representation
        self.simulation_manager = SimulationManager(self.representation, trace,jobs, parallel,
                                                    progress,chunk_size,record_statistics)

    def generate_mapping(self):
        """ Generates a full mapping using gradient descent
        """
        mapping_obj = self.random_mapper.generate_mapping()
        mapping = self.representation.toRepresentation(mapping_obj)

        self.dim = len(mapping)
        cur_exec_time = self.simulation_manager.simulate([mapping])[0]
        self.best_mapping = mapping
        self.best_exec_time = cur_exec_time

        for _ in range(self.gd_iterations):
            grad = self.calculate_gradient(mapping, cur_exec_time)

            if np.allclose(grad, np.zeros(self.dim)): #found local minimum
                break
            mapping = mapping + (self.stepsize / self.best_exec_time) * (-grad)
            mapping = self.representation.approximate(np.array(mapping))

            cur_exec_time = self.simulation_manager.simulate([mapping])[0]

            if cur_exec_time < self.best_exec_time:
                self.best_exec_time = cur_exec_time
                self.best_mapping = mapping

        self.best_mapping = np.array(self.representation.approximate(np.array(self.best_mapping)))
        self.simulation_manager.statistics.log_statistics()
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump('mapping_cache.csv')

        return self.representation.fromRepresentation(self.best_mapping)


    def calculate_gradient(self, mapping, cur_exec_time):
        grad = np.zeros(self.dim)
        for i in range(self.dim):
            evec = np.zeros(self.dim)
            if mapping[i] == 0:
                evec[i] = 1.
                exec_time = self.simulation_manager.simulate([mapping + evec])[0]
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                gr = exec_time - cur_exec_time
                grad[i] = max(gr, 0)  # can go below 0 here
            elif mapping[i] == self.num_PEs - 1:
                evec[i] = -1.
                exec_time = self.simulation_manager.simulate([mapping + evec])[0]
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                gr = cur_exec_time - exec_time  # because of the -h in the denominator of the difference quotient
                grad[i] = min(gr, 0)  # can't go above self.num_PEs-1 here

            else:
                evec[i] = 1.
                exec_time = self.simulation_manager.simulate([mapping + evec])[0]
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                diff_plus = exec_time - cur_exec_time
                evec[i] = -1.
                exec_time = self.simulation_manager.simulate([mapping + evec])[0]
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                diff_minus = cur_exec_time - exec_time  # because of the -h in the denominator of the difference quotient
                grad[i] = (diff_plus + diff_minus) / 2
        return grad

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import numpy as np
import tqdm
from hydra.utils import instantiate

from pykpn.util import logging
from pykpn.representations import MappingRepresentation
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.utils import SimulationManager
from pykpn.mapper.utils import Statistics


log = logging.getLogger(__name__)


class SimulatedAnnealingMapper(object):
    """Generates a full mapping by using a simulated annealing algorithm from:
    Orsila, H., Kangas, T., Salminen, E., Hämäläinen, T. D., & Hännikäinen, M. (2007).
    Automated memory-aware application distribution for multi-processor system-on-chips.
    Journal of Systems Architecture, 53(11), 795-815.e.
    """

    def __init__(self, kpn, platform, trace, representation, random_seed=42, record_statistics=False,
                 initial_temperature=1.0, final_temperature=0.1, temperature_proportionality_constant=.5,
                 radius=3.0, dump_cache=False, chunk_size=10, progress=False, parallel=False, jobs=1):
        """Generates a full mapping for a given platform and KPN application.

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
        :param initial_temperature: Initial temperature for simmulated annealing
        :type initial_temperature: float
        :param final_temperature: Final temperature for simmulated annealing
        :type final_temperature: float
        :param temperature_proportionality_constant: Temperature prop. constant for simmulated annealing
        :type temperature_proportionality_constant: float
        :param radius: Radius for search when moving
        :type radius: int
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
        self.random_mapper = RandomPartialMapper(self.kpn, self.platform, seed=None)
        self.statistics = Statistics(log, len(self.kpn.processes()), record_statistics)
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.max_rejections = len(self.kpn.processes()) * (len(self.platform.processors()) - 1) #R_max = L
        self.p = temperature_proportionality_constant
        self.radius = radius
        self.progress = progress
        self.dump_cache = dump_cache

        if not (1 > self.p > 0):
            log.error(f"Temperature proportionality constant {self.p} not suitable, "
                      f"it should be close to, but smaller than 1 (algorithm probably won't terminate).")

        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not issubclass(type(type(representation)), MappingRepresentation):
            representation = instantiate(representation,kpn,platform)
        self.representation = representation

        self.simulation_manager = SimulationManager(self.representation, trace,jobs, parallel,
                                                    progress,chunk_size,record_statistics)

    def temperature_cooling(self, temperature, iter):
        return self.initial_temperature*self.p**np.floor(iter/self.max_rejections)

    def query_accept(self,time,temperature):
        normalized_probability = 1 / (np.exp(time/(0.5*temperature*self.initial_cost)))
        return normalized_probability

    def move(self, mapping, temperature):
        radius = self.radius
        while(1):
            new_mappings = self.representation._uniformFromBall(mapping,radius,20)
            for m in new_mappings:
                if list(m) != list(mapping):
                    return m
            radius *= 1.1
            if radius > 10000 * self.radius:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")


    def generate_mapping(self):
        """ Generates a full mapping using simulated anealing
        """
        mapping_obj = self.random_mapper.generate_mapping()
        if hasattr(self.representation,'canonical_operations') and not self.representation.canonical_operations:
            mapping = self.representation.toRepresentationNoncanonical(mapping_obj)
        else:
            mapping = self.representation.toRepresentation(mapping_obj)

        last_mapping = mapping
        last_exec_time = self.simulation_manager.simulate([mapping])[0]
        self.initial_cost = last_exec_time
        best_mapping = mapping
        best_exec_time = last_exec_time
        rejections = 0

        iter = 0
        temperature = self.initial_temperature
        if self.progress:
            pbar = tqdm.tqdm(total=self.max_rejections*20)

        while rejections < self.max_rejections:
            temperature = self.temperature_cooling(temperature,iter)
            log.info(f"Current temperature {temperature}")
            mapping = self.move(last_mapping,temperature)
            cur_exec_time = self.simulation_manager.simulate([mapping])[0]
            faster = cur_exec_time < last_exec_time
            if not faster and cur_exec_time != last_exec_time:
                prob = self.query_accept(cur_exec_time - last_exec_time, temperature)
                rand = random.random()
                accept_randomly = prob > rand
            else:
                accept_randomly = False #don't accept if no movement.
            if faster or accept_randomly:
                #accept
                if cur_exec_time < best_exec_time:
                    best_exec_time = cur_exec_time
                    best_mapping = mapping
                last_mapping = mapping
                last_exec_time = cur_exec_time
                rejections = 0
            else:
                #reject
                if temperature <= self.final_temperature:
                    rejections += 1
            iter += 1
            if self.progress:
                pbar.update(1)
        if self.progress:
            pbar.update(self.max_rejections*20-iter)
            pbar.close()

        self.simulation_manager.statistics.log_statistics()
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump('mapping_cache.csv')

        return self.representation.fromRepresentation(best_mapping)

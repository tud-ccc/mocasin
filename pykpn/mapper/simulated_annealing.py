# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import numpy as np
import hydra

from pykpn.util import logging
from pykpn.representations.__init__ import RepresentationType
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.utils import SimulationManager
from pykpn.mapper.utils import Statistics


log = logging.getLogger(__name__)

#TODO: Skip this cause representation object is needed?

class SimulatedAnnealingMapper(object):
    """Generates a full mapping by using a simulated annealing algorithm from:
    Orsila, H., Kangas, T., Salminen, E., Hämäläinen, T. D., & Hännikäinen, M. (2007).
    Automated memory-aware application distribution for multi-processor system-on-chips.
    Journal of Systems Architecture, 53(11), 795-815.e.
    """
    def __init__(self, kpn, platform, config, random_seed, record_statistics, initial_temperature, final_temperature,
                 temperature_proportionality_constant, radius, dump_cache, chunk_size, progress, parallel, jobs):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type config: OmniConf
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
        self.dump_cache = dump_cache

        if not (1 > self.p > 0):
            log.error(f"Temperature proportionality constant {self.p} not suitable, "
                      f"it should be close to, but smaller than 1 (algorithm probably won't terminate).")

        rep_type_str = config['representation']

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform, config)

        self.representation = representation

        self.simulation_manager = SimulationManager(representation, config)

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
        mapping = self.representation.toRepresentation(mapping_obj)

        last_mapping = mapping
        last_exec_time = self.simulation_manager.simulate([mapping])[0]
        self.initial_cost = last_exec_time
        best_mapping = mapping
        best_exec_time = last_exec_time
        rejections = 0

        iter = 0
        temperature = self.initial_temperature
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
        self.simulation_manager.statistics.log_statistics()
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump('mapping_cache.csv')

        return self.representation.fromRepresentation(best_mapping)

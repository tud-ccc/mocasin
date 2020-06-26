# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import numpy as np

from pykpn.util import logging
from pykpn.representations.representations import RepresentationType
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.utils import MappingCache
from pykpn.mapper.utils import Statistics


log = logging.getLogger(__name__)


class SimulatedAnnealingFullMapper(object):
    """Generates a full mapping by using a simulated annealing algorithm from:
    Orsila, H., Kangas, T., Salminen, E., Hämäläinen, T. D., & Hännikäinen, M. (2007).
    Automated memory-aware application distribution for multi-processor system-on-chips.
    Journal of Systems Architecture, 53(11), 795-815.e.
    """
    def __init__(self, kpn,platform,config):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type config: OmniConf
        """
        random.seed(config['random_seed'])
        np.random.seed(config['random_seed'])
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = kpn
        self.platform = platform
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config,seed=None)
        self.statistics = Statistics(log, len(self.kpn.processes()),config['record_statistics'])
        self.initial_temperature = config['initial_temperature']
        self.final_temperature = config['final_temperature']
        self.max_rejections = len(self.kpn.processes()) * (len(self.platform.processors()) - 1) #R_max = L
        self.p = config['temperature_proportionality_constant']
        if not (self.p < 1 and self.p > 0):
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

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation
        self.mapping_cache = MappingCache(representation,config)

    def temperature_cooling(self,temperature,iter):
        return self.initial_temperature*self.p**np.floor(iter/self.max_rejections)

    def query_accept(self,time,temperature):
        normalized_probability = 1 / (np.exp(time/(0.5*temperature*self.initial_cost)))
        return normalized_probability

    def move(self,mapping,temperature):
        radius = self.config['radius']
        while(1):
            new_mappings = self.representation._uniformFromBall(mapping,radius,20)
            for m in new_mappings:
                if list(m) != list(mapping):
                    return m
            radius *= 1.1
            if radius > 10000 * self.config['radius']:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")


    def generate_mapping(self):
        """ Generates a full mapping using simulated anealing
        """
        mapping_obj = self.random_mapper.generate_mapping()
        mapping = self.representation.toRepresentation(mapping_obj)

        last_mapping = mapping
        last_exec_time = self.mapping_cache.evaluate_mapping(mapping)
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
            cur_exec_time = self.mapping_cache.evaluate_mapping(mapping)
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
        self.statistics.log_statistics()
        self.statistics.to_file()

        return self.representation.fromRepresentation(best_mapping)

class TabuSearchFullMapper(object):
    """Generates a full mapping by using a tabu search on the mapping space.

    """
    def __init__(self, kpn,platform,config):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type config: OmniConf
        """
        random.seed(config['random_seed'])
        np.random.seed(config['random_seed'])
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = kpn
        self.platform = platform
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config,seed=None)
        self.max_iterations = config['max_iterations']
        self.iteration_size = config['iteration_size']
        self.tabu_tenure = config['tabu_tenure']
        self.move_set_size = config['move_set_size']
        self.radius = config['radius']
        self.tabu_moves = dict()
        self.statistics = Statistics(log, len(self.kpn.processes()), config['record_statistics'])
        rep_type_str = config['representation']

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation
        self.mapping_cache = MappingCache(representation,config)

    def update_candidate_moves(self,mapping):
        new_mappings = self.representation._uniformFromBall(mapping, self.radius, self.move_set_size)
        new_mappings = map(np.array, new_mappings)
        moves = set([(tuple(new_mapping - np.array(mapping)),
                      self.mapping_cache.evaluate_mapping(new_mapping)) for new_mapping in new_mappings])
        missing = self.move_set_size - len(moves)
        retries = 0
        while missing > 0 and retries < 10:
            new_mappings = self.representation._uniformFromBall(mapping, self.radius, missing)
            moves = moves.union( set([(tuple(np.array(new_mapping)-np.array(mapping)),
                                       self.mapping_cache.evaluate_mapping(new_mapping))
                                      for new_mapping in new_mappings]) )
            missing = self.move_set_size - len(moves)
            retries += 1
        if missing > 0:
            log.warning(f"Running with smaller move list  (by {missing} moves). The radius might be set too small?")
        self.moves = moves

    def move(self, best):
        delete = []
        for move in self.tabu_moves:
            self.tabu_moves[move] -= 1
            if self.tabu_moves[move] <= 0:
                delete.append(move)

        tabu = set(self.tabu_moves.keys())
        for move in delete:
            del self.tabu_moves[move]

        moves_sorted =  sorted(list(self.moves), key = lambda x : x[1])
        if moves_sorted[0][1] < best:
            self.tabu_moves[ moves_sorted[0][0] ] = self.tabu_tenure
            return moves_sorted[0]
        else:
            no_move = np.zeros(len(moves_sorted[0][0]))
            non_tabu = [m for m in moves_sorted if m[0] not in tabu.union(no_move)]
            #no need to re-sort:
            # https://stackoverflow.com/questions/1286167/is-the-order-of-results-coming-from-a-list-comprehension-guaranteed
            if len(non_tabu) > 0:
                self.tabu_moves[non_tabu[0][0]] = self.tabu_tenure
                return non_tabu[0]
            else:
                self.tabu_moves[moves_sorted[0][0]] = self.tabu_tenure
                return moves_sorted[0]



    def diversify(self,mapping):
        new_mappings = self.representation._uniformFromBall(mapping, 3*self.radius, self.move_set_size)
        new_mappings = map(np.array, new_mappings)
        moves = [(tuple(mapping - new_mapping),self.mapping_cache.evaluate_mapping(new_mapping)) for new_mapping in new_mappings]
        return(sorted(moves,key= lambda x : x[1])[0])



    def generate_mapping(self):
        """ Generates a full mapping using gradient descent
        """
        mapping_obj = self.random_mapper.generate_mapping()
        cur_mapping = self.representation.toRepresentation(mapping_obj)

        best_mapping = cur_mapping
        best_exec_time = self.mapping_cache.evaluate_mapping(cur_mapping)
        since_last_improvement = 0

        for iter in range(self.max_iterations):
            while since_last_improvement < self.iteration_size:
                self.update_candidate_moves(cur_mapping)
                move,cur_exec_time = self.move(best_exec_time) #updates tabu set
                cur_mapping = cur_mapping + np.array(move)
                since_last_improvement += 1
                if cur_exec_time < best_exec_time:
                    since_last_improvement = 0
                    best_exec_time = cur_exec_time
                    best_mapping = cur_mapping

            since_last_improvement = 0
            move, cur_exec_time = self.diversify(cur_mapping)
            cur_mapping = cur_mapping + np.array(move)

        self.statistics.log_statistics()
        self.statistics.to_file()

        return self.representation.fromRepresentation(np.array(best_mapping))


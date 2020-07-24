# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import numpy as np

from pykpn.util import logging
from pykpn.representations.representations import RepresentationType
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.utils import SimulationManager
from pykpn.mapper.utils import Statistics


log = logging.getLogger(__name__)


class TabuSearchMapper(object):
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
        self.simulation_manager = SimulationManager(representation, config)

    def update_candidate_moves(self,mapping):
        new_mappings = self.representation._uniformFromBall(mapping, self.radius, self.move_set_size)
        new_mappings = map(np.array, new_mappings)
        moves = set([(tuple(new_mapping - np.array(mapping)),
                      self.simulation_manager.simulate(new_mapping)) for new_mapping in new_mappings])
        missing = self.move_set_size - len(moves)
        retries = 0
        while missing > 0 and retries < 10:
            new_mappings = self.representation._uniformFromBall(mapping, self.radius, missing)
            moves = moves.union( set([(tuple(np.array(new_mapping)-np.array(mapping)),
                                       self.simulation_manager.simulate(new_mapping))
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
        moves = [(tuple(mapping - new_mapping),self.simulation_manager.simulate(new_mapping)) for new_mapping in new_mappings]
        return(sorted(moves,key= lambda x : x[1])[0])



    def generate_mapping(self):
        """ Generates a full mapping using gradient descent
        """
        mapping_obj = self.random_mapper.generate_mapping()
        cur_mapping = self.representation.toRepresentation(mapping_obj)

        best_mapping = cur_mapping
        best_exec_time = self.simulation_manager.simulate(cur_mapping)
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

        self.simulation_manager.statistics.log_statistics()
        self.simulation_manager.statistics.to_file()
        if self.config['dump_cache']:
            self.simulation_manager.dump('mapping_cache.csv')

        return self.representation.fromRepresentation(np.array(best_mapping))


# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import tqdm
from hydra.utils import instantiate
import numpy as np

from mocasin.util import logging
from mocasin.representations import MappingRepresentation
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper.utils import SimulationManager


log = logging.getLogger(__name__)


class TabuSearchMapper(object):
    """Generates a full mapping by using a tabu search on the mapping space."""

    def __init__(
        self,
        graph,
        platform,
        trace,
        representation,
        random_seed=42,
        record_statistics=False,
        max_iterations=10,
        iteration_size=5,
        tabu_tenure=5,
        move_set_size=10,
        radius=2.0,
        dump_cache=False,
        chunk_size=10,
        progress=False,
        parallel=False,
        jobs=1,
    ):
        """Generates a full mapping for a given platform and dataflow application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
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
        :param max_iterations: Maximal number of iterations of tabu search
        :type max_iterations: int
        :param iteration_size: Size (# mappings) of a single iteration
        :type iteration_size: int
        :param tabu_tenure: How long until a tabu move is allowed again?
        :type tabu_tenure: int
        :param move_set_size: Size of the move set considered in an iteration
        :type move_set_size: int
        :param radius: Radius for updating candidate moves
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
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.full_mapper = True  # flag indicating the mapper type
        self.graph = graph
        self.platform = platform
        self.random_mapper = RandomPartialMapper(
            self.graph, self.platform, seed=None
        )
        self.max_iterations = max_iterations
        self.iteration_size = iteration_size
        self.tabu_tenure = tabu_tenure
        self.move_set_size = move_set_size
        self.dump_cache = dump_cache
        self.radius = radius
        self.progress = progress
        self.tabu_moves = dict()

        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not issubclass(type(type(representation)), MappingRepresentation):
            representation = instantiate(representation, graph, platform)
        self.representation = representation

        self.simulation_manager = SimulationManager(
            self.representation,
            trace,
            jobs,
            parallel,
            progress,
            chunk_size,
            record_statistics,
        )

    def update_candidate_moves(self, mapping):
        new_mappings = self.representation._uniformFromBall(
            mapping, self.radius, self.move_set_size
        )
        new_mappings = list(map(np.array, new_mappings))
        sim_results = self.simulation_manager.simulate(new_mappings)
        moves = set(
            zip(
                [
                    tuple(new_mapping - np.array(mapping))
                    for new_mapping in new_mappings
                ],
                sim_results,
            )
        )
        missing = self.move_set_size - len(moves)
        retries = 0
        while missing > 0 and retries < 10:
            new_mappings = self.representation._uniformFromBall(
                mapping, self.radius, missing
            )
            sim_results = self.simulation_manager.simulate(new_mappings)
            new_moves = set(
                zip(
                    [
                        tuple(new_mapping - np.array(mapping))
                        for new_mapping in new_mappings
                    ],
                    sim_results,
                )
            )
            moves = moves.union(new_moves)
            missing = self.move_set_size - len(moves)
            retries += 1
        if missing > 0:
            log.warning(
                f"Running with smaller move list  (by {missing} moves). The radius might be set too small?"
            )
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

        moves_sorted = sorted(list(self.moves), key=lambda x: x[1])
        if moves_sorted[0][1] < best:
            self.tabu_moves[moves_sorted[0][0]] = self.tabu_tenure
            return moves_sorted[0]
        else:
            no_move = np.zeros(len(moves_sorted[0][0]))
            non_tabu = [
                m for m in moves_sorted if m[0] not in tabu.union(no_move)
            ]
            # no need to re-sort:
            # https://stackoverflow.com/questions/1286167/is-the-order-of-results-coming-from-a-list-comprehension-guaranteed
            if len(non_tabu) > 0:
                self.tabu_moves[non_tabu[0][0]] = self.tabu_tenure
                return non_tabu[0]
            else:
                self.tabu_moves[moves_sorted[0][0]] = self.tabu_tenure
                return moves_sorted[0]

    def diversify(self, mapping):
        new_mappings = self.representation._uniformFromBall(
            mapping, 3 * self.radius, self.move_set_size
        )
        new_mappings = list(map(np.array, new_mappings))
        sim_results = self.simulation_manager.simulate(new_mappings)
        moves = set(
            zip(
                [
                    tuple(new_mapping - np.array(mapping))
                    for new_mapping in new_mappings
                ],
                sim_results,
            )
        )
        return sorted(moves, key=lambda x: x[1])[0]

    def generate_mapping(self):
        """Generates a full mapping using gradient descent"""
        mapping_obj = self.random_mapper.generate_mapping()
        if (
            hasattr(self.representation, "canonical_operations")
            and not self.representation.canonical_operations
        ):
            cur_mapping = self.representation.toRepresentationNoncanonical(
                mapping_obj
            )
        else:
            cur_mapping = self.representation.toRepresentation(mapping_obj)

        best_mapping = cur_mapping
        best_exec_time = self.simulation_manager.simulate([cur_mapping])[0]
        since_last_improvement = 0

        if self.progress:
            iterations_range = tqdm.tqdm(range(self.max_iterations))
        else:
            iterations_range = range(self.max_iterations)
        for iter in iterations_range:
            while since_last_improvement < self.iteration_size:
                self.update_candidate_moves(cur_mapping)
                move, cur_exec_time = self.move(
                    best_exec_time
                )  # updates tabu set
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
        if self.dump_cache:
            self.simulation_manager.dump("mapping_cache.csv")

        return self.representation.fromRepresentation(np.array(best_mapping))

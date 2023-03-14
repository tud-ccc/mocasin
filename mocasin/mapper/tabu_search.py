# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Robert Khasanov

import random

import numpy as np
import tqdm

from mocasin.mapper import BaseMapper
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper.utils import SimulationManager, SimulationManagerConfig
from mocasin.util import logging


log = logging.getLogger(__name__)


class TabuSearchMapper(BaseMapper):
    """Generates a full mapping by using a tabu search on the mapping space.

    Args:
        platform (Platform): A platform
        random_seed (int, optional): A random seed for the RNG. Defautls to 42.
        record_statistics (bool, optional): Record statistics on mappings
            evaluated? Defautls to False.
        max_iterations (int, optional): Maximal number of iterations of tabu
            search. Defaults to 10.
        iteration_size (int, optional): Size (# mappings) of a single iteration.
            Defaults to 5.
        tabu_tenure (int, optional): The number of iterations that a move stays
            in the tabu list. Defaults to 5.
        move_set_size (int, optional): The size of the move set considered in an
            iteration. Defaults to 10.
        radius (float, optional): Radius for updating candidate moves.
            Defaults to 2.0.
        dump_cache (bool, optional): Dump the mapping cache? Defaults to False.
        chunk_size (int, optional): Size of chunks for parallel simulation.
            Defaults to 10.
        progress (bool, optional): Display simulation progress visually?
            Defaults to False.
        parallel (bool, optional): Execute simulations in parallel?
            Defaults to False.
        jobs (int, optional): Number of jobs for parallel simulation.
            Defaults to 1.
    """

    def __init__(
        self,
        platform,
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
        super().__init__(platform, full_mapper=True)
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.random_mapper = RandomPartialMapper(self.platform, seed=None)
        self.max_iterations = max_iterations
        self.iteration_size = iteration_size
        self.tabu_tenure = tabu_tenure
        self.move_set_size = move_set_size
        self.dump_cache = dump_cache
        self.radius = radius
        self.progress = progress
        self.tabu_moves = dict()

        # save parameters to simulation manager
        simulation_config = SimulationManagerConfig(
            jobs=jobs,
            parallel=parallel,
            progress=progress,
            chunk_size=chunk_size,
        )
        self._simulation_manager = SimulationManager(
            self.platform, config=simulation_config
        )
        self._record_statistics = record_statistics

    def update_candidate_moves(self, graph, trace, representation, mapping):
        new_mappings = representation._uniformFromBall(
            mapping, self.radius, self.move_set_size
        )
        new_mappings = list(map(np.array, new_mappings))
        sim_results = self._simulation_manager.simulate(
            graph, trace, representation, new_mappings
        )
        sim_exec_times = [x.exec_time for x in sim_results]
        moves = set(
            zip(
                [
                    tuple(new_mapping - np.array(mapping))
                    for new_mapping in new_mappings
                ],
                sim_exec_times,
            )
        )
        missing = self.move_set_size - len(moves)
        retries = 0
        while missing > 0 and retries < 10:
            new_mappings = representation._uniformFromBall(
                mapping, self.radius, missing
            )
            sim_results = self._simulation_manager.simulate(
                graph, trace, representation, new_mappings
            )
            sim_exec_times = [x.exec_time for x in sim_results]
            new_moves = set(
                zip(
                    [
                        tuple(new_mapping - np.array(mapping))
                        for new_mapping in new_mappings
                    ],
                    sim_exec_times,
                )
            )
            moves = moves.union(new_moves)
            missing = self.move_set_size - len(moves)
            retries += 1
        if missing > 0:
            log.warning(
                f"Running with smaller move list  (by {missing} moves). "
                "The radius might be set too small?"
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
            # https://stackoverflow.com/questions/1286167/is-the-order-of-results-coming-from-a-list-comprehension-guaranteed # noqa
            if len(non_tabu) > 0:
                self.tabu_moves[non_tabu[0][0]] = self.tabu_tenure
                return non_tabu[0]
            else:
                self.tabu_moves[moves_sorted[0][0]] = self.tabu_tenure
                return moves_sorted[0]

    def diversify(self, graph, trace, representation, mapping):
        new_mappings = representation._uniformFromBall(
            mapping, 3 * self.radius, self.move_set_size
        )
        new_mappings = list(map(np.array, new_mappings))
        sim_results = self._simulation_manager.simulate(
            graph, trace, representation, new_mappings
        )
        sim_exec_times = [x.exec_time for x in sim_results]
        moves = set(
            zip(
                [
                    tuple(new_mapping - np.array(mapping))
                    for new_mapping in new_mappings
                ],
                sim_exec_times,
            )
        )
        return sorted(moves, key=lambda x: x[1])[0]

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        """Generate a full mapping using gradient descent.

        Args:
            graph (DataflowGraph): a dataflow graph
            trace (TraceGenerator, optional): a trace generator
            representation (MappingRepresentation, optional): a mapping
                representation object
            processors (:obj:`list` of :obj:`Processor`, optional): a list of
                processors to map to.
            partial_mapping (Mapping, optional): a partial mapping to complete

        Returns:
            Mapping: the generated mapping.
        """
        self._simulation_manager.reset_statistics()
        if processors:
            raise NotImplementedError(
                "This mapper does not support `processors` argument"
            )

        if partial_mapping:
            raise NotImplementedError(
                "This mapper does not support `partial_mapping` argument"
            )

        mapping_obj = self.random_mapper.generate_mapping(
            graph, trace=trace, representation=representation
        )
        if (
            hasattr(representation, "canonical_operations")
            and not representation.canonical_operations
        ):
            to_representation_fun = representation.toRepresentationNoncanonical
        else:
            to_representation_fun = representation.toRepresentation
        cur_mapping = to_representation_fun(mapping_obj)

        best_mapping = cur_mapping
        best_simres = self._simulation_manager.simulate(
            graph, trace, representation, [cur_mapping]
        )[0]
        best_exec_time = best_simres.exec_time
        since_last_improvement = 0

        if self.progress:
            iterations_range = tqdm.tqdm(range(self.max_iterations))
        else:
            iterations_range = range(self.max_iterations)
        for iter in iterations_range:
            while since_last_improvement < self.iteration_size:
                self.update_candidate_moves(
                    graph, trace, representation, cur_mapping
                )
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
            move, cur_exec_time = self.diversify(
                graph, trace, representation, cur_mapping
            )
            cur_mapping = cur_mapping + np.array(move)

        self._simulation_manager.statistics.log_statistics()
        if self._record_statistics:
            self._simulation_manager.statistics.to_file()
        if self.dump_cache:
            self._simulation_manager.dump("mapping_cache.csv")

        return representation.fromRepresentation(np.array(best_mapping))

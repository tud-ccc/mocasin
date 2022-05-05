# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Robert Khasanov

import copy
import random
import sys

import numba as nb
import numpy as np
import tqdm

from mocasin.mapper import BaseMapper
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper.utils import SimulationManager, SimulationManagerConfig
from mocasin.util import logging


log = logging.getLogger(__name__)
eps = 1e-8


if sys.version_info[0:2] == (3, 7):

    def _calculate_gammas(grads, old_grads, xs, old_xs):
        gammas = []
        for i in range(len(grads)):
            if np.allclose(grads[i], old_grads[i]):
                gammas.append(np.int64(1))
                continue
            grad_diff = old_grads[i] - grads[i]
            gamma = np.dot(old_xs[i] - xs[i], grad_diff) / np.dot(
                grad_diff, grad_diff
            )
            gammas.append(gamma)
        return gammas

else:
    # Can't use `nopython` because of np.allclose apparently
    # See: https://github.com/numba/numba/pull/6286
    @nb.jit(fastmath=True, parallel=True, cache=True)
    def _calculate_gammas(grads, old_grads, xs, old_xs):
        gammas = []
        for i in nb.prange(len(grads)):
            if np.allclose(grads[i], old_grads[i]):
                gammas.append(np.int64(1))
                continue
            grad_diff = old_grads[i] - grads[i]
            gamma = np.dot(old_xs[i] - xs[i], grad_diff) / np.dot(
                grad_diff, grad_diff
            )
            gammas.append(gamma)
        return gammas


class GradientDescentMapper(BaseMapper):
    # TODO: Update the description of the last two arguments
    """This mapper generates a full mapping by using a gradient descent on the
    mapping space.

    Args:
        platform (Platform): A platform.
        gd_iterations (int, optional): Number of iterations for gradient
            descent. Defaults to 100.
        stepsize (float, optional): Factor to multiply to (Barzilai–Borwein)
            factor gradient in step. Defaults to 2.
        random_seed (int, optional): A random seed for the RNG. Defaults to 42.
        record_statistics (bool, optional): Record statistics on mappings
            evaluated? Defautls to False.
        dump_cache (bool, optional): Dump the mapping cache? Defaults to False.
        chunk_size (int, optional): Size of chunks for parallel simulation.
            Defaults to 10.
        progress (bool, optional): Display simulation progress visually?
            Defaults to False.
        parallel (bool, optional): Execute simulations in parallel?
            Defaults to False.
        jobs (int, optional): Number of jobs for parallel simulation.
            Defaults to 2.
        momentum_decay (float, optional): To be described. Defaults to 0.5.
        parallel_points (int, optional): To be described. Defaults to 5.
    """

    def __init__(
        self,
        platform,
        gd_iterations=100,
        stepsize=2,
        random_seed=42,
        record_statistics=False,
        dump_cache=False,
        chunk_size=10,
        progress=False,
        parallel=False,
        jobs=2,
        momentum_decay=0.5,
        parallel_points=5,
    ):
        super().__init__(platform, full_mapper=True)
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.num_PEs = len(self.platform.processors())
        self.random_mapper = RandomPartialMapper(self.platform, seed=None)
        self.gd_iterations = gd_iterations
        self.stepsize = stepsize
        self.momentum_decay = momentum_decay
        self.parallel_points = parallel_points
        self.dump_cache = dump_cache
        self.progress = progress

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
        mappings = []

        if (
            hasattr(representation, "canonical_operations")
            and not representation.canonical_operations
        ):
            to_representation_fun = representation.toRepresentationNoncanonical
        else:
            to_representation_fun = representation.toRepresentation

        for _ in range(self.parallel_points):
            mapping_obj = self.random_mapper.generate_mapping(
                graph, trace=trace, representation=representation
            )
            m = to_representation_fun(mapping_obj)
            mappings.append(m)

        self.dim = len(mappings[0])
        cur_sim_results = self._simulation_manager.simulate(
            graph, trace, representation, mappings
        )
        cur_exec_times = [x.exec_time for x in cur_sim_results]
        idx = np.argmin(cur_exec_times)
        self.best_mapping = mappings[idx]
        self.best_exec_time = cur_exec_times[idx]
        active_points = list(range(self.parallel_points))
        if self.progress:
            iterations_range = tqdm.tqdm(range(self.gd_iterations))
        else:
            iterations_range = range(self.gd_iterations)
        grads = [0] * self.parallel_points

        # don't check for a loop the first time
        last_mappings = [[np.inf] * self.dim] * self.parallel_points
        log.info(
            f"Starting gradient descent with {self.parallel_points}"
            f" parallel points for {self.gd_iterations} iterations."
            f" Best starting mapping ({idx}): {self.best_exec_time}"
        )

        # main loop
        for _ in iterations_range:
            old_grads = copy.copy(grads)
            for i in active_points:
                grads[i] = self.momentum_decay * old_grads[
                    i
                ] + self.calculate_gradient(
                    graph, trace, representation, mappings[i], cur_exec_times[i]
                )
                log.debug(f"gradient (point {i}): {grads[i]}")

            before_last_mappings = copy.copy(last_mappings)
            last_mappings = copy.copy(mappings)

            # Barzilai–Borwein. Note that before_last_mappings here holds the
            # value for the last mappings still, since we are currently updating
            # the mappigs
            gammas = _calculate_gammas(
                [grads[i] for i in active_points],
                [old_grads[i] for i in active_points],
                [np.array(mappings[i]) for i in active_points],
                [np.array(before_last_mappings[i]) for i in active_points],
            )
            for idx, i in enumerate(active_points):
                # note that gamma has lost the ordering
                # due to that we enumerate
                mappings[i] = (
                    mappings[i] + gammas[idx] * (-grads[i]) * self.stepsize
                )
                log.debug(f"moving mapping {i} to: {mappings[i]}")
                mappings[i] = representation.approximate(np.array(mappings[i]))
                log.debug(f"approximating to: {mappings[i]}")

            cur_sim_results = self._simulation_manager.simulate(
                graph, trace, representation, mappings
            )
            cur_exec_times = [x.exec_time for x in cur_sim_results]
            idx = np.argmin(cur_exec_times)
            log.info(f"{idx} best mapping in batch: {cur_exec_times[idx]}")
            if cur_exec_times[idx] < self.best_exec_time:
                log.info(
                    f"better than old best time ({self.best_exec_time})."
                    " Replacing"
                )
                self.best_exec_time = cur_exec_times[idx]
                self.best_mapping = mappings[idx]

            # remove points on (local) minima or stuck on a loop
            finished_points = []
            for i in active_points:
                # found local minimum
                if np.allclose(grads[i], np.zeros(self.dim)):
                    log.info(f"Found local minimum in {i}. Removing point.")
                    finished_points.append(i)

                # stuck in a loop.
                if np.allclose(mappings[i], last_mappings[i]) or np.allclose(
                    mappings[i], before_last_mappings[i]
                ):
                    log.info(f"Point {i} stuck in a loop. Removing point.")
                    log.debug(
                        f"mapping: {mappings[i]}\n last:"
                        f" {last_mappings[i]}\n"
                        f" before_last: {before_last_mappings[i]}"
                    )
                    finished_points.append(i)

            for i in finished_points:
                if i in active_points:
                    active_points.remove(i)
            if len(active_points) == 0:
                break

        self.best_mapping = np.array(
            representation.approximate(np.array(self.best_mapping))
        )
        self._simulation_manager.statistics.log_statistics()
        if self._record_statistics:
            self._simulation_manager.statistics.to_file()
        if self.dump_cache:
            self._simulation_manager.dump("mapping_cache.csv")

        return representation.fromRepresentation(self.best_mapping)

    def calculate_gradient(
        self, graph, trace, representation, mapping, cur_exec_time
    ):
        grad = np.zeros(self.dim)
        m_plus = []
        m_minus = []
        for i in range(self.dim):
            evec = np.zeros(self.dim)
            evec[i] = 1
            m_plus.append(mapping + evec)
            m_minus.append(mapping - evec)

        sim_results = self._simulation_manager.simulate(
            graph, trace, representation, m_plus + m_minus
        )
        exec_times = [x.exec_time for x in sim_results]

        for i in range(self.dim):
            diff_plus = exec_times[i] - cur_exec_time
            #  because of the -h in the denominator of the difference quotient
            diff_minus = cur_exec_time - exec_times[i + self.dim]
            grad[i] = (diff_plus + diff_minus) / 2
        return grad

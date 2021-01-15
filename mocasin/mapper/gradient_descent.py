# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
from hydra.utils import instantiate
import numpy as np
import numba as nb
import tqdm
import copy

from mocasin.util import logging
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper.utils import SimulationManager
from mocasin.mapper.utils import Statistics
from mocasin.representations import MappingRepresentation

log = logging.getLogger(__name__)
eps = 1e-8

import sys

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
    # can't use `nopython` because of np.allclose apparently
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


class GradientDescentMapper(object):
    """Generates a full mapping by using a gradient descent on the mapping space."""

    def __init__(
        self,
        graph,
        platform,
        trace,
        representation,
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
        """Generates a full mapping for a given platform and dataflow application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param gd_iterations: Number of iterations for gradient descent
        :type gd_iterations: int
        :param stepsize: Factor to multiply to (Barzilai–Borwein) factor gradient in step
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
        self.full_mapper = True  # flag indicating the mapper type
        self.graph = graph
        self.platform = platform
        self.num_PEs = len(platform.processors())
        self.random_mapper = RandomPartialMapper(
            self.graph, self.platform, seed=None
        )
        self.gd_iterations = gd_iterations
        self.stepsize = stepsize
        self.momentum_decay = momentum_decay
        self.parallel_points = parallel_points
        self.dump_cache = dump_cache
        self.progress = progress
        self.statistics = Statistics(
            log, len(self.graph.processes()), record_statistics
        )

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

    def generate_mapping(self):
        """Generates a full mapping using gradient descent"""
        mappings = []
        for _ in range(self.parallel_points):
            mapping_obj = self.random_mapper.generate_mapping()
            if (
                hasattr(self.representation, "canonical_operations")
                and not self.representation.canonical_operations
            ):
                m = self.representation.toRepresentationNoncanonical(
                    mapping_obj
                )
            else:
                m = self.representation.toRepresentation(mapping_obj)
            mappings.append(m)

        self.dim = len(mappings[0])
        cur_exec_times = self.simulation_manager.simulate(mappings)
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
                ] + self.calculate_gradient(mappings[i], cur_exec_times[i])
                log.debug(f"gradient (point {i}): {grads[i]}")

            before_last_mappings = copy.copy(last_mappings)
            last_mappings = copy.copy(mappings)

            # Barzilai–Borwein. Note that before_last_mappings here holds the value for
            # the last mappings still, since we are currently updating the mappigs
            gammas = _calculate_gammas(
                [grads[i] for i in active_points],
                [old_grads[i] for i in active_points],
                [np.array(mappings[i]) for i in active_points],
                [np.array(before_last_mappings[i]) for i in active_points],
            )
            for idx, i in enumerate(active_points):
                # note that gamma has lost the ordering, which is why we enumerate
                mappings[i] = (
                    mappings[i] + gammas[idx] * (-grads[i]) * self.stepsize
                )
                log.debug(f"moving mapping {i} to: {mappings[i]}")
                mappings[i] = self.representation.approximate(
                    np.array(mappings[i])
                )
                log.debug(f"approximating to: {mappings[i]}")

            cur_exec_times = self.simulation_manager.simulate(mappings)
            idx = np.argmin(cur_exec_times)
            log.info(f"{idx} best mapping in batch: {cur_exec_times[idx]}")
            if cur_exec_times[idx] < self.best_exec_time:
                log.info(
                    f"better than old best time ({self.best_exec_time}). Replacing"
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
            self.representation.approximate(np.array(self.best_mapping))
        )
        self.simulation_manager.statistics.log_statistics()
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump("mapping_cache.csv")

        return self.representation.fromRepresentation(self.best_mapping)

    def calculate_gradient(self, mapping, cur_exec_time):
        grad = np.zeros(self.dim)
        m_plus = []
        m_minus = []
        for i in range(self.dim):
            evec = np.zeros(self.dim)
            evec[i] = 1
            m_plus.append(mapping + evec)
            m_minus.append(mapping - evec)

        exec_times = self.simulation_manager.simulate(m_plus + m_minus)

        for i in range(self.dim):
            diff_plus = exec_times[i] - cur_exec_time
            #  because of the -h in the denominator of the difference quotient
            diff_minus = cur_exec_time - exec_times[i + self.dim]
            grad[i] = (diff_plus + diff_minus) / 2
        return grad

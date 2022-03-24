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


class SimulatedAnnealingMapper(BaseMapper):
    """Generates a full mapping by using a simulated annealing algorithm from:
    Orsila, H., Kangas, T., Salminen, E., Hämäläinen, T. D., & Hännikäinen, M.
    (2007). Automated memory-aware application distribution for multi-processor
    system-on-chips. Journal of Systems Architecture, 53(11), 795-815.e.
    """

    def __init__(
        self,
        platform,
        random_seed=42,
        record_statistics=False,
        initial_temperature=1.0,
        final_temperature=0.1,
        temperature_proportionality_constant=0.5,
        radius=3.0,
        dump_cache=False,
        chunk_size=10,
        progress=False,
        parallel=False,
        jobs=1,
    ):
        """Generate a full mapping for a given platform and dataflow application.

        :param platform: a platform
        :type platform: Platform
        :param random_seed: A random seed for the RNG
        :type random_seed: int
        :param initial_temperature: Initial temperature for simmulated annealing
        :type initial_temperature: float
        :param final_temperature: Final temperature for simmulated annealing
        :type final_temperature: float
        :param temperature_proportionality_constant: Temperature prop. constanti
            for simmulated annealing
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
        super().__init__(platform, full_mapper=True)
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.random_mapper = RandomPartialMapper(self.platform, seed=None)
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.p = temperature_proportionality_constant
        self.radius = radius
        self.progress = progress
        self.dump_cache = dump_cache

        if not (1 > self.p > 0):
            log.error(
                f"Temperature proportionality constant {self.p} not suitable, "
                f"it should be close to, but smaller than 1 (algorithm probably"
                " won't terminate)."
            )

        # save parameters to simulation manager
        self._simulation_config = SimulationManagerConfig(
            jobs=jobs,
            parallel=parallel,
            progress=progress,
            chunk_size=chunk_size,
            record_statistics=record_statistics,
        )

    def temperature_cooling(self, temperature, iteration, max_rejections):
        return self.initial_temperature * self.p ** np.floor(
            iteration / max_rejections
        )

    def query_accept(self, time, temperature):
        with np.errstate(over="raise"):
            try:
                normalized_probability = 1 / (
                    np.exp(time / (0.5 * temperature * self.initial_cost))
                )
            except FloatingPointError:
                normalized_probability = 0

        return normalized_probability

    def move(self, representation, mapping, temperature):
        radius = self.radius
        while 1:
            new_mappings = representation._uniformFromBall(mapping, radius, 20)
            for m in new_mappings:
                if list(m) != list(mapping):
                    return m
            radius *= 1.1
            if radius > 10000 * self.radius:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        """Generate a full mapping using simulated annealing.

        Args:
        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param processors: list of processors to map to.
        :type processors: a list[Processor]
        :param partial_mapping: a partial mapping to complete
        :type partial_mapping: Mapping

        """
        # R_max = L
        max_rejections = len(graph.processes()) * (
            len(self.platform.processors()) - 1
        )
        self.simulation_manager = SimulationManager(
            representation, trace, config=self._simulation_config
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
        mapping = to_representation_fun(mapping_obj)

        last_mapping = mapping
        last_simres = self.simulation_manager.simulate([mapping])[0]
        last_exec_time = last_simres.exec_time
        self.initial_cost = last_exec_time
        best_mapping = mapping
        best_exec_time = last_exec_time
        rejections = 0

        iteration = 0
        temperature = self.initial_temperature
        if self.progress:
            pbar = tqdm.tqdm(total=max_rejections * 20)

        while rejections < max_rejections:
            temperature = self.temperature_cooling(
                temperature, iteration, max_rejections
            )
            log.info(f"Current temperature {temperature}")
            mapping = self.move(representation, last_mapping, temperature)
            cur_simres = self.simulation_manager.simulate([mapping])[0]
            cur_exec_time = cur_simres.exec_time
            faster = cur_exec_time < last_exec_time
            if not faster and cur_exec_time != last_exec_time:
                prob = self.query_accept(
                    cur_exec_time - last_exec_time, temperature
                )
                rand = random.random()
                accept_randomly = prob > rand
            else:
                accept_randomly = False  # don't accept if no movement.
            if faster or accept_randomly:
                # accept
                if cur_exec_time < best_exec_time:
                    best_exec_time = cur_exec_time
                    best_mapping = mapping
                last_mapping = mapping
                last_exec_time = cur_exec_time
                log.info(f"Rejected ({rejections})")
                rejections = 0
            else:
                # reject
                if temperature <= self.final_temperature:
                    rejections += 1
            iteration += 1
            if self.progress:
                pbar.update(1)
        if self.progress:
            pbar.update(max_rejections * 20 - iteration)
            pbar.close()

        self.simulation_manager.statistics.log_statistics()
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump("mapping_cache.csv")

        return representation.fromRepresentation(best_mapping)

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

    Args:
        platform (Platform): A platform
        random_seed (int, optional): A random seed for the RNG. Defautls to 42.
        record_statistics (bool, optional): Record statistics on mappings
            evaluated? Defautls to False.
        initial_temperature (float, optional): Initial temperature for
            simmulated annealing. Defaults to 1.0.
        final_temperature (float, optional): Final temperature for simmulated
            annealing. Defaults to 0.1.
        temperature_proportionality_constant (float, optional): Temperature
            prop. constant for simmulated annealing. Defaults to 0.5.
        radius (float, optional): The radius for searching when moving.
            Defaults to 3.0.
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
        # R_max = L
        max_rejections = len(graph.processes()) * (
            len(self.platform.processors()) - 1
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
        last_simres = self._simulation_manager.simulate(
            graph, trace, representation, [mapping]
        )[0]
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
            cur_simres = self._simulation_manager.simulate(
                graph, trace, representation, [mapping]
            )[0]
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

        self._simulation_manager.statistics.log_statistics()
        if self._record_statistics:
            self._simulation_manager.statistics.to_file()
        if self.dump_cache:
            self._simulation_manager.dump("mapping_cache.csv")

        return representation.fromRepresentation(best_mapping)

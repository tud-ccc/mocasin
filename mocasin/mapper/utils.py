# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Felix Teweleit, Robert Khasanov

import csv
from dataclasses import dataclass
import multiprocessing as mp
import os
import pickle
from time import process_time

import cloudpickle
import h5py
import hydra
from hydra.core.hydra_config import HydraConfig
import numpy as np
import tqdm

from mocasin.common.mapping import Mapping
from mocasin.simulate import DataflowSimulation
from mocasin.util.logging import getLogger

log = getLogger(__name__)


class Statistics(object):
    """Simulation Manager Statistics.

    Args:
        logger (Logger): a logger
    """

    def __init__(self, logger):
        self._log = logger
        self.reset()

    def reset(self):
        self._mappings_cached = 0
        self._mappings_evaluated = 0
        self._simulation_time = 0
        self._representation_time = 0
        self._representation_init_time = 0

    def mappings_cached(self, num=1):
        self._mappings_cached += num

    def mapping_evaluated(self, simulation_time):
        self._mappings_evaluated += 1
        self._simulation_time += simulation_time

    def add_offset(self, time):
        self._simulation_time += time

    def add_rep_time(self, time):
        self._representation_time += time

    def set_rep_init_time(self, time):
        self._representation_init_time = time

    def log_statistics(self):
        self._log.info(f"Mappings cached: {self._mappings_cached}")
        self._log.info(f"Mappings evaluated: {self._mappings_evaluated}")
        self._log.info(f"Time spent simulating: {self._simulation_time}")

    def to_file(self):
        with open("statistics.txt", "x") as file:
            file.write(f"Mappings cached: {self._mappings_cached}\n")
            file.write(f"Mappings evaluated: {self._mappings_evaluated}\n")
            file.write(f"Time spent simulating: {self._simulation_time}\n")
            file.write(f"Representation time: {self._representation_time}\n")
            file.write(
                "Representation initialization time:"
                f" {self._representation_init_time}\n"
            )


@dataclass
class SimulationManagerConfig:
    """A configuration for simulation manager."""

    jobs: int = 1
    parallel: bool = False
    progress: bool = False
    chunk_size: int = 10


class SimulationManager:
    def __init__(self, platform, config=None):
        if not config:
            config = SimulationManagerConfig()
        self.config = config
        self.platform = platform
        self.statistics = Statistics(log)
        self._cache = {}

    def lookup(self, graph, mapping):
        """Look up the results from the cache."""
        if graph not in self._cache:
            self._cache.update({graph: {}})

        if mapping not in self._cache[graph]:
            self._cache[graph].update({mapping: None})
            return False

        return self._cache[graph][mapping]

    def add_mapping_result(self, graph, mapping, sim_res):
        """Save the simulation results in the cache."""
        assert graph in self._cache
        self._cache[graph][mapping] = sim_res

    def reset_statistics(self):
        self.statistics.reset()

    def _prepare_mappings_tuples(self, representation, input_mappings):
        if isinstance(input_mappings[0], Mapping):
            tup = [
                tuple(representation.toRepresentation(m))
                for m in input_mappings
            ]
            mappings = input_mappings
        else:  # assume mappings are list type then
            # transform into tuples
            tup = [
                tuple(representation.approximate(np.array(m)))
                for m in input_mappings
            ]
            mappings = [representation.fromRepresentation(m) for m in tup]
        return mappings, tup

    def _prepare_simulations(self, graph, trace, mappings, lookups):
        """Prepare arguments for simulations."""
        # create a list of simulations to be run.
        # each element is a tuple (simulation, hydra_configuration)
        simulations = []
        # Logging are not configured in the spawned processes on mac OS.
        # As a workaround, suggested in
        # https://github.com/facebookresearch/hydra/issues/1005
        # we pass the hydra configuration to the child processes
        cfg_pickled = None
        if HydraConfig.initialized():
            config = HydraConfig.get()
            cfg_pickled = cloudpickle.dumps(config)
        for i, mapping in enumerate(mappings):
            # skip if this particular mapping is in the cache
            if lookups[i]:
                continue

            simulation = DataflowSimulation(
                self.platform, graph, mapping, trace
            )

            simulations.append((simulation, cfg_pickled))
        return simulations

    def _run_simulations(self, simulations):
        """Perform simulations."""
        if self.config.parallel and len(simulations) > self.config.chunk_size:
            # since mappings are simulated in parallel, whole simulation time
            # is added later as offset
            for _ in simulations:
                self.statistics.mapping_evaluated(0)

            # run the simulations in parallel
            with mp.Pool(processes=self.config.jobs) as pool:
                to_simulate = pool.imap(
                    run_simulation_logger_wrapper,
                    simulations,
                    chunksize=self.config.chunk_size,
                )
                if self.config.progress:
                    to_simulate = tqdm.tqdm(
                        to_simulate,
                        total=len(simulations),
                    )
                simulated = list(to_simulate)
                time = sum([s[1] for s in simulated])
                simulated = [s[0] for s in simulated]
                self.statistics.add_offset(time)
        else:
            simulated = []
            # run the simulations sequentially
            for s in simulations:
                s, time = run_simulation(s[0])
                simulated.append(s)
                self.statistics.mapping_evaluated(time)
        return simulated

    def _append_mapping_metadata(self, mapping, sim_res):
        # save execution time and energy in ms and mJ, respectively
        mapping.metadata.exec_time = sim_res.exec_time / 1000000000.0
        mapping.metadata.energy = None
        if sim_res.dynamic_energy is not None:
            mapping.metadata.energy = sim_res.dynamic_energy / 1000000000.0

    def _store_simulation_results(
        self, graph, mappings, tup, lookups, simulated, update_metadata
    ):
        sim_results = []
        sim_iter = iter(simulated)
        for i, mapping in enumerate(mappings):
            sim_lookup = lookups[i]
            if sim_lookup:
                sim_res = sim_lookup
            else:
                s = next(sim_iter)
                sim_res = s.result
                self.add_mapping_result(graph, tup[i], sim_res)
            sim_results.append(sim_res)
            if update_metadata:
                self._append_mapping_metadata(mapping, sim_res)

        return sim_results

    def simulate(
        self, graph, trace, representation, input_mappings, update_metadata=True
    ):
        """Simulate multiple mappings.

        Args:
            input_mappings: input mappings

        Returns:
            list of the objects of the class `SimulationResult`. The length of
            the list is equal to the length of `input_mappings`.
        """
        # check inputs
        if len(input_mappings) == 0:
            log.warning("Trying to simulate an empty mapping list")
            return []

        self.statistics.set_rep_init_time(representation.init_time)

        time = process_time()
        mappings, tup = self._prepare_mappings_tuples(
            representation, input_mappings
        )
        self.statistics.add_rep_time(process_time() - time)

        # first look up as many as possible:
        lookups = [self.lookup(graph, t) for t in tup]
        num = len([m for m in lookups if m])
        log.info(f"{num} from cache.")
        self.statistics.mappings_cached(num)

        # if all were already cached, return them
        if num == len(tup):
            for m, sim_res in zip(mappings, lookups):
                self._append_mapping_metadata(m, sim_res)
            return lookups

        # Prepare simulation arguments
        simulations = self._prepare_simulations(graph, trace, mappings, lookups)

        # Run simulations itself
        simulated = self._run_simulations(simulations)

        # Collect the simulation results and store them
        sim_results = self._store_simulation_results(
            graph, mappings, tup, lookups, simulated, update_metadata
        )
        return sim_results

    def dump(self, filename):
        # TODO: Use MappingTableWriter
        log.info(f"dumping cache to {filename}")
        with open(filename, "x") as file:
            file.write("mapping,runtime\n")
            for mapping in self._cache:
                file.write(
                    f"\"{str(mapping).replace('(','').replace(')','')}\","
                    f"{self._cache[mapping]}\n"
                )
        # TODO: Use a separate method to dump this data
        filename = filename.replace("csv", "h5")
        log.info(f"dumping cache to {filename}")
        f = h5py.File(filename, "w")
        for i, mapping in enumerate(self._cache):
            f.create_dataset(str(i), data=np.array(mapping), compression="gzip")
            f[str(i)].attrs["runtime"] = self._cache[mapping]
        f.close()
        log.info("cache dumped.")


def run_simulation_logger_wrapper(arguments):
    """Simulation wrapper with logger settings.

    Logging are not configured in the spawned processes on mac OS.
    As a workaround, suggested in
    https://github.com/facebookresearch/hydra/issues/1005
    we pass the hydra configuration from the main process.
    """
    simulation, cfg_pickled = arguments
    if cfg_pickled:
        config = pickle.loads(cfg_pickled)
        hydra.core.utils.configure_log(config.job_logging, config.verbose)
    return run_simulation(simulation)


def run_simulation(simulation):
    with simulation:
        start_time = process_time()
        simulation.run()
        time = process_time() - start_time
    return simulation, time


def statistics_parser(dir):
    results = {}
    with open(os.path.join(dir, "statistics.txt"), "r") as f:
        results["processes_in_task"] = int(
            f.readline().replace("Processes: ", "")
        )
        results["mappings_cached"] = int(
            f.readline().replace("Mappings cached: ", "")
        )
        results["mappings_evaluated"] = int(
            f.readline().replace("Mappings evaluated: ", "")
        )
        results["time_simulating"] = float(
            f.readline().replace("Time spent simulating: ", "")
        )
        results["time_representation"] = float(
            f.readline().replace("Representation time: ", "")
        )
        results["representation_init_time"] = float(
            f.readline().replace("Representation initialization time: ", "")
        )
    return results, list(results.keys())


def best_time_parser(dir):
    try:
        with open(os.path.join(dir, "best_time.txt"), "r") as f:
            exec_time = float(f.readline())
        results = {"best_mapping_time": exec_time}
        return results, list(results.keys())
    except FileNotFoundError:
        return {}, []


def evolutionary_logbook_parser(dir):
    try:
        with open(os.path.join(dir, "evolutionary_logbook.txt"), "r") as f:
            results = []
            reader = csv.DictReader(f, dialect="excel-tab")
            for row in reader:
                row_mod = {}
                for key in row:
                    row_mod[
                        "genetic-" + key.replace(" ", "").replace("\t", "")
                    ] = (row[key].replace(" ", "").replace("\t", ""))
                results.append(row_mod)
            return results, list(results[0].keys())
    except FileNotFoundError:
        return {}, []


def cache_dump_csv_parser(dir):
    try:
        with open(os.path.join(dir, "mapping_cache.csv"), "r") as f:
            reader = csv.DictReader(f)
            keys = reader.fieldnames
            results = []
            for row in reader:
                results.append(row)
        return results, keys
    except FileNotFoundError:
        return {}, []


def cache_dump_h5_parser(dir):
    try:
        with h5py.File(os.path.join(dir, "mapping_cache.h5"), "r") as f:
            results = []
            keys = ["mapping", "runtime"]
            for m in f:
                mapping = np.array(f[m])
                runtime = f[m].attrs["runtime"]
                results.append({"mapping": mapping, "runtime": runtime})
        return results, keys
    except FileNotFoundError:
        return {}, []

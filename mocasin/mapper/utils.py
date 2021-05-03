# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Felix Teweleit, Robert Khasanov

import csv
import h5py
import multiprocessing as mp
import numpy as np
import os
from time import process_time

from mocasin.common.mapping import Mapping
from mocasin.simulate import DataflowSimulation

from mocasin.util.logging import getLogger

log = getLogger(__name__)


class Statistics(object):
    def __init__(self, logger, process_amount, record):
        self._log = logger
        self.record = record
        self._processes = process_amount
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
        self._log.info(f"Amount of processes in task:  {self._processes}")
        self._log.info(f"Mappings cached: {self._mappings_cached}")
        self._log.info(f"Mappings evaluated: {self._mappings_evaluated}")
        self._log.info(f"Time spent simulating: {self._simulation_time}")

    def to_file(self):
        if not self.record:
            return
        file = open("statistics.txt", "x")
        file.write("Processes: " + str(self._processes) + "\n")
        file.write("Mappings cached: " + str(self._mappings_cached) + "\n")
        file.write(
            "Mappings evaluated: " + str(self._mappings_evaluated) + "\n"
        )
        file.write(
            "Time spent simulating: " + str(self._simulation_time) + "\n"
        )
        file.write(
            "Representation time: " + str(self._representation_time) + "\n"
        )
        file.write(
            "Representation initialization time: "
            + str(self._representation_init_time)
            + "\n"
        )
        file.close()


class SimulationManager(object):
    def __init__(
        self,
        representation,
        trace,
        jobs=1,
        parallel=False,
        progress=False,
        chunk_size=10,
        record_statistics=False,
    ):
        self._cache = {}
        self.representation = representation
        self.graph = representation.graph
        self.platform = representation.platform
        self.statistics = Statistics(
            log, len(self.graph.processes()), record_statistics
        )
        self.statistics.set_rep_init_time(representation.init_time)
        self.jobs = jobs
        self.trace = trace
        self.parallel = parallel
        self.progress = progress
        self.chunk_size = chunk_size

    def lookup(self, mapping):
        """Look up the results from the cache."""
        if mapping not in self._cache:
            self._cache.update({mapping: None})
            return False

        return self._cache[mapping]

    def add_mapping_result(self, mapping, sim_res):
        """Save the simulation results in the cache."""
        self._cache[mapping] = sim_res

    def simulate(self, input_mappings):
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

        time = process_time()
        if isinstance(input_mappings[0], Mapping):
            tup = [
                tuple(self.representation.toRepresentation(m))
                for m in input_mappings
            ]
            mappings = input_mappings
        else:  # assume mappings are list type then
            # transform into tuples
            tup = [
                tuple(self.representation.approximate(np.array(m)))
                for m in input_mappings
            ]
            mappings = [self.representation.fromRepresentation(m) for m in tup]
        self.statistics.add_rep_time(process_time() - time)

        # first look up as many as possible:
        lookups = [self.lookup(t) for t in tup]
        num = len([m for m in lookups if m])
        log.info(f"{num} from cache.")
        self.statistics.mappings_cached(num)

        # if all were already cached, return them
        if num == len(tup):
            return lookups

        # create a list of simulations to be run
        simulations = []
        for i, mapping in enumerate(mappings):
            # skip if this particular mapping is in the cache
            if lookups[i]:
                continue

            simulation = DataflowSimulation(
                self.platform, self.graph, mapping, self.trace
            )

            simulations.append(simulation)

        if self.parallel and len(simulations) > self.chunk_size:
            # since mappings are simulated in parallel, whole simulation time
            # is added later as offset
            for _ in simulations:
                self.statistics.mapping_evaluated(0)

            # run the simulations in parallel
            with mp.Pool(processes=self.jobs) as pool:
                to_simulate = pool.imap(
                    run_simulation,
                    simulations,
                    chunksize=self.chunk_size,
                )
                if self.progress:
                    import tqdm

                    to_simulate = tqdm.tqdm(
                        to_simulate,
                        total=len(mappings),
                    )
                simulated = list(to_simulate)
                time = sum([s[1] for s in simulated])
                simulated = [s[0] for s in simulated]
                self.statistics.add_offset(time)
        else:
            simulated = []
            # run the simulations sequentially
            for s in simulations:
                s, time = run_simulation(s)
                simulated.append(s)
                self.statistics.mapping_evaluated(time)

        # Collect the simulation results and store them
        sim_results = []
        sim_iter = iter(simulated)
        for i, mapping in enumerate(mappings):
            sim_res = lookups[i]
            if sim_res:
                sim_results.append(sim_res)
            else:
                s = next(sim_iter)
                sim_results.append(s.result)
                self.add_mapping_result(tup[i], sim_res)
        return sim_results

    def append_mapping_metadata(self, mapping):
        """Append metadata to the mapping object such as execution_time, energy.

        Args:
            mapping (Mapping): a mapping object.
        """
        sim_res = self.simulate([mapping])[0]
        # save execution time and energy in ms and mJ, respectively
        mapping.metadata.exec_time = sim_res.exec_time / 1000000000.0
        mapping.metadata.energy = None
        if sim_res.dynamic_energy is not None:
            mapping.metadata.energy = sim_res.dynamic_energy / 1000000000.0

    def dump(self, filename):
        log.info(f"dumping cache to {filename}")
        file = open(filename, "x")
        file.write("mapping,runtime\n")
        for mapping in self._cache:
            file.write(
                f"\"{str(mapping).replace('(','').replace(')','')}\",{self._cache[mapping]}\n"
            )
        file.close()

        filename = filename.replace("csv", "h5")
        log.info(f"dumping cache to {filename}")
        f = h5py.File(filename, "w")
        for i, mapping in enumerate(self._cache):
            f.create_dataset(str(i), data=np.array(mapping), compression="gzip")
            f[str(i)].attrs["runtime"] = self._cache[mapping]
        f.close()
        log.info("cache dumped.")


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

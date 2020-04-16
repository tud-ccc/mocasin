# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Felix Teweleit
import timeit
import simpy
import hydra
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
import numpy as np

from pykpn.util.logging import getLogger
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

    def mapping_cached(self):
        self._mappings_cached += 1

    def mapping_evaluated(self, simulation_time):
        self._mappings_evaluated += 1
        self._simulation_time += simulation_time

    def add_offset(self, time):
        self._simulation_time += time

    def log_statistics(self):
        self._log.info(f"Amount of processes in task:  {self._processes}")
        self._log.info(f"Mappings cached: {self._mappings_cached}")
        self._log.info(f"Mappings evaluated: {self._mappings_evaluated}")
        self._log.info(f"Time spent simulating: {self._simulation_time}")

    def to_file(self):
        if not self.record:
            return
        file = open('statistics.txt', 'x')
        file.write("Processes: " + str(self._processes) + "\n")
        file.write("Mappings cached: " + str(self._mappings_cached) + "\n")
        file.write("Mappings evaluated: " + str(self._mappings_evaluated) + "\n")
        file.write("Time spent simulating: " + str(self._simulation_time) + "\n")
        file.write("Representation time: " + str(self._representation_time) + "\n")
        file.close()


class MappingCache(object):

    def __init__(self,representation,config):
        self._cache = {}
        self.representation = representation
        self.config = config
        self.kpn = representation.kpn
        self.platform = representation.platform
        self.statistics = Statistics(log, len(self.kpn.processes()), config['record_statistics'])
        self._last_added = None

    def lookup(self, mapping):
        if mapping not in self._cache:
            self._cache.update({mapping : None})
            self._last_added = mapping
            return False

        return self._cache[mapping]

    def add_time(self, time):
        if not self._last_added:
            raise RuntimeError("Cache mapping before adding a simulation time!")

        self._cache[self._last_added] = time
        self._last_added = None

    def evaluate_mapping(self,mapping):
        tup = tuple(self.representation.approximate(np.array(mapping)))
        log.info(f"evaluating mapping: {tup}...")

        runtime = self.lookup(tup)
        if runtime:
            log.info(f"... from cache: {runtime}")
            self.statistics.mapping_cached()
            return runtime
        else:
            time = timeit.default_timer()
            m_obj = self.representation.fromRepresentation(np.array(tup))
            trace = hydra.utils.instantiate(self.config['trace'])
            env = simpy.Environment()
            app = RuntimeKpnApplication(name=self.kpn.name,
                                        kpn_graph=self.kpn,
                                        mapping=m_obj,
                                        trace_generator=trace,
                                        env=env,)
            system = RuntimeSystem(self.platform, [app], env)
            system.simulate()
            exec_time = float(env.now) / 1000000000.0
            self.add_time(exec_time)
            time = timeit.default_timer() - time
            self.statistics.mapping_evaluated(time)
            log.info(f"... from simulation: {exec_time}.")
            return exec_time


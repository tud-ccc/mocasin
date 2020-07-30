# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Felix Teweleit

import timeit
import simpy
import hydra
import numpy as np


from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem

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
    def __init__(self, representation, trace_generator, record_statistics=False):
        self._cache = {}
        self.representation = representation
        self.trace_generator = trace_generator
        self.kpn = representation.kpn
        self.platform = representation.platform
        self.statistics = Statistics(log, len(self.kpn.processes()), record_statistics)
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
            env = simpy.Environment()
            system = RuntimeSystem(self.platform, env)
            app = RuntimeKpnApplication(name=self.kpn.name,
                                        kpn_graph=self.kpn,
                                        mapping=m_obj,
                                        trace_generator=self.trace_generator,
                                        system=system,)
            system.simulate()
            exec_time = float(env.now) / 1000000000.0
            self.add_time(exec_time)
            time = timeit.default_timer() - time
            self.statistics.mapping_evaluated(time)
            log.info(f"... from simulation: {exec_time}.")
            self.trace_generator.reset()
            return exec_time


class ApplicationContext(object):
    def __init__(self, name=None, kpn=None, mapping=None, trace_reader=None,
                 start_time=None):
        self.name = name
        self.kpn = kpn
        self.mapping = mapping
        self.trace_reader = trace_reader
        self.start_time = start_time


class SimulationContext(object):
    def __init__(self, platform=None, app_contexts=None):
        self.platform = platform
        if app_contexts is None:
            self.app_contexts = []
        else:
            self.app_contexts = app_contexts
        self.exec_time = None


def run_simulation(sim_context):
    # Create simulation environment
    env = simpy.Environment()

    # Create the system
    system = RuntimeSystem(sim_context.platform, env)

    # create the applications
    for ac in sim_context.app_contexts:
        app = RuntimeKpnApplication(ac.name, ac.kpn, ac.mapping,
                                    ac.trace_reader, system)

    # run the simulation
    system.simulate()
    system.check_errors()

    sim_context.exec_time = env.now

    return sim_context


class DerivedPrimitive:
    """Representing communication from one single processor to another one.

    This class represents a further abstraction from the common pykpn primitive and
    only covers the communication between one specific source and one specific sink
    processor.

    Attributes:
        name (string): Name of the primitive. A combination of source and target name.
        source (pykpn.common.platform.Processor): The source processor, capable of sending data
            via this primitive.
        sink (pykpn.common.platform.Processor): The sink processor, which should receive the data
            send via the primitive.
        write_cost (int): The amount of ticks it costs to write via this primitive.
        read_cost (int): The amount if ticks it costs to read from this primitive.
        cost (int): Complete static cost for one token, send via this primitive.
        ref_primitive (pykpn.common.platform.Primitive): The pykpn primitive, this primitive was
            derived from.
    """
    def __init__(self, source, sink, ref_prim):
        """Constructor of a derived primitive

        Args:
            source (pykpn.common.platform.Processor): The source processor.
            target (pykpn.common.platform.Processor): The target processor.
            ref_prim (pykpn.commom.platform.Primitive): The pykpn primitive this primitive was
                derived from.
        """
        self.name = "prim_{}_{}".format(source.name, sink.name)

        self.source = source
        self.sink = sink

        self.write_cost = ref_prim.static_produce_costs(source)
        self.read_cost = ref_prim.static_consume_costs(sink)
        self.cost = self.write_cost + self.read_cost

        self.ref_primitive = ref_prim


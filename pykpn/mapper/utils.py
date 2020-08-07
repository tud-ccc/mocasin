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
from pykpn.common.mapping import Mapping

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
        self._representation_init_time = 0

    def mappings_cached(self,num=1):
        self._mappings_cached += num

    def mapping_evaluated(self, simulation_time):
        self._mappings_evaluated += 1
        self._simulation_time += simulation_time

    def add_offset(self, time):
        self._simulation_time += time

    def add_rep_time(self,time):
        self._representation_time += time

    def set_rep_init_time(self,time):
        self._representation_init_time = time

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
        file.write("Representation initialization time: " + str(self._representation_init_time) + "\n")
        file.close()

class SimulationManager(object):
    def __init__(self, representation, config):
        self._cache = {}
        self.representation = representation
        self.config = config
        self.kpn = representation.kpn
        self.platform = representation.platform
        self.statistics = Statistics(log, len(self.kpn.processes()), config['record_statistics'])
        self.statistics.set_rep_init_time(representation.init_time)
        self._last_added = None
        self.jobs = config['jobs']
        self.parallel = config['parallel']
        self.progress = config['progress']
        self.chunk_size = config['chunk_size']

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

    def add_time_mapping(self, mapping, time):
        self._cache[mapping] = time
        self._last_added = None

    def simulate(self, input_mappings):

        #check inputs
        if len(input_mappings) == 0:
            log.warning("Trying to simulate an empty mapping list")
            return []
        else:
            if isinstance(input_mappings[0],Mapping):
                time = timeit.default_timer()
                tup = [tuple(self.representation.toRepresentation(m)) for m in input_mappings]
                self.statistics.add_rep_time(timeit.default_timer() - time)
                mappings = input_mappings
            else: #assume mappings are list type then
                #transform into tuples
                time = timeit.default_timer()
                tup = [tuple(self.representation.approximate(np.array(m))) for m in input_mappings]
                mappings = [self.representation.fromRepresentation(m) for m in input_mappings]
                self.statistics.add_rep_time(timeit.default_timer() - time)

        # first look up as many as possible:
        lookups = [self.lookup(t) for t in tup]
        num = len([m for m in lookups if m])
        log.info(f"{num} from cache.")

        #if all were already cached, return them
        if num == len(tup):
            return lookups

        if self.parallel:
            import multiprocessing as mp
            simulations = []

            #results = mp.Array() #Do we need thread-safe data structure?
            for i,mapping in enumerate(mappings):
                if lookups[i]:
                    continue
                # create a simulation context
                sim_context = SimulationContext(self.platform)

                # create the application context
                name = self.kpn.name
                app_context = ApplicationContext(name, self.kpn)
                app_context.start_time = 0
                app_context.representation = self.representation
                app_context.mapping = mapping

                # since mappings are simulated in parallel, whole simulation time is added later as offset
                self.statistics.mapping_evaluated(0)

                # create the trace reader
                app_context.trace_reader = hydra.utils.instantiate(self.config['trace'])
                sim_context.app_contexts.append(app_context)
                simulations.append(sim_context)

            # run the simulations and search for the best mapping
            pool = mp.Pool(processes=self.jobs)

            time = timeit.default_timer()
            # execute the simulations in parallel
            if self.progress:
                import tqdm
                results = list(tqdm.tqdm(pool.imap(run_simulation, simulations,
                                                   chunksize = self.chunk_size), total =len(mappings)))
            else:
                results = list(pool.map(run_simulation, simulations, chunksize = self.chunk_size))
            self.statistics.add_offset(timeit.default_timer() - time)

            # calculate the execution times in milliseconds and store them
            exec_times = []  # keep a list of exec_times for later
            res_iter = iter(results)
            for i,mapping in enumerate(mappings):
                exec_time = lookups[i]
                if exec_time:
                    exec_times.append(exec_time)
                else:
                    r = next(res_iter)
                    exec_time = float(r.exec_time / 1000000000.0)
                    exec_times.append(exec_time)
                    self.add_time_mapping(tup[i],exec_time)
            return exec_times

        else: #sequential
            exec_times = []
            for i,mapping in enumerate(mappings):
                if not lookups[i]:
                    exec_times.append(lookups[i])
                # create a simulation context
                sim_context = SimulationContext(self.platform)

                # create the application context
                name = self.kpn.name
                app_context = ApplicationContext(name, self.kpn)
                app_context.start_time = 0
                app_context.representation = self.rep_type
                app_context.mapping = mapping


                # create the trace reader
                app_context.trace_reader = hydra.utils.instantiate(self.config['trace'])
                sim_context.app_contexts.append(app_context)

                time = timeit.default_timer()
                r = run_simulation(sim_context)
                self.statistics.mapping_evaluated(timeit.default_timer() - time)

                exec_time = float(r.exec_time / 1000000000.0)
                self.add_time_mapping(tup[i], exec_time)
                exec_times.append(exec_time)
            return exec_times

    def dump(self,filename):
        log.info(f"dumping cache to {filename}")
        file = open(filename,'x')
        file.write("mapping,runtime\n")
        for mapping in self._cache:
            file.write(f"\"{str(mapping).replace('(','').replace(')','')}\",{self._cache[mapping]}\n")
        file.close()
        log.info("cache dumped.")


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


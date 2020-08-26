# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Felix Teweleit

import timeit
import hydra
import multiprocessing as mp
import numpy as np

from pykpn.common.mapping import Mapping
from pykpn.simulate import KpnSimulation

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
        self.config = config
        self.representation = representation
        self.kpn = representation.kpn
        self.platform = representation.platform
        self.statistics = Statistics(log, len(self.kpn.processes()), config['mapper']['params']['record_statistics'])
        self.statistics.set_rep_init_time(representation.init_time)
        self._last_added = None
        self.jobs = config['mapper']['params']['jobs']
        self.parallel = config['mapper']['params']['parallel']
        self.progress = config['mapper']['params']['progress']
        self.chunk_size = config['mapper']['params']['chunk_size']

        if self.parallel:
            self.pool = mp.Pool(processes=self.jobs)

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
        # check inputs
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

        # create a list of simulations to be run
        simulations = []
        for i, mapping in enumerate(mappings):
            # skip if this particular mapping is in the cache
            if lookups[i]:
                continue

            trace = hydra.utils.instantiate(self.config['trace'])
            simulation = KpnSimulation(self.platform, self.kpn, mapping, trace)

            # since mappings are simulated in parallel, whole simulation time is added later as offset
            self.statistics.mapping_evaluated(0)
            simulations.append(simulation)

        if self.parallel and len(simulations) > self.chunk_size:
            # run the simulations in parallel
            time = timeit.default_timer()
            if self.progress:
                import tqdm
                results = list(tqdm.tqdm(self.pool.imap(run_simulation,
                                                        simulations,
                                                        chunksize=self.chunk_size),
                                         total=len(mappings)))
            else:
                results = list(self.pool.map(run_simulation,
                                             simulations,
                                             chunksize=self.chunk_size))
            self.statistics.add_offset(timeit.default_timer() - time)
        else:
            results = []
            # run the simulations sequentially
            for s in simulations:
                time = timeit.default_timer()
                r = run_simulation(s)
                results.append(r)
                self.statistics.mapping_evaluated(timeit.default_timer() - time)

        # calculate the execution times in milliseconds and store them
        exec_times = []  # keep a list of exec_times for later
        res_iter = iter(results)
        for i, mapping in enumerate(mappings):
            exec_time = lookups[i]
            if exec_time:
                exec_times.append(exec_time)
            else:
                r = next(res_iter)
                exec_time = float(r.exec_time / 1000000000.0)
                exec_times.append(exec_time)
                self.add_time_mapping(tup[i],exec_time)
        return exec_times

    def dump(self,filename):
        log.info(f"dumping cache to {filename}")
        file = open(filename,'x')
        file.write("mapping,runtime\n")
        for mapping in self._cache:
            file.write(f"\"{str(mapping).replace('(','').replace(')','')}\",{self._cache[mapping]}\n")
        file.close()
        log.info("cache dumped.")


def run_simulation(simulation):
    with simulation:
        simulation.run()
    return simulation


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

class TraceGeneratorMock:
    def __init__(self):
        pass

    def next_segment(self, param_1, param_2):
        return None

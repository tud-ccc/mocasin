# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens

from sortedcontainers import SortedList

from mocasin.common.mapping import Mapping, ProcessMappingInfo
from mocasin.mapper.pareto import filter_pareto_front
from mocasin.mapper.partial import ComPartialMapper
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper.utils import SimulationManager
from mocasin.util import logging


log = logging.getLogger(__name__)


def gen_trace_summary(graph, platform, trace):
    summary = {}
    p_types = set()
    for p in platform.processors():
        p_types.add(p.type)
    for proc in graph.processes():
        acc_cycles = trace.accumulate_processor_cycles(proc.name)
        if acc_cycles is None:
            # in this case there are no compute segments for the given process
            for p_type in p_types:
                summary[(proc, p_type)] = 0
        else:
            for p_type in p_types:
                summary[(proc, p_type)] = acc_cycles[p_type]
    return summary


class StaticCFS(object):
    """Base class for mapping using a static method similar to the Linux CFS.

    See: http://people.redhat.com/mingo/cfs-scheduler/sched-design-CFS.txt
    """

    def __init__(self, platform):
        """Generates a full mapping for a given platform and dataflow application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        """
        self.platform = platform
        # self.statistics = Statistics()

    def generate_mapping_dict(
        self, graphs, trace_summary, load=None, restricted=None
    ):
        """Generates a full mapping using a static algorithm
        inspired by Linux'
        """
        core_types = dict(self.platform.get_processor_types())
        processes = {}
        mappings = {}
        if restricted is None:
            restricted = []
        if load is None:
            load = []

        for type in core_types:
            processes[type] = SortedList()
            # use best time at first and update depending on the process
            # that is next
            for graph in graphs:
                for p in graph.processes():
                    processes[type].add(
                        (trace_summary[(p, type)], graph.name + p.name)
                    )

        finished = False  # to avoid converting the lists every time
        while not finished:
            # round robin
            for core in self.platform.processors():
                if core.name in restricted:
                    continue
                _, pr = processes[core.type].pop()
                process = None
                for graph in graphs:
                    for proc in graph.processes():
                        if graph.name + proc.name == pr:
                            process = proc
                            break
                    if process is not None:
                        break

                # map process to core
                mappings[process] = core

                # remove process from the other lists
                for type in core_types:
                    if core.type == type:
                        continue
                    to_remove = [
                        (time, p) for (time, p) in processes[type] if p == pr
                    ]
                    assert (len(to_remove)) == 1
                    processes[type].remove(to_remove[0])

                if len(processes[core.type]) == 0:
                    finished = True
                    break

        # finish mapping
        return mappings

    def map_to_core(self, mapping, process, core):
        scheduler = list(self.platform.schedulers())[0]
        affinity = core
        priority = 0
        info = ProcessMappingInfo(scheduler, affinity, priority)
        mapping.add_process_info(process, info)


class StaticCFSMapper(StaticCFS):
    """
    Generates a full mapping by using the static CFS method.
    """

    def __init__(self, graph, platform, trace, representation):
        super().__init__(platform)
        self.full_mapper = True  # flag indicating the mapper type
        self.graph = graph
        self.trace = trace
        self.representation = representation
        self.randMapGen = RandomPartialMapper(self.graph, self.platform)
        self.comMapGen = ComPartialMapper(
            self.graph, self.platform, self.randMapGen
        )

    def generate_mapping(self, load=None, restricted=None):
        trace_summary = gen_trace_summary(self.graph, self.platform, self.trace)
        mapping = Mapping(self.graph, self.platform)
        mapping_dict = self.generate_mapping_dict(
            [self.graph], trace_summary, load=load, restricted=restricted
        )
        for proc in self.graph.processes():
            self.map_to_core(mapping, proc, mapping_dict[proc])
        return self.comMapGen.generate_mapping(mapping)

    def generate_pareto_front(self, evaluate_metadata=None):
        """Generate Pareto front of the mappings."""
        # By default, we do not evaluate metadata
        if evaluate_metadata is None:
            evaluate_metadata = False
        pareto = []
        restricted = [[]]
        cores = {}
        all_cores = list(self.platform.processors())
        for core_type, _ in self.platform.get_processor_types().items():
            cores[core_type] = [
                core.name for core in all_cores if core.type == core_type
            ]
        for core_type, _ in self.platform.get_processor_types().items():
            new_res = []
            for r in restricted:
                for i in range(len(cores[core_type])):
                    new_res.append(r + cores[core_type][: i + 1])
            restricted = restricted + new_res
        restricted = restricted[:-1]
        log.debug(f"Length of restricted = {len(restricted)}")
        log.debug(f"{restricted}")
        for res in restricted:
            mapping = self.generate_mapping(restricted=res)
            # num_resources = []
            # for core_type in cores:
            #    tot = 0
            #    for core in res:
            #        if core == cores[core_type]:
            #            tot += 1
            #    num_resources.append(tot)
            pareto.append(mapping)

        if not evaluate_metadata:
            return pareto

        # Obtain simulation values
        simulation_manager = SimulationManager(
            self.representation, self.trace, jobs=None, parallel=True
        )
        simulation_manager.simulate(pareto)
        for mapping in pareto:
            simulation_manager.append_mapping_metadata(mapping)

        filtered = filter_pareto_front(pareto)

        return filtered


class StaticCFSMapperMultiApp(StaticCFS):
    def __init__(self, platform):
        super().__init__(platform)

    def generate_mappings(self, graphs, traces, load=None, restricted=None):
        if len(graphs) == 0:
            return []
        else:
            log.info(f"generating fair mapping for {len(graphs)} apps")
        comMapGen = {}
        if len(traces) != len(graphs):
            raise RuntimeError(
                f"Mapper received unbalanced number of traces ({len(traces)}) "
                f"and applications ({len(graphs)})"
            )
        for graph in graphs:
            randMapGen = RandomPartialMapper(graph, self.platform)
            comMapGen[graph] = ComPartialMapper(
                graph, self.platform, randMapGen
            )

        trace_summaries = {}
        mappings = {}
        for graph, trace in zip(graphs, traces):
            trace_summaries.update(
                gen_trace_summary(graph, self.platform, trace)
            )
            mappings[graph] = Mapping(graph, self.platform)
        mapping_dict = self.generate_mapping_dict(
            graphs, trace_summaries, load=load, restricted=restricted
        )
        for graph in graphs:
            for proc in graph.processes():
                self.map_to_core(mappings[graph], proc, mapping_dict[proc])

        res = []
        for graph in mappings:
            res.append(comMapGen[graph].generate_mapping(mappings[graph]))
        return res

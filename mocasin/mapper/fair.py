# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Robert Khasanov

from sortedcontainers import SortedList

from mocasin.common.mapping import Mapping, ProcessMappingInfo
from mocasin.common.mapping_constraints import MappingConstraints
from mocasin.mapper import BaseMapper
from mocasin.mapper.partial import ComPartialMapper
from mocasin.mapper.random import RandomPartialMapper
from mocasin.util import logging

log = logging.getLogger(__name__)


def gen_trace_summary(graph, platform, trace, mapping_constraints=None):
    summary = {}
    p_types = set()
    for p in platform.processors():
        p_types.add(p.type)
    if mapping_constraints is None:
        mapping_constraints = MappingConstraints.unrestricted(graph, platform)
    for proc in graph.processes():
        acc_cycles = trace.accumulate_processor_cycles(proc.name)
        eligible_types = mapping_constraints.eligible_processor_types(proc)
        if acc_cycles is None:
            for p_type in eligible_types:
                summary[(proc, p_type)] = 0
        else:
            profiled_types = set(acc_cycles)
            for p_type in p_types.intersection(eligible_types, profiled_types):
                summary[(proc, p_type)] = acc_cycles[p_type]
    return summary


class StaticCFS(BaseMapper):
    """Base class for mapping using a static method similar to the Linux CFS.

    See: http://people.redhat.com/mingo/cfs-scheduler/sched-design-CFS.txt

    Note:
        The implemented heuristic more closely resembles longest-first
        round-robin process mapping and does not appear to model the runtime
        scheduling behavior of Linux CFS directly. It may also produce poor
        mappings on heterogeneous platforms because it does not compare the
        relative execution costs across processor types.

    Args:
        platform (Platform): a platform
    """

    def __init__(self, platform):
        super().__init__(platform, full_mapper=True)

    def generate_mapping_dict(self, graphs, trace_summary, processors=None):
        """Generate a full mapping using a static CFS algorithm.

        If a parameter `processors` is given, map processes to the processors
        listed in this argument.
        """
        core_types = dict(self.platform.get_processor_types())
        processes = {}
        mappings = {}
        if processors is None:
            processors = list(self.platform.processors())

        process_by_name = {}
        unmapped = set()
        for core_type in core_types:
            processes[core_type] = SortedList()
            for graph in graphs:
                for p in graph.processes():
                    process_name = graph.name + p.name
                    process_by_name[process_name] = p
                    unmapped.add(p)
                    if (p, core_type) in trace_summary:
                        processes[core_type].add(
                            (trace_summary[(p, core_type)], process_name)
                        )

        while unmapped:
            made_progress = False
            # round robin
            for core in processors:
                if not processes[core.type]:
                    continue
                # Preserve the original heuristic: map the process with the
                # largest cycle count for this processor type first.
                _, pr = processes[core.type].pop()
                process = process_by_name[pr]

                # map process to core
                mappings[process] = core
                unmapped.remove(process)
                made_progress = True

                # remove process from the other lists
                for core_type in core_types:
                    if core.type == core_type:
                        continue
                    to_remove = [
                        (time, p)
                        for (time, p) in processes[core_type]
                        if p == pr
                    ]
                    if to_remove:
                        processes[core_type].remove(to_remove[0])

                if not unmapped:
                    break

            if not made_progress:
                names = ", ".join(sorted(process.name for process in unmapped))
                raise RuntimeError(
                    "static_cfs: No eligible processor available for "
                    f"processes: {names}"
                )

        # finish mapping
        return mappings

    def map_to_core(self, mapping, process, core):
        scheduler = self.platform.find_scheduler_for_processor(core)
        affinity = core
        priority = 0
        info = ProcessMappingInfo(scheduler, affinity, priority)
        mapping.add_process_info(process, info)


class StaticCFSMapper(StaticCFS):
    """This mapper generates a full mapping using the static CFS method."""

    def __init__(self, platform):
        super().__init__(platform)
        random_partial_mapper = RandomPartialMapper(self.platform)
        self.com_mapper = ComPartialMapper(self.platform, random_partial_mapper)

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
        mapping_constraints=None,
    ):
        if mapping_constraints is None:
            mapping_constraints = MappingConstraints.unrestricted(
                graph, self.platform
            )
        trace_summary = gen_trace_summary(
            graph, self.platform, trace, mapping_constraints
        )
        mapping = Mapping(graph, self.platform)
        mapping_dict = self.generate_mapping_dict(
            [graph], trace_summary, processors=processors
        )
        for proc in graph.processes():
            self.map_to_core(mapping, proc, mapping_dict[proc])

        return self.com_mapper.generate_mapping(
            graph,
            trace=trace,
            representation=representation,
            partial_mapping=mapping,
            mapping_constraints=mapping_constraints,
        )


class StaticCFSMapperMultiApp(StaticCFS):
    def __init__(self, platform):
        super().__init__(platform)

    def generate_mappings(self, graphs, traces, restricted=None):
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
            graphs, trace_summaries, restricted=restricted
        )
        for graph in graphs:
            for proc in graph.processes():
                self.map_to_core(mappings[graph], proc, mapping_dict[proc])

        res = []
        for graph in mappings:
            res.append(comMapGen[graph].generate_mapping(mappings[graph]))
        return res

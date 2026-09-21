# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import pytest

from mocasin.common.mapping import Mapping
from mocasin.common.mapping_constraints import MappingConstraints
from mocasin.common.trace import ComputeSegment, DataflowTrace
from mocasin.mapper.fair import StaticCFS, StaticCFSMapper, gen_trace_summary


class MockTrace(DataflowTrace):
    def __init__(self, proc_names, core_types, lookup_function, max_length=1):
        self.cores = core_types
        self.procs = proc_names
        self.lookup = lookup_function
        self.max_length = max_length

    def get_trace(self, proc_name):
        for _ in range(0, self.max_length):
            processor_cycles = {}
            for core in self.cores:
                processor_cycles[core] = self.lookup((core, proc_name))

            yield ComputeSegment(processor_cycles)


class ProfileTrace(DataflowTrace):
    def __init__(self, profiles):
        self.profiles = profiles

    def get_trace(self, process):
        yield ComputeSegment(self.profiles[process])


def test_gen_trace_summary(graph, platform):
    const_value = 3
    num_iter = 10
    proc_names = [proc.name for proc in graph.processes()]
    core_types = [core.type for core in platform.processors()]
    const_func = lambda _: const_value
    trace = MockTrace(proc_names, core_types, const_func, max_length=num_iter)
    trace_summary = gen_trace_summary(graph, platform, trace)
    for proc in proc_names:
        assert len(list(trace.get_trace(proc))) == num_iter
    for core in core_types:
        for proc in graph.processes():
            assert trace_summary[(proc, core)] == const_value * num_iter

    for core in core_types:
        for proc in graph.processes():
            single_comb = (
                lambda x: (x[0] == core) * (x[1] == proc.name) * const_value
            )
            trace = MockTrace(
                proc_names, core_types, single_comb, max_length=num_iter
            )
            trace_summary = gen_trace_summary(graph, platform, trace)

            for other_core in core_types:
                for other_proc in graph.processes():
                    val = trace_summary[(other_proc, other_core)]
                    assert (
                        other_core == core
                        and other_proc == proc
                        and val == num_iter * const_value
                    ) or val == 0


def test_map_to_core(graph, platform):
    cfs = StaticCFS(platform)
    for core in platform.processors():
        for proc in graph.processes():
            mapping = Mapping(graph, platform)
            cfs.map_to_core(mapping, proc, core)
            assert mapping._process_info[proc.name].affinity == core


def test_static_cfs_uses_only_eligible_processors(
    graph, heterogeneous_platform
):
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"FPGA": 20}})
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )

    mapping = StaticCFSMapper(heterogeneous_platform).generate_mapping(
        graph, trace=trace, mapping_constraints=constraints
    )

    assert mapping.affinity(graph.find_process("a")).type == "CPU"
    assert mapping.affinity(graph.find_process("b")).type == "FPGA"
    for process in graph.processes():
        info = mapping.process_info(process)
        assert process in mapping.scheduler_processes(info.scheduler)


def test_static_cfs_continues_after_an_eligible_queue_becomes_empty(
    graph, heterogeneous_platform
):
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"CPU": 20}})
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )

    mapping = StaticCFSMapper(heterogeneous_platform).generate_mapping(
        graph, trace=trace, mapping_constraints=constraints
    )

    assert all(
        mapping.affinity(process).type == "CPU" for process in graph.processes()
    )


def test_static_cfs_requires_cycle_data_for_an_eligible_processor(
    graph, heterogeneous_platform
):
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"CPU": 20}})
    constraints = MappingConstraints.unrestricted(graph, heterogeneous_platform)

    mapping = StaticCFSMapper(heterogeneous_platform).generate_mapping(
        graph, trace=trace, mapping_constraints=constraints
    )

    assert all(
        mapping.affinity(process).type == "CPU" for process in graph.processes()
    )


def test_static_cfs_reports_missing_eligible_processor(
    graph, heterogeneous_platform
):
    cpu = heterogeneous_platform.find_processor("cpu")
    fpga = heterogeneous_platform.find_processor("fpga")
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"CPU": 20}})
    constraints = MappingConstraints(
        graph,
        heterogeneous_platform,
        {"a": [cpu], "b": [cpu]},
    )

    with pytest.raises(
        RuntimeError,
        match="No eligible processor available for processes: a, b",
    ):
        StaticCFSMapper(heterogeneous_platform).generate_mapping(
            graph,
            trace=trace,
            processors=[fpga],
            mapping_constraints=constraints,
        )

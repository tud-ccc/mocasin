# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

import pytest

from mocasin.common.graph import DataflowGraph, DataflowProcess
from mocasin.common.mapping import Mapping, ProcessMappingInfo
from mocasin.common.mapping_constraints import MappingConstraints
from mocasin.common.platform import Platform, Processor, Scheduler
from mocasin.common.trace import ComputeSegment, DataflowTrace, EmptyTrace


class ProfileTrace(DataflowTrace):
    def __init__(self, profiles):
        self.profiles = profiles

    def get_trace(self, process):
        yield ComputeSegment(self.profiles[process])


@pytest.fixture
def graph():
    graph = DataflowGraph("graph")
    graph.add_process(DataflowProcess("a"))
    graph.add_process(DataflowProcess("b"))
    return graph


@pytest.fixture
def heterogeneous_platform(mocker):
    platform = Platform("heterogeneous")
    cpu = Processor("cpu", "CPU", mocker.Mock(), mocker.Mock())
    fpga = Processor("fpga", "FPGA", mocker.Mock(), mocker.Mock())
    platform.add_processor(cpu)
    platform.add_processor(fpga)
    platform.add_scheduler(Scheduler("cpu_scheduler", [cpu], [mocker.Mock()]))
    platform.add_scheduler(
        Scheduler("fpga_scheduler", [fpga], [mocker.Mock()])
    )
    return platform


def test_mapping_constraints_expand_processor_types(
    graph, heterogeneous_platform
):
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"FPGA": 20}})

    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )

    assert [
        processor.name for processor in constraints.eligible_processors("a")
    ] == ["cpu"]
    assert constraints.eligible_processor_types("b") == {"FPGA"}


def test_mapping_constraints_unrestricted(graph, heterogeneous_platform):
    constraints = MappingConstraints.unrestricted(
        graph, heterogeneous_platform
    )

    assert set(constraints.eligible_processors("a")) == set(
        heterogeneous_platform.processors()
    )


def test_mapping_constraints_intersection(graph, heterogeneous_platform):
    unrestricted = MappingConstraints.unrestricted(
        graph, heterogeneous_platform
    )
    from_trace = MappingConstraints.from_trace(
        graph,
        heterogeneous_platform,
        ProfileTrace({"a": {"CPU": 10}, "b": {"FPGA": 20}}),
    )

    constraints = unrestricted.intersection(from_trace)

    assert constraints.eligible_processor_types("a") == {"CPU"}
    assert constraints.eligible_processor_types("b") == {"FPGA"}


def test_mapping_constraints_treat_empty_trace_as_unrestricted(
    graph, heterogeneous_platform
):
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, EmptyTrace()
    )

    assert set(constraints.eligible_processors("a")) == set(
        heterogeneous_platform.processors()
    )


def test_mapping_constraints_validate_mapping(graph, heterogeneous_platform):
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"FPGA": 20}})
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )
    mapping = Mapping(graph, heterogeneous_platform)
    cpu = heterogeneous_platform.find_processor("cpu")
    fpga = heterogeneous_platform.find_processor("fpga")
    mapping.add_process_info(
        graph.find_process("a"),
        ProcessMappingInfo(
            heterogeneous_platform.find_scheduler_for_processor(cpu), cpu
        ),
    )
    mapping.add_process_info(
        graph.find_process("b"),
        ProcessMappingInfo(
            heterogeneous_platform.find_scheduler_for_processor(fpga), fpga
        ),
    )

    assert constraints.is_mapping_eligible(mapping)

    mapping.process_info(graph.find_process("a")).affinity = fpga
    assert not constraints.is_mapping_eligible(mapping)


def test_mapping_constraints_require_an_eligible_processor(
    graph, heterogeneous_platform
):
    trace = ProfileTrace({"a": {"GPU": 10}, "b": {"CPU": 20}})

    with pytest.raises(
        RuntimeError,
        match="No eligible processor for process 'a'.*GPU",
    ):
        MappingConstraints.from_trace(graph, heterogeneous_platform, trace)

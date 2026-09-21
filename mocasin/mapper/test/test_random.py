# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

import pytest

from mocasin.common.mapping import Mapping, ProcessMappingInfo
from mocasin.common.mapping_constraints import MappingConstraints
from mocasin.common.trace import ComputeSegment, DataflowTrace
from mocasin.mapper.random import RandomMapper, RandomPartialMapper


class ProfileTrace(DataflowTrace):
    def __init__(self, profiles):
        self.profiles = profiles

    def get_trace(self, process):
        yield ComputeSegment(self.profiles[process])


def test_random_mapper_uses_only_eligible_processors(
    graph, heterogeneous_platform
):
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"FPGA": 20}})
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )
    mapper = RandomMapper(heterogeneous_platform, random_seed=1)

    mapping = mapper.generate_mapping(graph, mapping_constraints=constraints)

    assert mapping.affinity(graph.find_process("a")).type == "CPU"
    assert mapping.affinity(graph.find_process("b")).type == "FPGA"


def test_random_mapper_rejects_incompatible_partial_mapping(
    graph, heterogeneous_platform
):
    process = graph.find_process("a")
    fpga = heterogeneous_platform.find_processor("fpga")
    scheduler = heterogeneous_platform.find_scheduler_for_processor(fpga)
    partial_mapping = Mapping(graph, heterogeneous_platform)
    partial_mapping.add_process_info(
        process, ProcessMappingInfo(scheduler, fpga)
    )
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"CPU": 20}})
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )

    with pytest.raises(
        RuntimeError,
        match="Process 'a' is not eligible for processor 'fpga'",
    ):
        RandomMapper(heterogeneous_platform).generate_mapping(
            graph,
            partial_mapping=partial_mapping,
            mapping_constraints=constraints,
        )


def test_random_mapper_reports_missing_compatible_processor(
    graph, heterogeneous_platform
):
    cpu = heterogeneous_platform.find_processor("cpu")
    fpga = heterogeneous_platform.find_processor("fpga")
    constraints = MappingConstraints(
        graph,
        heterogeneous_platform,
        {"a": [cpu], "b": [cpu]},
    )

    with pytest.raises(
        RuntimeError,
        match="Could not map process 'a'.*eligible processors: cpu",
    ):
        RandomMapper(heterogeneous_platform).generate_mapping(
            graph,
            processors=[fpga],
            mapping_constraints=constraints,
        )


def test_resources_first_covers_eligible_processors(
    graph, heterogeneous_platform, mocker
):
    cpu = heterogeneous_platform.find_processor("cpu")
    fpga = heterogeneous_platform.find_processor("fpga")
    mocker.patch("mocasin.mapper.random.random.randint", return_value=1)
    mocker.patch("mocasin.mapper.random.random.sample", return_value=[fpga])
    trace = ProfileTrace({"a": {"CPU": 10}, "b": {"FPGA": 20}})
    constraints = MappingConstraints.from_trace(
        graph, heterogeneous_platform, trace
    )

    mapping = RandomPartialMapper(
        heterogeneous_platform, resources_first=True
    ).generate_mapping(graph, mapping_constraints=constraints)

    assert mapping.affinity(graph.find_process("a")) is cpu
    assert mapping.affinity(graph.find_process("b")) is fpga

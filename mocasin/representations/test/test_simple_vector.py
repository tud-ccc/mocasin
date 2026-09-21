# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.common.graph import DataflowGraph, DataflowProcess
from mocasin.common.mapping_constraints import MappingConstraints
from mocasin.common.platform import Platform, Processor, Scheduler
from mocasin.representations import SimpleVectorRepresentation


def test_crossover_exchanges_both_parents(mocker):
    mocker.patch("mocasin.representations.random.sample", return_value=[1])
    representation = object.__new__(SimpleVectorRepresentation)
    first = [0, 0]
    second = [1, 1]

    representation._crossover(first, second, 1)

    assert first == [0, 1]
    assert second == [1, 0]


def test_approximate_eligible_uses_nearest_mapping(mocker):
    graph = DataflowGraph("graph")
    graph.add_process(DataflowProcess("a"))
    graph.add_process(DataflowProcess("b"))

    platform = Platform("platform")
    processors = tuple(
        Processor(f"processor{i}", "type", mocker.Mock(), mocker.Mock())
        for i in range(7)
    )
    for processor in processors:
        platform.add_processor(processor)
    platform.add_scheduler(Scheduler("scheduler", processors, [mocker.Mock()]))

    constraints = MappingConstraints(
        graph,
        platform,
        {"a": (processors[1], processors[5]), "b": processors},
    )
    representation = SimpleVectorRepresentation(
        graph, platform, mapping_constraints=constraints
    )
    periodic_representation = SimpleVectorRepresentation(
        graph,
        platform,
        periodic_boundary_conditions=True,
    )
    periodic_representation.set_mapping_constraints(constraints)

    assert representation.approximate_eligible([3.4, 0]) == [5, 0]
    assert representation.approximate_eligible([100, 0]) == [5, 0]
    assert representation.approximate_eligible([101.3, 0]) == [5, 0]
    assert periodic_representation.approximate_eligible([100, 0]) == [1, 0]
    assert periodic_representation.approximate_eligible([101.3, 0]) == [5, 0]
    assert periodic_representation.approximate_eligible([104.7, 0]) == [1, 0]

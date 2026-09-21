# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.common.mapping_constraints import MappingConstraints
from mocasin.mapper.random_walk import RandomWalkMapper
from mocasin.mapper.test.mock_cache import MockMappingCache
from mocasin.representations import SimpleVectorRepresentation


def test_random_walk_respects_mapping_constraints(
    graph,
    heterogeneous_platform,
    trace,
    simres_evaluation_function,
    mocker,
):
    processors = tuple(heterogeneous_platform.processors())
    cpu = next(processor for processor in processors if processor.type == "CPU")
    constraints = MappingConstraints(
        graph,
        heterogeneous_platform,
        {"a": (cpu,), "b": processors},
    )
    representation = SimpleVectorRepresentation(
        graph,
        heterogeneous_platform,
        mapping_constraints=constraints,
    )

    def evaluate(candidate):
        mapping = representation.fromRepresentation(candidate)
        assert constraints.is_mapping_eligible(mapping)
        return simres_evaluation_function(candidate)

    mapper = RandomWalkMapper(
        heterogeneous_platform,
        num_iterations=10,
        parallel=False,
        progress=False,
    )
    mapper._simulation_manager = MockMappingCache(evaluate, mocker)

    result = mapper.generate_mapping(
        graph,
        trace=trace,
        representation=representation,
        mapping_constraints=constraints,
    )

    assert constraints.is_mapping_eligible(result)

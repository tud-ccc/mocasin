# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

import pytest

from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper
from mocasin.mapper.test.test_fair import MockTrace
from mocasin.mapper.utils import SimulationManager, SimulationManagerConfig
from mocasin.simulate import SimulationResult


@pytest.fixture
def mapper(graph, platform_odroid):
    com_mapper = ComFullMapper(platform_odroid)
    return ProcPartialMapper(graph, platform_odroid, com_mapper)


def test_simulation_manager_cache(
    graph, platform_odroid, representation_odroid, mapper
):
    proc_names = [proc.name for proc in graph.processes()]
    core_types = [core.type for core in platform_odroid.processors()]
    trace = MockTrace(proc_names, core_types, lambda _: 5, max_length=10)
    mapping = mapper.generate_mapping([0, 4])
    simulation_manager = SimulationManager(
        platform_odroid,
        SimulationManagerConfig(jobs=None, parallel=True),
    )
    assert not simulation_manager._cache
    lookup_result = simulation_manager.lookup(graph, tuple([0, 4]))
    assert not lookup_result
    simulation_result = simulation_manager.simulate(
        graph, trace, representation_odroid, [mapping]
    )
    assert len(simulation_manager._cache) == 1
    lookup_result = simulation_manager.lookup(graph, tuple([0, 4]))
    assert isinstance(lookup_result, SimulationResult)
    assert simulation_result[0] == lookup_result

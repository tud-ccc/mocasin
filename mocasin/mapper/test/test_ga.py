# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Robert Khasanov

import pytest

from mocasin.mapper.genetic import GeneticMapper, Objectives
from mocasin.mapper.test.mock_cache import MockMappingCache


@pytest.fixture
def mapper(
    graph, platform, trace, representation, simres_evaluation_function, mocker
):
    m = GeneticMapper(platform)
    m.simulation_manager = MockMappingCache(simres_evaluation_function, mocker)
    return m


def test_ga(mapper, graph, trace, representation):
    result = mapper.generate_mapping(
        graph, trace=trace, representation=representation
    )

    # minimum of 1 + cos(x-y) sin(2y-1)
    assert result.to_list() == [6, 6]


def test_objectives():
    flags = Objectives.from_string_list(["exec_time", "energy"])

    assert Objectives.EXEC_TIME in flags
    assert Objectives.ENERGY in flags
    assert Objectives.RESOURCES not in flags

    flags = Objectives.from_string_list(["resources"])

    assert Objectives.EXEC_TIME not in flags
    assert Objectives.ENERGY not in flags
    assert Objectives.RESOURCES in flags


@pytest.mark.raises(exception=RuntimeError)
def test_objectives_raise():
    Objectives.from_string_list(["dumb"])

# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.mapper.genetic import GeneticMapper
from mocasin.mapper.test.mock_cache import MockMappingCache

import pytest


@pytest.fixture
def mapper(
    graph, platform, trace, representation, simres_evaluation_function, mocker
):
    m = GeneticMapper(graph, platform, trace, representation)
    m.simulation_manager = MockMappingCache(simres_evaluation_function, mocker)
    return m


def test_ga(mapper):
    result = mapper.generate_mapping()

    # minimum of 1 + cos(x-y) sin(2y-1)
    assert result.to_list() == [6, 6]

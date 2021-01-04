from pykpn.mapper.test.mock_cache import MockMappingCache
from pykpn.mapper.genetic import GeneticMapper
import pytest
import numpy as np

@pytest.fixture
def evaluation_function():
    return lambda m : 1 + np.cos(m[0]-m[1])*np.sin(m[1]*2-1)

@pytest.fixture
def mapper(kpn, platform, trace, representation, evaluation_function, mocker):
    m = GeneticMapper(kpn, platform, trace, representation)
    m.simulation_manager = MockMappingCache(evaluation_function, mocker)
    return m

def test_ga(mapper):
    result = mapper.generate_mapping()

    #minimum of 1 + cos(x-y) sin(2y-1)
    assert result.to_list() == [6, 6]

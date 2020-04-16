from pykpn.mapper.test.mock_cache import MockMappingCache
from pykpn.mapper.sa_fullmapper import SimulatedAnnealingFullMapper
import pytest
import numpy as np

@pytest.fixture
def conf():
    return {'random_seed' : 42, 'initial_temperature' : 1.0,
            'final_temperature'  : 0.01, 'record_statistics' : False,
           'temperature_proportionality_constant' : 0.5, 'radius' : 2,
            'periodic_boundary_conditions' : False,
           'representation' : 'SimpleVector', 'channels' : False,
            }

@pytest.fixture
def evaluation_function():
    return lambda m : 1+ np.cos(m[0]-m[1])*np.sin(m[1]*2-1)
@pytest.fixture
def mapper(kpn,platform,conf,evaluation_function):
    m =  SimulatedAnnealingFullMapper(kpn,platform,conf)
    m.mapping_cache = MockMappingCache(evaluation_function)
    return m


def test_sa(mapper):
    result = mapper.generate_mapping()
    assert result.to_list() == [6,6] #minimum of 1 + cos(x-y) sin(2y-1)

def test_temperature_cooling(conf,mapper):
    timeout = 10000
    temperature = conf['initial_temperature']
    for i in range(timeout):
        temperature = mapper.temperature_cooling(temperature,i)
        if temperature <= conf['final_temperature']:
            break

    assert temperature <= conf['final_temperature']

def test_query_accept(mapper):
    mapper.initial_cost = 1
    assert np.isclose(mapper.query_accept(1000,0.0001),0)
    positive = mapper.query_accept(1.000001,1)
    assert positive > 0 and positive < 1



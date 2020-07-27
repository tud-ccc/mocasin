from pykpn.mapper.test.mock_cache import MockMappingCache
from pykpn.mapper.simulated_annealing import SimulatedAnnealingMapper
from itertools import product
import pytest
import numpy as np

@pytest.fixture
def conf():
    return {'mapper' : {'random_seed' : 42,
                        'record_statistics' : False,
                        'initial_temperature' : 1.0,
                        'final_temperature'  : 0.01,
                        'temperature_proportionality_constant' : 0.5,
                        'radius' : 2
                        },
            'norm_p' : 2,
            'periodic_boundary_conditions' : False,
            'representation' : 'SimpleVector',
            'channels' : False
            }

@pytest.fixture
def evaluation_function():
    return lambda m : 1 + np.cos(m[0]-m[1]) * np.sin(m[1] * 2-1)

@pytest.fixture
def mapper(kpn, platform, conf, evaluation_function):
    m = SimulatedAnnealingMapper(kpn, platform, conf)
    m.mapping_cache = MockMappingCache(evaluation_function)
    return m

def test_ts(mapper, evaluation_function):
    result_mapper = mapper.generate_mapping()
    results = [ (evaluation_function([x, y]), x, y) for x, y in product(range(7), range(7))]
    expected = set([(x, y) for (_, x, y) in sorted(results)[:5]])

    #result is top 5 best
    assert tuple(result_mapper.to_list()) in expected

def test_temperature_cooling(conf, mapper):
    timeout = 10000
    temperature = conf['mapper']['initial_temperature']

    for i in range(timeout):
        temperature = mapper.temperature_cooling(temperature, i)
        if temperature <= conf['mapper']['final_temperature']:
            break

    assert temperature <= conf['mapper']['final_temperature']

def test_query_accept(mapper):
    mapper.initial_cost = 1

    assert np.isclose(mapper.query_accept(1000, 0.0001), 0)

    positive = mapper.query_accept(1.000001, 1)
    assert positive > 0
    assert positive < 1

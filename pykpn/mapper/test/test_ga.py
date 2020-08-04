from pykpn.mapper.test.mock_cache import MockMappingCache
from pykpn.mapper.genetic import GeneticMapper
from pykpn.mapper.utils import TraceGeneratorMock
import pytest
import numpy as np

@pytest.fixture
def conf():
    return {'mapper' : {'pop_size' : 10,
                         'num_gens' : 5,
                         'cxpb' : 0.35,
                         'mutpb' : 0.5,
                         'tournsize' : 4,
                         'mupluslambda': True,
                         'initials' : 'random',
                         'radius' : 5,
                         'random_seed': 42,
                         'crossover_rate' : 1,
                         'record_statistics' : False
                        },
            'channels' : False,
            'representation' : 'SimpleVector',
            'norm_p' : 2,
            'periodic_boundary_conditions' : False,
            }

@pytest.fixture
def evaluation_function():
    return lambda m : 1 + np.cos(m[0]-m[1])*np.sin(m[1]*2-1)

@pytest.fixture
def mapper(kpn, platform, conf, evaluation_function):
    trace_generator = TraceGeneratorMock()
    m = GeneticMapper(kpn, platform, conf, trace_generator=trace_generator)
    m.mapping_cache = MockMappingCache(evaluation_function)
    return m

def test_ga(mapper):
    result = mapper.generate_mapping()

    #minimum of 1 + cos(x-y) sin(2y-1)
    assert result.to_list() == [6, 6]

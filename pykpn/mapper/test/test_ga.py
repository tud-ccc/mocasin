from pykpn.mapper.test.mock_cache import MockMappingCache
from pykpn.mapper.genetic import GeneticMapper
import pytest
import numpy as np

@pytest.fixture
def conf():
    return {'mapper':
            { 'pop_size' : 10, 'num_gens' : 5, 'cxpb' : 0.35, 'mutpb' : 0.5,
              'tournsize' : 4, 'mupluslambda': True, 'initials' : 'random',
              'objective_exec_time': True, 'objective_num_resources': False,
              'radius' : 5, 'random_seed': 42, 'jobs' : 8, 'chunk_size' : 10,
              'parallel' : True, 'progress' : False, 'dump_cache' : False,
              'crossover_rate' : 1, 'record_statistics' : False},
            'representation' : 'SimpleVector',
            'channels' : False,
            'norm_p' : 2,
            'periodic_boundary_conditions' : False,
            }

@pytest.fixture
def evaluation_function():
    return lambda m : 1 + np.cos(m[0]-m[1])*np.sin(m[1]*2-1)

@pytest.fixture
def mapper(kpn, platform, conf, evaluation_function):
    m = GeneticMapper(kpn, platform, conf)
    m.simulation_manager = MockMappingCache(evaluation_function)
    return m

def test_ga(mapper):
    result = mapper.generate_mapping()

    #minimum of 1 + cos(x-y) sin(2y-1)
    assert result.to_list() == [6, 6]

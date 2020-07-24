from pykpn.mapper.test.mock_cache import MockMappingCache
from pykpn.mapper.gradient_descent import GradientDescentMapper
import pytest
import numpy as np
from itertools import product

@pytest.fixture
def conf():
    return {'random_seed' : 42, 'gd_iterations' : 100,
            'stepsize' : 2, 'norm_p' : 2, 'record_statistics' : False,
            'periodic_boundary_conditions' : True, 'dump_cache' : False,
            'representation' : 'SimpleVector', 'channels' : False
            }

@pytest.fixture
def evaluation_function():
    return lambda m : 1+ np.cos(m[0]-m[1])*np.sin(m[1]*2-1)

@pytest.fixture
def evaluation_function_gradient():
    return lambda m : [np.sin(1 - 2*m[1])*np.sin(m[0] - m[1]), 1/2*(3*np.cos(1 + m[0] - 3*m[1]) + np.cos(1 - m[0] - m[1]))]

@pytest.fixture
def mapper(kpn,platform,conf,evaluation_function):
    m =  GradientDescentMapper(kpn,platform,conf)
    m.simulation_manager = MockMappingCache(evaluation_function)
    return m


def test_gd(mapper,evaluation_function):
    result_mapper = mapper.generate_mapping()
    results = [ (evaluation_function([x,y]),x,y) for x,y in product(range(7),range(7))]
    expected = set([(x,y) for (_,x,y) in sorted(results)[:3]])
    assert tuple(result_mapper.to_list()) in expected #result is top 3 best

def test_gradient(mapper,evaluation_function,evaluation_function_gradient):
    mapper.dim = 2
    good = 0
    bad = 0
    for (x,y) in product(range(1,6),range(1,6)):
        mapper.best_exec_time = 3 #> max(evaluation_function)
        mapper.best_mapping = np.zeros(mapper.dim)
        actual_grad = np.array(evaluation_function_gradient([x,y]))
        calculated_grad = mapper.calculate_gradient([x,y],evaluation_function([x,y]))
        if not np.allclose(actual_grad,np.zeros(mapper.dim)):
            actual_grad_normed = actual_grad * 1/np.linalg.norm(actual_grad)
        else:
            actual_grad_normed = actual_grad
        if not np.allclose(calculated_grad,np.zeros(mapper.dim)):
            calculated_grad_normed = calculated_grad * 1/np.linalg.norm(calculated_grad)
        else:
            calculated_grad_normed = calculated_grad
        if  np.allclose(actual_grad_normed, calculated_grad_normed,atol=0.4):
            good += 1
        else:
            bad += 1
    assert(good > bad)



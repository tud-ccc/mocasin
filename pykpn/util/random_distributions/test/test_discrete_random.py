from functools import reduce
from itertools import product

import numpy as np
from pykpn.util.random_distributions.discrete_random import _discrete_gauss_plain, _discrete_uniform_plain, _discrete_random

def template_test_plain_distribution(distribution_func,dims,eigens,num_executions=1000):
    np.random.seed(0)
    randoms =[]
    for i in range(num_executions):
        randoms.append(distribution_func(dims,eigens)[0])
    median_vec = distribution_func(dims,eigens)[1]

    #median = distribution_func(dims,eigens)[1]

    #for i in range(len(dims)):
    #    empty_dict = dict()
    #    for j in range(dims[i]):
    #        empty_dict[j] = 0
    #    #print( "Frequencies for component " + str(i) +": "  + str( reduce(lambda res, x : res.update({x[i] : res[x[i]]+1}) or res,randoms, empty_dict)))

    #empty_dict = dict()
    #for i in product(*map(lambda dim: range(dim),dims)):
    #    empty_dict[tuple(i)] = 0
    #reduce(lambda res, x : res.update({tuple(x) : res[tuple(x)]+1}) or res,randoms, empty_dict)
    #non_zero_freqs = [ x for x in empty_dict.values() if x != 0]
    #print("Non-zero frequencies: " + str( non_zero_freqs))
    #print("Mean non-zero frequency: " + str( np.mean(non_zero_freqs)))
    #print("Std. dev: " + str(np.std(non_zero_freqs,ddof=1)))
    mean = np.mean(randoms, axis=0)
    std = np.std(randoms, axis=0, ddof=1)
    return mean,std,median_vec

def constant_nums(dims,eigenvals):
    eigenvals_int = eigenvals.astype(int)
    median_vec = eigenvals_int/2.
    res = list(product(*tuple([range(val) for val in eigenvals_int])))
    return res,median_vec

    #plot_distribution(ns,mu,Q,r,discrete_uniform,num_points=1000)
    #plot_distribution(ns,mu,Q,r,discrete_gauss,num_points=10000)
def test_discrete_uniform(ns,eigenv):
    np.random.seed(0)
    mean,std,_ = template_test_plain_distribution(_discrete_uniform_plain, ns, eigenv, 100000)
    expected_std = [ np.sqrt(((b - 0 + 1)**2-1)/12) for b in eigenv.flat]
    assert(np.allclose(mean,eigenv/2.,atol=0.5))
    assert(np.allclose(std,expected_std,atol=0.5))

def test_discrete_gauss(ns,eigenv):
    np.random.seed(0)
    mean,std,median_vec = template_test_plain_distribution(_discrete_gauss_plain, ns, eigenv, 100000)
    deviation = np.abs(mean-median_vec)
    assert(np.allclose(deviation, 0,atol=0.5))
    assert(np.allclose(std,np.array([[2.28, 1.32]]),atol=0.3))

def test_discrete_random(ns,mu,r,Q):
    Sigma = float(r**2) * Q @ np.transpose(Q)
    eigenvals,_ = np.linalg.eig(Sigma)
    transformed = []
    vals, median_vec = constant_nums(ns,eigenvals)
    for val in vals:
        func = lambda x,y: (val, median_vec)
        transformed.append(_discrete_random(ns, mu, r, Q, func))
    #perhaps instead of an expected result we should do sanity-checks (i.e. that transforming
    #back with mu, Q yields the original eigenvals)?
    assert transformed == \
           [[ 2, 33], [ 2, 34], [ 2, 35], [ 3, 33], [ 3, 34], [ 3, 35], [ 4, 33], [ 4, 34],
            [ 4, 35], [ 5, 33], [ 5, 34], [ 5, 35], [ 6, 33], [ 6, 34], [ 6, 35], [ 7, 33],
            [ 7, 34], [ 7, 35], [ 8, 33], [ 8, 34], [ 8, 35], [ 9, 33], [ 9, 34], [ 9, 35],
            [10, 33], [10, 34], [10, 35], [11, 33], [11, 34], [11, 35], [12, 33], [12, 34],
            [12, 35], [13, 33], [13, 34], [13, 35], [14, 33], [14, 34], [14, 35], [15, 33],
            [15, 34], [15, 35], [16, 33], [16, 34], [16, 35], [17, 33], [17, 34], [17, 35],
            [18, 33], [18, 34], [18, 35], [19, 33], [19, 34], [19, 35], [20, 33], [20, 34],
            [20, 35], [21, 33], [21, 34], [21, 35], [22, 33], [22, 34], [22, 35], [23, 33],
            [23, 34], [23, 35], [24, 33], [24, 34], [24, 35], [25, 33], [25, 34], [25, 35],
            [26, 33], [26, 34], [26, 35], [27, 33], [27, 34], [27, 35]]



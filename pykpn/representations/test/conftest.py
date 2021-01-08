# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
import numpy as np
from pykpn.representations import permutations as perm
from pykpn.representations.metric_spaces import FiniteMetricSpace, FiniteMetricSpaceSym

@pytest.fixture
def exampleClusterArch():
    return FiniteMetricSpace( [ [0,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2],
                                [1,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2],
                                [1,1,0,1,2,2,2,2,2,2,2,2,2,2,2,2],
                                [1,1,1,0,2,2,2,2,2,2,2,2,2,2,2,2],
                                [2,2,2,2,0,1,1,1,2,2,2,2,2,2,2,2],
                                [2,2,2,2,1,0,1,1,2,2,2,2,2,2,2,2],
                                [2,2,2,2,1,1,0,1,2,2,2,2,2,2,2,2],
                                [2,2,2,2,1,1,1,0,2,2,2,2,2,2,2,2],
                                [2,2,2,2,2,2,2,2,0,1,1,1,2,2,2,2],
                                [2,2,2,2,2,2,2,2,1,0,1,1,2,2,2,2],
                                [2,2,2,2,2,2,2,2,1,1,0,1,2,2,2,2],
                                [2,2,2,2,2,2,2,2,1,1,1,0,2,2,2,2],
                                [2,2,2,2,2,2,2,2,2,2,2,2,0,1,1,1],
                                [2,2,2,2,2,2,2,2,2,2,2,2,1,0,1,1],
                                [2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,1],
                                [2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,0]])
 
@pytest.fixture
def exampleClusterArchSymmetries(exampleClusterArch, autExampleClusterArch):
    return FiniteMetricSpaceSym(exampleClusterArch, autExampleClusterArch)

@pytest.fixture
def autExampleClusterArch():
    S4 = perm.SymmetricGroupTranspositions(4)
    return perm.ProductGroup([S4,S4,S4,S4]) # this should actually be a wreath product... 

   
@pytest.fixture
def exampleParallella16():
    return generateExampleParallella(4,2,20)

class mockPlatform:
    def __init__(self,adjacency_dict):
        self.adjacency_dict = adjacency_dict
    def to_adjacency_dict(self):
        return self.adjacency_dict

@pytest.fixture
def exampleDijkstraArch(exampleDijkstra):
    return mockPlatform(exampleDijkstra)

@pytest.fixture
def exampleDijkstra():
    # from: https://people.sc.fsu.edu/~jburkardt/m_src/dijkstra/dijkstra.html
    #   N0--15--N2-100--N3
    #     \      |     /
    #      \     |    /
    #       40  20  10
    #         \  |  /
    #          \ | /
    #           N1
    #           / \
    #          /   \
    #         6    25
    #        /       \
    #       /         \
    #     N5----8-----N4
    return {'N0' : [('N1' , 40), ('N2' , 15)], 'N2' : [('N0' , 15), ('N3' , 100), ('N1' , 20)],
                    'N3' : [('N2' , 100), ('N1' , 10)], 'N1': [('N0' , 40), ('N2', 20), ('N3' , 10), ('N5' , 6), ('N4' , 25)],
                    'N4': [('N1' , 25),( 'N5' , 8)], 'N5' : [('N1' , 6), ('N4' , 8)]}

@pytest.fixture
def dimension():
    return 5

@pytest.fixture
def distortion():
    return 1.05

@pytest.fixture
def N():
    return 1000


def generateExampleParallella(n,num_arm,dist_mem):
    mat = np.zeros((n*n+num_arm,n*n+num_arm))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    dist = abs(i-k) + abs(j-l)
                    mat[j*n+i,l*n+k] = dist
    for i in range(n*n,n*n+num_arm):
        mat[i,i] = 0
        for j in range(n*n):
            mat[i,j] = dist_mem
            mat[j,i] = dist_mem
        for j in range(i+1,n*n+num_arm):
            mat[i,j] = 1
            mat[j,i] = 1
    #print(mat)
    return FiniteMetricSpace(mat)

@pytest.fixture
def D():
    return np.array([
    [0., 2., 2., 4., 2., 4., 4., 4., 4., 4., 4., 4., 2., 4., 2., 2., 4., 2., 4., 2.],
    [2., 0., 4., 2., 2., 4., 4., 4., 2., 4., 2., 4., 4., 4., 4., 2., 4., 2., 2., 4.],
    [2., 4., 0., 4., 4., 2., 2., 4., 4., 4., 4., 4., 2., 4., 2., 4., 2., 4., 2., 2.],
    [4., 2., 4., 0., 4., 4., 4., 4., 2., 2., 1., 4., 4., 2., 2., 4., 4., 4., 2., 4.],
    [2., 2., 4., 4., 0., 4., 2., 4., 4., 4., 4., 2., 4., 2., 4., 2., 2., 2., 4., 4.],
    [4., 4., 2., 4., 4., 0., 2., 2., 4., 2., 4., 4., 4., 4., 4., 2., 2., 2., 2., 4.],
    [4., 4., 2., 4., 2., 2., 0., 4., 4., 4., 4., 2., 4., 2., 4., 4., 1., 4., 2., 4.],
    [4., 4., 4., 4., 4., 2., 4., 0., 2., 2., 4., 2., 2., 4., 4., 2., 4., 2., 4., 2.],
    [4., 2., 4., 2., 4., 4., 4., 2., 0., 4., 2., 2., 2., 4., 4., 4., 4., 4., 2., 2.],
    [4., 4., 4., 2., 4., 2., 4., 2., 4., 0., 2., 4., 4., 2., 2., 2., 4., 2., 4., 4.],
    [4., 2., 4., 1., 4., 4., 4., 4., 2., 2., 0., 4., 4., 2., 2., 4., 4., 4., 2., 4.],
    [4., 4., 4., 4., 2., 4., 2., 2., 2., 4., 4., 0., 2., 2., 4., 4., 2., 4., 4., 2.],
    [2., 4., 2., 4., 4., 4., 4., 2., 2., 4., 4., 2., 0., 4., 2., 4., 4., 4., 4., 1.],
    [4., 4., 4., 2., 2., 4., 2., 4., 4., 2., 2., 2., 4., 0., 2., 4., 2., 4., 4., 4.],
    [2., 4., 2., 2., 4., 4., 4., 4., 4., 2., 2., 4., 2., 2., 0., 4., 4., 4., 4., 2.],
    [2., 2., 4., 4., 2., 2., 4., 2., 4., 2., 4., 4., 4., 4., 4., 0., 4., 1., 4., 4.],
    [4., 4., 2., 4., 2., 2., 1., 4., 4., 4., 4., 2., 4., 2., 4., 4., 0., 4., 2., 4.],
    [2., 2., 4., 4., 2., 2., 4., 2., 4., 2., 4., 4., 4., 4., 4., 1., 4., 0., 4., 4.],
    [4., 2., 2., 2., 4., 2., 2., 4., 2., 4., 2., 4., 4., 4., 4., 4., 2., 4., 0., 4.],
    [2., 4., 2., 4., 4., 4., 4., 2., 2., 4., 4., 2., 1., 4., 2., 4., 4., 4., 4., 0.]])


@pytest.fixture
def d():
    return 11

@pytest.fixture
def k():
    return 17

@pytest.fixture
def split_d():
    return 8

@pytest.fixture
def split_k():
    return 12

@pytest.fixture
def n():
    return 5


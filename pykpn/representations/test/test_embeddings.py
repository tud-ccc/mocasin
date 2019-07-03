# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Felix Teweleit


from pykpn.representations.embeddings import MetricSpaceEmbeddingBase, MetricSpaceEmbedding
from pykpn.representations.metric_spaces import FiniteMetricSpaceLP
import numpy as np
import pytest

class TestEmbeddings(object):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    
    def test_approx(self, exampleClusterArch):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)
        
        result = E.approx(np.random.random(E.k))
        
        for value in result:
            assert(value < 1.0 and value > -1.0)
        
    def test_Evec(self, exampleClusterArch, dimension, distortion):
        M = exampleClusterArch
        MLP = FiniteMetricSpaceLP(M, dimension,p=2)
        Evec = MetricSpaceEmbedding(M, dimension)
        in1 = [1,0,1,1,3]
        in2 = [0,0,2,1,0]
        dist = MLP.dist(in1,in2)

        evec1 = Evec.i(in1)
        evec2 = Evec.i(in2)
        assert(len(evec1) == dimension)
        assert(len(evec1[0]) == M.n)
        dist_embedded = np.linalg.norm(np.array(evec1).flatten()
                                       - np.array(evec2).flatten())
        assert(dist / distortion < dist_embedded and dist_embedded < dist * distortion)

        
    def test_Evec_inv(self, exampleClusterArch, dimension):
        M = exampleClusterArch
        Evec = MetricSpaceEmbedding(M, dimension)
        
        result = Evec.inv(Evec.i([1,0,1,1,3]))
        assert(list(np.around(result).astype(int)) == [1, 0, 1, 1, 3])
        
    def test_Evec_invapprox(self, exampleClusterArch, dimension):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)
        Evec = MetricSpaceEmbedding(M, dimension)
        
        result = Evec.invapprox(np.random.random((dimension*E.k)).flatten())
        
        for value in result:
            assert(value >= 0 and value < 16)
            
    def test_Par_invapprox(self, exampleParallella16, dimension):
        Par = MetricSpaceEmbedding(exampleParallella16, dimension,distortion=1.5)
        
        result = Par.invapprox((10*np.random.random((dimension,Par.k))).flatten())
        for value in result:
            assert(value >= 0 and value < 16)
    
    @pytest.mark.skip("Test can't succeed. Need fix by Goens.")
    def test_L(self, distortion):
        D = self.__give_matrix()
        L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D, distortion))
        
        assert(L ==  None)
    
    @pytest.mark.skip("Test can't succeed. Need fix by Goens.")
    def test_vecs(self, distortion):
        D = self.__give_matrix()
        L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D, distortion))
        vecs = L.A
        
        assert(vecs == None)
    
    @pytest.mark.skip("Test can't succeed. Need fix by Goens.")
    def test_dist(self, distortion):
        D = self.__give_matrix()
        L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D, distortion))
        vecs = L.A
        
        dists = []
        for i,v in enumerate(vecs):
            for j,w in enumerate(vecs):
                if D[i,j] != 0:
                    dists.append(np.linalg.norm(v-w)/D[i,j])
        
        assert(dists == None)
    
    
    def __give_matrix(self):
        return np.matrix([[ 0.,  2.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  2.,  4.,  2., 4.,  2.],
                [ 2.,  0.,  4.,  2.,  2.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  4.,  2., 2.,  4.],
                [ 2.,  4.,  0.,  4.,  4.,  2.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  2.,  4., 2.,  2.],
                [ 4.,  2.,  4.,  0.,  4.,  4.,  4.,  4.,  2.,  2.,  1.,  4.,  4.,  2.,  2.,  4.,  4.,  4., 2.,  4.],
                [ 2.,  2.,  4.,  4.,  0.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  2.,  2.,  2., 4.,  4.],
                [ 4.,  4.,  2.,  4.,  4.,  0.,  2.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  2.,  2., 2.,  4.],
                [ 4.,  4.,  2.,  4.,  2.,  2.,  0.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  4.,  1.,  4., 2.,  4.],
                [ 4.,  4.,  4.,  4.,  4.,  2.,  4.,  0.,  2.,  2.,  4.,  2.,  2.,  4.,  4.,  2.,  4.,  2., 4.,  2.],
                [ 4.,  2.,  4.,  2.,  4.,  4.,  4.,  2.,  0.,  4.,  2.,  2.,  2.,  4.,  4.,  4.,  4.,  4., 2.,  2.],
                [ 4.,  4.,  4.,  2.,  4.,  2.,  4.,  2.,  4.,  0.,  2.,  4.,  4.,  2.,  2.,  2.,  4.,  2., 4.,  4.],
                [ 4.,  2.,  4.,  1.,  4.,  4.,  4.,  4.,  2.,  2.,  0.,  4.,  4.,  2.,  2.,  4.,  4.,  4., 2.,  4.],
                [ 4.,  4.,  4.,  4.,  2.,  4.,  2.,  2.,  2.,  4.,  4.,  0.,  2.,  2.,  4.,  4.,  2.,  4., 4.,  2.],
                [ 2.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  2.,  4.,  4.,  2.,  0.,  4.,  2.,  4.,  4.,  4., 4.,  1.],
                [ 4.,  4.,  4.,  2.,  2.,  4.,  2.,  4.,  4.,  2.,  2.,  2.,  4.,  0.,  2.,  4.,  2.,  4., 4.,  4.],
                [ 2.,  4.,  2.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  2.,  4.,  2.,  2.,  0.,  4.,  4.,  4., 4.,  2.],
                [ 2.,  2.,  4.,  4.,  2.,  2.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  0.,  4.,  1., 4.,  4.],
                [ 4.,  4.,  2.,  4.,  2.,  2.,  1.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  4.,  0.,  4., 2.,  4.],
                [ 2.,  2.,  4.,  4.,  2.,  2.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  1.,  4.,  0., 4.,  4.],
                [ 4.,  2.,  2.,  2.,  4.,  2.,  2.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  4., 0.,  4.],
                [ 2.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  2.,  4.,  4.,  2.,  1.,  4.,  2.,  4.,  4.,  4., 4.,  0.]])


#Remaining original code from goens. Need to be checked!
# D = np.matrix([[ 0.,  2.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  2.,  4.,  2., 4.,  2.],
#                [ 2.,  0.,  4.,  2.,  2.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  4.,  2., 2.,  4.],
#                [ 2.,  4.,  0.,  4.,  4.,  2.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  2.,  4., 2.,  2.],
#                [ 4.,  2.,  4.,  0.,  4.,  4.,  4.,  4.,  2.,  2.,  1.,  4.,  4.,  2.,  2.,  4.,  4.,  4., 2.,  4.],
#                [ 2.,  2.,  4.,  4.,  0.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  2.,  2.,  2., 4.,  4.],
#                [ 4.,  4.,  2.,  4.,  4.,  0.,  2.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  2.,  2., 2.,  4.],
#                [ 4.,  4.,  2.,  4.,  2.,  2.,  0.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  4.,  1.,  4., 2.,  4.],
#                [ 4.,  4.,  4.,  4.,  4.,  2.,  4.,  0.,  2.,  2.,  4.,  2.,  2.,  4.,  4.,  2.,  4.,  2., 4.,  2.],
#                [ 4.,  2.,  4.,  2.,  4.,  4.,  4.,  2.,  0.,  4.,  2.,  2.,  2.,  4.,  4.,  4.,  4.,  4., 2.,  2.],
#                [ 4.,  4.,  4.,  2.,  4.,  2.,  4.,  2.,  4.,  0.,  2.,  4.,  4.,  2.,  2.,  2.,  4.,  2., 4.,  4.],
#                [ 4.,  2.,  4.,  1.,  4.,  4.,  4.,  4.,  2.,  2.,  0.,  4.,  4.,  2.,  2.,  4.,  4.,  4., 2.,  4.],
#                [ 4.,  4.,  4.,  4.,  2.,  4.,  2.,  2.,  2.,  4.,  4.,  0.,  2.,  2.,  4.,  4.,  2.,  4., 4.,  2.],
#                [ 2.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  2.,  4.,  4.,  2.,  0.,  4.,  2.,  4.,  4.,  4., 4.,  1.],
#                [ 4.,  4.,  4.,  2.,  2.,  4.,  2.,  4.,  4.,  2.,  2.,  2.,  4.,  0.,  2.,  4.,  2.,  4., 4.,  4.],
#                [ 2.,  4.,  2.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  2.,  4.,  2.,  2.,  0.,  4.,  4.,  4., 4.,  2.],
#                [ 2.,  2.,  4.,  4.,  2.,  2.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  0.,  4.,  1., 4.,  4.],
#                [ 4.,  4.,  2.,  4.,  2.,  2.,  1.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  4.,  4.,  0.,  4., 2.,  4.],
#                [ 2.,  2.,  4.,  4.,  2.,  2.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  1.,  4.,  0., 4.,  4.],
#                [ 4.,  2.,  2.,  2.,  4.,  2.,  2.,  4.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  2.,  4., 0.,  4.],
#                [ 2.,  4.,  2.,  4.,  4.,  4.,  4.,  2.,  2.,  4.,  4.,  2.,  1.,  4.,  2.,  4.,  4.,  4., 4.,  0.]])

# L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D,distortion))
# vecs = L.A
# dists = []
# for i,v in enumerate(vecs):
#     for j,w in enumerate(vecs):
#         if D[i,j] != 0:
#             dists.append(np.linalg.norm(v-w)/D[i,j])

#print(vecs)
#print(np.mean(dists))


#print(L)

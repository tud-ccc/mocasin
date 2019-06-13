# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Felix Teweleit


import unittest
from pykpn.representations.embeddings import *
import pykpn.representations.metric_spaces as metric
from pykpn.representations.examples import *
import numpy as np


class test_Embeddings(unittest.TestCase):
    
    def setUp(self):
        self.dimension = 5
        self.distortion = 1.05
        
    def tearDown(self):
        pass

    
    def test_approx(self):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)
        
        result = E.approx(np.random.random(E.k))
        
        for value in result:
            self.assertTrue(value < 1.0 and value > -1.0, 'Error in approx()! Value out of range:' + str(value))
        
    def test_Evec(self):
        M = exampleClusterArch
        MLP = FiniteMetricSpaceLP(M,self.dimension,p=2)
        Evec = MetricSpaceEmbedding(M,self.dimension)
        in1 = [1,0,1,1,3]
        in2 = [0,0,2,1,0]
        dist = MLP.dist(in1,in2)

        evec1 = Evec.i(in1)
        evec2 = Evec.i(in2)
        self.assertEqual(len(evec1), self.dimension,
                        'Error in i()!')
        self.assertEqual(len(evec1[0]), M.n,
                        'Error in i()!')
        dist_embedded = np.linalg.norm(np.array(np.array(evec1).flat)
                                       - np.array(np.array(evec2).flat))
        self.assertTrue(dist / self.distortion < dist_embedded and
                        dist_embedded < dist * self.distortion,
                        f"Error in embedding distance! {dist}/{self.distortion}"+
                        f"< {dist_embedded} !< {dist} * {self.distortion}")

        
    def test_Evec_inv(self):
        M = exampleClusterArch
        Evec = MetricSpaceEmbedding(M,self.dimension)
        
        result = Evec.inv(Evec.i([1,0,1,1,3]))
        self.assertListEqual(result, [1, 0, 1, 1, 3], 'Error in inv() or i()!')
        
    def test_Evec_invapprox(self):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)
        Evec = MetricSpaceEmbedding(M,self.dimension)
        
        result = Evec.invapprox(list(np.random.random((self.dimension*E.k)).flat))
        
        for value in result:
            self.assertTrue(value >= 0 and value < 16, 'Error in invapprox()! Value out of range:' + str(value))
            
    def test_Par_invapprox(self):
        Par = MetricSpaceEmbedding(exampleParallella16,self.dimension,distortion=1.5)
        
        result = Par.invapprox(list((10*np.random.random((self.dimension,Par.k))).flat))
        for value in result:
            self.assertTrue(value >= 0 and value < 16, 'Error in invapprox()! Value out of range: ' + str(value))
    
    @unittest.expectedFailure
    def test_L(self):
        D = self.__give_matrix()
        L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D,self.distortion))
        
        self.assertEqual(L, None, 'Error in algorithm! Please check!')
    
    @unittest.expectedFailure
    def test_vecs(self):
        D = self.__give_matrix()
        L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D,self.distortion))
        vecs = L.A
        
        self.assertEqual(vecs, None, 'Error in algorithm! Please check!')
    
    @unittest.expectedFailure
    def test_dist(self):
        D = self.__give_matrix()
        L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D,self.distortion))
        vecs = L.A
        
        dists = []
        for i,v in enumerate(vecs):
            for j,w in enumerate(vecs):
                if D[i,j] != 0:
                    dists.append(np.linalg.norm(v-w)/D[i,j])
        
        self.assertListEqual(dists, None, 'Error in algorithm! PLease check!')
    
    
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

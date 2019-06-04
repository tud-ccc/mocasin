# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Andrès Goens, Felix Teweleit


import unittest
from pykpn.representations.embeddings import *
import pykpn.representations.metric_spaces as metric
from pykpn.representations.examples import *

class test_Embeddings(unittest.TestCase):
    
    def setUp(self):
        self.helpvar = 5
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
        Evec = MetricSpaceEmbedding(M,self.helpvar)
        
        result = Evec.i([1,0,1,1,3])
        self.assertEqual(result, [(0.8633706466147922, 0.9388001940469392, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                                (1.2754429339561864, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                                (0.8633706466147922, 0.9388001940469392, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                                (0.8633706466147922, 0.9388001940469392, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                                (0.8633706466147969, 0.37896361699745584, 0.2470070582420815, 0.8226298648319808, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0)],
                        'Error in i()!')
        
    def test_Evec_inv(self):
        M = exampleClusterArch
        Evec = MetricSpaceEmbedding(M,self.helpvar)
        
        result = Evec.inv(Evec.i([1,0,1,1,3]))
        self.assertListEqual(result, [1, 0, 1, 1, 3], 'Error in inv() or i()!')
        
    def test_Evec_invapprox(self):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)
        Evec = MetricSpaceEmbedding(M,self.helpvar)
        
        result = Evec.invapprox(list(np.random.random((self.helpvar*E.k)).flat))
        
        for value in result:
            self.assertTrue(value >= 0 and value < 16, 'Error in invapprox()! Value out of range:' + str(value))
            
    def test_Par_invapprox(self):
        Par = MetricSpaceEmbedding(exampleParallella16,self.helpvar,distortion=1.5)
        
        result = Par.invapprox(list((10*np.random.random((self.helpvar,Par.k))).flat))
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
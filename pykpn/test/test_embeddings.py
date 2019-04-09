import unittest
from pykpn.representations.embeddings import *
import pykpn.representations.metric_spaces as metric
from pykpn.representations.examples import *


class Embeddings_Test(unittest.TestCase):
    
    def setUp(self):
        self.helpvar = 5
        
        np.set_printoptions(threshold=np.nan)
        self.M = exampleClusterArch 
        self.E = MetricSpaceEmbeddingBase(self.M)
        self.Evec = MetricSpaceEmbedding(M,self.helpvar)
        
        self.Par = MetricSpaceEmbedding(exampleParallella16,self.helpvar,distortion=1.5)
        
        self.D = np.matrix([[ 0.,  2.,  2.,  4.,  2.,  4.,  4.,  4.,  4.,  4.,  4.,  4.,  2.,  4.,  2.,  2.,  4.,  2., 4.,  2.],
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
        
        self.L = np.matrix(MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(self.D,distortion))
        self.vecs = self.L.A
        
    def tearDown(self):
        pass

    
    def test_approx(self):
        result = self.E.approx(np.random.random(self.E.k))
        self.assertEqual(result, None, "Test case needs to be implemented")
        
    def test_Evec(self):
        result = self.Evec.i([1,0,1,1,3])
        self.assertEqual(result, None, "Test case needs to be implemented")
        
    def test_Evec_inv(self):
        result = self.Evec.inv(self.Evec.i([1,0,1,1,3]))
        self.assertEqual(result, None, "Test case needs to be implemented")
        
    def test_Evec_invapprox(self):
        result = self.Evec.invapprox(list(np.random.random((self.helpvar,E.k))))
        self.assertEqual(result, None, "Test case needs to be implemented")
    
    def test_Par_invapprox(self):
        result = self.Par.invapprox(list(10*np.random.random((self.helpvar,Par.k))))
        self.assertEqual(result, None, "Test case needs to be implemented")
    
    def test_L(self):
        self.assertEqual(self.L, None, "Test case needs to be implemented")
    
    def test_vecs(self):
        self.assertEqual(self.vecs, None, "Test case needs to be implemented")
    
    def test_dist(self):
        dists = []
        for i,v in enumerate(self.vecs):
            for j,w in enumerate(self.vecs):
                if self.fD[i,j] != 0:
                    dists.append(np.linalg.norm(v-w)/self.D[i,j])
        
        self.assertListEqual(dists, None, "Test case needs to be implemented")

    
np.set_printoptions(threshold=np.nan)


distortion = 1.05
M = exampleClusterArch 
E = MetricSpaceEmbeddingBase(M)
print(E.approx(np.random.random(E.k)))
d=5
Evec = MetricSpaceEmbedding(M,d)
print(Evec.i([1,0,1,1,3]))
print(Evec.inv(Evec.i([1,0,1,1,3])))
print(Evec.invapprox(list(np.random.random((d,E.k)))))

Par = MetricSpaceEmbedding(exampleParallella16,d,distortion=1.5)
print(Par.invapprox(list(10*np.random.random((d,Par.k)))))



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

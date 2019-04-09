import unittest
from pykpn.representations.metric_spaces import *
from pykpn.representations.examples import *

class Metric_Spaces_Test(unittest.TestCase):
    
    def setUp(self):
        self.N = 10000
        self.testSpace = exampleClusterArch
        self.runs = self.testSpace.uniformFromBall(3,1,self.N)
        self.testProdSpace = FiniteMetricSpaceLP(self.testSpace,d=3)
        self.uniformFromFourBall = self.testProdSpace.uniformFromBall([3,2,7],4,10)
        self.oneBall = self.testProdSpace.ball([3,2,7],1)
        self.testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        #self.testLargeProdSpace = FiniteMetricSpaceLP(self.testSpace,d=13)
        #self.uniformFromLargeBall = self.testLargeProdSpace.uniformFromBall([1,3,15,10,9,0,0,3,2,7,1,0,12],3,10)
    
    def tearDown(self):
        pass
    
    def test_dijkstra(self):
        self.assertTupleEqual(arch_graph_to_distance_metric(exampleDiijkstra),
                              ([[0, 15, 45, 35, 49, 41], [15, 0, 30, 20, 34, 26], [45, 30, 0, 10, 24, 16],[35, 20, 10, 0, 14, 6],
                                [49, 34, 24, 14, 0, 8], [41, 26, 16, 6, 8, 0]], {0: 'N0', 1: 'N2', 2: 'N3', 3: 'N1', 4: 'N4', 5: 'N5'},
                                {'N0': 0, 'N2': 1, 'N3': 2, 'N1': 3, 'N4': 4, 'N5': 5}),
                              'Error performing dijkstra')

    def test_probabilities(self):
        result = list(zip(range(4),map(lambda x : len(x)/float(self.N), [ [run for run in self.runs if run == i] for i in range(4)])))
        self.assertListEqual(result, [(0, 0.3415), (1, 0.3233), (2, 0.3352), (3, 0.0)], 'Error calculating probabilities')
        
    def test_uniform_in_ball_length(self):
        result = len(self.testProdSpace.ball([3,2,7],4))
        self.assertEqual(result, 1072, "Error in ball()")
    
    def test_uniform_in_ball_list(self):
        self.assertListEqual(self.uniformFromFourBall, [147, 1971, 1035, 1219, 1301, 1886, 2560, 530, 115, 1983], 'Error in uniformFromBall()')
        
    def test_uniform_in_ball_in2tuple(self):
        result = list(map(self.testProdSpace.int2Tuple, self.uniformFromFourBall))
        self.assertListEqual(result, [[3, 13, 10], [2, 1, 7], [14, 7, 7], [0, 11, 7], [5, 3, 5], [4, 2, 12], [0, 0, 9], [2, 0, 15], [2, 1, 0], [3, 13, 3]],
                            'Error in int2Tuple()')
        
    def test_dist_calc(self):
        result = self.testProdSpace._distCalc([3,2,7],[3,0,4])
        self.assertEqual(result, 2.0, 'Error in _distCalc()')
        
    def test_dist(self):
        result = []
        for j in self.uniformFromFourBall:
            result.append(self.testProdSpace.dist(self.testProdSpace.tuple2Int([3,2,7]),j))
        self.assertListEqual(result, [4.0, 2.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0], 'Error in dist()')
    
    def test_ball_as_tuple(self):
        result = list(map( self.testProdSpace.int2Tuple, self.oneBall ))
        self.assertListEqual(result, [[3, 2, 4], [3, 2, 5], [3, 2, 6], [3, 0, 7], [3, 1, 7], [0, 2, 7], [1, 2, 7], [2, 2, 7], [3, 2, 7], [3, 3, 7]],
                            'Error in ball()')
    
    def test_one_ball_length(self):
        self.assertEqual(len(self.oneBall), 10, 'Error in ball()')
        
    def test_sym_space_length(self):
        result = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=2).n
        self.assertEqual(result, 20, 'Error in calculating sym_space length')
    
    def test_dist_1(self):
        result = exampleClusterArchSymmetries.dist([3],[4])
        self.assertEqual(result, 2, 'Error in dist() with ClusterArchsymmetries')
    
    def test_dist_2(self):
        result = exampleClusterArchSymmetries.dist([3],[0])
        self.assertEqual(result, 0, 'Error in dist() with ClusterArchsymmetries')
    
    def test_dist_3(self):
        result = self.testSymSpace.dist([3,2,7],[3,0,4])
        self.assertEqual(result, 0.0, 'Error in dist() with SymSpace')
        
    def test_dist_4(self):
        result = self.testSymSpace.dist([3,4,7],[3,0,4])
        self.assertEqual(result, 2.0, 'Error in dist() with SymSpace')
    
    def test_dist_5(self):
        result = self.testSymSpace.dist([3,4,3],[5,11,4])
        self.assertEqual(result, 6.0, 'Error in dist() with SymSpace')
        
    def test_tuple_orbit(self):
        result = autExampleClusterArch.tuple_orbit([3,4,3])
        self.assertEqual(result, None, "Test case not implemented")
    
    def test_something(self):
        result = list(map(self.testProdSpace.int2Tuple,self.uniformFromLargeBall))
        self.assertEqual(result, None, "Test case not implemented")
"""
print("using dijkstra everywhere:" + str(arch_graph_to_distance_metric(exampleDiijkstra)))
N = 10000
testSpace = exampleClusterArch
runs = testSpace.uniformFromBall(3,1,N)
print("probabilities for " + str(N) +" runs:  " + str(list(zip(range(4),map(lambda x : len(x)/float(N), [ [run for run in runs if run == i] for i in range(4)])))))

testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
print("uniform in ball [3,2,7], 4  (" + str(len(testProdSpace.ball([3,2,7],4))) +" elements): " + str(uniformFromFourBall) + " = " + str(list(map(testProdSpace.int2Tuple,uniformFromFourBall))))
print("dist([3,2,7],[3,0,4] = " + str(testProdSpace._distCalc([3,2,7],[3,0,4])))
print("; ".join( [ "dist( [3,2,7]," + str(testProdSpace.int2Tuple(j)) + ") = " + str(testProdSpace.dist(testProdSpace.tuple2Int([3,2,7]),j))  for j in uniformFromFourBall]))
oneBall = testProdSpace.ball([3,2,7],1)
print("the ball [3,2,7] , 1 (as tuples) " + str(list(map( testProdSpace.int2Tuple, oneBall ))))
assert(len(oneBall)==10)

testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
print("sym_space with d=2 has length: " + str(FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=2).n))
print("dist_sym(3,4) = " + str(exampleClusterArchSymmetries.dist([3],[4]))) # should be 2, 0 if we have wreath
print("dist_sym(3,0) = " + str(exampleClusterArchSymmetries.dist([3],[0]))) # should be 0
print("dist_sym([3,2,7],[3,0,4]) = " + str(testSymSpace.dist([3,2,7],[3,0,4]))) # should be 0
print("dist_sym([3,4,7],[3,0,4]) = " + str(testSymSpace.dist([3,4,7],[3,0,4]))) # should be 2
print("dist_sym([3,4,3],[5,11,4]) = " + str(testSymSpace.dist([3,4,3],[5,11,4]))) #should be 6, 1 if we have wreath
#print(autExampleClusterArch.tuple_orbit([3,4,3]))
#testLargeProdSpace = finiteMetricSpaceLP(testSpace,d=13)
#uniformFromLargeBall = testLargeProdSpace.uniformFromBall([1,3,15,10,9,0,0,3,2,7,1,0,12],3,10)
#print("uniform in ball [1,3,15,10,9,0,0,3,2,7,1,0,12], 3  (" + str(len(testProdSpace.ball([1,3,15,10,9,0,0,3,2,7,1,0,12],3))) +" elements): " + str(unifromFromLargeBall) + " = " + str(list(map(testProdSpace.int2Tuple,uniformFromLargeBall))))
"""
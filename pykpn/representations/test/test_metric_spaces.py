# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Andrès Goens, Felix Teweleit

import unittest
from pykpn.representations.metric_spaces import *
from pykpn.representations.examples import *

class test_MetricSpaces(unittest.TestCase):
    
    def setUp(self):
        self.N = 10000
        
    def tearDown(self):
        pass
    
    def test_dijkstra(self):
        self.assertTupleEqual(arch_graph_to_distance_metric(exampleDiijkstra),
                              ([[0, 15, 45, 35, 49, 41], [15, 0, 30, 20, 34, 26], [45, 30, 0, 10, 24, 16],[35, 20, 10, 0, 14, 6],
                                [49, 34, 24, 14, 0, 8], [41, 26, 16, 6, 8, 0]], {0: 'N0', 1: 'N2', 2: 'N3', 3: 'N1', 4: 'N4', 5: 'N5'},
                                {'N0': 0, 'N2': 1, 'N3': 2, 'N1': 3, 'N4': 4, 'N5': 5}),
                              'Error performing dijkstra')

    def test_finiteMetricSpace_uniformFromBall(self):
        testSpace = exampleClusterArch
        runs = testSpace.uniformFromBall(3,1,self.N)
        result = list(zip(range(4),map(lambda x : len(x)/float(self.N), [ [run for run in runs if run == i] for i in range(4)])))
        
        for probabilitie in result:
            self.assertTrue((probabilitie[1] == 0.0 or (probabilitie[1] >= 0.3 and probabilitie[1] <= 0.35)), 'Error calculating probabilities')
        
    def test_finiteMetricSpaceLP_ball1(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        
        result = len(testProdSpace.ball([3,2,7],4))
        self.assertEqual(result, 1072, "Error in ball()")
        
    def test_finiteMetricSpaceLP_ball2(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        oneBall = testProdSpace.ball([3,2,7],1)
        
        result = list(map(testProdSpace.int2Tuple, oneBall ))
        self.assertListEqual(result, [[3, 2, 4], [3, 2, 5], [3, 2, 6], [3, 0, 7], [3, 1, 7], [0, 2, 7], [1, 2, 7], [2, 2, 7], [3, 2, 7], [3, 3, 7]],
                            'Error in ball()')
    
    def test_finiteMetricSpaceLP_uniformFromBall1(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
        
        self.assertTrue(len(uniformFromFourBall) == 10, 'Error in uniformFromBall(). To many output values!')
        
        for value in uniformFromFourBall:
            self.assertTrue(testProdSpace.dist(testProdSpace.tuple2Int([3,2,7]), value) <= 4.0,
                            'Error in uniformFromBall(). Points out of ball!')
        
    def test_finiteMetricSpaceLP_uniformFromBall2(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
        
        result = list(map(testProdSpace.int2Tuple, uniformFromFourBall))
        result = list(map(testProdSpace.tuple2Int, result))
        self.assertListEqual(result, uniformFromFourBall,'Error in int2Tuple()')
        
    def test_finiteMetricSpaceLP_calc(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        
        result = testProdSpace._distCalc([3,2,7],[3,0,4])
        self.assertEqual(result, 2.0, 'Error in _distCalc()')
        
    def test_finiteMetricSpaceLP_dist(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
        
        result = []
        for j in uniformFromFourBall:
            result.append(testProdSpace.dist(testProdSpace.tuple2Int([3,2,7]),j))
        
        self.assertTrue(len(result) == 10, 'Error in dist(). To many output values!')
        
        for value in result:
            self.assertTrue((value <= 4.0), 'Error in dist(). Value outside of the ball!')
    
    def test_finiteMetricSpaceLP_uniform(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        
        result = testProdSpace.uniform()
        for value in result:
            self.assertTrue((testProdSpace.dist([3,2,7], testProdSpace.int2Tuple(value)) <= 5,
                             'Error in uniform()'))
    
    def test_finiteMetricSpaceLP_oneBall(self):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        oneBall = testProdSpace.ball([3,2,7],1)
        
        self.assertEqual(len(oneBall), 10, 'Error in ball()')
        
    def test_FiniteMetricSpaceLPSym_length(self):
        result = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=2).n
        self.assertEqual(result, 20, 'Error in calculating sym_space length')
        
    def test_dist_1(self):
        result = exampleClusterArchSymmetries.dist([3],[4])
        self.assertEqual(result, 2, 'Error in dist() with ClusterArchsymmetries')
    
    def test_dist_2(self):
        result = exampleClusterArchSymmetries.dist([3],[0])
        self.assertEqual(result, 0, 'Error in dist() with ClusterArchsymmetries')
    
    def test_dist_3(self):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        result = testSymSpace.dist([3,2,7],[3,0,4])
        self.assertEqual(result, 0.0, 'Error in dist() with SymSpace')
        
    def test_dist_4(self):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        result = testSymSpace.dist([3,4,7],[3,0,4])
        self.assertEqual(result, 2.0, 'Error in dist() with SymSpace')
    
    def test_dist_5(self):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        result = testSymSpace.dist([3,4,3],[5,11,4])
        self.assertEqual(result, 6.0, 'Error in dist() with SymSpace')
        
    def test_tuple_orbit(self):
        result = autExampleClusterArch.tuple_orbit([3,4,3])
        self.assertEqual(result, frozenset({(3, 4, 3), (0, 7, 0), (2, 6, 2), (1, 7, 1), (2, 7, 2), (1, 4, 1), (2, 4, 2), (0, 4, 0), 
                                            (1, 6, 1), (3, 5, 3), (3, 6, 3), (1, 5, 1), (0, 5, 0), (2, 5, 2), (3, 7, 3), (0, 6, 0)}),
                                            "Error in tuple_orbit()")
if __name__ == "__main__":
    unittest.main()
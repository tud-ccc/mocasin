# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Andrès Goens, Felix Teweleit


from pykpn.representations.metric_spaces import arch_graph_to_distance_metric, FiniteMetricSpaceLP, FiniteMetricSpaceLPSym

class TestMetricSpaces(object):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_dijkstra(self, exampleDijkstra):
        assert(arch_graph_to_distance_metric(exampleDijkstra) ==
                              ([[0, 15, 45, 35, 49, 41], [15, 0, 30, 20, 34, 26], [45, 30, 0, 10, 24, 16],[35, 20, 10, 0, 14, 6],
                                [49, 34, 24, 14, 0, 8], [41, 26, 16, 6, 8, 0]], {0: 'N0', 1: 'N2', 2: 'N3', 3: 'N1', 4: 'N4', 5: 'N5'},
                                {'N0': 0, 'N2': 1, 'N3': 2, 'N1': 3, 'N4': 4, 'N5': 5}))

    def test_finiteMetricSpace_uniformFromBall(self, exampleClusterArch, N):
        testSpace = exampleClusterArch
        runs = testSpace.uniformFromBall(3,1,N)
        result = list(zip(range(4),map(lambda x : len(x)/float(N), [ [run for run in runs if run == i] for i in range(4)])))
        
        for probabilitie in result:
            assert((probabilitie[1] == 0.0 or probabilitie[1] >= 0.3) and probabilitie[1] <= 0.35)
        
    def test_finiteMetricSpaceLP_ball1(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        
        result = len(testProdSpace.ball([3,2,7],4))
        assert(result == 1072)
        
    def test_finiteMetricSpaceLP_ball2(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        oneBall = testProdSpace.ball([3,2,7],1)
        
        result = list(map(testProdSpace.int2Tuple, oneBall ))
        assert(result == [[3, 2, 4], [3, 2, 5], [3, 2, 6], [3, 0, 7], [3, 1, 7], [0, 2, 7], [1, 2, 7], [2, 2, 7], [3, 2, 7], [3, 3, 7]])
    
    def test_finiteMetricSpaceLP_uniformFromBall1(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
        
        assert(len(uniformFromFourBall) == 10)
        
        for value in uniformFromFourBall:
            assert(testProdSpace.dist(testProdSpace.tuple2Int([3,2,7]), value) <= 4.0)
        
    def test_finiteMetricSpaceLP_uniformFromBall2(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
        
        result = list(map(testProdSpace.int2Tuple, uniformFromFourBall))
        result = list(map(testProdSpace.tuple2Int, result))
        assert(result == uniformFromFourBall)
        
    def test_finiteMetricSpaceLP_calc(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        
        result = testProdSpace._distCalc([3,2,7],[3,0,4])
        assert(result == 2.0)
        
    def test_finiteMetricSpaceLP_dist(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
        
        result = []
        for j in uniformFromFourBall:
            result.append(testProdSpace.dist(testProdSpace.tuple2Int([3,2,7]),j))
        
        assert(len(result) == 10)
        
        for value in result:
            assert(value <= 4.0)
    
    def test_finiteMetricSpaceLP_uniform(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        
        result = testProdSpace.uniform()
        for value in result:
            assert(testProdSpace.dist([3,2,7], testProdSpace.int2Tuple(value)) <= 5)
            
    def test_finiteMetricSpaceLP_oneBall(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace,d=3)
        oneBall = testProdSpace.ball([3,2,7],1)
        
        assert(len(oneBall) == 10)
        
    def test_FiniteMetricSpaceLPSym_length(self, exampleClusterArchSymmetries):
        result = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=2).n
        assert(result == 20)
        
    def test_dist_1(self, exampleClusterArchSymmetries):
        result = exampleClusterArchSymmetries.dist([3],[4])
        assert(result == 2)
    
    def test_dist_2(self, exampleClusterArchSymmetries):
        result = exampleClusterArchSymmetries.dist([3],[0])
        assert(result == 0)
    
    def test_dist_3(self, exampleClusterArchSymmetries):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        result = testSymSpace.dist([3,2,7],[3,0,4])
        assert(result == 0.0)
        
    def test_dist_4(self, exampleClusterArchSymmetries):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        result = testSymSpace.dist([3,4,7],[3,0,4])
        assert(result == 2.0)
    
    def test_dist_5(self, exampleClusterArchSymmetries):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
        
        result = testSymSpace.dist([3,4,3],[5,11,4])
        assert(result == 6.0)
        
    def test_tuple_orbit(self, autExampleClusterArch):
        result = autExampleClusterArch.tuple_orbit([3,4,3])
        assert(result == frozenset({(3, 4, 3), (0, 7, 0), (2, 6, 2), (1, 7, 1), (2, 7, 2), (1, 4, 1), (2, 4, 2), (0, 4, 0), 
                                            (1, 6, 1), (3, 5, 3), (3, 6, 3), (1, 5, 1), (0, 5, 0), (2, 5, 2), (3, 7, 3), (0, 6, 0)}))
        
        
        
        
        
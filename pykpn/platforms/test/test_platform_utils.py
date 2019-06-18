# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.platforms import utils

class TestUtils(object):
    
    def test_dijkstra_DAG_1(self, DAG):
        result = utils.simpleDijkstra(DAG, 0, 7)
        assert(result == [0,1,3,7])
    
    def test_dijkstra_DAG_2(self, DAG):
        result = utils.simpleDijkstra(DAG, 4, 8)
        assert(result == [4,9,8])
    
    def test_dijkstra_DAG_3(self, DAG):
        result = utils.simpleDijkstra(DAG, 3, 6)
        assert(result == None)
    
    def test_dijkstra_cyclic_1(self, cyclicGraph):
        result = utils.simpleDijkstra(cyclicGraph, 0, 6)
        assert(result == [0, 4, 5, 6])
    
    def test_dijkstra_cyclic_2(self, cyclicGraph):
        result = utils.simpleDijkstra(cyclicGraph, 3, 0)
        assert(result == [3, 2, 1, 0] or result == [3, 8, 7, 0])
    
    def test_dijkstra_cyclic_3(self, cyclicGraph):
        result = utils.simpleDijkstra(cyclicGraph, 9, 4)
        assert(result == [9, 8, 7, 4] or result == [9, 8, 5, 4])
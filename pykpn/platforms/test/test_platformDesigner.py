# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.platforms.utils import simpleDijkstra


class TestPlatformDesigner(object):
    
    def test_singleCluster(self, designer):
        designer.newElement('chip')
        designer.addPeCluster(0, 'TestCluster', 4, 1000)
        designer.addCommunicationResource('RAM', [0], 1000, 1000, 1000, 1000)
        designer.finishElement()
        
        platform = designer.getPlatform()
        
        assert(len(platform.processors()) == 4)
        assert(len(platform.primitives()) == 1)
        
        for primitive in platform.primitives():
            assert(len(primitive.consumers) == len(primitive.producers) == 4)
            
    def test_doubleCluster(self, designer):
        designer.newElement('chip')
        designer.addPeCluster(0, 'cluster_0', 4, 1000)
        designer.addPeCluster(1, 'cluster_1', 4, 1000)
        designer.addCommunicationResource('L2Cache_0', [0], 1000, 1000, 1000, 1000)
        designer.addCommunicationResource('L2Cache_1', [1], 1000, 1000, 1000, 1000)
        designer.addCommunicationResource('RAM', [0,1], 1000, 1000, 1000, 1000)
        designer.finishElement()
        
        platform = designer.getPlatform()
        
        assert(len(platform.processors()) == 8)
        i = 0
        for element in platform.primitives():
            i += 1
        assert(i == 3)
        
        l2caches = 0
        RAM = 0
        for primitive in platform.primitives():
            if primitive.name == 'prim_chip_RAM_1':
                RAM += 1
                assert(len(primitive.consumers) == len(primitive.producers) == 8)
            else:
                l2caches +=1
                assert(len(primitive.consumers) == len(primitive.producers) == 4)
        assert(l2caches == 2)
        assert(RAM == 1)
        
    def test_doubleClusterL1(self, designer):
        designer.newElement('chip')
        designer.addPeCluster(0, 'cluster_0', 4, 1000)
        designer.addPeCluster(1, 'cluster_1', 4, 1000)
        designer.addCacheForPEs(0, 1000, 1000, 1000, 1000)
        designer.addCacheForPEs(1, 1000, 1000, 1000, 1000)
        designer.addCommunicationResource('L2Cache_0', [0], 1000, 1000, 1000, 1000)
        designer.addCommunicationResource('L2Cache_1', [1], 1000, 1000, 1000, 1000)
        designer.addCommunicationResource('RAM', [0,1], 1000, 1000, 1000, 1000)
        designer.finishElement()
        
        platform = designer.getPlatform()
        
        assert(len(platform.processors()) == 8)
        i = 0
        for element in platform.primitives():
            i += 1
        assert(i == 11)
        
        l1caches = 0
        l2caches = 0
        RAM = 0
        for primitive in platform.primitives():
            if primitive.name == 'prim_chip_RAM_1':
                RAM += 1
                assert(len(primitive.consumers) == len(primitive.producers) == 8)
            elif primitive.name.split('_')[1] == 'L1':
                l1caches += 1
            else:
                l2caches +=1
                assert(len(primitive.consumers) == len(primitive.producers) == 4)
        
        assert(l1caches == 8)
        assert(l2caches == 2)
        assert(RAM == 1)
        
    def test_networkOnChip(self, designer):
        designer.newElement('chip')
        designer.addPeCluster(0, 'cluster_0', 4, 1000)
        
    
    
    
    
    
    
    
    
    
    
    
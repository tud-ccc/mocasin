# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from mocasin.common.platform import Platform, CommunicationResourceType
from mocasin.platforms import platformDesigner
from mocasin.platforms.utils import simpleDijkstra

class TestPlatform(Platform):
    """REMOVE IF NOT NEEDED ANYMORE
    """
    def __init__(self):
        super(TestPlatform, self).__init__("TestPlatform")
        designer = platformDesigner.PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        
        designer.addPeCluster(0, 'ARM', 4, 10000)
        designer.addPeCluster(1, 'ARM', 4, 10000)
        designer.addPeCluster(2, 'ARM', 4, 10000)
        designer.addPeCluster(3, 'ARM', 4, 10000)
        designer.addPeCluster(4, 'ARM', 4, 10000)
        
        designer.addCacheForPEs(0, 100, 100, 100, 100, 'L1Cache')
        designer.addCacheForPEs(1, 100, 100, 100, 100, 'L1Cache')
        designer.addCacheForPEs(2, 100, 100, 100, 100, 'L1Cache')
        designer.addCacheForPEs(3, 100, 100, 100, 100, 'L1Cache')
        designer.addCacheForPEs(4, 100, 100, 100, 100, 'L1Cache')
        
        designer.addCommunicationResource("L2_0", [0], 100, 100, 100, 100)
        designer.addCommunicationResource("L2_1", [1], 100, 100, 100, 100)
        designer.addCommunicationResource("L2_2", [2], 100, 100, 100, 100)
        designer.addCommunicationResource("L2_3", [3], 100, 100, 100, 100)
        designer.addCommunicationResource("L2_4", [4], 100, 100, 100, 100)
        
        designer.addCommunicationResource("L3_0", [0,1,2,3,4], 100, 100, 100, 100)        
        
        
        
        

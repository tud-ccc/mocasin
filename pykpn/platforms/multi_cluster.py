# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.common.platform import Platform
from pykpn.platforms.platformDesigner import PlatformDesigner

class DesignerPlatformMultiCluster(Platform):
    def __init__(self, processor_1, processor_2, name='multi_cluster'):
        super(DesignerPlatformMultiCluster, self).__init__(name)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('multi_cluster')

        #add first cluster with L2 cache
        designer.addPeClusterForProcessor('cluster_0', processor_1.to_pykpn_processor(), 2)
        designer.addCommunicationResource('cl0_l2', ['cluster_0'], 100, 100, float('inf'), float('inf'),
                                          frequencyDomain=10000)

        #add second cluster with L2 cache
        designer.addPeClusterForProcessor('cluster_1', processor_2.to_pykpn_processor(), 2)
        designer.addCommunicationResource('cl1_l2', ['cluster_1'], 100, 100, float('inf'), float('inf'),
                                          frequencyDomain=10000)

        #connect both clusters via RAM
        designer.addCommunicationResource('RAM', ['cluster_0', 'cluster_1'], 1000, 1000, float('inf'), float('inf'),
                                          frequencyDomain=1000)

        designer.finishElement()

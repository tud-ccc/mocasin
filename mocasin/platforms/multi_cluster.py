# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.common.platform import Platform, Processor
from mocasin.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate

class DesignerPlatformMultiCluster(Platform):
    def __init__(self, processor_0, processor_1, name='multi_cluster',symmetries_json=None,embedding_json=None):
        super(DesignerPlatformMultiCluster, self).__init__(name,symmetries_json,embedding_json)

        #woraround for Hydra < 1.1
        if not isinstance(processor_0,Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1,Processor):
            processor_1 = instantiate(processor_1)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('multi_cluster')

        #add first cluster with L2 cache
        designer.addPeClusterForProcessor('cluster_0', processor_0, 2)
        designer.addCommunicationResource('cl0_l2', ['cluster_0'], 100, 100, float('inf'), float('inf'),
                                          frequencyDomain=10000)

        #add second cluster with L2 cache
        designer.addPeClusterForProcessor('cluster_1', processor_1, 2)
        designer.addCommunicationResource('cl1_l2', ['cluster_1'], 100, 100, float('inf'), float('inf'),
                                          frequencyDomain=10000)

        #connect both clusters via RAM
        designer.addCommunicationResource('RAM', ['cluster_0', 'cluster_1'], 1000, 1000, float('inf'), float('inf'),
                                          frequencyDomain=1000)

        designer.finishElement()

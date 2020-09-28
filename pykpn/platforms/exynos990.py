# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.common.platform import Platform
from pykpn.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate
from pykpn.common.platform import Processor

class DesignerPlatformExynos990(Platform):
    def __init__(self, processor_0, processor_1, processor_2, processor_3, name="exynos-990"):
        super(DesignerPlatformExynos990, self).__init__(name)
        #This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not isinstance(processor_0,Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1,Processor):
            processor_1 = instantiate(processor_1)
        if not isinstance(processor_2,Processor):
            processor_2 = instantiate(processor_2)
        if not isinstance(processor_3,Processor):
            processor_3 = instantiate(processor_3)
        designer = PlatformDesigner(self)

        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")

        # cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_0",
                                          processor_0,
                                          2)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_0", 5, 7, float('inf'), float('inf'), frequencyDomain=6000000.0, name='L1')
        designer.addCommunicationResource("lvl2_cl0",
                                          ["cluster_0"],
                                          225,
                                          300,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=600000000.0)

        # cluster 1, with l2 cache
        designer.addPeClusterForProcessor("cluster_1",
                                          processor_1,
                                          2)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_1", 5, 7, float('inf'), float('inf'), frequencyDomain=6670000.0, name='L1')
        designer.addCommunicationResource("lvl2_cl1",
                                          ["cluster_1"],
                                          225,
                                          300,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=667000000.0)

        # cluster 2, with l2 cache
        designer.addPeClusterForProcessor("cluster_2",
                                          processor_2,
                                          4)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_2", 5, 7, float('inf'), float('inf'), frequencyDomain=6670000.0, name='L1')
        designer.addCommunicationResource("lvl2_cl2",
                                          ["cluster_2"],
                                          225,
                                          300,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=667000000.0)

        # RAM connecting all clusters
        designer.addCommunicationResource("RAM",
                                          ["cluster_0", "cluster_1", "cluster_2"],
                                          800,
                                          2000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=6000000.0)

        # single GPU
        designer.addPeClusterForProcessor("GPU",
                                          processor_3,
                                          1)
        designer.addCacheForPEs("GPU", 5, 7, float('inf'), float('inf'), frequencyDomain=6670000.0, name='GPU_MEM')

        # another memory, simulating BUS
        designer.addCommunicationResource("BUS",
                                          ["cluster_0", "cluster_1", "cluster_2", "GPU"],
                                          2000,
                                          6000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=4000000.0)

        designer.finishElement()

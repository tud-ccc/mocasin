# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.platforms.topologies import meshTopology
from pykpn.platforms.utils import simpleDijkstra as sd
from pykpn.common.platform import Platform
from pykpn.platforms.platformDesigner import PlatformDesigner

class DesignerPlatformMesh(Platform):
    def __init__(self, tgff_processor, processor_2, name="parallella-styled"):
        super(DesignerPlatformMesh, self).__init__(name)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")

        designer.addPeClusterForProcessor("cluster_0", tgff_processor.to_pykpn_processor(), 16)
        topology = meshTopology(['processor_0', 'processor_1', 'processor_2', 'processor_3', 'processor_4',
                                 'processor_5', 'processor_6', 'processor_7', 'processor_8', 'processor_9',
                                 'processor_10', 'processor_11', 'processor_12', 'processor_13', 'processor_14',
                                 'processor_15'])
        designer.createNetworkForCluster("cluster_0", 'testNet', topology, sd, 6000000.0, 100, 150, 100, 60)

        designer.addPeClusterForProcessor("cluster_1", processor_2.to_pykpn_processor(), 2)
        designer.addCommunicationResource("lvl2_cl1",
                                          ["cluster_1"],
                                          500,
                                          1000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=600000000.0)


        designer.addCommunicationResource("RAM",
                                          ["cluster_0", "cluster_1"],
                                          1000,
                                          3000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=6000000.0)
        designer.finishElement()

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.common.platform import Platform, Processor
from pykpn.platforms.topologies import fullyConnectedTopology
from pykpn.platforms.platformDesigner import PlatformDesigner
from pykpn.platforms.utils import simpleDijkstra as sd
from hydra.utils import instantiate

class DesignerPlatformCoolidge(Platform):
    #The topology and latency numbers (!) of this should come from the MPPA3 Coolidge
    #sheet published by Kalray
    def __init__(self, processor_0, processor_1, name="coolidge", symmetries_json=None,embedding_json=None):
        super(DesignerPlatformCoolidge, self).__init__(name,symmetries_json,embedding_json)

        #workaround until Hydra 1.1
        if not isinstance(processor_0,Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1,Processor):
            processor_1 = instantiate(processor_1)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('coolidge')

        #create five chips with 16 cores, NoC, +Security Core
        clusters = []
        for i in range(5):
            cluster = 'cluster_{0}'.format(i)
            designer.newElement(cluster)
            clusters.append(cluster)

            designer.addPeClusterForProcessor(f'cluster_{i}_0', processor_0, 16)

            topology = fullyConnectedTopology(['processor_{:04d}'.format(i * 17), 'processor_{:04d}'.format(i * 17 + 1),
                                               'processor_{:04d}'.format(i * 17 + 2), 'processor_{:04d}'.format(i * 17 + 3),
                                               'processor_{:04d}'.format(i * 17 + 4), 'processor_{:04d}'.format(i * 17 + 5),
                                               'processor_{:04d}'.format(i * 17 + 6), 'processor_{:04d}'.format(i * 17 + 7),
                                               'processor_{:04d}'.format(i * 17 + 8), 'processor_{:04d}'.format(i * 17 + 9),
                                               'processor_{:04d}'.format(i * 17 + 10), 'processor_{:04d}'.format(i * 17 + 11),
                                               'processor_{:04d}'.format(i * 17 + 12), 'processor_{:04d}'.format(i * 17 + 13),
                                               'processor_{:04d}'.format(i * 17 + 14), 'processor_{:04d}'.format(i * 17 + 15)
                                               ])

            designer.createNetworkForCluster(f'cluster_{i}_0', f'noc_{i}', topology, sd, 40000.0, 100, 150, 100, 60)

            designer.addPeClusterForProcessor(f'cluster_{i}_1', processor_1, 1)

            designer.addCommunicationResource(f'L2_{i}', [f'cluster_{i}_0', f'cluster_{i}_1'], 500, 1500,
                                              float('inf'), float('inf'), frequencyDomain=600000.0)

            designer.finishElement()

        designer.addCommunicationResource("RAM", clusters,
                                          1000, 3000, float('inf'), float('inf'), frequencyDomain=10000)

        designer.finishElement()

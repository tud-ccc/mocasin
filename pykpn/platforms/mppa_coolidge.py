# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.common.platform import Platform
from pykpn.platforms.topologies import fullyConnectedTopology
from pykpn.platforms.platformDesigner import PlatformDesigner
from pykpn.platforms.utils import simpleDijkstra as sd

class DesignerPlatformCoolidge(Platform):
    #The topology and latency numbers (!) of this should come from the MPPA3 Coolidge
    #sheet published by Kalray
    def __init__(self, processor_1, processor_2, name="coolidge"):
        super(DesignerPlatformCoolidge, self).__init__(name)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('coolidge')

        #create five chips with 16 cores, NoC, +Security Core
        for i in range(0, 5):
            designer.newElement('cluster_{0}'.format(i))

            designer.addPeClusterForProcessor(f'cluster_{i}_0', processor_1, 16)

            topology = fullyConnectedTopology(['processor_{0}'.format(i * 17), 'processor_{0}'.format(i * 17 + 1),
                                               'processor_{0}'.format(i * 17 + 2), 'processor_{0}'.format(i * 17 + 3),
                                               'processor_{0}'.format(i * 17 + 4), 'processor_{0}'.format(i * 17 + 5),
                                               'processor_{0}'.format(i * 17 + 6), 'processor_{0}'.format(i * 17 + 7),
                                               'processor_{0}'.format(i * 17 + 8), 'processor_{0}'.format(i * 17 + 9),
                                               'processor_{0}'.format(i * 17 + 10), 'processor_{0}'.format(i * 17 + 11),
                                               'processor_{0}'.format(i * 17 + 12), 'processor_{0}'.format(i * 17 + 13),
                                               'processor_{0}'.format(i * 17 + 14), 'processor_{0}'.format(i * 17 + 15)
                                               ])

            designer.createNetworkForCluster(f'cluster_{i}_0', f'noc_{i}', topology, sd, 40000.0, 100, 150, 100, 60)

            designer.addPeClusterForProcessor(f'cluster_{i}_1', processor_2, 1)

            designer.addCommunicationResource(f'L2_{i}', [f'cluster_{i}_0', f'cluster_{i}_1'], 500, 1500,
                                              float('inf'), float('inf'), frequencyDomain=600000.0)

            designer.finishElement()

        designer.addCommunicationResource("RAM", ['chip_0', 'chip_1', 'chip_2', 'chip_3', 'chip_4'],
                                          1000, 3000, float('inf'), float('inf'), frequencyDomain=10000)

        designer.finishElement()

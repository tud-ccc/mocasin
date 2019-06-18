# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Platform
from pykpn.platforms import platformDesigner
from pykpn.platforms.utils import simpleDijkstra

class KalrayMppa(Platform):
    def __init__(self):
        super(KalrayMppa, self).__init__("KalrayMppa")
        designer = platformDesigner.platformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        
        designer.newElement('chip')
        designer.addPeCluster(0, 'ARM', 4, 1000)
        designer.addPeCluster(1, 'cluster_1', 4, 1000)
        
        designer.createNetworkForCluster(0, 'testNet', {'PE00' : ['PE01', 'PE02'],
                                                                  'PE01' : ['PE00', 'PE03'],
                                                                  'PE02' : ['PE00', 'PE03'],
                                                                  'PE03' : ['PE01', 'PE02']},
                    simpleDijkstra, 
                    1000,
                    1000,
                    1000,
                    1000,
                    1000)
        
        designer.addCommunicationResource('L2Cache_1', [1], 1000, 1000, 1000, 1000)
        designer.addCommunicationResource('RAM', [0,1], 1000, 1000, 1000, 1000)
        designer.finishElement()
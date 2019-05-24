# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Platform
from pykpn.platforms import platformDesigner
from pykpn.platforms import utils

class KalrayMppa(Platform):
    def __init__(self):
        super(KalrayMppa, self).__init__("KalrayMppa")
        designer = platformDesigner.platformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        
        '''
        for i in range(0,4):
            designer.newElement(i)
            designer.addPeCluster(0, 'TypeD', 4, 40000)
            designer.addPeCluster(1, 'TypeC', 4, 40000)
            designer.addCommunicationResource('D-Noc', [0], 1000, 1000, 1000, 1000)
            designer.addCommunicationResource('C-Noc', [1], 1000, 1000, 1000, 1000)
            designer.addCommunicationResource('SharedMemory', [0,1], 1000, 1000, 1000, 1000)
            designer.finishElement()
        designer.createNetwork('testnet', [[1,2],[0,3],[0,3],[1,2]], utils.simpleDijkstra, 0,0,0,0,0)
        '''
        for i in range(0,4):
            designer.nNewElement(i)
            designer.nAddPeCluster(0, 'TypeD', 4, 40000)
            designer.nAddPeCluster(1, 'TypeC', 4, 40000)
            designer.nFinishElement()
        designer.finishElement()
        print('Statement')
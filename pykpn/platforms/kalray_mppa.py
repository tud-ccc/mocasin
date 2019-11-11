# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Platform
from pykpn.platforms import platformDesigner
from pykpn.platforms import utils

class KalrayMppa(Platform):
    """This class should describe a KalrayMppa chip as pykpn platform. It is also meant as a how to use example
    for the platform designer class.
    """
    def __init__(self):
        super(KalrayMppa, self).__init__("KalrayMppa")
        designer = platformDesigner.PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        
        for i in range(0,16):
            identifier = "chip_" + str(i)
            designer.newElement(identifier)
            
            for j in range(0,4):
                designer.addPeCluster(j,"PE",4, 0)
                resourceName = "L1_" + str(j)
                designer.addCommunicationResource(resourceName, [j], 0, 0, 0, 0)
            
            resourceName = "sharedMemory_" + str(i)
            designer.addCommunicationResource(resourceName, [0,1,2,3], 0, 0, 0, 0)
            
            designer.finishElement()
            
        designer.createNetworkForChips("NOC", {"chip_0": ["chip_1","chip_4"], 
                                           "chip_1":["chip_0","chip_5", "chip_2"], 
                                           "chip_2":["chip_1","chip_6", "chip_3"], 
                                           "chip_3":["chip_2","chip_7"],
                                           "chip_4":["chip_0","chip_5", "chip_8"],
                                           "chip_5":["chip_4","chip_1", "chip_9", "chip_6"],
                                           "chip_6":["chip_2","chip_5", "chip_10", "chip_7"],
                                           "chip_7":["chip_3","chip_6", "chip_11"],
                                           "chip_8":["chip_4","chip_9", "chip_12"],
                                           "chip_9":["chip_5","chip_8", "chip_13", "chip_10"],
                                           "chip_10":["chip_6","chip_9", "chip_11","chip_14"],
                                           "chip_11":["chip_7","chip_10", "chip_15"],
                                           "chip_12":["chip_8","chip_13"],
                                           "chip_13":["chip_9","chip_12", "chip_14"],
                                           "chip_14":["chip_10","chip_13", "chip_15"],
                                           "chip_15":["chip_11","chip_14"]}, 
                                utils.simpleDijkstra, 0, 0, 0, 0, 0)
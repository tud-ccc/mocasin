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
        
        for k in range(0,4):
            name = "kalray_" + str(k)
            designer.newElement(name)
            
            for i in range(0,16):
                identifier = "chip_" + str(i) + str(k)
                designer.newElement(identifier)
            
                for j in range(0,4):
                    designer.addPeCluster(j,"PE",4, 0)
                    resourceName = "L1_" + str(j) + str(k)
                    designer.addCommunicationResource(resourceName, [j], 0, 0, 0, 0)
            
                    resourceName = "sharedMemory_" + str(i) + str(k)
                    designer.addCommunicationResource(resourceName, [0,1,2,3], 0, 0, 0, 0)
            
                designer.finishElement()
            
            designer.createNetwork("NOC", {"chip_0" + str(k): ["chip_1"+ str(k),"chip_4"+ str(k)], 
                                           "chip_1"+ str(k):["chip_0"+ str(k),"chip_5"+ str(k), "chip_2"+ str(k)], 
                                           "chip_2"+ str(k):["chip_1"+ str(k),"chip_6"+ str(k), "chip_3"+ str(k)], 
                                           "chip_3"+ str(k):["chip_2"+ str(k),"chip_7"+ str(k)],
                                           "chip_4"+ str(k):["chip_0"+ str(k),"chip_5"+ str(k), "chip_8"+ str(k)],
                                           "chip_5"+ str(k):["chip_4"+ str(k),"chip_1"+ str(k), "chip_9"+ str(k), "chip_6"+ str(k)],
                                           "chip_6"+ str(k):["chip_2"+ str(k),"chip_5"+ str(k), "chip_10"+ str(k), "chip_7"+ str(k)],
                                           "chip_7"+ str(k):["chip_3"+ str(k),"chip_6"+ str(k), "chip_11"+ str(k)],
                                           "chip_8"+ str(k):["chip_4"+ str(k),"chip_9"+ str(k), "chip_12"+ str(k)],
                                           "chip_9"+ str(k):["chip_5"+ str(k),"chip_8"+ str(k), "chip_13"+ str(k), "chip_10"+ str(k)],
                                           "chip_10"+ str(k):["chip_6"+ str(k),"chip_9"+ str(k), "chip_11"+ str(k),"chip_14"+ str(k)],
                                           "chip_11"+ str(k):["chip_7"+ str(k),"chip_10"+ str(k), "chip_15"+ str(k)],
                                           "chip_12"+ str(k):["chip_8"+ str(k),"chip_13"+ str(k)],
                                           "chip_13"+ str(k):["chip_9"+ str(k),"chip_12"+ str(k), "chip_14"+ str(k)],
                                           "chip_14"+ str(k):["chip_10"+ str(k),"chip_13"+ str(k), "chip_15"+ str(k)],
                                           "chip_15"+ str(k):["chip_11"+ str(k),"chip_14"+ str(k)]}, 
                                utils.simpleDijkstra, 0, 0, 0, 0, 0)
            
            designer.finishElement()
        
        designer.createNetwork("outerNet", {"kalray_0" : ["kalray_1", "kalray_2"], 
                                            "kalray_1" : ["kalray_0", "kalray_3"],
                                            "kalray_2" : ["kalray_0", "kalray_3"],
                                            "kalray_3" : ["kalray_1", "kalray_2"]}, 
                                            utils.simpleDijkstra, 0, 0, 0, 0, 0)
        print('Statement')
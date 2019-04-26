# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import FrequencyDomain, Platform, Processor, \
    SchedulingPolicy, Scheduler, Storage, CommunicationPhase, Primitive


class platformDesigner():
    """"One instance of the platform designer is meant to create exactly one platform.
    It provides the necessary methods to create PE clusters and connect PEs in clusters
    or clusters themselves with communication ressources.
    
    :ivar int __peAmount: Holds the amount of currently initialized PEs.
    :ivar int __clusters: Holds the amount of currently initialized PE clusters.
    :ivar dict {int : list[Processors]} __clusterDict: Holds the initialized clusters and mapps them on an ID.
    :ivar SchedulingPolicy __schedulingPolicy: Holds the currently applied scheduling policy. This policy will 
    be applied to all PE clusters initialized afterwards.
    :ivar Platform __platform: The platform object, that is created and manipulated.
    """
    
    def __init__(self, name):
        """Initialize a new instance of the platformDesigner.
        :param String name: The name of the platform that will be created.
        """
        self.__peAmount = 0
        self.__clusters = 0
        self.__clusterDict = {}
        self.__schedulingPolicy = None
        self.__platform = Platform(name)
    
    def setSchedulingPolicy(self, policy, cycles):
        self.__schedulingPolicy = SchedulingPolicy(policy, cycles)
    
    def addPeCluster(self, name, amount, frequency):
        """
        """
        if self.__schedulingPolicy == None:
            return -1
        
        fd = FrequencyDomain('fd_' + name, frequency)
        
        start = self.__peAmount
        processors = []
        for i in range (start, amount):
            processor = Processor('PE%02d' % i, name, fd)
            self.__platform.add_scheduler(Scheduler('sched%02d' % i, processor, [self.__schedulingPolicy]))
            processors.append(processor)
            self.__peAmount += 1
        
        self.__clusterDict.update({self.__clusters : processors})
        self.__clusters += 1
        
        return self.__clusters-1
            
    def addCommunicationRessource(self):
        pass
    
    def getPlatform(self):
        return self.__platform
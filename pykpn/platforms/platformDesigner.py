# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import FrequencyDomain, Platform, Processor, \
    SchedulingPolicy, Scheduler, Storage, CommunicationPhase, Primitive
import sys


class platformDesigner():
    """"One instance of the platform designer is meant to create exactly one platform.
    It provides the necessary methods to create PE clusters and connect PEs in clusters
    or clusters themselves with communication resources.
    
    :ivar int __peAmount: Holds the amount of currently initialized PEs.
    :ivar int __clusters: Holds the amount of currently initialized PE clusters.
    :ivar dict {int : tupel(Processors, [communicationRessources])} __clusterDict: 
            A dict which holds for every initialized cluster the PEs and their communication
            resources.
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
        """Sets a new scheduling policy, which will be applied to all schedulers of new PE Clusters.
        :param String policy: The kind of policy.
        :param int cycles: The cycles of the policy.
        :returns: Whether the policy set successfully or not.
        :rtype: bool
        """
        try:
            self.__schedulingPolicy = SchedulingPolicy(policy, cycles)
            return True
        except:
            print(sys.exc_info()[0])
            return False
    
    def addPeCluster(self, name, amount, frequency, noc=False):
        """Adds a new cluster of PEs to the platform.
        :param String name: The name of the processor type
        :param int amount: The amount of PEs in the cluster
        :param int frequency: The frequency of the PEs
        :param bool noc: Whether the PEs are connected via network on chip or not
        :returns: The intern id of the cluster or -1 of the cluster cant be created
        :rtype: int
        """
        if self.__schedulingPolicy == None:
            return -1
        
        fd = FrequencyDomain('fd_' + name, frequency)
        
        if noc:
            #TODO: implement a network on chip cluster
            return
        try:
            start = self.__peAmount
            end = self.__peAmount + amount
            processors = []
            for i in range (start, end):
                processor = Processor('PE%02d' % i, name, fd)
                self.__platform.add_processor(processor)
                self.__platform.add_scheduler(Scheduler('sched%02d' % i, [processor], [self.__schedulingPolicy]))
                processors.append((processor,[]))
                self.__peAmount += 1
            self.__clusterDict.update({self.__clusters : processors})
            self.__clusters += 1
        except:
            print(sys.exc_info()[0])
            return -1
        
        return self.__clusters-1
    
    def addCacheForPEs(self, clusterId, readLatency, writeLatency, readThroughput, writeThroughput, name='default'):
        """Adds a level 1 cache for each PE of the given cluster.
        :param int clusterId: The ID of the cluster.
        :param int readLatency: The read latency of the cache.
        :param int writeLatency: The write latency of the cache.
        :param int readThroughput: The read throughput of the cache.
        :param int writeThroughput: The write throughput of the cache.
        :param String name: The cache name, in case it differs from L1.
        :returns: Whether the caches had been added successfully or not.
        :rtype: bool
        """
        if not clusterId in self.__clusterDict:
            return False
        
        if self.__schedulingPolicy == None:
            return False
        
        toName = None
        if name != 'default':
            toName = name
        else:
            toName = 'L1_'
        
        try:
            for pe in self.__clusterDict[clusterId]:
                communicationRessource = Storage(toName + pe[0].name,
                                                 self.__schedulingPolicy,
                                                 read_latency = readLatency,
                                                 write_latency = writeLatency,
                                                 read_throughput = readThroughput,
                                                 write_throughput = writeThroughput)
                self.__platform.add_communication_resource(communicationRessource)
                produce = CommunicationPhase('produce', [communicationRessource], 'write')
                consume = CommunicationPhase('consume', [communicationRessource], 'read')

                prim = Primitive('prim_' + toName + pe[0].name)
                prim.add_producer(pe[0], [produce])
                prim.add_consumer(pe[0], [consume])
                self.__platform.add_primitive(prim)
                
                pe[1].append(communicationRessource)
        except:
            print(sys.exc_info()[0])
            return False
        
        return True
            
    def connectClusters(self, name, clusterIds, readLatency, writeLatency, readThroughput, writeThroughput):
        """Connects all the given clusters with a storage. For example RAM. Also you can add a L2 cache for a cluster
        if you just give one cluster.
        :param String name: The name of the storage
        :param list[int] clusterIds: A list containing all cluster IDs of clusters which will be connected
        :param int readLatency: The read latency of the storage
        :param int writeLatency: The write latency of the storage
        :param int readThroughput: The read throughput of the storage
        :param int writeThroughput: The write throughput of the storage
        :returns: Whether the storage had been added successfully or not
        :rtype: bool
        """
        
        if self.__schedulingPolicy == None:
            return False 
        
        for clusterId in clusterIds:
            if not clusterId in self.__clusterDict:
                return False
        
        try:
            communicationRessource = Storage(name,
                                        self.__schedulingPolicy,
                                        read_latency=readLatency,
                                        write_latency=writeLatency,
                                        read_throughput=readThroughput, 
                                        write_throughput=writeThroughput)
            self.__platform.add_communication_resource(communicationRessource)
            prim = Primitive('prim_' + name)

            for clusterId in clusterIds:
                for pe in self.__clusterDict[clusterId]:
                    produce = CommunicationPhase('produce', pe[1] + [communicationRessource], 'write')
                    consume = CommunicationPhase('consume', pe[1] + [communicationRessource], 'read')
                    prim.add_producer(pe[0], [produce])
                    prim.add_consumer(pe[0], [consume])        
            self.__platform.add_primitive(prim)
        except :
            print(sys.exc_info()[0])
            return False
        
        return True
    
    
    def getPlatform(self):
        return self.__platform
    
    def reset(self, name='newPlatform'):
        self.__peAmount = 0
        self.__clusters = 0
        self.__clusterDict = {}
        self.__schedulingPolicy = None
        self.__platform = Platform(name)
    
    
    
    
    
    
    
# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import FrequencyDomain, Platform, Processor, \
    SchedulingPolicy, Scheduler, Storage, CommunicationPhase, Primitive, \
    CommunicationResource, CommunicationResourceType
from collections import OrderedDict
from pykpn.platforms.utils import simpleDijkstra
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
    
    def __init__(self, platform):
        """Initialize a new instance of the platformDesigner.
        :param String name: The name of the platform that will be created.
        :param Platform platform: The platform object which will be modified.
        """
        self.__peAmount = 0
        self.__elementDict = {}
        self.__activeScope = None
        self.__clusterDict = OrderedDict()
        
        self.__schedulingPolicy = None
        self.__platform = platform
    
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
    
    def addPeCluster(self, identifier, name, amount, frequency, noc=False):
        """Adds a new cluster of PEs to the platform.
        :param String name: The name of the processor type
        :param int amount: The amount of PEs in the cluster
        :param int frequency: The frequency of the PEs
        :param bool noc: Whether the PEs are connected via network on chip or not
        :returns: The intern id of the cluster or -1 of the cluster cant be created
        :rtype: int
        """
        if self.__schedulingPolicy == None:
            return
        if self.__activeScope == None:
            return
        
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
                self.__elementDict[self.__activeScope].update({identifier : processors})
        except:
            print(sys.exc_info()[0])
        
    def addCacheForPEs(self, 
                       identifier, 
                       readLatency, 
                       writeLatency, 
                       readThroughput, 
                       writeThroughput, 
                       name='default'):
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
        if self.__schedulingPolicy == None:
            return False
        if self.__activeScope == None:
            return
        
        nameToGive = None
        
        if not identifier in self.__clusterDict:
            return False
        if name != 'default':
            nameToGive = name
        else:
            nameToGive = 'L1_'
        peList = self.__clusterDict[identifier]
        
        try:
            for pe in peList:
                communicationRessource = Storage(nameToGive + pe[0].name,
                                                 self.__schedulingPolicy,
                                                 read_latency = readLatency,
                                                 write_latency = writeLatency,
                                                 read_throughput = readThroughput,
                                                 write_throughput = writeThroughput)
                self.__platform.add_communication_resource(communicationRessource)
                pe[1].append(communicationRessource)
                
                prim = Primitive('prim_' + nameToGive + pe[0].name)
                produce = CommunicationPhase('produce', pe[1], 'write')
                consume = CommunicationPhase('consume', pe[1], 'read')
                prim.add_producer(pe[0], [produce])
                prim.add_consumer(pe[0], [consume])
                self.__platform.add_primitive(prim)
                
        except:
            print(sys.exc_info()[0])
            return False
        
        return True
            
    def addCommunicationResource(self, 
                                  name,
                                  clusterIds, 
                                  readLatency, 
                                  writeLatency, 
                                  readThroughput, 
                                  writeThroughput, 
                                  resourceType = CommunicationResourceType.Storage, 
                                  frequencyDomain=0):
        """Adds a communication resource to the platform. All cores of the given cluster ID's can communicate
        via this resource.
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
            return
        if self.__activeScope == None:
            return
        
        for clusterId in clusterIds:
            if not clusterId in self.__elementDict[self.__activeScope]:
                return
        clusterDict = self.__elementDict[self.__activeScope]
        nameToGive = str(self.__activeScope) + '_' + name
        
        try:
            if resourceType == CommunicationResourceType.Storage:
                communicationRessource = Storage(nameToGive, 
                                                 self.__schedulingPolicy,
                                                 readLatency,
                                                 writeLatency,
                                                 readThroughput, 
                                                 writeThroughput)
                
            
            else:
                communicationRessource = CommunicationResource(nameToGive,
                                                               resourceType,
                                                               frequencyDomain,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)

            self.__platform.add_communication_resource(communicationRessource)
            prim = Primitive('prim_' + nameToGive)
            for clusterId in clusterIds:
                for pe in clusterDict[clusterId]:
                    pe[1].append(communicationRessource)
                    produce = CommunicationPhase('produce', pe[1], 'write')
                    consume = CommunicationPhase('consume', pe[1], 'read')
                    prim.add_producer(pe[0], [produce])
                    prim.add_consumer(pe[0], [consume])        
            self.__platform.add_primitive(prim)
        except :
            print(sys.exc_info()[0])
            return False
        
        return
    
    def createNetwork(self, 
                      networkName, 
                      adjacencyList,
                      routingFunction, 
                      frequencyDomain,
                      readLatency,
                      writeLatency,
                      readThroughput,
                      writeThroughput):
        
        if self.__activeScope == None:
            '''Creating a network between independent chips
            '''
            if self.__elementDict == {}:
                return
            i = 0
            for element in adjacencyList:
                if element == []:
                    i += 1
                    continue
                '''workaround with i, because different elements can have the same 
                adjacency entry
                '''
                source = i
                name = networkName + "_" + "router_" + str(source)
                communicationRessource = CommunicationResource(name,
                                                               CommunicationResourceType.Router,
                                                               frequencyDomain,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                self.__platform.add_communication_resource(communicationRessource)
                
                for target in element:
                    name = networkName + "_pl_" + str(target) + "_" + str(source)
                    communicationRessource = CommunicationResource(name,
                                                               CommunicationResourceType.PhysicalLink,
                                                               frequencyDomain,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                    self.__platform.add_communication_resource(communicationRessource)
                i += 1
            
            for key in self.__elementDict:
                if adjacencyList[key] == []:
                    continue
                for clusterId in self.__elementDict[key]:
                    for pe in self.__elementDict[key][clusterId]:
                        '''Adding a primitive for each pe in the network
                        '''
                        prim = Primitive('prim_' + networkName + '_' + pe[0].name)
                        
                        for innerKey in self.__elementDict:
                            if adjacencyList[innerKey] == []:
                                continue
                            
                            routerName = networkName + "_" + "router_" + str(innerKey)
                            router = self.__platform.find_communication_resource(routerName)
                            resourceList = [router]
                            
                            if innerKey != key:
                                path = routingFunction(adjacencyList, key, innerKey)
                                lastPoint = None
                                
                                for point in path:
                                    if lastPoint != None:
                                        name = networkName + "_pl_" + lastPoint + "_" + point
                                        resource = self.__platform.find_communication_resource(name)
                                        resourceList.append(resource)
                                    lastPoint = point
                                
                            for innerCluster in self.__elementDict[innerKey]:
                                for innerPe in innerCluster:
                                    '''Iterating again over all pe's in the network to 
                                    create their consumer and producer phases etc. for 
                                    the primitive.
                                    '''
                                    produce = CommunicationPhase('produce', resourceList, 'write')
                                    consume = CommunicationPhase('consume', resourceList, 'read')
                                        
                                    prim.add_producer(innerPe[0].name, [produce])
                                    prim.add_consumer(innerPe[0].name, [consume])
                                        
                                        
            
        
        else:
            '''Creating a network between clusters on the same chip
            '''
            if self.__clusterDict == {}:
                return
        
        
        
        
    
    def newElement(self, identifier):
        self.__elementDict.update({identifier : {}})
        self.__activeScope = identifier
    
    def finishElement(self):
        self.__activeScope = None
    
    
    
    
    
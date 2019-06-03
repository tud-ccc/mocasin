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
        self.__namingSuffix = 0
        
        self.__clusterDict = OrderedDict()
        
        self.__schedulingPolicy = None
        self.__platform = platform
        
        self.__activeScope = 'base'
        self.__scopeStack = []
        self.__elementDict = { 'base' : {} }
    
    def newElement(self, identifier):
        self.__scopeStack.append(self.__activeScope)
        self.__activeScope = identifier
        
        self.__namingSuffix += 1
        
        self.__elementDict.update({ identifier : {}})
    
    def finishElement(self):
        if len(self.__scopeStack) == 0:
            print("base scope can't be closed")
            return
        
        tmpScope = self.__activeScope
        self.__activeScope = self.__scopeStack.pop()
        
        tmpPElist = []
        
        for element in self.__elementDict[tmpScope]: 
            if isinstance(self.__elementDict[tmpScope][element], list):
                for entry in self.__elementDict[tmpScope][element]:
                    tmpPElist.append(entry)
            
            elif isinstance(self.__elementDict[tmpScope][element], dict):
                for innerElement in self.__elementDict[tmpScope][element]:
                    for entry in innerElement:
                        tmpPElist.append(entry)
            else:
                raise RuntimeWarning("Expected an element of type list or dict!")
        
        self.__elementDict[self.__activeScope].update({tmpScope : tmpPElist})
        
        self.__elementDict.pop(tmpScope, None)
        
    def addPeCluster(self, 
                    identifier, 
                    name, 
                    amount, 
                    frequency):
        try:
            fd = FrequencyDomain('fd_' + name, frequency)
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
    
    def setSchedulingPolicy(self, 
                            policy, 
                            cycles):
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
        
        if not identifier in self.__elementDict[self.__activeScope]:
            raise RuntimeWarning("Identifier does not exist in active scope.")
        if name != 'default':
            nameToGive = name
        else:
            nameToGive = 'L1_'
        peList = self.__elementDict[self.__activeScope][identifier]
        
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
        nameToGive = str(self.__activeScope) + '_' + name + "_" + str(self.__namingSuffix)
        
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
        
        if self.__activeScope != None:
            '''Creating a network between independent chips
            '''
            if self.__elementDict == {}:
                return
            for key in adjacencyList:
                '''workaround with i, because different elements can have the same 
                adjacency entry
                '''
                name = networkName + "_" + "router_" + key
                communicationRessource = CommunicationResource(name,
                                                               CommunicationResourceType.Router,
                                                               frequencyDomain,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                self.__platform.add_communication_resource(communicationRessource)
                
                for target in adjacencyList[key]:
                    name = networkName + "_pl_" + str(target) + "_" + key
                    communicationRessource = CommunicationResource(name,
                                                               CommunicationResourceType.PhysicalLink,
                                                               frequencyDomain,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                    self.__platform.add_communication_resource(communicationRessource)
            
            for key in self.__elementDict[self.__activeScope]:
                if adjacencyList[key] == []:
                    continue
                for pe in self.__elementDict[self.__activeScope][key]:
                    '''Adding a primitive for each pe in the network
                    '''
                    prim = Primitive('prim_' + networkName + '_' + pe[0].name)
                    
                    routerName = networkName + "_" + "router_" + str(key)
                    router = self.__platform.find_communication_resource(routerName)
                        
                    for innerKey in self.__elementDict[self.__activeScope]:
                        if adjacencyList[innerKey] == []:
                            continue
                            
                        resourceList = [router]
                            
                        if innerKey != key:
                            path = routingFunction(adjacencyList, key, innerKey)
                            lastPoint = None
                                
                            for point in path:
                                if lastPoint != None:
                                    name = networkName + "_pl_" + str(lastPoint) + "_" + str(point)
                                    resource = self.__platform.find_communication_resource(name)
                                    resourceList.append(resource)
                                lastPoint = point
                            
                        for innerPe in self.__elementDict[self.__activeScope][innerKey]:
                            '''Iterating again over all pe's in the network to 
                            create their consumer and producer phases etc. for 
                            the primitive.
                                    '''
                            produce = CommunicationPhase('produce', resourceList, 'write')
                            consume = CommunicationPhase('consume', resourceList, 'read')
                                        
                            prim.add_producer(innerPe[0], [produce])
                            prim.add_consumer(innerPe[0], [consume])
                    
                    self.__platform.add_primitive(prim)                    
                                        
            
        
        else:
            return
    
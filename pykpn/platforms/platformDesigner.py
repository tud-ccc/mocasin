# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import FrequencyDomain, Platform, Processor, \
    SchedulingPolicy, Scheduler, Storage, CommunicationPhase, Primitive, \
    CommunicationResource, CommunicationResourceType
from collections import OrderedDict
import sys


class PlatformDesigner():
    """"One instance of the platform designer is meant to create exactly one platform.
    It provides the necessary methods to create PE clusters and connect PEs in clusters
    or clusters themselves with communication resources.
    
    :ivar int __peAmount: Holds the amount of the platforms PEs.
    :ivar int __namingSuffix: Increases every time a new element is pushed on the stack. Will be added to the
                            name of every communication resource added to this element.
    :ivar SchedulingPolicy __schedulingPolicy: Holds the currently set scheduling policy. This policy will 
                            be applied to all PE clusters initialized afterwards.
    :ivar Platform __platform: The platform object, that is created and manipulated.
    :ivar string __activeScope: The identifier of the scope, the designer is currently working on.
    :ivar list[string] __scopeStack: A stack for the identifiers of the scopes that are currently opened.
    :ivar dict{string : {int : [processors]}} __elementDict: For each scope it maps the cluster identifiers to 
                            the list of processing elements of the cluster. 
    """
    
    def __init__(self, platform):
        """Initialize a new instance of the platformDesigner. Should be called by the constructor of a class inheriting
        from Platform.
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
        """A new scope is opened and pushed on the stack.
        :param int identifier: The identifier, the element can be addressed with.
        """
        self.__scopeStack.append(self.__activeScope)
        self.__activeScope = identifier
        
        self.__namingSuffix += 1
        
        self.__elementDict.update({ identifier : {}})
    
    def finishElement(self):
        """The first scope on the stack is closed. The element is still addressable with
        the scopes identifier.
        """
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
        """Creates a new cluster of processing elements on the platform.
        :param int identifier: The identifier the cluster can be addressed within the currently active scope.
        :param string name: The name of the processing elements.
        :param int amount: The amount of processing elements in the cluster.
        :param int frequency: The frequency of the processing elements.
        """
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
        :param String policy: The name of the policy.
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
        """Adds a level 1 cache to each PE of the given cluster.
        :param int identifier: The identifier of the cluster to which the cache will be added. 
        :param int readLatency: The read latency of the cache.
        :param int writeLatency: The write latency of the cache.
        :param int readThroughput: The read throughput of the cache.
        :param int writeThroughput: The write throughput of the cache.
        :param string name: The cache name, in case it differs from L1.
        """
        if self.__schedulingPolicy == None:
            return
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
         
    def addCommunicationResource(self, 
                                  name,
                                  clusterIds, 
                                  readLatency, 
                                  writeLatency, 
                                  readThroughput, 
                                  writeThroughput, 
                                  resourceType = CommunicationResourceType.Storage, 
                                  frequencyDomain=0):
        """Adds a communication resource to the platform. All cores of the given cluster identifiers can communicate
        via this resource. 
        :param string name: The name of the storage
        :param list[int] clusterIds: A list of identifiers for all clusters which will be connected.
        :param int readLatency: The read latency of the communication resource.
        :param int writeLatency: The write latency of the communication resource.
        :param int readThroughput: The read throughput of the communication resource.
        :param int writeThroughput: The write throughput of the communication resource.
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
        fd = FrequencyDomain('fd_' + name, frequencyDomain)
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
                                                               fd,
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
            return
        
        return
    
    def createNetworkForCluster(self,
                    clusterIdentifier,
                    networkName,
                    adjacencyList,
                    routingFunction, 
                    frequencyDomain,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput):
        """Creates a network on chip topology for the given cluster.
        :param int clusterIdentifier: The identifier of the cluster the network will be created for.
        :param string networkName: The name of the network. (primitives belonging to the network will be named
                                like this.
        :param dict {string : list[string]} adjacencyList: The adjacency list of the processing elements within
                                the network. The key is the name of a processing element and the list contains
                                the names of processing elements the key has a physical link to.
        :param function routingFunction: A function, that takes the name of a source processing element, a target 
                                processing element and the adjacency list. Should return the path, taken to communicate
                                between source and target, in case there is no direct physical link between them.
        :param int frequencyDomain: The frequency of the physical links an network routers.
        :param int readLatency: The read latency of the physical links an network routers.
        :param int writeLatency: The write latency of the physical links an network routers.
        :param int readThroughput: The read throughput of the physical links an network routers.
        :param int writeThroughput: The write throughput of the physical links and network routers.
        """
        
        fd = FrequencyDomain('fd_' + networkName, frequencyDomain)
        
        if self.__activeScope != None:
            processorList = self.__elementDict[self.__activeScope][clusterIdentifier]
            
            '''Adding physical links and NOC memories according to the adjacency list
            '''
            for key in adjacencyList:
                name = str(clusterIdentifier) + "_noc_mem_" + str(key)
                communicationResource = Storage(name,
                                                fd,
                                                readLatency,
                                                writeLatency,
                                                readThroughput,
                                                writeThroughput)
                self.__platform.add_communication_resource(communicationResource)
                
                for target in adjacencyList[key]:
                    name = str(clusterIdentifier) + "_pl_" + str(target) + "_" + key
                    communicationResource = CommunicationResource(name,
                                                               CommunicationResourceType.PhysicalLink,
                                                               fd,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                    self.__platform.add_communication_resource(communicationResource)
                    
            for processor in processorList:
                if  adjacencyList[processor[0].name] == []:
                    continue
                else:
                    prim = Primitive(networkName + "_" + processor[0].name)
                    memoryName = str(clusterIdentifier) + "_noc_mem_" + str(processor[0].name)
                    memory = self.__platform.find_communication_resource(memoryName)
                    
                    for innerProcessor in processorList:
                        if adjacencyList[innerProcessor[0].name] == []:
                            continue
                            
                        resourceList = [memory]
                            
                        if innerProcessor != processor:
                            path = routingFunction(adjacencyList, processor[0].name, innerProcessor[0].name)
                            lastPoint = None
                                
                            for point in path:
                                if lastPoint != None:
                                    name = str(clusterIdentifier) + "_pl_" + str(lastPoint) + "_" + str(point)
                                    resource = self.__platform.find_communication_resource(name)
                                    resourceList.append(resource)
                                lastPoint = point
                            
                            produce = CommunicationPhase('produce', resourceList, 'write')
                            consume = CommunicationPhase('consume', resourceList, 'read')
                                        
                            prim.add_producer(innerProcessor[0], [produce])
                            prim.add_consumer(innerProcessor[0], [consume])
                        
                        else:
                            produce = CommunicationPhase('produce', resourceList, 'write')
                            consume = CommunicationPhase('consume', resourceList, 'read')
                                        
                            prim.add_producer(innerProcessor[0], [produce])
                            prim.add_consumer(innerProcessor[0], [consume])
                    
                    self.__platform.add_primitive(prim)
        else:
            return
    
    def createNetworkForChips(self, 
                      networkName, 
                      adjacencyList,
                      routingFunction, 
                      frequencyDomain,
                      readLatency,
                      writeLatency,
                      readThroughput,
                      writeThroughput):
        """Creates a network between the given elements.
        :param string networkName: The name of the network. (primitives belonging to the network will be named
                                like this.
        :param dict {string : list[string]} adjacencyList: The adjacency list of the elements within the network. 
                                The key is the name of an element and the list contains the names of elements the
                                key has a physical link to.
        :param function routingFunction: A function, that takes the name of a source element, a target element and
                                the adjacency list. Should return the path, taken to communicate between source and
                                target, in case there is no direct physical link between them.
        :param int frequencyDomain: The frequency of the physical links an network routers.
        :param int readLatency: The read latency of the physical links an network routers.
        :param int writeLatency: The write latency of the physical links an network routers.
        :param int readThroughput: The read throughput of the physical links an network routers.
        :param int writeThroughput: The write throughput of the physical links and network routers.
        """
        
        fd = FrequencyDomain('fd_' + networkName, frequencyDomain)
        
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
                communicationResource = CommunicationResource(name,
                                                               CommunicationResourceType.Router,
                                                               fd,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                self.__platform.add_communication_resource(communicationResource)
                
                for target in adjacencyList[key]:
                    name = networkName + "_pl_" + str(target) + "_" + key
                    communicationResource = CommunicationResource(name,
                                                               CommunicationResourceType.PhysicalLink,
                                                               fd,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)
                    self.__platform.add_communication_resource(communicationResource)
            
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
           
    def getPlatform(self):
        """Returns the platform, created with the designer. (Only needed for test issues.
        :returns: The platform object the designer is working on.
        :rtype Platform:
        """
        return self.__platform
    
    
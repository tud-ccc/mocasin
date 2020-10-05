# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit,Andres Goens

from pykpn.common.platform import FrequencyDomain, Processor, \
    SchedulingPolicy, Scheduler, Storage, CommunicationPhase, \
    Primitive, CommunicationResource, CommunicationResourceType
from collections import OrderedDict
from pykpn.util import logging
import sys

log = logging.getLogger(__name__)


class PlatformDesigner():
    """"One instance of the platform designer is meant to create exactly one platform.
    It provides the necessary methods to create PE clusters and connect PEs in clusters
    or clusters themselves with communication resources.
    
    :ivar int __peAmount: Holds the amount of the platforms PEs.
    :type __peAmount: int
    :ivar __namingSuffix: Increases every time a new element is pushed on the stack. Will be added to the
                            name of every communication resource added to this element.
    :type __namingSuffix: int
    :ivar __schedulingPolicy: Holds the currently set scheduling policy. This policy will 
                            be applied to all PE clusters initialized afterwards.
    :type __schedulingPolicy: SchedulingPolicy
    :ivar __platform: The platform object, that is created and manipulated.
    :type __platform: Platform
    :ivar __activeScope: The identifier of the scope, the designer is currently working on.
    :type __activeScope: string
    :ivar __scopeStack: A stack for the identifiers of the scopes that are currently opened.
    :type __scopeStack: list[string]
    :ivar __elementDict: For each scope it maps the cluster identifiers to 
                            the list of processing elements of the cluster. 
    :type __elementDict: dict{string : {int : [processors]}}
    """
    
    def __init__(self, platform):
        """Initialize a new instance of the platformDesigner. Should be called by the constructor of a class inheriting
        from Platform.
        :param platform: The platform object which will be modified.
        :type platform: Platform
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
        :param identifier: The identifier, the element can be addressed with.
        :type identifier: int
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
        :param identifier: The identifier the cluster can be addressed within the currently active scope.
        :type identifier: int
        :param name: The name of the processing elements.
        :type name: string
        :param amount: The amount of processing elements in the cluster.
        :type amount: int
        :param frequency: The frequency of the processing elements.
        :type frequency: int
        """
        try:
            fd = FrequencyDomain('fd_' + name, frequency)
            start = self.__peAmount
            end = self.__peAmount + amount
            processors = []
            for i in range (start, end):
                processor = Processor('PE%02d' % i, name, fd)
                self.__platform.add_processor(processor)
                self.__platform.add_scheduler(Scheduler('sched%02d' % i, [processor], self.__schedulingPolicy))
                processors.append((processor,[]))
                self.__peAmount += 1
                
                self.__elementDict[self.__activeScope].update({identifier : processors})
        except:
            log.error("Exception caught: " + sys.exc_info()[0])
    
    def addPeClusterForProcessor(self,
                     identifier,
                     processor,
                     amount):
        """Creates a new cluster of processing elements on the platform.
        :param identifier: The identifier the cluster can be addressed within the currently active scope.
        :type identifier: int
        :param processor: The pykpn Processor object which will be used for the cluster.
        :type processor: Processor
        :param amount: The amount of processing elements in the cluster.
        :type amount: int
        """
        try:
            start = self.__peAmount
            end = self.__peAmount + amount
            processors = []
            for i in range (start, end):
                #copy the input processor since a single processor can only be added once
                name = "processor_" + str(self.__peAmount)
                new_processor = Processor(name,
                                          processor.type,
                                          processor.frequency_domain,
                                          processor.context_load_cycles,
                                          processor.context_store_cycles)
                
                self.__platform.add_processor(new_processor)
                self.__platform.add_scheduler(Scheduler('sched%02d' % i, [new_processor], self.__schedulingPolicy))
                processors.append((new_processor,[]))
                self.__peAmount += 1
                
                self.__elementDict[self.__activeScope].update({identifier : processors})
        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))
    
    def setSchedulingPolicy(self, 
                            policy, 
                            cycles):
        """Sets a new scheduling policy, which will be applied to all schedulers of new PE Clusters.
        :param policy: The name of the policy.
        :type policy: String
        :param cycles: The cycles of the policy.
        :type cycles: int
        :returns: Whether the policy set successfully or not.
        :rtype: bool
        """
        try:
            self.__schedulingPolicy = SchedulingPolicy(policy, cycles)
            return True
        except:
            log.error("Exception caught: " + sys.exc_info()[0])
            return False
          
    def addCacheForPEs(self, 
                       identifier, 
                       readLatency, 
                       writeLatency, 
                       readThroughput, 
                       writeThroughput,
                       frequencyDomain=100000, #TODO: this should be added to tests
                       name='default'):
        """Adds a level 1 cache to each PE of the given cluster.
        :param identifier: The identifier of the cluster to which the cache will be added. 
        :type identifier: int
        :param readLatency: The read latency of the cache.
        :type readLatency: int
        :param writeLatency: The write latency of the cache.
        :type writeLatency: int
        :param readThroughput: The read throughput of the cache.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the cache.
        :type writeThroughput: int
        :param name: The cache name, in case it differs from L1.
        :type name: String
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

        fd = FrequencyDomain('fd_' + name, frequencyDomain)

        try:
            for pe in peList:
                communicationRessource = Storage(nameToGive + pe[0].name,
                                                 frequency_domain= fd,
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
            log.error("Exception caught: " + sys.exc_info()[0])
         
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
        :param name: The name of the storage
        :type name: String
        :param clusterIds: A list of identifiers for all clusters which will be connected.
        :type clusterIds: list[int]
        :param readLatency: The read latency of the communication resource.
        :type readLatency: int
        :param writeLatency: The write latency of the communication resource.
        :type writeLatency: int
        :param readThroughput: The read throughput of the communication resource.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the communication resource.
        :type writeThroughput: int
        """
        if not self.__schedulingPolicy:
            return
        if not self.__activeScope:
            return
        
        for clusterId in clusterIds:
            if clusterId not in self.__elementDict[self.__activeScope]:
                return
        
        clusterDict = self.__elementDict[self.__activeScope]
        nameToGive = str(self.__activeScope) + '_' + name + "_" + str(self.__namingSuffix)
        fd = FrequencyDomain('fd_' + name, frequencyDomain)
        
        try:
            if resourceType == CommunicationResourceType.Storage:
                com_resource = Storage(nameToGive,
                                                 fd,
                                                 readLatency,
                                                 writeLatency,
                                                 readThroughput, 
                                                 writeThroughput)
            else:
                com_resource = CommunicationResource(nameToGive,
                                                               resourceType,
                                                               fd,
                                                               readLatency,
                                                               writeLatency,
                                                               readThroughput,
                                                               writeThroughput)

            self.__platform.add_communication_resource(com_resource)
            prim = Primitive('prim_' + nameToGive)

            for clusterId in clusterIds:
                for pe in clusterDict[clusterId]:
                    pe[1].append(com_resource)
                    produce = CommunicationPhase('produce', [com_resource], 'write')
                    consume = CommunicationPhase('consume', [com_resource], 'read')
                    prim.add_producer(pe[0], [produce])
                    prim.add_consumer(pe[0], [consume])        
            
            self.__platform.add_primitive(prim)
        
        except :
            log.error("Exception caught: " + str(sys.exc_info()[0]))
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
        :param clusterIdentifier: The identifier of the cluster the network will be created for.
        :type clusterIdentifier: int 
        :param networkName: The name of the network. (primitives belonging to the network will be named
                                like this.
        :type networkName: String
        :param adjacencyList: The adjacency list of the processing elements within the network. 
                                The key is the name of a processing element and the list contains
                                the names of processing elements the key has a physical link to.
        :type adjacencyList: dict {String : list[String]}
        :param routingFunction: A function, that takes the name of a source processing element, a target 
                                processing element and the adjacency list. Should return the path, taken to communicate
                                between source and target, in case there is no direct physical link between them.
        :type routingFunction: function
        :param frequencyDomain: The frequency of the physical links an network routers.
        :type frequencyDomain: int
        :param readLatency: The read latency of the physical links an network routers.
        :type readLatency: int
        :param writeLatency: The write latency of the physical links an network routers.
        :type witeLatency: int
        :param readThroughput: The read throughput of the physical links an network routers.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the physical links and network routers.
        :type writeThroughput: int
        """
        fd = FrequencyDomain('fd_' + networkName, frequencyDomain)
        
        if self.__activeScope is not None:
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
                    name = str(clusterIdentifier) + "_pl_" + str(target) + "_" + str(key)
                    communicationResource = CommunicationResource(name,
                                                                  fd,
                                                                  CommunicationResourceType.PhysicalLink,
                                                                  readLatency,
                                                                  writeLatency,
                                                                  readThroughput,
                                                                  writeThroughput)
                    self.__platform.add_communication_resource(communicationResource)
                    
            for processor in processorList:
                if not adjacencyList[processor[0].name]:
                    continue
                else:
                    prim = Primitive(networkName + "_" + processor[0].name)
                    memoryName = str(clusterIdentifier) + "_noc_mem_" + str(processor[0].name)
                    memory = self.__platform.find_communication_resource(memoryName)
                    
                    for innerProcessor in processorList:
                        if not adjacencyList[innerProcessor[0].name]:
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
                            consume = CommunicationPhase('consume', reversed(resourceList), 'read')
                                        
                            prim.add_producer(innerProcessor[0], [produce])
                            prim.add_consumer(innerProcessor[0], [consume])
                        
                        else:
                            produce = CommunicationPhase('produce', resourceList, 'write')
                            consume = CommunicationPhase('consume', reversed(resourceList), 'read')
                                        
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
        :param networkName: The name of the network. (primitives belonging to the network will be named
                                like this.
        :type networkName: String
        :param adjacencyList: The adjacency list of the elements within the network. The key is the name of 
                                an element and the list contains the names of elements the key has a physical
                                link to.
        :type adjacencyList: dict {String : list[String]}
        :param routingFunction: A function, that takes the name of a source element, a target element and
                                the adjacency list. Should return the path, taken to communicate between source and
                                target, in case there is no direct physical link between them.
        :type routingFunction: function
        :param frequencyDomain: The frequency of the physical links an network routers.
        :type frequencyDomaing: int
        :param readLatency: The read latency of the physical links an network routers.
        :type readLatency: int
        :param writeLatency: The write latency of the physical links an network routers.
        :type writeLatency: int
        :param readThroughput: The read throughput of the physical links an network routers.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the physical links and network routers.
        :type writeThroughput: int
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
    
    def getClusterList(self, identifier):
        """Returns a list of all processing elements contained in specified cluster.
        :param identifier: The identifier of the target cluster.
        :type identifier: int
        :returns: A list of names of processing elements
        :rtype list[string]:
        """
        if not identifier in self.__elementDict[self.__activeScope]:
            return None
        else:
            return self.__elementDict[self.__activeScope][identifier]
           
    def getPlatform(self):
        """Returns the platform, created with the designer. (Only needed for test issues.)
        :returns: The platform object the designer is working on.
        :rtype Platform:
        """
        return self.__platform

class genericProcessor(Processor):
    """This class is a generic processor to be passed to the
    different architectures generated with the platform designer.
    :param type: The processor type string (needs to match traces!).
    :type type: string
    :param frequency: The processor frequency
    :type type: int
    :returns: A processor object
    :rtype pykpn.common.platform.Processor:
    """

    def __init__(self,type,frequency=2000000000):
        fd = FrequencyDomain('fd_' + type, frequency)
        super().__init__("DesignerGenericProc" + str(type) + str(frequency), type, fd)






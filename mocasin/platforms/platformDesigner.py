# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Timo Nicolai

from mocasin.common.platform import (
    FrequencyDomain,
    Processor,
    SchedulingPolicy,
    Scheduler,
    Storage,
    CommunicationPhase,
    Primitive,
    CommunicationResource,
    CommunicationResourceType,
)
from collections import OrderedDict
from mocasin.util import logging
import sys

try:
    import pympsym
except:
    pass

log = logging.getLogger(__name__)


class PlatformDesigner:
    """ "One instance of the platform designer is meant to create exactly one platform.
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

        self.__activeScope = "base"
        self.__scopeStack = []
        self.__elementDict = {"base": {}}

        try:
            pympsym
            self.__symLibrary = False  # Disabled for now. Needn refactoring
            self.__agDict = {"base": {}}
        except NameError:
            self.__symLibrary = False

    def newElement(self, identifier):
        """A new scope is opened and pushed on the stack.

        :param identifier: The identifier, the element can be addressed with.
        :type identifier: int
        """
        if self.__symLibrary:
            if self._ag_hasSuperGraph():
                raise ValueError("pympsym: extending super graph not supported")

        self.__scopeStack.append(self.__activeScope)
        self.__activeScope = identifier

        self.__namingSuffix += 1

        self.__elementDict.update({identifier: {}})

        if self.__symLibrary:
            self.__agDict.update({identifier: {}})

    def finishElement(self):
        """The first scope on the stack is closed. The element is still addressable with
        the scopes identifier.
        """
        if len(self.__scopeStack) == 0:
            return

        lastScope = self.__activeScope
        nextScope = self.__scopeStack.pop()

        tmpPElist = []

        for element in self.__elementDict[lastScope]:
            if isinstance(self.__elementDict[lastScope][element], list):
                for entry in self.__elementDict[lastScope][element]:
                    tmpPElist.append(entry)

            elif isinstance(self.__elementDict[lastScope][element], dict):
                for innerElement in self.__elementDict[lastScope][element]:
                    for entry in innerElement:
                        tmpPElist.append(entry)
            else:
                raise RuntimeWarning(
                    "Expected an element of type list or dict!"
                )

        self.__elementDict[nextScope].update({lastScope: tmpPElist})
        self.__elementDict.pop(lastScope, None)

        if self.__symLibrary:
            self._ag_updateAgs(lastScope, nextScope)

        self.__activeScope = nextScope

    def addPeCluster(self, identifier, name, amount, frequency):
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
        log.warning(
            "Deprecationg warning: use addPEClusterForProcessor instead."
        )
        try:
            fd = FrequencyDomain("fd_" + name, frequency)
            start = self.__peAmount
            end = self.__peAmount + amount
            processors = []
            for i in range(start, end):
                processor = Processor("PE%02d" % i, name, fd)
                self.__platform.add_processor(processor)
                self.__platform.add_scheduler(
                    Scheduler(
                        "sched%02d" % i, [processor], self.__schedulingPolicy
                    )
                )
                processors.append((processor, []))
                self.__peAmount += 1

                self.__elementDict[self.__activeScope].update(
                    {identifier: processors}
                )

        except:
            log.error("Exception caught: " + sys.exc_info()[0])

        if self.__symLibrary:
            self._ag_addCluster(identifier, name, amount, processors)

    def addPeClusterForProcessor(self, identifier, processor, amount):
        """Creates a new cluster of processing elements on the platform.

        :param identifier: The identifier the cluster can be addressed within the currently active scope.
        :type identifier: int
        :param processor: The mocasin Processor object which will be used for the cluster.
        :type processor: Processor
        :param amount: The amount of processing elements in the cluster.
        :type amount: int
        """
        try:
            start = self.__peAmount
            end = self.__peAmount + amount
            processors = []
            for i in range(start, end):
                # copy the input processor since a single processor can only be added once
                name = f"processor_{self.__peAmount:04d}"
                new_processor = Processor(
                    name,
                    processor.type,
                    processor.frequency_domain,
                    processor.context_load_cycles,
                    processor.context_store_cycles,
                )

                self.__platform.add_processor(new_processor)
                self.__platform.add_scheduler(
                    Scheduler(
                        "sched%02d" % i,
                        [new_processor],
                        self.__schedulingPolicy,
                    )
                )
                processors.append((new_processor, []))
                self.__peAmount += 1

                self.__elementDict[self.__activeScope].update(
                    {identifier: processors}
                )
        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))

        if self.__symLibrary:
            self._ag_addCluster(identifier, processor.name, amount, processors)

    def setSchedulingPolicy(self, policy, cycles):
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

    def addCacheForPEs(
        self,
        identifier,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequencyDomain=100000,  # TODO: this should be added to tests
        name="default",
    ):
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
        if name != "default":
            nameToGive = name
        else:
            nameToGive = "L1_"
        peList = self.__elementDict[self.__activeScope][identifier]

        fd = FrequencyDomain("fd_" + name, frequencyDomain)

        try:
            for pe in peList:
                communicationRessource = Storage(
                    nameToGive + pe[0].name,
                    frequency_domain=fd,
                    read_latency=readLatency,
                    write_latency=writeLatency,
                    read_throughput=readThroughput,
                    write_throughput=writeThroughput,
                )
                self.__platform.add_communication_resource(
                    communicationRessource
                )
                pe[1].append(communicationRessource)

                prim = Primitive("prim_" + nameToGive + pe[0].name)
                produce = CommunicationPhase("produce", pe[1], "write")
                consume = CommunicationPhase("consume", pe[1], "read")
                prim.add_producer(pe[0], [produce])
                prim.add_consumer(pe[0], [consume])
                self.__platform.add_primitive(prim)

        except:
            log.error("Exception caught: " + sys.exc_info()[0])

        if self.__symLibrary:
            self._ag_addClusterCache(identifier, name)

    def addCommunicationResource(
        self,
        name,
        clusterIds,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        resourceType=CommunicationResourceType.Storage,
        frequencyDomain=0,
    ):
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
        nameToGive = (
            str(self.__activeScope)
            + "_"
            + name
            + "_"
            + str(self.__namingSuffix)
        )
        fd = FrequencyDomain("fd_" + name, frequencyDomain)

        try:
            if resourceType == CommunicationResourceType.Storage:
                com_resource = Storage(
                    nameToGive,
                    fd,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )
            else:
                com_resource = CommunicationResource(
                    nameToGive,
                    resourceType,
                    fd,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )

            self.__platform.add_communication_resource(com_resource)
            prim = Primitive("prim_" + nameToGive)

            for clusterId in clusterIds:
                for pe in clusterDict[clusterId]:
                    pe[1].append(com_resource)
                    produce = CommunicationPhase(
                        "produce", [com_resource], "write"
                    )
                    consume = CommunicationPhase(
                        "consume", [com_resource], "read"
                    )
                    prim.add_producer(pe[0], [produce])
                    prim.add_consumer(pe[0], [consume])

            self.__platform.add_primitive(prim)

        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

        if self.__symLibrary:
            idType = self._ag_classifyIdentifiers(clusterIds)

            if self._ag_hasChips():
                if idType != "chips":
                    raise ValueError(
                        "pympsym: cannot mix clusters/chips connections"
                    )

                if self._ag_hasIdenticalChips():
                    if not self._ag_hasSuperGraph():
                        self._ag_createSuperGraph()

                    self._ag_fullyConnectSuperGraph(clusterIds, name)

                    if self.__activeScope == "base":
                        self._ag_updateBaseAgs()
            else:
                if idType != "clusters":
                    raise ValueError(
                        "pympsym: cannot mix clusters/chips connections"
                    )

                self._ag_fullyConnectClusters(clusterIds, name)

    def createNetworkForCluster(
        self,
        clusterIdentifier,
        networkName,
        adjacencyList,
        routingFunction,
        frequencyDomain,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
    ):
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
        :param routingFunction: A function that takes the name of a source processing element, a target
                                processing element and the adjacency list. Should return the path taken to communicate
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
        fd = FrequencyDomain("fd_" + networkName, frequencyDomain)

        if self.__activeScope is not None:
            processorList = self.__elementDict[self.__activeScope][
                clusterIdentifier
            ]
            processorNames = [p.name for p, _ in processorList]

            """Adding physical links and NOC memories according to the adjacency list
            """
            for key in adjacencyList:
                name = str(clusterIdentifier) + "_noc_mem_" + str(key)
                communicationResource = Storage(
                    name,
                    fd,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )
                self.__platform.add_communication_resource(
                    communicationResource
                )

                for target in adjacencyList[key]:
                    name = (
                        str(clusterIdentifier)
                        + "_pl_"
                        + str(target)
                        + "_"
                        + str(key)
                    )
                    communicationResource = CommunicationResource(
                        name,
                        fd,
                        CommunicationResourceType.PhysicalLink,
                        readLatency,
                        writeLatency,
                        readThroughput,
                        writeThroughput,
                    )
                    self.__platform.add_communication_resource(
                        communicationResource
                    )

                    if self.__symLibrary:
                        self._ag_addClusterChannel(key, target, networkName)

            for processor in processorList:
                if not adjacencyList[processor[0].name]:
                    continue
                else:
                    prim = Primitive(networkName + "_" + processor[0].name)
                    memoryName = (
                        str(clusterIdentifier)
                        + "_noc_mem_"
                        + str(processor[0].name)
                    )
                    memory = self.__platform.find_communication_resource(
                        memoryName
                    )

                    for innerProcessor in processorList:
                        if not adjacencyList[innerProcessor[0].name]:
                            continue

                        resourceList = [memory]

                        if innerProcessor != processor:
                            path = routingFunction(
                                adjacencyList,
                                processor[0].name,
                                innerProcessor[0].name,
                            )
                            lastPoint = None

                            for point in path:
                                if lastPoint != None:
                                    name = (
                                        str(clusterIdentifier)
                                        + "_pl_"
                                        + str(lastPoint)
                                        + "_"
                                        + str(point)
                                    )
                                    resource = self.__platform.find_communication_resource(
                                        name
                                    )
                                    resourceList.append(resource)
                                lastPoint = point

                            produce = CommunicationPhase(
                                "produce", resourceList, "write"
                            )
                            consume = CommunicationPhase(
                                "consume", reversed(resourceList), "read"
                            )

                            prim.add_producer(innerProcessor[0], [produce])
                            prim.add_consumer(innerProcessor[0], [consume])

                        else:
                            produce = CommunicationPhase(
                                "produce", resourceList, "write"
                            )
                            consume = CommunicationPhase(
                                "consume", reversed(resourceList), "read"
                            )

                            prim.add_producer(innerProcessor[0], [produce])
                            prim.add_consumer(innerProcessor[0], [consume])

                    self.__platform.add_primitive(prim)
        else:
            return

    def createNetworkForChips(
        self,
        networkName,
        adjacencyList,
        routingFunction,
        frequencyDomain,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
    ):
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

        fd = FrequencyDomain("fd_" + networkName, frequencyDomain)

        if self.__activeScope != None:
            """Creating a network between independent chips"""
            if self.__elementDict == {}:
                return
            for key in adjacencyList:
                """workaround with i, because different elements can have the same
                adjacency entry
                """
                name = networkName + "_" + "router_" + key
                communicationResource = CommunicationResource(
                    name,
                    CommunicationResourceType.Router,
                    fd,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )
                self.__platform.add_communication_resource(
                    communicationResource
                )

                for target in adjacencyList[key]:
                    name = networkName + "_pl_" + str(target) + "_" + key
                    communicationResource = CommunicationResource(
                        name,
                        CommunicationResourceType.PhysicalLink,
                        fd,
                        readLatency,
                        writeLatency,
                        readThroughput,
                        writeThroughput,
                    )
                    self.__platform.add_communication_resource(
                        communicationResource
                    )

            for key in self.__elementDict[self.__activeScope]:
                if adjacencyList[key] == []:
                    continue
                for pe in self.__elementDict[self.__activeScope][key]:
                    """Adding a primitive for each pe in the network"""
                    prim = Primitive("prim_" + networkName + "_" + pe[0].name)

                    routerName = networkName + "_" + "router_" + str(key)
                    router = self.__platform.find_communication_resource(
                        routerName
                    )

                    for innerKey in self.__elementDict[self.__activeScope]:
                        if adjacencyList[innerKey] == []:
                            continue

                        resourceList = [router]

                        if innerKey != key:
                            path = routingFunction(adjacencyList, key, innerKey)
                            lastPoint = None

                            for point in path:
                                if lastPoint != None:
                                    name = (
                                        networkName
                                        + "_pl_"
                                        + str(lastPoint)
                                        + "_"
                                        + str(point)
                                    )
                                    resource = self.__platform.find_communication_resource(
                                        name
                                    )
                                    resourceList.append(resource)
                                lastPoint = point

                        for innerPe in self.__elementDict[self.__activeScope][
                            innerKey
                        ]:
                            """Iterating again over all pe's in the network to
                            create their consumer and producer phases etc. for
                            the primitive.
                            """
                            produce = CommunicationPhase(
                                "produce", resourceList, "write"
                            )
                            consume = CommunicationPhase(
                                "consume", resourceList, "read"
                            )

                            prim.add_producer(innerPe[0], [produce])
                            prim.add_consumer(innerPe[0], [consume])

                    self.__platform.add_primitive(prim)

            if self.__symLibrary:
                chipIds = set(adjacencyList.keys()) | set(
                    c for v in adjacencyList.values() for c in v
                )

                if not self._ag_classifyIdentifiers(chipIds):
                    raise ValueError(
                        "pympsym: chip network must consist of chips only"
                    )

                if self._ag_hasIdenticalChips():
                    if not self._ag_hasSuperGraph():
                        self._ag_createSuperGraph()

                    self._ag_connectSuperGraph(adjacencyList, networkName)

                    if self.__activeScope == "base":
                        self._ag_updateBaseAgs()
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
        if self.__symLibrary:
            self.__platform.ag = self._ag_makeChipAgs("base")

        return self.__platform

    def _ag(self, scope=None):
        if scope is None:
            scope = self.__activeScope

        return self.__agDict[scope]

    def _ag_pop(self, scope=None):
        return self.__agDict.pop(scope)

    def _ag_isBase(self, scope=None):
        return scope == "base"

    def _ag_classifyIdentifiers(self, ids, scope=None):
        if not self._ag_hasChips(scope):
            return "clusters"

        chipNames = set(chipName for chipName, _ in self._ag(scope)["chips"])

        if all(id in chipNames for id in ids):
            return "chips"
        elif not any(id in chipNames for id in ids):
            return "clusters"
        else:
            return "mixed"

    def _ag_hasAgs(self, scope=None):
        return "system" in self._ag(scope)

    def _ag_setAgs(self, system, scope=None):
        self._ag(scope)["system"] = system

    def _ag_makeAgs(self, scope=None):
        if self._ag_hasSuperGraph(scope):
            return self._ag_makeSuperGraphAgs(scope)
        elif self._ag_hasChips(scope):
            return self._ag_makeChipAgs(scope)
        else:
            return self._ag_makeClusterAgs(scope)

    def _ag_updateBaseAgs(self):
        assert self.__activeScope == "base"

        self._ag_setAgs(self._ag_makeAgs())

    def _ag_updateAgs(self, lastScope, nextScope):
        if self._ag_isBase(lastScope):
            raise ValueError("pympsym: improperly nested elements")

        if self._ag_hasAgs(lastScope):
            raise ValueError("pympsym: improperly nested elements")

        self._ag_setAgs(self._ag_makeAgs(lastScope), lastScope)

        self._ag_addChip(lastScope, self._ag_pop(lastScope), nextScope)

    def _ag_hasChips(self, scope=None):
        return "chips" in self._ag(scope)

    def _ag_hasIdenticalChips(self, scope=None):
        return True  # TODO

    def _ag_addChip(self, chipName, chip, scope=None):
        if self._ag_hasClusters(scope):
            raise ValueError("pympsym: mixing cannot mix chips/clusters")

        ag = self._ag(scope)

        ag["chips"] = ag.get("chips", []) + [(chipName, chip)]

    def _ag_makeChipAgs(self, scope=None):
        agc = pympsym.ArchGraphCluster()
        for _, chip in self._ag(scope)["chips"]:
            agc.add_subsystem(chip["system"])

        return agc

    def _ag_hasSuperGraph(self, scope=None):
        ag = self._ag(scope)

        return "proto" in ag and "super_graph" in ag

    def _ag_createSuperGraph(self, scope=None):
        ag = self._ag(scope)

        protoChipName, protoChip = ag["chips"][0]
        proto = protoChip["system"]

        superGraph = pympsym.ArchGraph()
        superGraphProcessors = {}

        for i, (chipName, chip) in enumerate(ag["chips"]):
            superGraphProcessors[chipName] = superGraph.add_processor(
                protoChipName
            )

        ag["proto"] = proto
        ag["super_graph"] = superGraph
        ag["super_graph_processors"] = superGraphProcessors

    def _ag_connectSuperGraph(self, chipAdjacencies, chType, scope=None):
        ag = self._ag(scope)

        superGraph = ag["super_graph"]
        superGraphProcessors = ag["super_graph_processors"]

        chipAdjacencies = {
            superGraphProcessors[k]: [superGraphProcessors[c] for c in v]
            for k, v in chipAdjacencies.items()
        }

        superGraph.add_channels(chipAdjacencies, chType)

    def _ag_fullyConnectSuperGraph(self, chips, chType, scope=None):
        ag = self._ag(scope)

        superGraph = ag["super_graph"]
        superGraphProcessors = ag["super_graph_processors"]

        for chip1 in chips:
            chip1 = superGraphProcessors[chip1]

            for chip2 in chips:
                chip2 = superGraphProcessors[chip2]

                superGraph.add_channel(chip1, chip2, chType)
                superGraph.add_channel(chip2, chip1, chType)

    def _ag_makeSuperGraphAgs(self, scope=None):
        ag = self._ag(scope)

        return pympsym.ArchUniformSuperGraph(ag["super_graph"], ag["proto"])

    def _ag_hasClusters(self, scope=None):
        return "clusters" in self._ag(scope)

    def _ag_addCluster(self, clusterId, peName, peAmount, pes, scope=None):
        if self._ag_hasChips(scope):
            raise ValueError("pympsym: mixing cannot mix chips/clusters")

        ag = self._ag(scope)

        if "clusters" not in ag:
            ag["clusters"] = {
                "processors": {},
                "groups": {},
                "graph": pympsym.ArchGraph(),
            }

        pes = [p.name for p, _ in pes]

        # graph
        peMax = ag["clusters"]["graph"].add_processors(peAmount, peName)

        # cluster
        ag["clusters"]["groups"][clusterId] = set(pes)

        # processors
        peOffs = peMax - peAmount + 1
        for i, pe in enumerate(pes, start=peOffs):
            ag["clusters"]["processors"][pe] = i

    def _ag_clusterProcessors(self, scope=None):
        return self._ag(scope)["clusters"]["processors"]

    def _ag_clusterGroups(self, scope=None):
        return self._ag(scope)["clusters"]["groups"]

    def _ag_clusterGraph(self, scope=None):
        return self._ag(scope)["clusters"]["graph"]

    def _ag_addClusterChannel(self, peSource, peTarget, chType, scope=None):
        clusterProcessors = self._ag_clusterProcessors(scope)
        clusterGraph = self._ag_clusterGraph(scope)

        peSource = clusterProcessors[peSource]
        peTarget = clusterProcessors[peTarget]

        clusterGraph.add_channel(peSource, peTarget, chType)

    def _ag_addClusterCache(self, cluster, cacheType, scope=None):
        clusterProcessors = self._ag_clusterProcessors(scope)
        clusterGroups = self._ag_clusterGroups(scope)
        clusterGraph = self._ag_clusterGraph(scope)

        for pe in clusterGroups[cluster]:
            pe = clusterProcessors[pe]

            clusterGraph.add_channel(pe, pe, "cache_" + cacheType)

    def _ag_fullyConnectClusters(self, clusters, chType, scope=None):
        clusterGroups = self._ag_clusterGroups(scope)

        for cluster1 in clusters:
            for cluster2 in clusters:
                for pe1 in clusterGroups[cluster1]:
                    for pe2 in clusterGroups[cluster2]:
                        self._ag_addClusterChannel(pe1, pe2, chType)
                        self._ag_addClusterChannel(pe2, pe1, chType)

    def _ag_makeClusterAgs(self, scope=None):
        return self._ag_clusterGraph(scope)


class genericProcessor(Processor):
    """This class is a generic processor to be passed to the
    different architectures generated with the platform designer.

    :param type: The processor type string (needs to match traces!).
    :type type: string
    :param frequency: The processor frequency
    :type type: int
    :returns: A processor object
    :rtype mocasin.common.platform.Processor:
    """

    def __init__(self, type, frequency=2000000000):
        fd = FrequencyDomain("fd_" + type, frequency)
        super().__init__(
            "DesignerGenericProc" + str(type) + str(frequency), type, fd
        )

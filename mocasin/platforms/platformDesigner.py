# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Timo Nicolai, Julian Robledo

from mocasin.common.platform import (
    FrequencyDomain,
    Processor,
    SchedulingPolicy,
    Scheduler,
    Storage,
    CommunicationPhase,
    Primitive,
    ProcessorPowerModel,
    CommunicationResource,
    CommunicationResourceType,
)
from mocasin.util import logging
import sys

log = logging.getLogger(__name__)


class PlatformDesigner:
    """ "One instance of the platform designer is meant to create exactly one platform.
    It provides the necessary methods to create PE clusters and connect PEs in clusters
    or clusters themselves with communication resources.

    :ivar __schedulingPolicy: Holds the currently set scheduling policy. This policy will
                            be applied to all PE clusters initialized afterwards.
    :type __schedulingPolicy: SchedulingPolicy
    :ivar __platform: The platform object, that is created and manipulated.
    :type __platform: Platform
    :ivar __clusterList: List of clusters in the platform.
    :type __clusterList: list[clusters]
    """

    def __init__(self, platform):
        """Initialize a new instance of the platformDesigner. Should be called by the constructor of a class inheriting
        from Platform.
        :param platform: The platform object which will be modified.
        :type platform: Platform
        """
        self.__schedulingPolicy = None
        self.__platform = platform
        self.__clusterList = []

    def addCluster(self, name, parent=None):
        """Add a new cluster to the platform.

        :param name: The name, the cluster can be addressed with.
        :type name: int
        :param parent: The parent cluster in which the new cluster will be contained.
        :type parent: cluster
        :returns: The generated cluster.
        :rtype: cluster
        """
        newCluster = cluster(name)
        self.__clusterList.append(newCluster)
        if not self.__clusterList:
            parent.innerClusters.append(newCluster)
            newCluster.outerCluster = parent
        return newCluster

    def addPeToCluster(
        self,
        cluster,
        name,
        processorType,
        frequency_domain,
        power_model,
        context_load_cycles,
        context_store_cycles
    ):
        """Adds a processing element to cluster.

        :param cluster: The cluster the processing element will be added to.
        :type cluster: cluster
        :param name: processor name.
        :type name: string
        :param processorType: Processor type.
        :type processorType: string
        :param frequency_domain: Prequency domain for processor.
        :type frequency_domain: FrequencyDomain
        :param power_model: Power model for processor.
        :type power_model: ProcessorPowerModel
        :param context_load_cycles: Context load cycles for processor.
        :type context_load_cycles: int
        :param context_store_cycles: Context store cycles for processor.
        :type context_store_cycles: int
        """
        try:
            new_processor = Processor(
                name,
                processorType,
                frequency_domain,
                power_model,
                context_load_cycles,
                context_store_cycles,
            )
            self.__platform.add_processor(new_processor)
            self.__platform.add_scheduler(
                Scheduler(
                    f"sched_{new_processor.name}",
                    [new_processor],
                    self.__schedulingPolicy,
                )
            )
            cluster.pes.append(new_processor)
        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))

    def getPesInCluster(self, cluster):
        """get list of PEs contained in a cluster. It does not consider PEs contined in inner clusters.

        :param cluster: The cluster the processing elements will be added to.
        :type cluster: cluster
        :returns: list of PEs in cluster.
        :rtype: list[processor]
        """
        return cluster.pes

    def addCacheToPE(
        self,
        name,
        processor,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        # FIXME, this is a strange default
        frequencyDomain=100000,  # TODO: this should be added to tests
    ):
        """Adds a level 1 cache to each of the given PEs.

        :param processors: The processors the cache will be added to.
        :type processors: list[Processor]
        :param name: The cache name, in case it differs from L1.
        :type name: String
        :param readLatency: The read latency of the cache.
        :type readLatency: int
        :param writeLatency: The write latency of the cache.
        :type writeLatency: int
        :param readThroughput: The read throughput of the cache.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the cache.
        :type writeThroughput: int
        """

        fd = FrequencyDomain("fd_" + name, frequencyDomain)

        l1 = Storage(
            name,
            frequency_domain=fd,
            read_latency=readLatency,
            write_latency=writeLatency,
            read_throughput=readThroughput,
            write_throughput=writeThroughput,
        )
        self.__platform.add_communication_resource(l1)
        prim = Primitive("prim_" + name)

        produce = CommunicationPhase("produce", [l1], "write")
        consume = CommunicationPhase("consume", [l1], "read")
        prim.add_producer(processor, [produce])
        prim.add_consumer(processor, [consume])
        self.__platform.add_primitive(prim)

    def addCommunicationResource(
        self,
        name,
        cluster,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        # FIXME: probably we should just rename the method to add_storage
        resourceType=CommunicationResourceType.Storage,
        # FIXME: this argument should either be renamed to frequency or
        # expect an actual FrequencyDomain object
        frequencyDomain=0,
    ):
        """Adds a communication resource to the platform. All cores of the given cluster names can communicate
        via this resource.

        :param name: The name of the storage
        :type name: String
        :param cluster: A list of clusters which will be connected.
        :type cluster: list[int]
        :param readLatency: The read latency of the communication resource.
        :type readLatency: int
        :param writeLatency: The write latency of the communication resource.
        :type writeLatency: int
        :param readThroughput: The read throughput of the communication resource.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the communication resource.
        :type writeThroughput: int
        """
        #TODO: check that there are not other fd with the same name
        fd = FrequencyDomain("fd_" + name, frequencyDomain)

        try:
            # FIXME: why distinguish storage and other types here?
            if resourceType == CommunicationResourceType.Storage:
                comResource = Storage(
                    name,
                    fd,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )
            else:
                comResource = CommunicationResource(
                    name,
                    fd,
                    resourceType,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )
            self.__platform.add_communication_resource(comResource)
            cluster.commResources.append(comResource)
            return comResource

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def connectPesInClusterToComm(
        self,
        clusters,
        comResource,):
        """Adds a communication resource to the platform. All cores of the given cluster names can communicate
        via this resource.

        :param clusters: A list of clusters whose inner PEs will be connected to the given communication resource.
        :type clusters: list[cluster]
        :param comResource: Communication resource the PEs in the given cluster will be connected to.
        :type comResource: communicationResource
        """
        prim = Primitive("prim_" + comResource.name)

        for cluster in clusters:
            for pe in cluster.pes:
                produce = CommunicationPhase(
                    "produce", [comResource], "write"
                )
                consume = CommunicationPhase(
                    "consume", [comResource], "read"
                )
                prim.add_producer(pe, [produce])
                prim.add_consumer(pe, [consume])
        self.__platform.add_primitive(prim)

    def connectPeToCom(
        self,
        elements,
        communicationResource):
        """Adds a communication resource to the platform. All cores of the given cluster names can communicate
        via this resource.

        :param elements: A list of elements (communicationResource or Processor) to be connected to the given communication resource.
        :type elements: list[communicationResource or Processor]
        :param communicationResource: Communication resource the PEs in the given cluster will be connected to.
        :type communicationResource: communicationResource
        """
        name = "prim_" + communicationResource.name
        if name in self.__platform.primitives():
            prim = self.__platform.find_primitive(name)
        else:
            prim = Primitive(name)

        for element in elements:
            # if pe, must be contained in the current cluster
            if isinstance(element, Processor):
                for cluster in self.__clusterList:
                    for comRes in cluster.commResources:
                        if comRes.name == communicationResource.name:
                            currentCluster = cluster
                            break
                    else:
                        continue
                    break
                if element in currentCluster.pes:
                    produce = CommunicationPhase(
                        "produce", [communicationResource], "write"
                    )
                    consume = CommunicationPhase(
                        "consume", [communicationResource], "read"
                    )
                    prim.add_producer(element, [produce])
                    prim.add_consumer(element, [consume])
                #TODO: else: error pe not in cluster
        self.__platform.add_primitive(prim)

    def connectClusterToCom(
        self,
        elements,
        communicationResource):
        """Adds a communication resource to the platform. All cores of the given cluster names can communicate
        via this resource.

        :param elements: A list of elements (communicationResource or Processor) to be connected to the given communication resource.
        :type elements: list[communicationResource or Processor]
        :param communicationResource: Communication resource the PEs in the given cluster will be connected to.
        :type communicationResource: communicationResource
        """
        name = "prim_" + communicationResource.name
        if name in self.__platform.primitives():
            prim = self.__platform.find_primitive("prim_" + communicationResource.name)
        else:
            prim = Primitive("prim_" + communicationResource.name)

        for element in elements:
            # TODO: check that element is a comm resource or pe
            if isinstance(element, CommunicationResource):
                # if comm resource, it must be contained in one of the inner clusters
                # take inner communicationResource as base, and add up the given commResource
                # to the new primitive
                for cluster in self.__clusterList:
                    for comRes in cluster.commResources:
                        if comRes.name == element.name:
                            innerComPrim = self.__platform.find_primitive("prim_" + comRes.name)
                            break
                        # TODO: else - error, comResource not in cluster
                    # work around to break out of nested loops if the inner loop breaks
                    else:
                        continue
                    break

                for producer in innerComPrim.producers:
                    resources = innerComPrim.produce_phases[producer.name]
                    res = []
                    for ns in resources:
                        res.extend(ns.resources)
                    res.append(communicationResource)
                    produce = CommunicationPhase(
                        "produce", res, "write"
                    )
                    prim.add_producer(producer, [produce])
                for consumer in innerComPrim.consumers:
                    resources = innerComPrim.consume_phases[consumer.name]
                    res = []
                    for ns in resources:
                        res.extend(ns.resources)
                    res.append(communicationResource)
                    consume = CommunicationPhase(
                        "consume", res, "read"
                    )
                    prim.add_consumer(consumer, [consume])

        self.__platform.add_primitive(prim)

    def connectComToCom(
        self,
        elements,
        communicationResource):
        """Adds a communication resource to the platform. All cores of the given cluster names can communicate
        via this resource.

        :param elements: A list of elements (communicationResource or Processor) to be connected to the given communication resource.
        :type elements: list[communicationResource or Processor]
        :param communicationResource: Communication resource the PEs in the given cluster will be connected to.
        :type communicationResource: communicationResource
        """
        name = "prim_" + communicationResource.name
        if name in self.__platform.primitives():
            prim = self.__platform.find_primitive("prim_" + communicationResource.name)
        else:
            prim = Primitive("prim_" + communicationResource.name)

        for element in elements:
            # TODO: check that element is a comm resource or pe
            if isinstance(element, CommunicationResource):
                # if comm resource, it must be contained in one of the inner clusters
                # take inner communicationResource as base, and add up the given commResource
                # to the new primitive
                for cluster in self.__clusterList:
                    for comRes in cluster.commResources:
                        if comRes.name == communicationResource.name:
                            currentCluster = cluster
                            break
                    else:
                        continue
                    break
                if element in currentCluster.pes:
                    for producer in element.producers:
                        resources = element.produce_phases[producer.name]
                        res = []
                        for ns in resources:
                            res.extend(ns.resources)
                        res.append(communicationResource)
                        produce = CommunicationPhase(
                            "produce", res, "write"
                        )
                        prim.add_producer(producer, [produce])
                    for consumer in element.consumers:
                        resources = element.consume_phases[consumer.name]
                        res = []
                        for ns in resources:
                            res.extend(ns.resources)
                        res.append(communicationResource)
                        consume = CommunicationPhase(
                            "consume", res, "read"
                        )
                        prim.add_consumer(consumer, [consume])

        self.__platform.add_primitive(prim)

    def createNetworkForCluster(
        self,
        cluster,
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

        :param cluster: The cluster the network will be created for.
        :type cluster: cluster
        :param networkName: The name of the network. (primitives belonging to the network will be named
                                like this.
        :type networkName: String
        :param adjacencyList: The adjacency list of the processing clusters within the network.
                                The key is the name of a processing cluster and the list contains
                                the names of processing clusters the key has a physical link to.
        :type adjacencyList: dict {String : list[String]}
        :param routingFunction: A function that takes the name of a source processing cluster, a target
                                processing cluster and the adjacency list. Should return the path taken to communicate
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
        processorList = cluster.pes

        """Adding physical links and NOC memories according to the adjacency list
        """
        for key in adjacencyList:
            name = str(cluster.name) + "_noc_mem_" + str(key)
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
                    str(cluster.name)
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

        for processor in processorList:
            if not adjacencyList[processor[0].name]:
                continue
            else:
                prim = Primitive(networkName + "_" + processor[0].name)
                memoryName = (
                    str(cluster.name)
                    # FIXME: this will lead to issues if we have >=2 NoCs
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
                                    str(cluster.name)
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
                            "consume", list(reversed(resourceList)), "read"
                        )

                        prim.add_producer(innerProcessor[0], [produce])
                        prim.add_consumer(innerProcessor[0], [consume])

                    else:
                        produce = CommunicationPhase(
                            "produce", resourceList, "write"
                        )
                        consume = CommunicationPhase(
                            "consume", list(reversed(resourceList)), "read"
                        )

                        prim.add_producer(innerProcessor[0], [produce])
                        prim.add_consumer(innerProcessor[0], [consume])

                self.__platform.add_primitive(prim)

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

    def setPeripheralStaticPower(self, static_power):
        """Set peripheral static power of the platform."""
        self.__platform.peripheral_static_power = static_power

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
    :param static_power: The static power of the processing elements.
    :type static_power: float
    :param dynamic_power: The dynamic power of the processing elements.
    :type dynamic_power: float
    :rtype mocasin.common.platform.Processor:
    """

    def __init__(
        self, type, frequency=2000000000, static_power=None, dynamic_power=None
    ):
        fd = FrequencyDomain("fd_" + type, frequency)
        if static_power is not None and dynamic_power is not None:
            ppm = ProcessorPowerModel(
                "ppm_" + type, static_power, dynamic_power
            )
        else:
            ppm = None
        super().__init__(
            "DesignerGenericProc" + str(type) + str(frequency), type, fd, ppm
        )

class cluster:
    """Represents one cluster in the platform. A cluster contains a set of clusters and/or processors.

    :ivar string name: Name of the cluster.
    :type name: string
    :ivar innerClusters: Holds all clusters inside the current cluster.
    :type innerClusters: list[cluster]
    :ivar commResources: Holds all communication resources inside cluster.
    :type commResources: list[CommunicationResource]
    :ivar pes: Holds all processors inside the cluster.
    :type pes: list[processor]
    :ivar outerCluster: Holds parent cluster in which the cluster will be contained.
                        outerCluster can be set to None.
    :type outerCluster: cluster
    """
    def __init__(self, name):
        self.name = name
        self.innerClusters = []
        self.commResources = []
        self.pes = []
        self.outerCluster = None

class myPrimitive:
    def __init__(self, identifier):
        #self.name = name
        self.consumers = []
        self.producers = []
        self.consume_phases = {}
        self.produce_phases = {}







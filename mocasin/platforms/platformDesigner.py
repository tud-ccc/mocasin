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

    :ivar __namingSuffix: Increases every time a new cluster is pushed on the stack. Will be added to the
                            name of every communication resource added to this cluster.
    :type __namingSuffix: int
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
        self.__namingSuffix = 0
        self.__schedulingPolicy = None
        self.__platform = platform
        self.__clusterList = []

    class cluster:
        """Represents one cluster in the platform. A cluster contains a set of clusters and/or processors.

        :ivar string identifier: Name of the cluster.
        :type identifier: string
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
        def __init__(self, identifier):
            self.identifier = identifier
            self.innerClusters = []
            self.commResources = []
            self.pes = []
            self.outerCluster = None

    def addCluster(self, identifier, parent=None):
        """Add a new cluster to the platform.

        :param identifier: The identifier, the cluster can be addressed with.
        :type identifier: int
        :param parent: The parent cluster in which the new cluster will be contained.
        :type parent: cluster
        :returns: The generated cluster.
        :rtype: cluster
        """
        newCluster = self.cluster(identifier)
        self.__clusterList.append(newCluster)
        if not self.__clusterList:
            parent.innerClusters.append(newCluster)
            newCluster.outerCluster = parent
        self.__namingSuffix += 1
        return newCluster

    def generatePeList(self, processor, amount, processor_names):
        """generates a list of processors from a base processor.

        :param processor: The identifier, the cluster can be addressed with.
        :type processor: Processor
        :param amount: Amount of processors to generate.
        :type amount: int
        :param processor_names: names to give to the processors.
        :type processor_names: list[string]
        :returns: list of generated processors.
        :rtype: list[processor]
        """

        if len(processor_names) != amount:
            raise RuntimeWarning(
                "processor_names must contain as many elements as the amount of processors"            
            )
                    
        processors = []
        for i in range(amount):
            new_processor = Processor(
                processor_names[i],
                processor.type,
                processor.frequency_domain,
                processor.power_model,
                processor.context_load_cycles,
                processor.context_store_cycles,
            )
            processors.append(new_processor)
        return processors

    def addPeSet(self, cluster, processors):
        """Adds a set of processing elements to a cluster.

        :param cluster: The cluster the processing elements will be added to.
        :type cluster: cluster
        :param processors: The set of Processor objects that will be added to the cluster.
        :type processors: list[Processor]
        """
        try:
            pes = []
            for pe in processors:
                self.__platform.add_processor(pe)
                self.__platform.add_scheduler(
                    Scheduler(
                        f"sched_{pe.name}",
                        [pe],
                        self.__schedulingPolicy,
                    )
                )
                pes.append((pe, []))
            cluster.pes.extend(pes)
        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))


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
        cluster,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        # FIXME, this is a strange default
        frequencyDomain=100000,  # TODO: this should be added to tests
        name="L1_",
    ):
        """Adds a level 1 cache to each PE of the given cluster.

        :param cluster: The cluster the cache will be added to.
        :type cluster: cluster
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
        # FIXME: this should probably produce an error instead of returning
        # silently
        if self.__schedulingPolicy == None:
            return
        if cluster == None:
            return

        peList = cluster.pes
        fd = FrequencyDomain("fd_" + name, frequencyDomain)

        try:
            for pe in peList:
                l1 = Storage(
                    name + pe[0].name,
                    frequency_domain=fd,
                    read_latency=readLatency,
                    write_latency=writeLatency,
                    read_throughput=readThroughput,
                    write_throughput=writeThroughput,
                )
                self.__platform.add_communication_resource(l1)

                # FIXME: What is this doing??
                pe[1].append(l1)
                prim = Primitive("prim_" + name + pe[0].name)

                produce = CommunicationPhase("produce", [l1], "write")
                consume = CommunicationPhase("consume", [l1], "read")
                prim.add_producer(pe[0], [produce])
                prim.add_consumer(pe[0], [consume])
                self.__platform.add_primitive(prim)

        except:  # FIXME: This is fishy
            log.error("Exception caught: " + sys.exc_info()[0])

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
        """Adds a communication resource to the platform. All cores of the given cluster identifiers can communicate
        via this resource.

        :param name: The name of the storage
        :type name: String
        :param clusterIds: A list of clusters which will be connected.
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

        nameToGive = (
            "_"
            + name
            + "_"
            + str(self.__namingSuffix)
        )
        fd = FrequencyDomain("fd_" + name, frequencyDomain)

        try:
            # FIXME: why distinguish storage and other types here?
            if resourceType == CommunicationResourceType.Storage:
                comResource = Storage(
                    nameToGive,
                    fd,
                    readLatency,
                    writeLatency,
                    readThroughput,
                    writeThroughput,
                )
            else:
                comResource = CommunicationResource(
                    nameToGive,
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
        name,
        clusters,
        comResource,):
        """Adds a communication resource to the platform. All cores of the given cluster identifiers can communicate
        via this resource.

        :param name: The name of the storage
        :type name: String
        :param clusterIds: A list of clusters which will be connected.
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
        nameToGive = (
            "_"
            + name
            + "_"
            + str(self.__namingSuffix)
        )
        prim = Primitive("prim_" + nameToGive)

        for cluster in clusters:
            for pe in cluster.pes:
                pe[1].append(comResource)
                produce = CommunicationPhase(
                    "produce", [comResource], "write"
                )
                consume = CommunicationPhase(
                    "consume", [comResource], "read"
                )
                prim.add_producer(pe[0], [produce])
                prim.add_consumer(pe[0], [consume])

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
            name = str(cluster.identifier) + "_noc_mem_" + str(key)
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
                    str(cluster.identifier)
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
                    str(cluster.identifier)
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
                                    str(cluster.identifier)
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
        #else:
            #return

    def setPeripheralStaticPower(self, static_power):
        """Set peripheral static power of the platform."""
        self.__platform.peripheral_static_power = static_power

    def getClusterList(self, identifier):
        """Returns a list of all processing clusters contained in specified cluster.

        :param identifier: The identifier of the target cluster.
        :type identifier: int
        :returns: A list of names of processing clusters
        :rtype list[string]:
        """
        if not identifier in self.__clusterList[self.__activeScope]:
            return None
        else:
            return self.__clusterList[self.__activeScope][identifier]

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

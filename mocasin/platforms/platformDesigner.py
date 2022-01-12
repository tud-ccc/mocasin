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
    with communication resources.

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
        :param clusterList: The clusters added to the platform.
        :type clusterList: List[cluster]
        :param __routerList: A dictionary of communication resources (type router) added to the
        platform, for every entry in the dict there are a list of processors and the communicatino
        resources used to connect the processors to the router.
        :type __routerList: dict{communicationResource: [[Processor, CommunicationResource]]}
        """
        self.__schedulingPolicy = None
        self.__platform = platform
        self.__clusterList = []
        self.__routerList = {}

    def addCluster(self, name, parent=None):
        """Add a new cluster to the platform.

        :param name: The name, the cluster can be addressed with.
        :type name: int
        :param parent: The parent cluster in which the new cluster will be contained, it can be None.
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
        context_store_cycles,
    ):
        """Adds a processing element to cluster.

        :param cluster: The cluster the processing element will be added to.
        :type cluster: cluster
        :param name: processor name.
        :type name: string
        :param processorType: Processor type.
        :type processorType: string
        :param frequency_domain: Frequency domain for processor.
        :type frequency_domain: FrequencyDomain
        :param power_model: Power model for processor.
        :type power_model: ProcessorPowerModel
        :param context_load_cycles: Context load cycles for processor.
        :type context_load_cycles: int
        :param context_store_cycles: Context store cycles for processor.
        :type context_store_cycles: int
        :returns: new PE added to the cluster.
        :rtype: Processor
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
            return new_processor
        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))

    def getPesInCluster(self, cluster):
        """get list of PEs contained in a cluster. It does not consider PEs contained in inner clusters.

        :param cluster: The cluster the processing elements will be returned.
        :type cluster: cluster
        :returns: list of PEs in cluster.
        :rtype: list[processor]
        """
        return cluster.pes

    def getClusterForPe(self, processor):
        """Get the cluster in which a communication resource is placed."""
        for cluster in self.__clusterList:
            for pe in cluster.pes:
                if pe.name == processor.name:
                    return cluster

    def addStorage(
        self,
        name,
        cluster,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequency,
    ):
        """Adds a storage to the platform. All PEs connected to the storage can communicate
        via this resource.

        :param name: The name of the storage
        :type name: String
        :param cluster: The cluster to which the storage will be added to.
        :type cluster: list[int]
        :param readLatency: The read latency of the communication resource.
        :type readLatency: int
        :param writeLatency: The write latency of the communication resource.
        :type writeLatency: int
        :param readThroughput: The read throughput of the communication resource.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the communication resource.
        :type writeThroughput: int
        :param frequency: The frequency of the communication resource.
        :type frequency: int
        """
        try:
            fd = FrequencyDomain("fd_" + name, frequency)
            comResource = Storage(
                name,
                fd,
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

    def addRouter(
        self,
        name,
        cluster,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequency,
    ):
        """Adds a storage to the platform. All PEs connected to the storage can communicate
        via this resource.

        :param name: The name of the storage
        :type name: String
        :param cluster: The cluster to which the storage will be added to.
        :type cluster: list[int]
        :param readLatency: The read latency of the communication resource.
        :type readLatency: int
        :param writeLatency: The write latency of the communication resource.
        :type writeLatency: int
        :param readThroughput: The read throughput of the communication resource.
        :type readThroughput: int
        :param writeThroughput: The write throughput of the communication resource.
        :type writeThroughput: int
        :param frequency: The frequency of the communication resource.
        :type frequency: int
        :returns: generated storage resource.
        :rtype: CommunicationResource
        """
        try:
            fd = FrequencyDomain("fd_" + name, frequency)
            comResource = CommunicationResource(
                name,
                fd,
                CommunicationResourceType.Router,
                readLatency,
                writeLatency,
                readThroughput,
                writeThroughput,
            )
            self.__routerList[name] = []
            self.__platform.add_communication_resource(comResource)
            cluster.commResources.append(comResource)
            return comResource

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def addCommunicationResource(
        self,
        name,
        cluster,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequency,
        resourceType=CommunicationResourceType.Storage,
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
        :param frequency: The frequency of the communication resource.
        :type frequency: int
        :param resourceType: The resource type of the communication resource.
        :type resourceType: int
        :returns: generated router.
        :rtype: CommunicationResource
        """
        try:
            fd = FrequencyDomain("fd_" + name, frequency)
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

    def connectPeToCom(
        self, processor, communicationResource, physicalLink=None
    ):
        """Connects a PE to a communication resource. The PE can communicate to other PEs via this resource.
        Both elements should be placed in the same cluster.

        :param processor: The PE to be connected to the given communication resource.
        :type processor: Processor
        :param communicationResource: Communication resource the PE will be connected to.
        :type communicationResource: communicationResource
        :param physicalLink: Physical link used to connect PE with the communication resource.
        :type physicalLink: communicationResource type physicalLink
        """
        try:
            # TODO: This is a workaround. The Platform class should provide a method to verify if a primitive exists
            name = "prim_" + communicationResource.name
            primitives = self.__platform._primitives
            if name in primitives:
                prim_exists = True
                prim = self.__platform.find_primitive(name)
            else:
                prim_exists = False
                prim = Primitive(name)

            comType = communicationResource.resource_type()
            if comType == CommunicationResourceType.Router:
                self.__routerList[communicationResource.name].append(
                    [processor, physicalLink]
                )
                return

            # check if processor and communication resource are placed in the same cluster
            currentCluster = self.getClusterForPe(processor)
            if communicationResource in currentCluster.commResources:
                produce = CommunicationPhase(
                    "produce", [communicationResource], "write"
                )
                consume = CommunicationPhase(
                    "consume", [communicationResource], "read"
                )
                prim.add_producer(processor, [produce])
                prim.add_consumer(processor, [consume])

            if not prim_exists:
                self.__platform.add_primitive(prim)

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def connectStorageLevels(self, storage1, storage2):
        """Connects two storage resources in a hierarchical fashion. Storage2
        represents a higher level in the memory hierarchy.
        Other elements with lower level must be already connected to storage1,
        in order to be propagated to storage2.

        :param storage1: lower level storage in the memory hierarchy.
        :type storage1: Storage
        :param storage2: higher level storage in the memory hierarchy.
        :type storage2: Storage
        """
        try:
            # TODO; add physicalLink
            # TODO: This is a workaround. The Platform class should provide a method to verify if a primitive exists
            name = "prim_" + storage1.name
            primitives = self.__platform._primitives
            if name in primitives:
                lowPrim = self.__platform.find_primitive(name)

            name = "prim_" + storage2.name
            primitives = self.__platform._primitives
            if name in primitives:
                prim_exists = True
                highPrim = self.__platform.find_primitive(name)
            else:
                prim_exists = False
                highPrim = Primitive(name)

            for producer in lowPrim.producers:
                phases = lowPrim.produce_phases[producer.name]
                resources = []
                for ph in phases:
                    resources.extend(ph.resources)
                resources.append(storage2)
                produce = CommunicationPhase("produce", resources, "write")
                highPrim.add_producer(producer, [produce])
            for consumer in lowPrim.consumers:
                phases = lowPrim.consume_phases[consumer.name]
                resources = []
                for ph in phases:
                    resources.extend(ph.resources)
                resources.insert(0, storage2)
                consume = CommunicationPhase("consume", resources, "read")
                highPrim.add_consumer(consumer, [consume])

            if not prim_exists:
                self.__platform.add_primitive(highPrim)

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def createNetworkForRouters(
        self,
        networkName,
        routerList,
        adjacencyList,
        routingFunction,
        physicalLink=None,
    ):
        """Adding physical links and NOC memories according to the adjacency list"""

        for key in adjacencyList:
            for target in adjacencyList[key]:
                if physicalLink:
                    name = "pl_" + str(target) + "_" + str(key)
                    communicationResource = CommunicationResource(
                        name,
                        physicalLink._frequency_domain,
                        CommunicationResourceType.PhysicalLink,
                        physicalLink._read_latency,
                        physicalLink._write_latency,
                        physicalLink._read_throughput,
                        physicalLink._write_throughput,
                    )
                    self.__platform.add_communication_resource(
                        communicationResource
                    )

        for router in routerList:
            pes = self.__routerList[router.name]
            for innerRouter in routerList:
                innerPes = self.__routerList[innerRouter.name]

                if innerRouter != router:
                    resourceList = []
                    path = routingFunction(adjacencyList, router, innerRouter)
                    lastPoint = None
                    for point in path:
                        if lastPoint != None:
                            if physicalLink:
                                name = "pl_" + str(lastPoint) + "_" + str(point)
                                resource = (
                                    self.__platform.find_communication_resource(
                                        name
                                    )
                                )
                                resourceList.append(resource)
                        lastPoint = point

                    for pe in pes:
                        name = networkName + "_" + pe[0].name
                        primitives = self.__platform._primitives
                        if name in primitives:
                            prim_exists = True
                            prim = self.__platform.find_primitive(name)
                        else:
                            prim_exists = False
                            prim = Primitive(name)

                        resourcesList2 = resourceList.copy()
                        resourcesList2.insert(0, router)
                        if pe[1] is not None:
                            resourcesList2.insert(0, pe[1])

                        for innerPe in innerPes:
                            resourcesList3 = resourcesList2.copy()
                            resourcesList3.append(innerRouter)
                            if innerPe[1] is not None:
                                resourcesList3.append(innerPe[1])

                            produce = CommunicationPhase(
                                "produce", resourcesList3, "write"
                            )
                            consume = CommunicationPhase(
                                "consume",
                                list(reversed(resourcesList3)),
                                "read",
                            )

                            prim.add_producer(innerPe[0], [produce])
                            prim.add_consumer(innerPe[0], [consume])

                        if not prim_exists:
                            self.__platform.add_primitive(prim)

                else:
                    for pe in pes:
                        name = networkName + "_" + pe[0].name
                        primitives = self.__platform._primitives
                        if name in primitives:
                            prim_exists = True
                            prim = self.__platform.find_primitive(name)
                        else:
                            prim_exists = False
                            prim = Primitive(name)

                        resourceList = []
                        resourceList.insert(0, router)
                        if pe[1] is not None:
                            resourceList.insert(0, pe[1])
 
                        produce = CommunicationPhase(
                            "produce", resourceList, "write"
                        )
                        consume = CommunicationPhase(
                            "consume", list(reversed(resourceList)), "read"
                        )

                        prim.add_producer(pe[0], [produce])
                        prim.add_consumer(pe[0], [consume])

                        if not prim_exists:
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

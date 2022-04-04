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
    """

    def __init__(self, platform):
        """Initialize a new instance of the platformDesigner. Should be called by the constructor of a class inheriting
        from Platform.
        """
        self.schedulingPolicy = None
        self.platform = platform
        self.nocList = platform.nocs
        self.adjacentList = platform.network
        self.clusterList = []
        self.links = []

    def find_cluster(self, name):
        """return a cluster with the given name"""
        for cluster in self.clusterList:
            if cluster.name == name:
                return name
        return None

    def getClusterForComponent(self, component):
        """Get the cluster in which a communication resource is placed."""
        # TODO: check replacing string
        for cluster in self.clusterList:
            if component in cluster.pes:
                return cluster
            elif component in cluster.commResources:
                return cluster

    def connectComponents(self, component1, component2, physicalLink=None):
        """Connect two different componentes with the given physical Link.
        The components may be either processor or communication resource
        """
        # TODO: check that element1 and element2 are processor or communicationResource
        try:
            self.adjacentList[component1].append(component2)
            self.adjacentList[component2].append(component1)
            if physicalLink:
                self.links.append(physicalLink)

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def createNetwork(
        self,
        networkName,
        nodeList,
        routingFunction,
        physicalLink=None,
    ):
        """Add physical links according to the adjacency list"""
        adjacencyList = routingFunction(nodeList)

        if physicalLink:
            if (
                physicalLink._resource_type
                == CommunicationResourceType.PhysicalLink
            ):
                for key in adjacencyList:
                    for target in adjacencyList[key]:
                        name = "pl_" + str(target) + "_" + str(key)
                        communicationResource = CommunicationResource(
                            name,
                            physicalLink._frequency_domain,
                            physicalLink._resource_type,
                            physicalLink._read_latency,
                            physicalLink._write_latency,
                            physicalLink._read_throughput,
                            physicalLink._write_throughput,
                        )
                        self.platform.add_communication_resource(
                            communicationResource
                        )

        self.nocList[networkName] = [{}, routingFunction]

        for k, v in adjacencyList.items():
            for i in v:
                if not self.adjacentList[k]:
                    self.adjacentList.update({k: [i]})
                else:
                    self.adjacentList[k].append(i)
            self.nocList[networkName][0].update({k: v})

    def setSchedulingPolicy(self, policy, cycles):
        """Sets a new scheduling policy, which will be applied to all schedulers of new PE Clusters."""
        try:
            self.schedulingPolicy = SchedulingPolicy(policy, cycles)
            return True
        except:
            log.error("Exception caught: " + sys.exc_info()[0])
            return False

    def setPeripheralStaticPower(self, static_power):
        """Set peripheral static power of the platform."""
        self.platform.peripheral_static_power = static_power

    def getPlatform(self):
        """Returns the platform, created with the designer."""
        return self.platform


class genericProcessor(Processor):
    """This class is a generic processor to be passed to the
    different architectures generated with the platform designer.
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
    """Represents one cluster in the platform. A cluster contains a set of clusters,
    processors and communication resources.
    """

    def __init__(self, name, designer):
        self.name = name
        self.pes = []
        self.commResources = []
        self.innerClusters = []
        self.outerCluster = None
        self.designer = designer

    def addCluster(self, innerCluster):
        """Add a cluster to the list of inner clusters."""
        # TODO: check the outer cluster is not an inner cluster
        self.innerClusters.append(innerCluster)
        innerCluster.outerCluster = self
        return innerCluster

    def addPeToCluster(
        self,
        name,
        processorType,
        frequency_domain,
        power_model,
        context_load_cycles,
        context_store_cycles,
    ):
        """Adds a processing element to cluster."""
        try:
            new_processor = Processor(
                name + "_" + self.name,
                processorType,
                frequency_domain,
                power_model,
                context_load_cycles,
                context_store_cycles,
            )
            self.designer.platform.add_processor(new_processor)
            self.designer.platform.add_scheduler(
                Scheduler(
                    f"sched_{new_processor.name}",
                    [new_processor],
                    self.designer.schedulingPolicy,
                )
            )
            self.pes.append(new_processor)
            self.designer.adjacentList.update({new_processor: []})
            return new_processor
        except:
            log.error("Exception caught: " + str(sys.exc_info()[0]))

    def addCommunicationResource(
        self,
        name,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequency,
        resourceType=Storage,
    ):
        """Adds a communication resource to the cluster."""
        try:
            name = f"{name}_{self.name}"
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
            self.designer.platform.add_communication_resource(comResource)
            self.commResources.append(comResource)
            self.designer.adjacentList.update({comResource: []})
            return comResource

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def addStorage(
        self,
        name,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequency,
    ):
        """Adds a storage to the cluster. All PEs connected to the storage can communicate
        via this resource.
        """
        try:
            name = f"{name}_{self.name}"
            fd = FrequencyDomain("fd_" + name, frequency)
            comResource = Storage(
                name,
                fd,
                readLatency,
                writeLatency,
                readThroughput,
                writeThroughput,
            )
            self.designer.platform.add_communication_resource(comResource)
            self.commResources.append(comResource)
            self.designer.adjacentList.update({comResource: []})
            return comResource

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def addRouter(
        self,
        name,
        readLatency,
        writeLatency,
        readThroughput,
        writeThroughput,
        frequency,
    ):
        """Adds a router to the cluster. All PEs connected to the storage can communicate
        via this resource.
        """
        try:
            name = f"{name}_{self.name}"
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
            self.designer.platform.add_communication_resource(comResource)
            self.commResources.append(comResource)
            self.designer.adjacentList.update({comResource: []})
            return comResource

        except:  # FIXME: this is fishy
            log.error("Exception caught: " + str(sys.exc_info()[0]))
            return

    def findPe(self, name):
        """Find pe with the given name into the cluster"""
        for pe in self.pes:
            peName = pe.name.replace(f"_{self.name}", "")
            if peName == name:
                return pe
        return None

    def findComRes(self, name):
        """Find communication resource with the given name"""
        for comRes in self.commResources:
            comName = comRes.name.replace(f"_{self.name}", "")
            if comName == name:
                return comRes
        return None

    def getProcessors(self):
        """get list of PEs contained in a cluster. It does not consider PEs
        contained in inner clusters.
        """
        return self.pes

    def getCommunicationResources(self):
        """get list of communication resources contained in a cluster. It does not consider
        resources contained in inner clusters.
        """
        return self.commResources

# Copyright (C) 2017-2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Felix Teweleit, Andres Goens


from mocasin.common.platform import (
    FrequencyDomain,
    Platform,
    Processor,
    Scheduler,
    SchedulingPolicy,
    Storage,
)
from mocasin.common.platform.bus import Bus, primitives_from_buses
from mocasin.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate


class GenericBusPlatform(Platform):
    """Represents a flat bus-based platform"""

    def __init__(
        self, name, num_processors, symmetries_json=None, embedding_json=None
    ):
        """Initialize the platform

        Generate `num_processors` processors and schedulers and connect
        them to a global shared bus. This also create a global RAM object and
        connects it to the bus. Based on this bus setup, the primitive for
        communication via shared RAM is generated.
        """
        super().__init__(name, symmetries_json, embedding_json)

        fd_pes = FrequencyDomain("fd_pes", 500000000)
        fd_ram = FrequencyDomain("fd_ram", 100000000)

        ram = Storage("RAM", fd_ram, 5, 7, 16, 12)
        self.add_communication_resource(ram)

        bus = Bus("bus", fd_pes, 1, 8)
        self.add_communication_resource(bus)
        bus.connect_storage(ram)

        policy = SchedulingPolicy("FIFO", 100)

        for i in range(0, num_processors):
            name = "PE%02d" % (i)
            processor = Processor(name, "RISC", fd_pes, 100, 100)
            bus.connect_processor(processor)
            self.add_processor(processor)
            self.add_scheduler(Scheduler("sp_" + name, [processor], policy))

        primitives = primitives_from_buses([bus])
        for p in primitives:
            self.add_primitive(p)


class GenericClusteredPlatform(Platform):
    """Represents a hierarchical, clustered, bus-based platform"""

    def __init__(self, name, num_clusters, cluster_size, hierarchy_levels):
        """Initialize the platform

        Generate a hierarchy of clusters connected by buses. On the lowest
        level, this generates a shared memory, `cluster_size` processors, and a
        bus. On the intermediate levels, this produces a shared memory and a
        bus that connects to all buses of lower level clusters. On the top
        level, this generates a bus as well as the global shared RAM and
        connects the bus to the lower level clusters.

        All in all this forms a tree with depth of `hierarchical_levels`. The
        root node hase `num_clusters` children and all other nodes have
        cluster_size chilren. The leafe nodes are processors and all other
        nodes are buses.

        :param str name: platform name
        :param int num_clusters: number of top-level clusters
        :param int cluster_size: number of nodes per cluster
        :param int hierarchy_levels: number of levels in the hierarchy
        """
        super().__init__(name)

        if hierarchy_levels < 2:
            raise ValueError("Number of hierarchies needs to be at least 2")

        level = 0  # current level in the hierarchy
        pe_id = 0  # current pe id
        buses = {}  # all buses

        policy = SchedulingPolicy("FIFO", 100)

        # start from the lowest level and generate all PEs
        buses[level] = []
        num_l0_clusters = num_clusters * cluster_size ** (hierarchy_levels - 2)
        for cluster_id in range(0, num_l0_clusters):
            cluster_name = "l%d_c%d" % (level, cluster_id)
            fd_pes = FrequencyDomain("fd_" + cluster_name, 500000000)
            bus = Bus("bus_" + cluster_name, fd_pes, 1, 8)
            buses[level].append(bus)
            self.add_communication_resource(bus)
            for j in range(0, cluster_size):
                name = "PE%02d" % (pe_id)
                pe_id += 1
                processor = Processor(name, "RISC", fd_pes, 100, 100)
                bus.connect_processor(processor)
                self.add_processor(processor)
                self.add_scheduler(
                    Scheduler("shared_" + name, [processor], policy)
                )
            mem = Storage("shared_" + cluster_name, fd_pes, 1, 1, 8, 8)
            self.add_communication_resource(mem)
            bus.connect_storage(mem)
        level += 1

        # intermediate levels
        while level < hierarchy_levels - 1:
            buses[level] = []
            bus_id = 0
            num_lx_clusters = num_clusters * cluster_size ** (
                hierarchy_levels - level - 2
            )
            for cluster_id in range(0, num_lx_clusters):
                cluster_name = "l%d_c%d" % (level, cluster_id)
                fd = FrequencyDomain("fd_" + cluster_name, 500000000)
                mem = Storage("shared_" + cluster_name, fd, 3, 4, 8, 8)
                self.add_communication_resource(mem)
                bus = Bus("bus_" + cluster_name, fd, 2, 8)
                self.add_communication_resource(bus)
                bus.connect_storage(mem)
                buses[level].append(bus)
                for i in range(0, cluster_size):
                    bus.connect_master_bus(buses[level - 1][bus_id])
                    bus_id += 1
            level += 1

        # top level
        fd_top = FrequencyDomain("fd_l%d" % level, 250000000)
        bus_top = Bus("bus_l%d" % level, fd_top, 3, 8)
        buses[level] = [bus_top]
        self.add_communication_resource(bus_top)
        for b in buses[level - 1]:
            bus_top.connect_master_bus(b)

        fd_ram = FrequencyDomain("fd_ram", 100000000)
        ram = Storage("RAM", fd_ram, 5, 7, 16, 12)
        self.add_communication_resource(ram)
        bus_top.connect_storage(ram)

        bus_list = []
        for l in range(0, hierarchy_levels):
            bus_list.extend(buses[l])
        primitives = primitives_from_buses(bus_list)
        for p in primitives:
            self.add_primitive(p)


class DesignerPlatformBus(Platform):
    def __init__(
        self, processor_0, name="bus", symmetries_json=None, embedding_json=None
    ):
        """Initializes an example platform with four processing
        elements connected via an shared memory.
        :param processor_0: the processing element for the platform
        :type processor_0: Processor
        :param name: The name for the returned platform
        :type name: String
        """
        super(DesignerPlatformBus, self).__init__(
            name, symmetries_json=symmetries_json, embedding_json=embedding_json
        )
        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        designer.newElement("test_chip")
        designer.addPeClusterForProcessor("cluster_0", processor_0, 4)
        designer.addCommunicationResource(
            "shared_memory",
            ["cluster_0"],
            100,
            100,
            1000,
            1000,
            frequencyDomain=2000,
        )
        designer.finishElement()

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pykpn.common.platform import (CommunicationPhase, CommunicationResource,
    Primitive, Processor)


class Bus(CommunicationResource):
    """Represents a bus in a platform

    This is a helper/wrapper class that is intended to simplify the creation of
    primitives that model communication in a bus based architecture. See the
    function :func:`~primitives_from_buses` for generation of primitives.
    """

    def __init__(self, name, frequency_domain, latency=1,
                 throughput=float('inf'), exclusive=False):
        super().__init__(name, frequency_domain, latency, latency, throughput,
                         throughput, exclusive, False)

        self._processors = []
        self._storages = []
        self._master_links = []
        self._slave_links = []

    def connect_processor(self, processor):
        """Connect a processor to the bus"""
        self._processors.append(processor)

    def connect_storage(self, storage):
        """Connect a storage to the bus"""
        self._storages.append(storage)

    def connect_master_bus(self, bus):
        """Connect to a master bus.

        Connects this bus as a slave to a master bus. This means that the
        master bus may send requests that are responded to by devices connected
        to this bus, but not vice versa.
        """
        self._master_links.append(bus)
        bus._slave_links.append(self)

    def connect_slave_bus(self, bus):
        """Connect to a slave bus.

        Connects this bus as a master to a slave bus. This means that this
        bus may send requests that are responded to by devices connected
        to the slave bus, but not vice versa.
        """
        self._slave_links.append(bus)
        bus._master_links.append(self)

    def get_processor_connections(self, hierarchy=None, connections=None):
        """Get a list of Processors that are reachable from this bus

        This is a recursive function. It iterates over the hierarchy of
        connected buses starting from self and returns a list of connection
        tuples. Each tuple contains a list of buses representing the hierarchy
        path and a list of processors that are reachable by this path.
        """
        if connections is None:
            connections = []

        if hierarchy is None:
            hierarchy = [self]
        else:
            hierarchy.prepend(self)

        connections.append((hierarchy, self._processors))

        for bus in self._slave_links:
            bus.get_processor_connections(hierarchy, connections)

        return connections


def primitives_from_buses(buses):
    """Generate a list of primitives from a list of buses.

    This creates a single phase communication primitive for each storage device
    that is connected to one of the buses. Processors that can reach the
    storage folowing the bus hierarchy are added as sources and sinks to these
    primitives. The buses that are required to reach the storage device from a
    processor are added as communication_resources to the consume or produce
    phases.
    """
    # first, get a list of all storages
    storages = []
    for b in buses:
        storages.extend(b._storages)

    primitives = []
    # create a primitive per storage
    for storage in storages:
        prim = Primitive('cp_%s' % (storage.name))

        print('storage: %s', storage.name)
        # find the bus that connects to this storage
        storage_bus = None
        for b in buses:
            if storage in b._storages:
                storage_bus = b
                break

        connections = storage_bus.get_processor_connections()
        for buses, processors in connections:
            produce = CommunicationPhase('produce', buses + [storage], 'write')
            consume = CommunicationPhase('consume', buses + [storage], 'read')
            for p in processors:
                prim.add_producer(p, produce)
                prim.add_consumer(p, consume)

        primitives.append(prim)

    return primitives

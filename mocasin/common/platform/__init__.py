# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Andres Goens

import pydot
import logging
import math

from collections import Counter
from enum import Enum
from hydra.utils import to_absolute_path
from mocasin.platforms.utils import simpleDijkstra, yxRouting
from mocasin.platforms.topologies import meshTopology

log = logging.getLogger(__name__)


class CommunicationResourceType(Enum):
    PhysicalLink = 1
    LogicalLink = 2
    DMAController = 3
    Storage = 4
    Router = 5


class FrequencyDomain:
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency
        self.base_frequency = frequency
        # Christian and I agreed that the  easiest way to adapt performance at runtime
        # is to dynamically change the frequency of the process as this feature was
        # supposed to be available in Mocasin (to study dynamic frequency scaling)
        # but never used in practice.
        # For the moment, I define a "base_frequency" that is acquired from the processor
        # model and never changed. The actual running frequency, i.e. "frequency", is
        # modified at runtime according to the number of running threads in the processor.

    def cycles_to_ticks(self, cycles):
        tmp = float(cycles) * 1000000000000 / float(self.frequency)
        return int(round(tmp))


class ProcessorPowerModel:
    def __init__(self, name, static_power, dynamic_power):
        self.name = name
        self.static_power = static_power
        self.dynamic_power = dynamic_power


class Processor:
    def __init__(
        self,
        name,
        type_,
        frequency_domain,
        power_model,
        context_load_cycles=0,
        context_store_cycles=0,
        n_threads=1,
    ):
        self.name = name
        self.type = type_
        self.frequency_domain = frequency_domain
        self.power_model = power_model
        self.context_load_cycles = context_load_cycles
        self.context_store_cycles = context_store_cycles
        self.n_threads = n_threads

    @property
    def base_frequency(self):
        """Returns the base frequency of the processor"""
        return self.frequency_domain.base_frequency

    @property
    def frequency(self):
        """Returns the running frequency of the processor"""
        return self.frequency_domain.frequency

    @frequency.setter
    def frequency(self, frequency):
        """Sets the running frequency of the processor"""
        self.frequency_domain.frequency = int(frequency)

    def ticks(self, cycles):
        return self.frequency_domain.cycles_to_ticks(cycles)

    def context_load_ticks(self):
        return self.ticks(self.context_load_cycles)

    def context_store_ticks(self):
        return self.ticks(self.context_store_cycles)

    def static_power(self):
        return (
            None if self.power_model is None else self.power_model.static_power
        )

    def dynamic_power(self):
        return (
            None if self.power_model is None else self.power_model.dynamic_power
        )

    def __str__(self):
        return self.name

    def __lt__(self, other_pe):
        return self.name.lower() < other_pe.name.lower()

    def __repr__(self):
        return self.__str__()


class CommunicationResource(object):
    """
    Represents a resource required for communication. This can be anything from
    a link or bus to a memory.

    This is a base class that can be specialized to model more complex
    resources like caches.
    """

    def __init__(
        self,
        name,
        frequency_domain,
        resource_type,
        read_latency,
        write_latency,
        read_throughput=float("inf"),
        write_throughput=float("inf"),
        exclusive=False,
        is_storage=False,
    ):
        self.name = name
        self._resource_type = resource_type
        self._frequency_domain = frequency_domain
        self._read_latency = read_latency
        self._write_latency = write_latency
        self._read_throughput = read_throughput
        self._write_throughput = write_throughput
        self.exclusive = exclusive
        self.is_storage = is_storage

    def resource_type(self):
        return self._resource_type

    def read_latency(self):
        return self._frequency_domain.cycles_to_ticks(self._read_latency)

    def write_latency(self):
        return self._frequency_domain.cycles_to_ticks(self._write_latency)

    def read_throughput(self):
        return self._read_throughput / self._frequency_domain.cycles_to_ticks(1)

    def write_throughput(self):
        return self._write_throughput / self._frequency_domain.cycles_to_ticks(
            1
        )

    def frequency_domain_name(self):
        return self._frequency_domain.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Storage(CommunicationResource):
    """
    This is a specialization of the CommunicationResource class and represents
    a storage device.
    """

    def __init__(
        self,
        name,
        frequency_domain,
        read_latency,
        write_latency,
        read_throughput=float("inf"),
        write_throughput=float("inf"),
        exclusive=False,
    ):
        super(Storage, self).__init__(
            name,
            frequency_domain,
            CommunicationResourceType.Storage,
            read_latency,
            write_latency,
            read_throughput,
            write_throughput,
            exclusive,
            True,
        )


class CommunicationPhase:
    """
    Represents a phase of communication. This basically is a list of required
    resources.
    """

    def __init__(
        self, name, resources, direction, ignore_latency=False, size=None
    ):
        self.name = name
        self.resources = resources
        self.direction = direction
        self.ignore_latency = ignore_latency
        self.size = size

    def get_costs(self, size):
        latency = 0
        min_throughput = float("inf")
        if self.direction == "read":
            for r in self.resources:
                if not self.ignore_latency:
                    latency += r.read_latency()
                min_throughput = min(min_throughput, r.read_throughput())
        elif self.direction == "write":
            for r in self.resources:
                if not self.ignore_latency:
                    latency += r.write_latency()
                min_throughput = min(min_throughput, r.write_throughput())
        else:
            raise RuntimeError('Direction must be "read" or "write"!')
        if self.size is None:
            return int(round(latency + size / min_throughput))
        else:
            return int(round(latency + self.size / min_throughput))


class Primitive:
    """Represents a communication primitive

    A communication primitive defines how a producer processor may send data
    tokens to a consumer processor. This class defines a list of communication
    phases for each producer and consumer of the primitive. The phases specify
    how exactly tokens are produced or consumed. Only processors that are known
    to the primitive may communicate using this primitive.
    """

    def __init__(self, name):
        self.name = name
        self.consume_phases = {}
        self.produce_phases = {}
        self.consumers = []
        self.producers = []

    def add_consumer(self, sink, phases):
        if sink.name in self.consume_phases:
            raise RuntimeError(
                "Primitive already has a consumer %s" % sink.name
            )
        for phase in phases:
            if phase.direction != "read":
                raise RuntimeError("A consumer can only use read phases")
        self.consume_phases[sink.name] = phases
        self.consumers.append(sink)

    def add_producer(self, src, phases):
        if src.name in self.produce_phases:
            raise RuntimeError("Primitive already has a producer %s" % src.name)
        for phase in phases:
            if phase.direction != "write":
                raise RuntimeError("A producer can only use produces phases")
        self.produce_phases[src.name] = phases
        self.producers.append(src)

    def static_consume_costs(self, sink_processor, token_size=8):
        """Returns the total (static) costs for a consume operation

        :param token_size: the size of a token for the costs
        :param sink_processor: the sink processor for which the costs are to be
            retrieved
        """
        costs = 0
        for ph in self.consume_phases[sink_processor.name]:
            costs += ph.get_costs(token_size)
        return costs

    def static_produce_costs(self, src_processor, token_size=8):
        """Returns the total (static) costs for a produce operation

        :param token_size: the size of a token for the costs
        :param src_processor: the processor for which the costs are to be
            retrieved
        """
        costs = 0
        for ph in self.produce_phases[src_processor.name]:
            costs += ph.get_costs(token_size)
        return costs

    def static_costs(self, src_processor, sink_processor, token_size=8):
        """Returns the total (static) costs for a produce and consume operation

        :param token_size: the size of a token for the costs
        :param src_processor: the src processor for which the costs are to be
            retrieved
        :param sink_processor: the sink processor for which the costs are to be
            retrieved
        """
        return self.static_produce_costs(
            src_processor, token_size
        ) + self.static_consume_costs(sink_processor, token_size)

    def is_suitable(self, src, sinks):
        """Check if the primitive is suitable to implement a desired channel

        Checks if the `src` processor is in the :attr:`producers` list and
        if all `sink` processors are in the :attr:`consumers` list.

        :param src: a src processor
        :type src: Processor
        :param sinks: non-empty list of sink processors
        :type sinks: list[Processor]
        :returns: ``True`` if the primitive is suitable for implementing the
            channel
        :rtype: bool
        """
        assert len(sinks) > 0

        if src not in self.producers:
            return False
        for s in sinks:
            if s not in self.consumers:
                return False
        return True


class SchedulingPolicy:
    """Represents a scheduling policy.

    Attributes:
       name (str): the policy name
       cycles (int): number of cycles a scheduler using this policy
                     requires to reach a decision
       time_slice (int): Length of a time slice in pico seconds
    """

    def __init__(self, name, cycles, time_slice=None):
        """Initialize a scheduling policy

        Args:
           name (str): the policy name
           cycles (int): number of cycles a scheduler using this policy
                         requires to reach a decision
           time_slice (int, optional): Length of a time slice in pico seconds.
               Defaults to None.
        """
        self.name = name
        self.scheduling_cycles = cycles
        self.time_slice = time_slice


class Scheduler:
    """Represents a scheduler provided by the platform.

    It schedules processes on one or more processors according to a policy.

    Attributes:
        name (str): name of the scheduler
        processors (list of Processor): list of Processor objects that are
            managed by this scheduler
        policy (SchedulingPolicy): the scheduling policy implemented by this
            scheduler
    """

    def __init__(self, name, processors, policy):
        """Initialize a Scheduler.

        Args:
           name (str): name of the scheduler
           processors (list of Processor): list of Processor objects that
               are managed by this scheduler
           policy (SchedulingPolicy): the scheduling policy implemented by
               this scheduler
        """
        assert (
            len(processors) > 0
        ), "A scheduler must be associated with at least one processor"

        self.name = name
        self.processors = processors
        self.policy = policy

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other_scheduler):
        return self.name.lower() < other_scheduler.name.lower()


class Platform(object):
    """Represents a complete hardware architecture.

    This is a container for processor, communication resource, communication
    primitive, and scheduler objects.

    This is intended as a base class. Derived classes may define a specific
    platform by creating the corresponding objects.
    """

    def __init__(
        self,
        name,
        symmetries_json=None,
        embedding_json=None,
        peripheral_static_power=None,
    ):
        """Initialize the platform.

        This initializes all attributes to empty dicts. Derived classes should
        fill these dicts with objects in order to build a real platform.
        """
        self.name = name
        self._processors = {}  #: dict of processors
        self._communication_resources = {}  #: dict of communication resources
        self._primitives = {}  #: dict of communication primitives
        self._schedulers = {}  #: dict of schedulers
        self.network = {}
        self.nocs = {}
        if symmetries_json is not None:
            self.ag_json = to_absolute_path(symmetries_json)
        if embedding_json is not None:
            self.embedding_json = to_absolute_path(embedding_json)

        # The static power not included to the processors' power
        self.peripheral_static_power = peripheral_static_power

    def processors(self):
        return self._processors.values()

    def primitives(self):
        return self._primitives.values()

    def schedulers(self):
        return self._schedulers.values()

    def communication_resources(self):
        return self._communication_resources.values()

    def find_scheduler_for_processor(self, processor):
        """Find the scheduler for a given processor.

        :param processor: a processor of the underlying platform
        :type processor: Processor
        :raises RuntimeError: if the processor or the scheduler was not found
        :returns: The scheduler object for the given processor
        """
        if processor.name not in self._processors:
            raise RuntimeError(
                "The processor {} is not defined for this "
                "platform!".format(processor.name)
            )
        schedulers = []

        for s in self._schedulers.values():
            if processor in s.processors:
                schedulers.append(s)

        if len(schedulers) == 0:
            raise RuntimeError(
                f"No scheduler found for processor {processor.name}!"
            )
        elif len(schedulers) > 1:
            raise RuntimeError(
                f"Found multiple schedulers for processor {processor.name}!"
            )

        return schedulers[0]

    def find_scheduler(self, name):
        """Search for a scheduler object by its name."""
        return self._schedulers[name]

    def find_processor(self, name):
        """Search for a processor object by its name."""
        return self._processors[name]

    def find_communication_resource(self, name):
        """Search for a communication resource object by its name."""
        if name in self._communication_resources:
            return self._communication_resources[name]
        return None

    def find_primitive(self, name):
        """Search for a communication primitive group."""
        return self._primitives[name]

    def add_scheduler(self, x):
        if x.name in self._schedulers:
            raise RuntimeError(
                "Scheduler %s was already added to the platform" % (x.name)
            )
        self._schedulers[x.name] = x

    def add_processor(self, x):
        if x.name in self._processors:
            raise RuntimeError(
                "Processor %s was already added to the platform" % (x.name)
            )
        self._processors[x.name] = x

    def add_communication_resource(self, x):
        if x.name in self._communication_resources:
            raise RuntimeError(
                "Communication_Resource %s was already added to the platform"
                % (x.name)
            )
        self._communication_resources[x.name] = x

    def add_primitive(self, x):
        if x.name in self._primitives:
            raise RuntimeError(
                "Primitive %s was already added to the platform" % (x.name)
            )
        self._primitives[x.name] = x

    def get_processor_types(self):
        """Returns the counter of processors of each type."""
        res = Counter()
        for p in self.processors():
            res[p.type] += 1
        return res

    def has_power_model(self):
        """Returns whether the platform has a power model."""
        result = any(pe.power_model is not None for pe in self.processors())
        if result:
            for pe in self.processors():
                if pe.power_model is None:
                    log.warning(
                        f"No power model exists for {pe.name}. "
                        "The energy consumption might be not complete."
                    )
        return result

    def to_pydot(self):
        """
        Convert the platform to a dot graph.

        This only prints processors, communication resources, and schedulers.
        Communication primitives are not printed.
        """
        dot = pydot.Dot(graph_type="digraph", strict=True)

        processor_nodes = {}
        for s in self.schedulers():
            cluster = pydot.Cluster("scheduler_" + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                node = pydot.Node(
                    "processor_" + p.name, label=p.name, shape="square"
                )
                processor_nodes[p.name] = node
                cluster.add_node(node)

        primitive_nodes = {}
        for p in self.primitives():
            if p.name in primitive_nodes:
                node = primitive_nodes[p.name]
            else:
                node = pydot.Node("primitive_" + p.name, label=p.name)
                dot.add_node(node)
            minlen = 1 + math.log(len(p.consumers) + len(p.producers)) * 2
            for x in p.producers:
                from_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(from_node, node, minlen=minlen))
            for x in p.consumers:
                to_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(node, to_node, minlen=minlen))

        return dot

    def to_adjacency_dict(self, precision=5, include_proc_type_labels=False):
        """
        Convert the platform to an adjacency dictionary.

        This only prints processors and communication resources.
        The edges are annotated with the static communication cost
        for a simple token of size 8.
        Schedulers and communication primitives are not considered.

        precision: number of significant figures to consider on costs.
        for full precision, select -1

        include_proc_type_labels: adds a flag that also includes labels
        for the processor types.
        """
        num_vertices = 0
        vertices = {}
        adjacency_dict = {}

        for s in self.schedulers():
            for p in s.processors:
                vertices[p.name] = num_vertices
                num_vertices = num_vertices + 1

        for p in self.primitives():
            for x in p.producers:
                if x.name not in adjacency_dict:
                    adjacency_dict[x.name] = {}
                for y in p.consumers:
                    cost = p.static_costs(x, y, token_size=8)
                    if precision < 0 or cost == 0:
                        pass
                    else:
                        cost = round(
                            cost,
                            precision
                            - 1
                            - int(math.floor(math.log10(abs(cost)))),
                        )
                    # print( (x,y,cost))
                    if y.name not in adjacency_dict[x.name]:
                        adjacency_dict[x.name][y.name] = cost
                    # here we should decide what to do with the different primitive
                    # I decided to just take the minimum for now.
                    else:
                        adjacency_dict[x.name][y.name] = min(
                            adjacency_dict[x.name][y.name], cost
                        )

        res = {}
        for elem in adjacency_dict:
            if include_proc_type_labels:
                key = (elem, self.find_processor(elem).type)
                res[key] = [
                    (
                        (adjacent, self.find_processor(adjacent).type),
                        adjacency_dict[elem][adjacent],
                    )
                    for adjacent in adjacency_dict[elem]
                ]

            else:
                res[elem] = [
                    (adjacent, adjacency_dict[elem][adjacent])
                    for adjacent in adjacency_dict[elem]
                ]
        return res

    def to_primitive_latency_dict(self, precision=5):
        """
        Convert the platform to a latency dictionary.

        For each communication primitive, the dictionary contains
        another dictionary with the static communication cost for a simple
        token of size 8 for every producer/consumer pair.
        Schedulers and processing elements are not considered.

        precision: number of significant figures to consider on costs.
        for full precision, select -1
        """
        latency_dict = {}
        for p in self.primitives():
            latency_dict[p.name] = {}
            for x in p.producers:
                for y in p.consumers:
                    cost = p.static_costs(x, y, token_size=8)
                    if precision < 0 or cost == 0:
                        pass
                    else:
                        cost = round(
                            cost,
                            precision
                            - 1
                            - int(math.floor(math.log10(abs(cost)))),
                        )
                    latency_dict[p.name][(x.name, y.name)] = cost
        return latency_dict

    def generate_all_primitives(self):
        for pe1 in self.processors():
            for pe2 in self.processors():
                prim = self.generate_primitive(pe1, pe2)
                self.add_primitive(prim[0])

    def generate_primitive(self, src, sink):
        platform = self

        # check if nodes are in the same noc
        nocResources = self.find_resources_for_Noc(src, sink)
        resources = nocResources

        # if not in the same noc, apply simpleDijkstra routing algorithm
        if not nocResources:
            resources = simpleDijkstra(platform.network, src, sink)
            # fill with physical links
            resources = self.find_physical_links(resources)

        # if element communicating to itself, find the nearest storage
        if src == sink:
            for storage in platform.network[src]:
                if storage._resource_type == CommunicationResourceType.Storage:
                    resources.append(storage)
                    resources.append(sink)
                    break

        # Check if there is a bus and use it to split produce-consume phases
        bus = False
        for i in range(len(resources)):
            if (
                resources[i].name.startswith("BUS")
                or resources[i].name.startswith("bus")
            ) and bus == False:
                index = i
                resources.insert(index, resources[index])
                bus = True
                break

        # Otherwise split in the central element
        if bus == False:
            index = int(len(resources) / 2)
            if len(resources) % 2:
                if type(resources[index]) is Storage:
                    resources.insert(index, resources[index])

        # remove processors from communication resources
        resources = resources[1:-1]

        # add produce/consume phases
        if nocResources:
            resources.reverse()
            produce = CommunicationPhase("produce", [resources[-1]], "write")
            consume = CommunicationPhase("consume", resources, "read")
        else:
            produce = CommunicationPhase("produce", resources[:index], "write")
            consume = CommunicationPhase("consume", resources[index:], "read")
        name = f"prim_{src.name}_{sink.name}"
        suitable_prim = Primitive(name)
        suitable_prim.add_producer(src, [produce])
        suitable_prim.add_consumer(sink, [consume])

        suitable_primitives = [suitable_prim]
        return suitable_primitives

    # checks if nodes are in a same Noc and returns communication
    # resources
    def find_resources_for_Noc(self, src, sink):
        platform = self

        # get all routers the src is connected to
        src_routers = list()
        for router in platform.network[src]:
            if router._resource_type == CommunicationResourceType.Router:
                src_routers.append(router)

        # get all routers the sink is connected to
        sink_routers = list()
        for router in platform.network[sink]:
            if router._resource_type == CommunicationResourceType.Router:
                sink_routers.append(router)

        # check if routers are in a same noc
        sameNoc = False
        for src in src_routers:
            for sink in sink_routers:
                for k, v in platform.nocs.items():
                    if src in v[0].keys() and sink in v[0].keys():
                        sameNoc = True
                        src_router = src
                        sink_router = sink
                        break
                else:
                    continue
                break
            else:
                continue
            break

        # get routing according to the noc topology
        resources = list()
        if sameNoc:
            if v[1] == meshTopology:
                resources = yxRouting(v[0], src_router, sink_router)
            else:
                resources = simpleDijkstra(v[0], src_router, sink_router)
            resources.insert(0, src)
            resources.append(sink)
            # fill with physical links
            resources = self.find_physical_links(resources)

            # remove noc nodes and leave only physical links
            for i in range(len(resources) - 3, 2, -1):
                if (
                    resources[i]._resource_type
                    == CommunicationResourceType.Router
                ):
                    resources.pop(i)

        return resources

    # fill resources with physical links
    def find_physical_links(self, resources):
        for i in range(len(resources) - 1, 1, -1):
            source = resources[i - 1].name
            target = resources[i].name
            pl_name = "pl_" + source + "_" + target
            pl = self.find_communication_resource(pl_name)
            if not pl:
                pl_name = "pl_" + target + "_" + source
                pl = self.find_communication_resource(pl_name)
            if pl:
                resources.insert(i, pl)
        return resources

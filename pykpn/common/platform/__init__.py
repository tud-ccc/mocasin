# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import pydot


class FrequencyDomain:

    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency

    def cycles_to_ticks(self, cycles):
        tmp = float(cycles) * 1000000000000 / float(self.frequency)
        return int(round(tmp))


class Processor:

    def __init__(self, name, type, frequency_domain, context_load_cycles=0,
                 context_store_cycles=0):
        self.name = name
        self.type = type
        self.frequency_domain = frequency_domain
        self.context_load_cycles = context_load_cycles
        self.context_store_cycles = context_store_cycles

    def ticks(self, cycles):
        return self.frequency_domain.cycles_to_ticks(cycles)

    def context_load_ticks(self):
        return self.ticks(self.context_load_cycles)

    def context_store_ticks(self):
        return self.ticks(self.context_store_cycles)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class CommunicationResource:
    '''
    Represents a resource required for communication. This can be anything from
    a link or bus to a memory.

    This is a base class that can be specialized to model more complex
    resources like caches.
    '''

    def __init__(self, name, frequency_domain, read_latency, write_latency,
                 read_throughput=float('inf'), write_throughput=float('inf'),
                 exclusive=False, is_storage=False):
        self.name = name
        self._frequency_domain = frequency_domain
        self._read_latency = read_latency
        self._write_latency = write_latency
        self._read_throughput = read_throughput
        self._write_throughput = write_throughput
        self.exclusive = exclusive
        self.is_storage = is_storage

    def read_latency(self):
        return self._frequency_domain.cycles_to_ticks(self._read_latency)

    def write_latency(self):
        return self._frequency_domain.cycles_to_ticks(self._write_latency)

    def read_throughput(self):
        return (self._read_throughput /
                self._frequency_domain.cycles_to_ticks(1))

    def write_throughput(self):
        return (self._write_throughput /
                self._frequency_domain.cycles_to_ticks(1))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Storage(CommunicationResource):
    """
    This is a specialization of the CommunicationResource class and represents
    a storage device.
    """
    def __init__(self, name, frequency_domain, read_latency, write_latency,
                 read_throughput=float('inf'), write_throughput=float('inf'),
                 exclusive=False):
        super().__init__(name, frequency_domain, read_latency, write_latency,
                         read_throughput, write_throughput, exclusive, True)


class CommunicationPhase:
    '''
    Represents a phase of communication. This basically is a list of required
    resources.
    '''
    def __init__(self, name, resources, direction,
                 ignore_latency=False, size=None):
        self.name = name
        self.resources = resources
        self.direction = direction
        self.ignore_latency = ignore_latency
        self.size = size

    def get_costs(self, size):
        latency = 0
        min_throughput = float('inf')
        if self.direction == 'read':
            for r in self.resources:
                if not self.ignore_latency:
                    latency += r.read_latency()
                min_throughput = min(min_throughput, r.read_throughput())
        elif self.direction == 'write':
            for r in self.resources:
                if not self.ignore_latency:
                    latency += r.write_latency()
                min_throughput = min(min_throughput,
                                     r.write_throughput())
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
            raise RuntimeError('Primitive already has a consumer %s' %
                               sink.name)
        self.consume_phases[sink.name] = phases
        self.consumers.append(sink)

    def add_producer(self, src, phases):
        if src.name in self.produce_phases:
            raise RuntimeError('Primitive already has a producer %s' %
                               src.name)
        self.produce_phases[src.name] = phases
        self.producers.append(src)


class SchedulingPolicy:
    """Represents a scheduling policy.

    Each scheduler may implement multiple policies.

    :param str name: the policy name
    :param int cycles:
        number of cycles a scheduler using this policy requires to reach a
        decision
    """

    def __init__(self, name, cycles, param=None):
        """Initialize a scheduling policy

        :param str name: the policy name
        :param int cycles:
            number of cycles a scheduler using this policy requires to reach a
            decision
        """
        self.name = name
        self.scheduling_cycles = cycles


class Scheduler:
    '''
    Represents a scheduler provided by the platform. It schedules processes on
    one or more processors according to a policy. The class defines a list of
    all supported scheduling policies.
    '''

    def __init__(self, name, processors, policies):
        '''
        Initialize a Scheduler.
        :param name: name of the scheduler
        :param processors: list of Processor objects that are managed by this
                           scheduler
        :param policies: list of SchedulingPolicies that are supported by this
                         scheduler
        '''
        assert len(processors) > 0, (
            "A scheduler must be associated with at least one processor")
        assert len(policies) > 0, (
            "A scheduler must support at least one policy")

        self.name = name
        self.processors = processors
        self.policies = policies

    def find_policy(self, name, throw=False):
        """Lookup a policy by its name.

        :param str name: name of the policy to search for
        :raises RuntimeError: if no processor was found and throw is True
        :returns: A scheduling policy object or None if no policy was found.
        """
        for p in self.policies:
            if p.name == name:
                return p
        if throw:
            raise RuntimeError('The policy %s is not defined for this '
                               'scheduler!', name)
        return None


class Platform(object):
    """Represents a complete hardware architecture.

    This is a container for processor, communication resource, communication
    primitive, and scheduler objects.

    This is intended as a base class. Derived classes may define a specific
    platform by creating the corresponding objects.
    """

    def __init__(self):
        """Initialize the platform.

        This initializes all attributes to empty dicts. Derived classes should
        fill these dicts with objects in order to build a real platform.
        """
        self.processors = {}               #: dict of processors
        self.communication_resources = {}  #: dict of communication resources
        self.primitives = {}               #: dict of communication primitives
        self.schedulers = {}               #: dict of schedulers

    def find_scheduler(self, name):
        """Search for a scheduler object by its name."""
        return self.schedulers[name]

    def find_processor(self, name, throw=False):
        """Search for a processor object by its name."""
        return self.processors[name]

    def find_communication_resource(self, name, throw=False):
        """Search for a communication resource object by its name."""
        return self.communication_resources[name]

    def find_primitive(self, name, throw=False):
        """Search for a communication primitive group."""
        return self.primitives[name]

    def add_scheduler(self, x):
        if x.name in self.schedulers:
            raise RuntimeError(
                'Scheduler %s was already added to the platform' % (x.name))
        self.schedulers[x.name] = x

    def add_processor(self, x):
        if x.name in self.processors:
            raise RuntimeError(
                'Processor %s was already added to the platform' % (x.name))
        self.processors[x.name] = x

    def add_communication_resource(self, x):
        if x.name in self.communication_resources:
            raise RuntimeError(
                'Communication_Resource %s was already added to the platform' %
                (x.name))
        self.communication_resources[x.name] = x

    def add_primitive(self, x):
        if x.name in self.primitives:
            raise RuntimeError(
                'Primitive %s was already added to the platform' % (x.name))
        self.primitives[x.name] = x

    def to_pydot(self):
        """
        Convert the platform to a dot graph.

        This only prints processors, communication resources, and schedulers.
        Communication primitives are not printed.
        """
        dot = pydot.Dot(graph_type='digraph', strict=True)

        processor_nodes = {}
        for s in self.schedulers.values():
            cluster = pydot.Cluster('scheduler_' + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                node = pydot.Node('processor_' + p.name, label=p.name,
                                  shape='square')
                processor_nodes[p.name] = node
                cluster.add_node(node)

        primitive_nodes = {}
        for p in self.primitives.values():
            if p.name in primitive_nodes:
                node = primitive_nodes[p.name]
            else:
                node = pydot.Node('primitive_' + p.name, label=p.name)
                dot.add_node(node)
            for x in p.producers:
                from_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(from_node, node, minlen=4))
            for x in p.consumers:
                to_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(node, to_node, minlen=4))

        return dot

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
        return self.frequency_domain.cycles_to_ticks(self._read_latency)

    def write_latency(self):
        return self.frequency_domain.cycles_to_ticks(self._write_latency)

    def read_throughput(self):
        return (self._read_throughput /
                self.frequency_domain.cycles_to_ticks(1))

    def write_throughput(self):
        return (self._write_throughput /
                self.frequency_domain.cycles_to_ticks(1))

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
    '''
    Represents a communication primitive.

    A communication primitive defines how a process running on a processor
    (from_) sends data tokens to a process running on a processor (to). Since
    multiple primitives may be defined for each combination of from_ and to, a
    type attribute distinguishes different kinds of primitives.

    The communication is modeled as two lists of CommunicationPhases, one
    for producing tokens and one for consuming tokens. Passive communication,
    e.g., using a DMA unit is not (yet) supported.
    '''

    def __init__(self, type, from_, to):
        self.type = type
        self.from_ = from_
        self.to = to
        self.consume = []
        self.produce = []

    def __str__(self):
        return '%s: %s -> %s' % (self.type, self.from_, self.to)

    def __repr__(self):
        return self.__str__()


class PrimitiveGroup:
    """Groups communication primitives of the same type"""

    def __init__(self, type, primitives=None):
        self.type = type
        self._primitives = {}
        self._sources = set()
        self._sinks = set()
        if primitives is not None:
            for p in primitives:
                self.add_primitive(p)

    def get_primitive(self, from_, to):
        return self._primitives[from_._name][to._name]

    def add_primitive(self, primitive):
        assert self.type == primitive.type
        from_name = primitive.from_.name
        to_name = primitive.to.name
        if from_name not in self._primitives:
            self._primitives[from_name] = {}
        if to_name in self._primitives[from_name]:
            raise RuntimeError('Group already contains the primitive %s' %
                               (str(primitive)))
        self._primitives[from_name][to_name] = primitive
        self._sources.add(primitive.from_)
        self._sinks.add(primitive.to)

    def sources(self):
        return self._sources

    def sinks(self):
        return self._sinks


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

        This initializes all attributes to empty lists. Derived classes should
        fill these lists with objects in order to build a real platform.
        """
        self.processors = []               #: list of processors
        self.communication_resources = []  #: list of communication resources
        self.primitive_groups = []  #: list of communication primitive groups
        self.schedulers = []               #: list of schedulers

    def find_scheduler(self, name, throw=False):
        """Search for a scheduler object by its name.

        :param str name: name of the scheduler to be searched for
        :param bool throw: raise a RuntimeError if no object is
                           found (default: False)

        :raises RuntimeError: if no scheduler was found and throw is True
        :returns: A scheduler object or None if no scheduler was found.
        """
        for s in self.schedulers:
            if s.name == name:
                return s
        if throw:
            raise RuntimeError('The scheduler %s is not part of the platform!',
                               name)
        return None

    def find_processor(self, name, throw=False):
        """Search for a processor object by its name.

        :param str name: name of the processor to be searched for
        :param bool throw: raise a RuntimeError if no object is
                           found (default: False)

        :raises RuntimeError: if no processor was found and throw is True
        :returns: A processor object or None if no processor was found.
        """
        for p in self.processors:
            if p.name == name:
                return p
        if throw:
            raise RuntimeError('The processor %s is not part of the platform!',
                               name)
        return None

    def find_communication_resource(self, name, throw=False):
        """Search for a communication resource object by its name.

        :param str name: name of the communication resource to be searched for
        :param bool throw: raise a RuntimeError if no object is
                           found (default: False)

        :raises RuntimeError: if no communication resource was found and throw
                              is True
        :returns: A communication resource object or None if no communication
                  resource was found.
        """
        for s in self.communication_resources:
            if s.name == name:
                return s
        if throw:
            raise RuntimeError('The communication resource %s is not part of ',
                               'the platform!', name)
        return None

    def find_primitive_group(self, type, throw=False):
        """Search for a communication primitive group.

        :param str type: type of the communication primitive group to be
                         searched for
        :param bool throw: raise a RuntimeError if no object is
                           found (default: False)

        :raises RuntimeError: if no communication primitive was found and throw
                              is True
        :returns: A communication primitive group object or None if no
                  group was found.
        """
        for pg in self.primitive_groups:
            if pg.type == type:
                return pg
        if throw:
            raise RuntimeError('The primitive group %s is not part of the '
                               'platform!' % (type))
        return None

    def to_pydot(self):
        """
        Convert the platform to a dot graph.

        This only prints processors, communication resources, and schedulers.
        Communication primitives are not printed.
        """
        dot = pydot.Dot(graph_type='digraph', strict=True)

        processor_nodes = {}
        for s in self.schedulers:
            cluster = pydot.Cluster('scheduler_' + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                node = pydot.Node('processor_' + p.name, label=p.name,
                                  shape='square')
                processor_nodes[p.name] = node
                cluster.add_node(node)

        primitive_nodes = {}
        for pg in self.primitive_groups:
            if pg.type in primitive_nodes:
                node = primitive_nodes[pg.type]
            else:
                node = pydot.Node('primitive_' + pg.type, label=pg.type)
                dot.add_node(node)
            for x in pg.sources():
                from_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(from_node, node, minlen=4))
            for x in pg.sinks():
                to_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(node, to_node, minlen=4))

        return dot

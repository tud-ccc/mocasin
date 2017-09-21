# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import pydot


class FrequencyDomain:

    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency

    def cyclesToTicks(self, cycles):
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
        return self.frequency_domain.cyclesToTicks(cycles)

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
        self.frequency_domain = frequency_domain
        self.read_latency = read_latency
        self.write_latency = write_latency
        self.read_throughput = read_throughput
        self.write_throughput = write_throughput
        self.exclusive = exclusive
        self.is_storage = is_storage

    def readLatencyInTicks(self):
        return self.frequency_domain.cyclesToTicks(self.read_latency)

    def writeLatencyInTicks(self):
        return self.frequency_domain.cyclesToTicks(self.write_latency)

    def readThroughputInTicks(self):
        return self.read_throughput / self.frequency_domain.cyclesToTicks(1)

    def writeThroughputInTicks(self):
        return self.read_throughput / self.frequency_domain.cyclesToTicks(1)

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
    reosurces.
    '''
    def __init__(self, name, resources, direction,
                 ignore_latency=False, size=None):
        self.name = name
        self.resources = resources
        self.direction = direction
        self.ignore_latency = ignore_latency
        self.size = size

    def getCosts(self, size):
        latency = 0
        min_throughput = float('inf')
        if self.direction == 'read':
            for r in self.resources:
                if not self.ignore_latency:
                    latency += r.readLatencyInTicks()
                min_throughput = min(min_throughput, r.readThroughputInTicks())
        elif self.direction == 'write':
            for r in self.resources:
                if not self.ignore_latency:
                    latency += r.writeLatencyInTicks()
                min_throughput = min(min_throughput,
                                     r.writeThroughputInTicks())
        else:
            raise RuntimeError('Direction must be "read" or "write"!')
        if self.size is None:
            return int(round(latency + size / min_throughput))
        else:
            return int(round(latency + self.size / min_throughput))


class Primitive:
    '''
    Represents a cmmunication primitive.

    A communication primitive defines how
    a process running on a processr (from_) sends data tokens to a process
    running on a processor (to) via a memory (via). Since multiple primitives
    may be defined for each combination of from_, via, and to, a type attribute
    distinguishes primitives.

    The communication is modeled as two lists of CommunicationPhases, one
    for producing tokens and one for consuming tokens. Passive communication,
    e.g., using a DMA unit is not (yet) supported.
    '''

    def __init__(self, type, from_, via, to):

        self.type = type
        self.from_ = from_
        self.via = via
        self.to = to
        self.consume = []
        self.produce = []

    def __str__(self):
        return '%s: %s -> %s -> %s' % (self.type, self.from_,
                                       self.via, self.to)

    def __repr__(self):
        return self.__str__()


class SchedulingPolicy:
    '''
    Represents a scheduling policy. Each scheduler may implement multiple
    policies.
    '''

    def __init__(self, name, cycles, param=None):
        '''
        Initialize a SchedulingPolicy.
        :param name: policy name
        :param cycles: number of cycles a scheduler using this policy requires
                       to reach a decision
        :param param: an optional parameter that allows for additional
                      configuration of the policy
        '''
        self.name = name
        self.scheduling_cycles = cycles
        self.param = param


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


class Platform(object):
    '''
    Represents a complete hardware architecture. This is a container for
    processor, communication resource, communication primitive, and scheduler
    objects.

    This is intended as a base class. Derived classes may define a specific
    platform by creating the corresponding objects.
    '''

    def __init__(self):
        self.processors = []
        self.communication_resources = []
        self.primitives = []
        self.schedulers = []
    def find_scheduler(self, name, throw=False):

        for s in self.schedulers:
            if s.name == name:
                return s
        if throw:
            raise RuntimeError('The scheduler %s is not part of the platform!',
                               name)
        return None

    def find_processor(self, name, throw=False):
        for p in self.processors:
            if p.name == name:
                return p
        if throw:
            raise RuntimeError('The processor %s is not part of the platform!',
                               name)
        return None

    def find_communication_resource(self, name, throw=False):
        for s in self.communication_resources:
            if s.name == name:
                return s
        if throw:
            raise RuntimeError('The communication resource %s is not part of ',
                               'the platform!', name)
        return None

    def find_primitive(self, type, processor_from, processor_to, via_storage,
                       throw=False):
        for p in self.primitives:
            if (p.type == type and p.from_ == processor_from and
                    p.to == processor_to and p.via == via_storage):
                return p
        if throw:
            raise RuntimeError('The communication primitive %s: %s->%s->%s is '
                               'not part of the platform!', type,
                               processor_from.name, via_storage.name,
                               processor_to.name)
        return None

    def to_pydot(self):
        """
        Convert the platform to a dot graph.

        This only prints processors, communication resources, and schedulers.
        Communication primitives are not printed.
        """
        # TODO print communication primitives in some way
        dot = pydot.Dot(graph_type='digraph')

        fd_clusters = {}
        processor_nodes = {}
        resource_nodes = {}

        for p in self.processors:
            fd = p.frequency_domain.name
            cluster = _get_fd_cluster(dot, fd_clusters, fd)
            node = pydot.Node(p.name, label=p.name, shape='square')
            processor_nodes[p.name] = node
            cluster.add_node(node)

        for c in self.communication_resources:
            fd = c.frequency_domain.name
            cluster = _get_fd_cluster(dot, fd_clusters, fd)
            if c.is_storage:
                shape = 'diamond'
            else:
                shape = 'ellipse'
            node = pydot.Node(c.name, label=c.name, shape=shape)
            resource_nodes[c.name] = node
            cluster.add_node(node)

        for s in self.schedulers:
            sched_node = pydot.Node(s.name, label=s.name, shape='octagon')
            dot.add_node(sched_node)
            for p in s.processors:
                dot.add_edge(pydot.Edge(processor_nodes[p.name], sched_node))

        return dot


def _get_fd_cluster(dot, fd_clusters, fd_name):
    if fd_name in fd_clusters:
        return fd_clusters[fd_name]
    else:
        cluster = pydot.Cluster(fd_name, label=fd_name)
        dot.add_subgraph(cluster)
        fd_clusters[fd_name] = cluster
        return cluster

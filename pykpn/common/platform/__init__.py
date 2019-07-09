# Copyright (C) 2017-2018 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import pydot

import math

from enum import Enum

#enum added by Felix Teweleit, 10.08.2018
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

    def __lt__(self, other_pe):
        return self.name.lower() < other_pe.name.lower()
    
    def __repr__(self):
        return self.__str__()


class CommunicationResource(object):
    '''
    Represents a resource required for communication. This can be anything from
    a link or bus to a memory.

    This is a base class that can be specialized to model more complex
    resources like caches.
    '''
    #resource Type attribute added by Felix Teweleit 10.08.2018

    def __init__(self, name, frequency_domain, resource_type, read_latency, write_latency,
                 read_throughput=float('inf'), write_throughput=float('inf'),
                 exclusive=False, is_storage=False, ):
        self.name = name
        self._resource_type = resource_type
        self._frequency_domain = frequency_domain
        self._read_latency = read_latency
        self._write_latency = write_latency
        self._read_throughput = read_throughput
        self._write_throughput = write_throughput
        self.exclusive = exclusive
        self.is_storage = is_storage
        
    def ressource_type(self):
        return self.ressource_type

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
        super(Storage, self).__init__(name, frequency_domain, CommunicationResourceType.Storage, read_latency, write_latency,
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
        return(self.static_produce_costs(src_processor, token_size) +
               self.static_consume_costs(sink_processor, token_size))

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
        assert(len(sinks) > 0)

        if src not in self.producers:
            return False
        for s in sinks:
            if s not in self.consumers:
                return False
        return True


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
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


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

    def __init__(self, name):
        """Initialize the platform.

        This initializes all attributes to empty dicts. Derived classes should
        fill these dicts with objects in order to build a real platform.
        """
        self.name = name
        self._processors = {}               #: dict of processors
        self._communication_resources = {}  #: dict of communication resources
        self._primitives = {}               #: dict of communication primitives
        self._schedulers = {}               #: dict of schedulers

    def processors(self):
        return self._processors.values()

    def primitives(self):
        return self._primitives.values()

    def schedulers(self):
        return self._schedulers.values()

    def communication_resources(self):
        return self._communication_resources.values()

    def find_scheduler_for_processor(self, processor):
        """Find all schedulers associated to a given processor.
           
           :param processor: a processer of the underlying platform
           :type processor: Processor
           :raises RuntimeError: if the processor was not found
           :returns: A set of possible schedulers for the processor.
        """
        if processor.name not in self._processors:
            raise RuntimeError('The processor {} is not defined for this '
                               'platform!'.format(processor.name))
        used_schedulers = set()

        for s in self._schedulers:
            if processor in self._schedulers[s].processors:
                used_schedulers.add( self._schedulers[s])
        
        #print("Found schedulers: {} for {}".format(used_schedulers, processor.name))
        return used_schedulers


    def find_scheduler(self, name):
        """Search for a scheduler object by its name."""
        return self._schedulers[name]

    def find_processor(self, name):
        """Search for a processor object by its name."""
        return self._processors[name]

    def find_communication_resource(self, name):
        """Search for a communication resource object by its name."""
        return self._communication_resources[name]

    def find_primitive(self, name):
        """Search for a communication primitive group."""
        return self._primitives[name]

    def add_scheduler(self, x):
        if x.name in self._schedulers:
            raise RuntimeError(
                'Scheduler %s was already added to the platform' % (x.name))
        self._schedulers[x.name] = x

    def add_processor(self, x):
        if x.name in self._processors:
            raise RuntimeError(
                'Processor %s was already added to the platform' % (x.name))
        self._processors[x.name] = x

    def add_communication_resource(self, x):
        if x.name in self._communication_resources:
            raise RuntimeError(
                'Communication_Resource %s was already added to the platform' %
                (x.name))
        self._communication_resources[x.name] = x

    def add_primitive(self, x):
        if x.name in self._primitives:
            raise RuntimeError(
                'Primitive %s was already added to the platform' % (x.name))
        self._primitives[x.name] = x

    def to_pydot(self):
        """
        Convert the platform to a dot graph.

        This only prints processors, communication resources, and schedulers.
        Communication primitives are not printed.
        """
        dot = pydot.Dot(graph_type='digraph', strict=True)

        processor_nodes = {}
        for s in self.schedulers():
            cluster = pydot.Cluster('scheduler_' + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                node = pydot.Node('processor_' + p.name, label=p.name,
                                  shape='square')
                processor_nodes[p.name] = node
                cluster.add_node(node)

        primitive_nodes = {}
        for p in self.primitives():
            if p.name in primitive_nodes:
                node = primitive_nodes[p.name]
            else:
                node = pydot.Node('primitive_' + p.name, label=p.name)
                dot.add_node(node)
            minlen = 1 + math.log(len(p.consumers) + len(p.producers)) * 2
            for x in p.producers:
                from_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(from_node, node, minlen=minlen))
            for x in p.consumers:
                to_node = processor_nodes[x.name]
                dot.add_edge(pydot.Edge(node, to_node, minlen=minlen))

        return dot

    def to_adjacency_dict(self,precision=5):
        """
        Convert the platform to an adjacency dictionary.

        This only prints processors and communication resources.
        The edges are annotated with the static communication cost
        for a simple token of size 8.
        Schedulers and communication primitives are not considered.
        
        precision: number of siginifcant figures to consider on costs.
        for full precision, select -1
        """
        num_vertices = 0
        vertices = {}
        adjacency_dict = {}
        coloring = []

    
        for s in self.schedulers():
            for p in s.processors:
                vertices[p.name] = num_vertices
                num_vertices = num_vertices + 1


        for p in self.primitives():
             
            for x in p.producers:
                if x.name not in adjacency_dict:
                    adjacency_dict[x.name] = {}
                for y in p.consumers:
                    cost = p.static_costs(x,y, token_size=8)
                    if precision < 0 or cost == 0:
                        pass
                    else:
                        cost = round(cost, precision-1-int(math.floor(math.log10(abs(cost)))))
                    #print( (x,y,cost))
                    if y.name not in adjacency_dict[x.name]:
                        adjacency_dict[x.name][y.name] = cost 
                    #here we should decide what to do with the different primitive
                    #I dediced to just take the minimum for now.
                    adjacency_dict[x.name][y.name] = min(adjacency_dict[x.name][y.name],cost)
                    if precision < 0 or cost == 0:
                        pass
                    else:
                        cost = round(cost, precision-1-int(math.floor(math.log10(abs(cost)))))
                    
        res = {}
        for elem in adjacency_dict:
            res[elem] = [(adjacent, adjacency_dict[elem][adjacent]) for adjacent in adjacency_dict[elem]]
        return res

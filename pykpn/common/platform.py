# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import parser


class FrequencyDomain:

    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency

    def cyclesToTicks(self, cycles):
        tmp = float(cycles) * 1000000000000 / float(self.frequency)
        return int(tmp)


class Memory:

    def __init__(self, name, size):
        self.name = name
        self.size = size


class Processor:

    def __init__(self, name, type, frequency_domain, contextSwitchInDelay=0,
                 contextSwitchOutDelay=0):
        self.name = name
        self.type = type
        self.frequency_domain = frequency_domain
        self.contextSwitchInDelay = contextSwitchInDelay
        self.contextSwitchOutDelay = contextSwitchOutDelay

    def ticks(self, cycles):
        return self.frequency_domain.cyclesToTicks(cycles)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Resource:
    '''
    Represents a shared hardware resource.

    This class is required for modeling the usage of shared resources in the
    cost model.
    '''

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity


class CostModel:

    def __init__(self, func, **params):
        self.resources = []
        self.params = params
        self.func = parser.expr(func).compile()

    def getCosts(self, **params):
        vars().update(self.params)
        vars().update(params)
        return eval(self.func)


class Primitive:
    '''
    Represents a cmmunication primitive.

    A communication primitive defines how
    a process running on a processr (from_) sends data tokens to a process
    running on a processor (to) via a memory (via). Since multiple primitives
    may be defined for each combination of from_, via, and to, a type attribute
    distinguishes primitives.

    The communication is modeled as two lists of CommunicationModels, one
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


class Scheduler:
    '''
    Represents a scheduler provided by the platform. It schedules processes
    on one or more processors according to a policy. The class defines a
    dictionary of policies and associated scheduling delays for each policy.
    '''

    implementedPolicies = ['None', 'FIFO', 'RoundRobin']

    def __init__(self, name, processors, policies):
        assert len(processors) > 0, \
            "A scheduler must be associated with at least one processor"
        assert len(policies) > 0, \
            "A scheduler must support at least one policy"

        self.name = name
        self.processors = processors
        self.policies = policies


class Platform(object):
    '''
    Represents a coplete hardware architecture. This is a container for
    processor, memory, communication primitive, and scheduler objects.

    This is intended as a base class. Derived classes may define a specifi
    platform by creating the corresponding objects.
    '''

    def __init__(self):
        self.processors = []
        self.memories = []
        self.primitives = []
        self.schedulers = []

    def findScheduler(self, name):
        for s in self.schedulers:
            if s.name == name:
                return s
        return None

    def findProcessor(self, name):
        for p in self.processors:
            if p.name == name:
                return p
        return None

    def findMemory(self, name):
        for m in self.memories:
            if m.name == name:
                return m
        return None

    def findPrimitive(self, type, processorFrom, processorTo, viaMemory):
        for p in self.primitives:
            if p.type == type and p.from_ == processorFrom and \
                    p.to == processorTo and p.via == viaMemory:
                return p
        return None

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from enum import Enum


class SchedulingPolicy(Enum):
    FIFO = 0
    RoundRobin=1


class ChannelInfo:
    name = None
    capacity = None
    fromProcessor = None
    toProcessor = None
    viaMemory = None
    primitive = None


class SchedulerInfo:
    name = None
    policy = None
    processNames = None
    processorNames = None


class Mapping:
    def __init__(self):
        self.schedulers = []
        self.channels = []

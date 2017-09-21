# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from itertools import product
import pydot


class ChannelMappingInfo:
    """Simple record to store mapping infos associated with a KpnChannel.

    :ivar Primitive primitive: the primitive that the channel is mapped to
    :ivar int capacity: the capacity that the channel is bound to
    """
    def __init__(self, primitive, capacity):
        self.primitive = primitive
        self.capacity = capacity


class ProcessMappingInfo:
    """Simple record to store mapping infos associated with a KpnProcess.

    :ivar Scheduler scheduler: the scheduler that the process is mapped to
    :ivar Processor affinity: the processor that the process should run on
    """
    def __init__(self, scheduler, affinity):
        self.scheduler = scheduler
        self.affinity = affinity


class SchedulerMappingInfo:
    """Simple record to store mapping infos associated with a Scheduler.

    :ivar list[KpnProcess] processes: a list of processes mapped to this
                                      scheduler
    :ivar SchedulingPolicy policy: the policy to be used by the scheduler
    :ivar param: a paramter that can be used to configure a scheduling policy
    """
    def __init__(self, processes, policy, param):
        self.processes = processes
        self.policy = policy
        self.param = param


class Mapping:
    """Describes the mapping of a KpnGraph to a Platform."""

    def __init__(self, kpn, platform):
        """Initialize a Mapping

        :param KpnGraph kpn: the kpn graph
        :param Platform platform: the platform
        """
        # The ProcessInfo record is not really required as it only has one
        # item. However, we might want to extend it later

        self._kpn = kpn            #: the kpn graph
        self._platform = platform  #: the platform

        self._channel_info = {}    #: dict of ChannelMappingInfo
        self._process_info = {}    #: dict of ProcessMappingInfo
        self._scheduler_info = {}  #: dict of SchedulerMappingInfo

        # initialize all valid dictionary entries to None
        for p in kpn.processes:
            self._process_info[p.name] = None
        for c in kpn.channels:
            self._channel_info[c.name] = None
        for s in platform.schedulers:
            self._scheduler_info[s.name] = None

    def channel_info(self, channel):
        """Look up the mapping info of a channel.

        :param KpnChannel channel: channel to look up
        :return the mapping info if the channel is mapped
        :rtype ChannelMappingInfo or None
        """
        return self._channel_info[channel.name]

    def process_info(self, process):
        """Look up the mapping info of a process.

        :param KpnProcess process: process to look up
        :return the mapping info if the process is mapped
        :rtype ProcessMappingInfo or None
        """
        return self._process_info[process.name]

    def scheduler_info(self, scheduler):
        """Look up the mapping info of a scheduler.

        :param KpnScheduler scheduler: scheduler to look up
        :return the mapping info if the scheduler is mapped
        :rtype SchedulerMappingInfo or None
        """
        return self._scheduler_info[scheduler.name]

    def to_pydot(self):
        """Convert the mapping to a dot graph

        The generated graph visualizes how a KPN application is mapped
        to a platform.

        :returns: pydot object
        """
        return self._platform.to_pydot()

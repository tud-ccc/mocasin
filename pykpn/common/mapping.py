# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import pydot


class ChannelMappingInfo:
    """Simple record to store mapping infos associated with a KpnChannel.

    :ivar primitive: the communication primitive that the channel is mapped to
    :type primitive: Primitive
    :ivar int capacity: the capacity that the channel is bound to
    """
    def __init__(self, primitive, capacity):
        self.primitive = primitive
        self.capacity = capacity


class ProcessMappingInfo:
    """Simple record to store mapping infos associated with a KpnProcess.

    :ivar Scheduler scheduler: the scheduler that the process is mapped to
    :ivar Processor affinity: the processor that the process should run on
    :ivar int priority: the scheduling priority
    """
    def __init__(self, scheduler, affinity, priority=0):
        self.scheduler = scheduler
        self.affinity = affinity
        self.priority = priority


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
            self._process_info[p] = None
        for c in kpn.channels:
            self._channel_info[c] = None
        for s in platform.schedulers:
            self._scheduler_info[s] = None

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

        :param Scheduler scheduler: scheduler to look up
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
        dot = pydot.Dot(graph_type='digraph')

        processor_clusters = {}
        for s in self._platform.schedulers.values():
            cluster = pydot.Cluster('scheduler_' + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                p_cluster = pydot.Cluster('processor_' + p.name, label=p.name)
                p_cluster.add_node(
                    pydot.Node('dummy_' + p.name, style='invis'))
                processor_clusters[p.name] = p_cluster
                cluster.add_subgraph(p_cluster)

        primitive_nodes = {}
        for p in self._platform.primitives.values():
            if p.name not in primitive_nodes:
                node = pydot.Node('primitive_' + p.name, label=p.name)
                dot.add_node(node)
                primitive_nodes[p.name] = node

        process_nodes = {}
        for p in self._kpn.processes.keys():
            info = self._process_info[p]
            p_cluster = processor_clusters[info.affinity.name]
            node = pydot.Node('process_' + p, label=p)
            process_nodes[p] = node
            p_cluster.add_node(node)

        channel_nodes = {}
        for c in self._kpn.channels.values():
            node = pydot.Node('channel_' + c.name, label=c.name,
                              shape='diamond')
            channel_nodes[c.name] = node
            dot.add_node(node)
            from_node = process_nodes[c.source.name]
            dot.add_edge(pydot.Edge(from_node, node, minlen=4))
            for p in c.sinks:
                to_node = process_nodes[p.name]
                dot.add_edge(pydot.Edge(node, to_node, minlen=4))
            info = self._channel_info[c.name]
            prim_node = primitive_nodes[info.primitive.name]
            dot.add_edge(pydot.Edge(node, prim_node, style='dashed',
                                    arrowhead='none'))

        return dot

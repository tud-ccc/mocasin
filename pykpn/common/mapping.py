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
    def __init__(self, policy, param):
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
        for p in kpn.processes():
            self._process_info[p.name] = None
        for c in kpn.channels():
            self._channel_info[c.name] = None
        for s in platform.schedulers():
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

        :param Scheduler scheduler: scheduler to look up
        :return the mapping info if the scheduler is mapped
        :rtype SchedulerMappingInfo or None
        """
        return self._scheduler_info[scheduler.name]

    def scheduler_processes(self, scheduler):
        """Get a list of processes mapped to a scheduler

        :param Scheduler scheduler: scheduler to look up
        :return: a list of processes
        :rtype: list[KpnProcess]
        """
        processes = []
        for p in self._kpn.processes():
            info = self.process_info(p)
            if scheduler is info.scheduler:
                processes.append(p)
        return processes

    def add_channel_info(self, channel, info):
        """Add a channel mapping"""
        assert channel.name in self._channel_info
        assert self._channel_info[channel.name] is None
        self._channel_info[channel.name] = info

    def add_process_info(self, process, info):
        """Add a process mapping"""
        assert process.name in self._process_info
        assert self._process_info[process.name] is None
        self._process_info[process.name] = info

    def add_scheduler_info(self, scheduler, info):
        """Add a scheduler config"""
        assert scheduler.name in self._scheduler_info
        assert self._scheduler_info[scheduler.name] is None
        self._scheduler_info[scheduler.name] = info

    def to_list(self):
        """Convert to a list (tuple) with processes as entries 
        and PEs labeled from 0 to NUM_PES"""

        #initialize lists for numbers
        procs_list = list(map(lambda o: o.name,self._kpn.processes()))
        chans_list = list(map(lambda o: o.name,self._kpn.channels()))
        pes_list = list(map(lambda o: o.name,self._platform.processors()))
        pes = {}
        for i,pe in enumerate(pes_list):
            pes[pe] = i
        res = []

        for proc in procs_list:
            info = self._process_info[proc]
            proc_target = pes[info.affinity.name]
            res.append( proc_target)

        for chan in chans_list:
            info = self._channel_info[chan]
            kpn_chan = self._kpn.find_channel(chan)
            src = kpn_chan.source 
            src_proc = self._process_info[src.name].affinity
            snks = kpn_chan.sinks 
            for snk in snks:
                snk_proc = self._process_info[snk.name].affinity
                primitive_costs = info.primitive.static_costs(
                    src_proc.name, snk_proc.name, token_size=kpn_chan.token_size)
                primitive_costs *= 1e-7
                res.append( primitive_costs)

        return res

    def to_pydot(self):
        """Convert the mapping to a dot graph

        The generated graph visualizes how a KPN application is mapped
        to a platform.

        :returns: pydot object
        """
        dot = pydot.Dot(graph_type='digraph')

        processor_clusters = {}
        for s in self._platform.schedulers():
            cluster = pydot.Cluster('scheduler_' + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                p_cluster = pydot.Cluster('processor_' + p.name, label=p.name)
                p_cluster.add_node(
                    pydot.Node('dummy_' + p.name, style='invis'))
                processor_clusters[p.name] = p_cluster
                cluster.add_subgraph(p_cluster)

        primitive_nodes = {}
        for p in self._platform.primitives():
            if p.name not in primitive_nodes:
                node = pydot.Node('primitive_' + p.name, label=p.name)
                dot.add_node(node)
                primitive_nodes[p.name] = node

        process_nodes = {}
        for p in self._kpn.processes():
            info = self._process_info[p.name]
            p_cluster = processor_clusters[info.affinity.name]
            node = pydot.Node('process_' + p.name, label=p.name)
            process_nodes[p.name] = node
            p_cluster.add_node(node)

        channel_nodes = {}
        for c in self._kpn.channels():
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

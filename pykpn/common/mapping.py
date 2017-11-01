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
    """Describes the mapping of a KpnGraph to a Platform.

    :ivar KpnGraph _kpn: the kpn graph
    :ivar Platform _platform: the platform
    :ivar dict[str, ChannelMappingInfo] _channel_info:
        dict of channel mapping infos
    :ivar dict[str, ProcessMappingInfo] _process_info:
        dict of process mapping infos
    :ivar dict[str, SchedulerMappingInfo] _scheduler_info:
        dict of scheduler mapping infos
    """

    def __init__(self, kpn, platform):
        """Initialize a Mapping

        :param KpnGraph kpn: the kpn graph
        :param Platform platform: the platform
        """
        # The ProcessInfo record is not really required as it only has one
        # item. However, we might want to extend it later

        self._kpn = kpn
        self._platform = platform

        self._channel_info = {}
        self._process_info = {}
        self._scheduler_info = {}

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
        :returns: the mapping info if the channel is mapped
        :rtype: ChannelMappingInfo or None
        """
        return self._channel_info[channel.name]

    def process_info(self, process):
        """Look up the mapping info of a process.

        :param KpnProcess process: process to look up
        :returns: the mapping info if the process is mapped
        :rtype: ProcessMappingInfo or None
        """
        return self._process_info[process.name]

    def scheduler_info(self, scheduler):
        """Look up the mapping info of a scheduler.

        :param Scheduler scheduler: scheduler to look up
        :returns: the mapping info if the scheduler is mapped
        :rtype: SchedulerMappingInfo or None
        """
        return self._scheduler_info[scheduler.name]

    def scheduler_processes(self, scheduler):
        """Get a list of processes mapped to a scheduler

        :param Scheduler scheduler: scheduler to look up
        :returns: a list of processes
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

    def affinity(self, process):
        """Returns the affinity of a KPN process

        :param KpnProcess process: the KPN process
        :rtype: Processor
        """
        return self._process_info[process.name].affinity

    def scheduler(self, process):
        """Returns the scheduler that a KPN process is mapped to

        :param KpnProcess process: the KPN process
        :rtype: Scheduler
        """
        return self._process_info[process.name].scheduler

    def primitive(self, channel):
        """Returns the primitive that a KPN channel is mapped to

        :param KpnChannel channel: the KPN channel
        :rtype: Primitive
        """
        return self._channel_info[channel.name].primitive

    def capacity(self, channel):
        """Returns the capacity (number of tokens) of a KPN channel

        :param KpnChannel channel: the KPN channel
        :rtype: int
        """
        return self._channel_info[channel.name].capacity

    def channel_source(self, channel):
        """Returns the source processor of a KPN channel

        :param KpnChannel channel: the KPN channel
        :rtype: Processor
        """
        source = self._kpn.find_channel(channel.name).source
        return self.affinity(source)

    def channel_sinks(self, channel):
        """Returns the list of sink processors for a KPN channel

        :param KpnChannel channel: the KPN channel
        :rtype: list[Processor]
        """
        sinks = self._kpn.find_channel(channel.name).sinks
        return [self.affinity(s) for s in sinks]

    def to_list(self):
        """Convert to a list (tuple) with processes as entries and PEs labeled
        from 0 to NUM_PES"""

        # initialize lists for numbers
        procs_list = self._kpn.processes()
        chans_list = self._kpn.channels()
        pes_list = self._platform.processors()

        # map PEs to an integer
        pes = {}
        for i, pe in enumerate(pes_list):
            pes[pe.name] = i
        res = []

        # add one result entry for each process mapping
        for proc in procs_list:
            res.append(pes[self.affinity(proc).name])

        # add one result entry for each KPN channel (multiple in case of
        # multiple reader channels)
        for chan in chans_list:
            src = self.channel_source(chan)
            sinks = self.channel_sinks(chan)
            prim = self.primitive(chan)
            for snk in sinks:
                primitive_costs = prim.static_costs(
                    src, snk, token_size=chan.token_size)
                primitive_costs *= 1e-7  # scale down
                # TODO Probably it is better to normalize the values
                res.append(primitive_costs)

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

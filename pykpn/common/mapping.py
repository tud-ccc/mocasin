# Copyright (C) 2017-2018 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import pydot
import random
from pykpn.util import logging
from pykpn.representations.representations import RepresentationType #MappingRepresentation, MetricSpaceRepresentation, SymmetryRepresentation, MetricSymmetryRepresentation, MetricEmbeddingRepresentation


log = logging.getLogger(__name__)

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
    :ivar MappingRepresentation _representation: the representation for mappings.
    """

    def __init__(self, kpn, platform, representation_type=RepresentationType['SimpleVector']):
        """Initialize a Mapping

        :param KpnGraph kpn: the kpn graph
        :param Platform platform: the platform
        """
        # The ProcessInfo record is not really required as it only has one
        # item. However, we might want to extend it later

        self._kpn = kpn
        self._platform = platform
        self._representation_type = representation_type
        self._representation = self._representation_type.getClassType()(self._kpn,self._platform)

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
    
    def change_affinity(self, processName, processorName):
        """Changes the affinity of a process to a processing element
        :param string processName: the name of the process for which the affinity should be changed
        :param string processorName: the name of the processor to which the process should be applied 
        """
        newProcessor = None
        for processor in self._platform.processors():
            if processor.name == processorName:
                newProcessor = processor
                break
        if newProcessor != None:
            priority = self._process_info[processName].priority
            scheduler = self._process_info[processName].scheduler
            del self._process_info[processName]
            self._process_info.update({processName : ProcessMappingInfo(scheduler, newProcessor, priority)})
        return True
    
    def to_string(self):
        """Convert mapping to a simple readable string 
        :rtype: string 
        """
        procs_list = self._kpn.processes()
        chans_list = self._kpn.channels()
        pes_list = self._platform.processors()
        
        # return processor - process mapping
        s = ("\nCore Mapping: \n")
        pes2procs = {}
        for pe in pes_list:
            pes2procs.update({pe.name:[]})
        max_width = max(map(len,pes2procs))
        for proc in procs_list:
            pes2procs[self.affinity(proc).name].append(proc.name)
        for key in sorted(pes2procs):
            s = ("{0}    {1:{3}} {2}\n".format(s, key,pes2procs[key],max_width))

        # return channel mapping
        chan2prim = {}
        s = ("{}Channels:\n".format(s))
        for c in chans_list:
            chan2prim.update({c.name:(self.channel_source(c).name,
                                      self.primitive(c).name)})

        max_width = max(map(len,chan2prim))
        for key in sorted(chan2prim):
            s = ("{0}    {1:{4}} {2} - {3}\n".format(s,key,chan2prim[key][0],
                                                     chan2prim[key][1],max_width))

        return s

    def to_list(self):
        """Convert to a list (tuple), the simple vector representation.
        It is a list with processes as entries and PEs labeled
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

    def from_list(self,list_from):
        """Convert from a list (tuple), the simple vector representation.
           Priority and policy chosen at random, and scheduler chosen randomly from the possible ones.
           If list has length # processes + # channels, then channels are chosen as the second part of the list.
           Otherwise, they are chosen at random.
           Note that this function assumes the input is sane.

           TODO: make it possible to give schedulers, too.
           TODO: check if we need to use correspondence of representation to ensure ordering is right
        """
        processors = list(self._platform.processors())
        all_schedulers = list(self._platform.schedulers())
        all_primitives = list(self._platform.primitives())
        #print(list_from)

        # configure schedulers
        for s in all_schedulers:
            i = random.randrange(0, len(s.policies))
            policy = s.policies[i]
            info = SchedulerMappingInfo(policy, None)
            self.add_scheduler_info(s, info)
            log.debug('configure scheduler %s to use the %s policy',
                      s.name, policy.name)
            
        # map processes
        for i,p in enumerate(self._kpn.processes()):
            idx = list_from[i]
            schedulers = [ sched for sched in all_schedulers if processors[idx] in sched.processors]
            j = random.randrange(0, len(schedulers))
            scheduler = schedulers[j]
            affinity = processors[idx] 
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            self.add_process_info(p, info)
            log.debug('map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)

        # map channels
        for i,c in enumerate(self._kpn.channels(),start=i+1):
            capacity = 4
            suitable_primitives = []
            for p in all_primitives:
                src = self.process_info(c.source).affinity
                sinks = [self.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError('Mapping failed! No suitable primitive for '
                                   'communication from %s to %s found!' %
                                   (src.name, str(sinks)))
            if len(list_from) == len(self._kpn.processes()) :
                if len(suitable_primitives) == 1:
                    primitive = suitable_primitives[0]
                else:
                    idx = random.randrange(0, len(suitable_primitives)-1)
                    primitive = suitable_primitives[idx]
            else:
                idx = list_from[i]
                primitive = all_primitives[idx]
                assert(primitive in suitable_primitives)

            info = ChannelMappingInfo(primitive, capacity)
            self.add_channel_info(c, info)
            log.debug('map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity))
    

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

    def toRepresentation(self):
        return self._representation.simpleVec2Elem(self.to_list())

    def fromRepresentation(self,elem):
        self.from_list(self._representation.elem2SimpleVec(elem))

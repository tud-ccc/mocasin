# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Andres Goens, Gerald Hempel

from collections import Counter
import pydot
import random
from mocasin.util import logging

log = logging.getLogger(__name__)


class ChannelMappingInfo:
    """Simple record to store mapping infos associated with a DataflowChannel.

    :ivar primitive: the communication primitive that the channel is mapped to
    :type primitive: Primitive
    :ivar int capacity: the capacity that the channel is bound to
    """

    def __init__(self, primitive, capacity):
        self.primitive = primitive
        self.capacity = capacity


class ProcessMappingInfo:
    """Simple record to store mapping infos associated with a DataflowProcess.

    :ivar Scheduler scheduler: the scheduler that the process is mapped to
    :ivar Processor affinity: the processor that the process should run on
    :ivar int priority: the scheduling priority
    """

    def __init__(self, scheduler, affinity, priority=0):
        self.scheduler = scheduler
        self.affinity = affinity
        self.priority = priority


class MappingMetadata:
    """Simple record to store mapping's energy-utility metadata.

    :ivar float exec_time: the execution time of the mapping
    :ivar float energy: the energy consumption of the mapping
    """

    def __init__(self, exec_time=None, energy=None):
        self.exec_time = exec_time
        self.energy = energy


class Mapping:
    """Describes the mapping of a DataflowGraph to a Platform.

    :ivar DataflowGraph graph: the dataflow graph
    :ivar Platform platform: the platform
    :ivar dict[str, ChannelMappingInfo] _channel_info:
        dict of channel mapping infos
    :ivar dict[str, ProcessMappingInfo] _process_info:
        dict of process mapping infos
    """

    def __init__(self, graph, platform):
        """Initialize a Mapping

        :param DataflowGraph graph: the dataflow graph
        :param Platform platform: the platform
        """

        self.graph = graph
        self.platform = platform

        self._channel_info = {}
        self._process_info = {}

        # initialize all valid dictionary entries to None
        for p in graph.processes():
            self._process_info[p.name] = None
        for c in graph.channels():
            self._channel_info[c.name] = None

        # initialize metadata
        self.metadata = MappingMetadata()

    def update_graph_object(self, graph):
        """
        This function updates the graph object in the mapping. Assumes both graphs describe the same application (just different python objects).
        It propagates all the references in the process/channel info dictionaries to the new object.
        :param graph:  The new graph object
        """
        self.graph = graph
        processors = self.platform.processors()
        schedulers = self.platform.schedulers()
        for p in graph.processes():
            proc_info = self._process_info[p.name]
            affinity = [
                proc
                for proc in processors
                if proc.name == proc_info.affinity.name
            ][0]
            proc_info.affinity = affinity
            scheduler = [
                sched
                for sched in schedulers
                if sched.name == proc_info.scheduler.name
            ][0]
            proc_info.scheduler = scheduler

        primitives = self.platform.primitives()
        for c in graph.channels():
            chan_info = self._channel_info[c.name]
            primitive = [
                prim
                for prim in primitives
                if prim.name == chan_info.primitive.name
            ][0]
            chan_info.primitive = primitive

    def channel_info(self, channel):
        """Look up the mapping info of a channel.

        :param DataflowChannel channel: channel to look up
        :returns: the mapping info if the channel is mapped
        :rtype: ChannelMappingInfo or None
        """
        return self._channel_info[channel.name]

    def process_info(self, process):
        """Look up the mapping info of a process.

        :param DataflowProcess process: process to look up
        :returns: the mapping info if the process is mapped
        :rtype: ProcessMappingInfo or None
        """
        return self._process_info[process.name]

    def get_unmapped_channels(self):
        """Returns a list of unmapped channels

        :returns: List of unmapped channels
        :rtype: List[Channels]
        """
        log.debug(
            "mapping remaining channels: {}".format(
                dict(
                    filter(lambda c: c[1] is None, self._channel_info.items())
                ).keys()
            )
        )
        # filter all channels with name is partof list
        unmapped_channels = dict(
            filter(lambda c: c[1] is None, self._channel_info.items())
        ).keys()
        return list(
            filter(lambda c: c.name in unmapped_channels, self.graph.channels())
        )

    def get_unmapped_processes(self):
        """Returns a list of unmapped processes
        :returns: List of unmapped processes
        :rtype: List[DataflowProcess]
        """
        log.debug(
            "mapping remaining processes: {}".format(
                dict(
                    filter(lambda c: c[1] is None, self._process_info.items())
                ).keys()
            )
        )
        unmapped_processes = dict(
            filter(lambda p: p[1] is None, self._process_info.items())
        ).keys()
        return list(
            filter(
                lambda p: p.name in unmapped_processes, self.graph.processes()
            )
        )

    def scheduler_processes(self, scheduler):
        """Get a list of processes mapped to a scheduler

        :param Scheduler scheduler: scheduler to look up
        :returns: a list of processes
        :rtype: list[DataflowProcess]
        """
        processes = []
        for p in self.graph.processes():
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

    def affinity(self, process):
        """Returns the affinity of a dataflow process

        :param DataflowProcess process: the dataflow process
        :rtype: Processor
        """
        if self._process_info[process.name] is None:
            return None
        return self._process_info[process.name].affinity

    def primitive(self, channel):
        """Returns the primitive that a dataflow channel is mapped to

        :param DataflowChannel channel: the dataflow channel
        :rtype: Primitive
        """
        return self._channel_info[channel.name].primitive

    def capacity(self, channel):
        """Returns the capacity (number of tokens) of a dataflow channel

        :param DataflowChannel channel: the dataflow channel
        :rtype: int
        """
        return self._channel_info[channel.name].capacity

    def channel_source(self, channel):
        """Returns the source processor of a dataflow channel

        :param DataflowChannel channel: the dataflow channel
        :rtype: Processor
        """
        source = self.graph.find_channel(channel.name).source
        return self.affinity(source)

    def channel_sinks(self, channel):
        """Returns the list of sink processors for a dataflow channel

        :param DataflowChannel channel: the dataflow channel
        :rtype: list[Processor]
        """
        sinks = self.graph.find_channel(channel.name).sinks
        return [self.affinity(s) for s in sinks]

    def get_numPEs(self):
        """Returns the maximum number of PEs for the platform

        :rtype: numPEs
        """
        return len(self.platform.processors()) - 1

    def get_numProcs(self):
        """Returns the number of processes in the mapping"""
        return len(self.graph.processes())

    def change_affinity(self, process_name, processor_name):
        """Changes the affinity of a process to a processing element

        Args:
            process_name (str): the name of the process for which the affinity
                should be changed
            processor_name (str): the name of the processor to which the
                process should be applied
        """
        processor = self.platform.find_processor(processor_name)
        assert (
            processor in self._process_info[process_name].scheduler.processors
        )
        self._process_info[process_name].affinity = processor

    def get_used_processors(self):
        """Returns a set of used processors."""
        return {self.affinity(p) for p in self.graph.processes()}

    def get_used_processor_types(self):
        """Returns the counter of processors of each type used by the mapping."""
        processors = self.get_used_processors()
        res = Counter()
        for p in processors:
            res[p.type] += 1
        return res

    def to_string(self):
        """Convert mapping to a simple readable string
        :rtype: string
        """
        procs_list = self.graph.processes()
        chans_list = self.graph.channels()
        pes_list = self.platform.processors()

        # return processor - process mapping
        s = "\nCore Mapping: \n"
        pes2procs = {}
        for pe in pes_list:
            pes2procs.update({pe.name: []})
        max_width = max(map(len, pes2procs))
        for proc in procs_list:
            pes2procs[self.affinity(proc).name].append(proc.name)
        for key in sorted(pes2procs):
            s = "{0}    {1:{3}} {2}\n".format(s, key, pes2procs[key], max_width)

        # return channel mapping
        chan2prim = {}
        s = "{}Channels:\n".format(s)
        for c in chans_list:
            chan2prim.update(
                {c.name: (self.channel_source(c).name, self.primitive(c).name)}
            )

        if len(chans_list) > 0:
            max_width = max(map(len, chan2prim))
            for key in sorted(chan2prim):
                s = "{0}    {1:{4}} {2} - {3}\n".format(
                    s, key, chan2prim[key][0], chan2prim[key][1], max_width
                )

        return s

    def to_coreDict(self):
        """Returns a dict where the Names of processing elements are the keys and
            mapped processes are the values
        :rtype dict[string, string]:
        """
        procs_list = self.graph.processes()
        pes_list = self.platform.processors()
        pes2procs = {}
        for pe in pes_list:
            pes2procs.update({pe.name: []})
        for proc in procs_list:
            pes2procs[self.affinity(proc).name].append(proc.name)
        return pes2procs

    def to_resourceDict(self):
        """Returns a dict where the types of processing elements are the keys and
           the values are the corresponding number of cores of that type which
           have processes mapped to them
        :rtype dict[string, int]:
        """
        resource_dict = {}
        # make sure that all core types are included in the dict
        counted_cores = []
        for core in self.platform.processors():
            if core.type not in resource_dict:
                resource_dict[core.type] = 0
        for proc in self.graph.processes():
            core = self.affinity(proc)
            if core.name in counted_cores:
                continue
            else:
                counted_cores.append(core.name)
                resource_dict[core.type] += 1
        return resource_dict

    def to_list(self, channels=False):
        """Convert to a list (tuple), the simple vector representation.
        It is a list with processes as entries and PEs labeled
        from 0 to NUM_PES"""

        # initialize lists for numbers
        procs_list = self.graph.processes()
        chans_list = self.graph.channels()
        pes_list = self.platform.processors()
        prim_list = self.platform.primitives()

        # map PEs to an integer in alphabetic order
        pes = {}
        pe_names = sorted([pe.name for pe in pes_list])
        for i, pe in enumerate(pe_names):
            pes[pe] = i
        res = []

        # add one result entry for each process mapping
        for proc in sorted(procs_list, key=(lambda p: p.name)):
            res.append(pes[self.affinity(proc).name])

        # if flag set,
        # add one result entry for each dataflow channel (multiple in case of
        # multiple reader channels)
        if channels:
            # map chans to an integer
            prims = {}
            prim_names = sorted([prim.name for prim in prim_list])
            for j, prim in enumerate(prim_names):
                prims[prim] = j + i
            for chan in sorted(chans_list, key=(lambda c: c.name)):
                prim = self.primitive(chan)
                res.append(prims[prim.name])

        return res

    def from_list(self, list_from):
        """
        Deprecated function. Corresponding mappers should be used instead,
        or from_list_random, which is explicit (in its name) in that it is
        non-deterministic.
        """
        log.warning(
            "Mapping.from_list is deprecated. Use either Mapping.from_list_random,"
            + "if determinism is not important. Better however is to use the classes"
            + "from the mocasin.mapper module."
        )

        return self.from_list_random(list_from)

    def from_list_random(self, list_from):
        """Convert from a list (tuple), the simple vector representation.
        Priority and policy chosen at random, and scheduler chosen randomly from the possible ones.
        If list has length # processes + # channels, then channels are chosen as the second part of the list.
        Otherwise, they are chosen at random.
        Note that this function assumes the input is sane.

        TODO: make it possible to give schedulers, too.
        TODO: check if we need to use correspondence of representation to ensure ordering is right
        """
        processors = sorted(
            list(self.platform.processors()), key=(lambda p: p.name)
        )
        all_schedulers = sorted(list(self.platform.schedulers()))
        all_primitives = sorted(
            list(self.platform.primitives()), key=(lambda p: p.name)
        )

        # map processes
        for i, p in enumerate(
            sorted(self.graph.processes(), key=(lambda p: p.name))
        ):
            idx = list_from[i]
            schedulers = [
                sched
                for sched in all_schedulers
                if processors[idx] in sched.processors
            ]
            j = random.randrange(0, len(schedulers))
            scheduler = schedulers[j]
            affinity = processors[idx]
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            self.add_process_info(p, info)
            log.debug(
                "map process %s to scheduler %s and processor %s "
                "(priority: %d)",
                p.name,
                scheduler.name,
                affinity.name,
                priority,
            )

        # map channels
        for i, c in enumerate(self.graph.channels(), start=i + 1):
            capacity = 16  # fixed channel bound this may cause problems
            suitable_primitives = []
            for p in all_primitives:
                src = self.process_info(c.source).affinity
                sinks = [self.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError(
                    "Mapping failed! No suitable primitive for "
                    "communication from %s to %s found!"
                    % (src.name, str(sinks))
                )
            if len(list_from) == len(self.graph.processes()):
                if len(suitable_primitives) == 1:
                    primitive = suitable_primitives[0]
                else:
                    idx = random.randrange(0, len(suitable_primitives) - 1)
                    primitive = suitable_primitives[idx]
            else:
                idx = list_from[i]
                primitive = all_primitives[idx]
                assert (
                    primitive in suitable_primitives
                ), f"error: insuitable primitive ({primitive.name}). Suitable: {[p.name for p in suitable_primitives]}"

            info = ChannelMappingInfo(primitive, capacity)
            self.add_channel_info(c, info)
            log.debug(
                "map channel %s to the primitive %s and bound to %d "
                "tokens" % (c.name, primitive.name, capacity)
            )

    def from_mapping(self, mapping):
        """
        Copy mapping

        TODO: implement this the proper way
        """
        self.from_list(mapping.to_list())

    def to_pydot(self, channels=True):
        """Convert the mapping to a dot graph

        The generated graph visualizes how a dataflow application is mapped
        to a platform.

        :returns: pydot object
        """
        dot = pydot.Dot(graph_type="digraph")

        processor_clusters = {}
        for s in self.platform.schedulers():
            cluster = pydot.Cluster("scheduler_" + s.name, label=s.name)
            dot.add_subgraph(cluster)
            for p in s.processors:
                p_cluster = pydot.Cluster("processor_" + p.name, label=p.name)
                p_cluster.add_node(pydot.Node("dummy_" + p.name, style="invis"))
                processor_clusters[p.name] = p_cluster
                cluster.add_subgraph(p_cluster)

        primitive_nodes = {}
        if channels:
            for p in self.platform.primitives():
                if p.name not in primitive_nodes:
                    node = pydot.Node("primitive_" + p.name, label=p.name)
                    dot.add_node(node)
                    primitive_nodes[p.name] = node

        process_nodes = {}
        for p in self.graph.processes():
            info = self._process_info[p.name]
            p_cluster = processor_clusters[info.affinity.name]
            node = pydot.Node("process_" + p.name, label=p.name)
            process_nodes[p.name] = node
            p_cluster.add_node(node)

        channel_nodes = {}
        if channels:
            for c in self.graph.channels():
                node = pydot.Node(
                    "channel_" + c.name, label=c.name, shape="diamond"
                )
                channel_nodes[c.name] = node
                dot.add_node(node)
                from_node = process_nodes[c.source.name]
                dot.add_edge(pydot.Edge(from_node, node, minlen=4))
                for p in c.sinks:
                    to_node = process_nodes[p.name]
                    dot.add_edge(pydot.Edge(node, to_node, minlen=4))
                info = self._channel_info[c.name]
                prim_node = primitive_nodes[info.primitive.name]
                dot.add_edge(
                    pydot.Edge(
                        node, prim_node, style="dashed", arrowhead="none"
                    )
                )

        return dot

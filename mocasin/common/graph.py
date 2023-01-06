# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import pydot
import logging

log = logging.getLogger(__name__)


class DataflowProcess(object):
    """Represents a dataflow process

    :ivar str name: name of the process
    :ivar outgoing_channels: list of dataflow channel the process writes to
    :type outgoing_channels: list[DataflowChannel]
    :ivar incoming_channels: list of dataflow channel the process reads from
    :type incoming_channels: list[DataflowChannel]
    """

    def __init__(self, name):
        """Initialize the dataflow process

        Sets the name and leaves the process unconnected
        """
        self.name = name
        self.outgoing_channels = []
        self.incoming_channels = []

    def connect_to_outgoing_channel(self, channel):
        """Connect the process to a outgoing channel

        This makes this process the source of the channel.

        :param DataflowChannel channel: the channel to connect to
        :raises RuntimeError: if the channel already has a source process
            assigned
        """
        if channel.source is not None:
            raise RuntimeError(
                "The channel %s is already connected to a " "source process!",
                channel.name,
            )
        channel.source = self
        self.outgoing_channels.append(channel)

    def connect_to_incomming_channel(self, channel):
        """Connect the process to a incomming channel

        This makes this process a sink of the channel.

        :param DataflowChannel channel: the channel to connect to
        """
        channel.sinks.append(self)
        self.incoming_channels.append(channel)


class DataflowChannel(object):
    """Represents a dataflow channel

    Each channel may have multiple sinks but only one source.

    :ivar str name: name of the channel
    :ivar source: the channel's source process
    :type source: DataflowProcess
    :ivar sinks: the channel's sink processes
    :type sinks: list[DataflowProcess]
    :ivar int token_size: size of one data token in byte
    """

    def __init__(self, name, token_size):
        """Initialize the channel.

        Sets the channel name and token size but leaves the channel
        unconnected.
        :param str name: name of the channel
        :param int token_size: size of one data token in byte
        """
        self.name = name
        self.source = None
        self.sinks = []
        self.token_size = token_size


class DataflowGraph(object):
    """Represents the DAG of a dataflow application.

    :ivar _processes: a dict of dataflow processes representing the graph's nodes
    :type _processes: dict[str, DataflowProcess]
    :ivar _channels: a dict of dataflow channels representing the graph's edges
    :type _channels: dict[str, DataflowChannel]
    """

    def __init__(self, name):
        """Create an empty graph"""
        self.name = name
        self._processes = {}
        self._channels = {}

    def find_process(self, name):
        """Search for a dataflow process by its name."""
        return self._processes[name]

    def find_channel(self, name, throw=False):
        """Search for a dataflow channel by its name."""
        return self._channels[name]

    def processes(self):
        return self._processes.values()

    def process_names(self):
        return list(self._processes.keys())

    def channels(self):
        return self._channels.values()

    def add_process(self, x):
        if x.name in self._processes:
            raise RuntimeError(
                "Process %s was already added to the graph" % (x.name)
            )
        self._processes[x.name] = x

    def add_channel(self, x):
        if x.name in self._channels:
            raise RuntimeError(
                "Channel %s was already added to the graph" % (x.name)
            )
        self._channels[x.name] = x

    def sort(self):
        """Sort process list in topological order"""
        if len(self.process_names()) == 0:
            return []
        if self.isCyclic():
            log.error(
                "ERROR: topological sort is only possible if graph is DAG"
            )

        WHITE = 0  # Not seen yet
        GRAY = 1  # Seen but not completed
        BLACK = 2  # Seen and completed
        colours = {n: WHITE for n in self.process_names()}
        nodes = []

        # The actual DFS
        def dfs(n):
            colours[n.name] = GRAY
            for channel in n.outgoing_channels:
                for ch in channel.sinks:
                    if colours[ch.name] == WHITE:
                        dfs(ch)
            colours[n.name] = BLACK
            nodes.append(n)

        # Do it from the root node first
        entry_nodes = list()
        for process in self.processes():
            if len(process.incoming_channels) == 0:
                entry_nodes.append(process)
        dfs(entry_nodes[0])

        # Then keep doing it while there are white nodes
        for n in colours:
            if colours[n] == WHITE:
                dfs(self.find_process(n))
        nodes.reverse()

        # get ordered channels
        channels = list()
        visited_nodes = list()
        for node in nodes:
            for v in visited_nodes:
                out_channels = self.find_process(v.name).outgoing_channels
                for ch in out_channels:
                    sink = ch.sinks[0]
                    if sink == node:
                        channels.append(ch)
            visited_nodes.append(node)

        return nodes, channels

    def isCyclic(self):
        """Check if graph is cyclic"""

        def isCyclicRec(currNode, path):
            if currNode in path:
                return True
            else:
                path.append(currNode)
                for ch in currNode.outgoing_channels:
                    node = ch.sinks[0]
                    if isCyclicRec(node, path):
                        return True
                    else:
                        path.remove(node)
            return False

        for node in self.processes():
            initPath = list()
            if isCyclicRec(node, initPath):
                return True
        return False

    def to_pydot(self, channels=True):
        """Convert the dataflow graph to a dot graph."""
        dot = pydot.Dot(graph_type="digraph")

        process_nodes = {}

        for p in self._processes.keys():
            node = pydot.Node("process_" + p, label=p)
            process_nodes[p] = node
            dot.add_node(node)

        if channels:
            for c in self._channels.values():
                src_node = process_nodes[c.source.name]
                for s in c.sinks:
                    sink_node = process_nodes[s.name]
                    dot.add_edge(pydot.Edge(src_node, sink_node, label=c.name))

        return dot

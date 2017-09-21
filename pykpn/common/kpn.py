# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import pydot


class KpnProcess(object):
    """Represents a KPN process

    :ivar str name: name of the process
    :ivar outgoing_channels: list of KPN channel the process writes to
    :type outgoing_channels: list[KpnChannel]
    :ivar incoming_channels: list of KPN channel the process reads from
    :type incoming_channels: list[KpnChannel]
    """

    def __init__(self, name):
        """Initialize the KPN process

        Sets the name and leaves the process unconnected
        """
        self.name = name
        self.outgoing_channels = []
        self.incoming_channels = []

    def connect_to_outgoing_channel(self, channel):
        """Connect the process to a outgoing channel

        This makes this process the source of the channel.

        :param KpnChannel channel: the channel to connect to
        :raises RuntimeError: if the channel already has a source process
            assigned
        """
        if channel.source is not None:
            raise RuntimeError('The channel %s is already connected to a '
                               'source process!', channel.name)
        channel.source = self
        self.outgoing_channels.append(channel)

    def connect_to_incomming_channel(self, channel):
        """Connect the process to a incomming channel

        This makes this process a sink of the channel.

        :param KpnChannel channel: the channel to connect to
        """
        channel.sinks.append(self)
        self.incoming_channels.append(channel)


class KpnChannel(object):
    """Represents a KPN channel

    Each channel may have multiple sinks but only one source.

    :ivar str name: name of the channel
    :ivar source: the channel's source process
    :type source: KpnProcess
    :ivar sinks: the channel's sink processes
    :type sinks: list[KpnProcess]
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


class KpnGraph(object):
    """Represents the DAG of a KPN application.

    :ivar processes: a list of KPN processes representing the graph's nodes
    :type processes: list[KpnProcess]
    :ivar channels: a list of KPN channels representing the graph's edges
    :type channels: list[KpnChannel]
    """

    def __init__(self):
        """Create an empty graph"""
        self.processes = []
        self.channels = []

    def find_process(self, name, throw=False):
        """Search for a KPN process by its name.

        :param str name: name of the process to be searched for
        :param bool throw: raise a RuntimeError if no process is
                           found (default: False)

        :raises RuntimeError: if no process was found and throw is True
        :returns: A KPN process object or None if no process was found.
        """
        for p in self.processes:
            if p.name == name:
                return p
        if throw:
            raise RuntimeError('The process %s is not part of the graph', name)
        return None

    def find_channel(self, name, throw=False):
        """Search for a KPN channel by its name.

        :param str name: name of the channel to be searched for
        :param bool throw: raise a RuntimeError if no channel is
                           found (default: False)

        :raises RuntimeError: if no channel was found and throw is True
        :returns: A KPN channel object or None if no channel was found.
        """
        for c in self.channels:
            if c.name == name:
                return c
        if throw:
            raise RuntimeError('The channel %s is not part of the graph', name)
        return None

    def to_pydot(self):
        """Convert the KPN graph to a dot graph."""
        dot = pydot.Dot(graph_type='digraph')

        process_nodes = {}

        for p in self.processes:
            node = pydot.Node('process_' + p.name, label=p.name)
            process_nodes[p.name] = node
            dot.add_node(node)

        for c in self.channels:
            src_node = process_nodes[c.source.name]
            for s in c.sinks:
                sink_node = process_nodes[s.name]
                dot.add_edge(pydot.Edge(src_node, sink_node, label=c.name))

        return dot

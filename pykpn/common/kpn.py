# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


class KpnProcess(object):

    def __init__(self, name):
        self.name = name
        self.outgoing_channels = []
        self.incoming_channels = []

    def connect_to_outgoing_channel(self, channel):
        if channel.source is not None:
            raise RuntimeError('The channel %s is already connected to a '
                               'source process!', channel.name)
        channel.source = self
        self.outgoing_channels.append(channel)

    def connect_to_incomming_channel(self, channel):
        channel.sinks.append(self)
        self.incoming_channels.append(channel)


class KpnChannel(object):

    def __init__(self, name, token_size):
        self.name = name
        self.source = None
        self.sinks = []
        self.token_size = token_size


class KpnGraph(object):

    def __init__(self):
        self.processes = []
        self.channels = []

    def find_process(self, name, throw=False):


        for p in self.processes:
            if p.name == name:
                return p
        if throw:
            raise RuntimeError('The process %s is not part of the graph', name)
        return None

    def find_channel(self, name, throw=False):
        for c in self.channels:
            if c.name == name:
                return c
        if throw:
            raise RuntimeError('The channel %s is not part of the graph', name)
        return None

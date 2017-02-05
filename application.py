# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


class KpnProcess(object):

    def __init__(self, name):
        self.name = name
        self.outgoing_channels = []
        self.incoming_channels = []


class KpnChannel(object):

    def __init__(self, name, token_size):
        self.name = name
        self.from_process = None
        self.to_process = None
        self.token_size = None


class KpnApplication:
    processes = []
    channels = []

    def connectProcessToOutgoingChannel(self, process, channel):
        assert channel.from_process is None

        channel.from_process = process
        process.outgoing_channels.append(channel)

    def connectProcessToIncomingChannel(self, process, channel):
        assert channel.to_process is None

        channel.to_process = process
        process.incoming_channels.append(channel)

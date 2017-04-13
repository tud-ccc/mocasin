# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


class ProcessEntry(object):
    def __init__(self, cycles):
        self.cycles = cycles


class ReadEntry(object):
    def __init__(self, channel, tokens):
        self.channel = channel
        self.tokens = tokens


class WriteEntry(object):
    def __init__(self, channel, tokens):
        self.channel = channel
        self.tokens = tokens


class TerminateEntry(object):
    def __init__(self):
        pass


class TraceReader(object):
    def __init__(self, file):
        self.file = file

    def getNextEntry(self):
        # TODO Implement a default trace reader
        return None

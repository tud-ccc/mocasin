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
    def __init__(self, process_name, app_name):
        self.type = None
        self.process_name = process_name
        self.app_name = app_name

    """
    Sets the type of the processor the process is running on.

    This information is essential for most trace readers. However, it is not
    known when on object initialization. Therefore, the type needs to be set
    after initialization and before the first trace entry is read.
    """
    def setProcessorType(self, type):
        # the type may only be set once, changing the type during simulation
        # (migrating to another core of another type) is not possible (yet!)
        if (self.type is not None and self.type != type):
            raise RuntimeError('Reassigning a process to a processor of ' +
                               'another type is not supported!')
        else:
            self.type = type

    def getNextEntry(self):
        # TODO Implement a default trace reader
        return None

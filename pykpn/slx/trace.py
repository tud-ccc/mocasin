# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from ..common import TraceReader
from ..common import ProcessEntry
from ..common import ReadEntry
from ..common import WriteEntry
from ..common import TerminateEntry


class SlxTraceReader(TraceReader):

    def __init__(self, process_name, app_name, trace_dir):
        super().__init__(process_name, app_name)
        self.trace_dir = trace_dir
        self.trace = None
        self.buffer = None

    def getNextEntry(self):
        if self.trace is None:  # first read, need to open trace file
            assert(self.type is not None)
            self.trace = open('%s/%s.%s.cpntrace' % (self.trace_dir,
                                                     self.process_name,
                                                     self.type))
            assert(self.trace is not None)

        if self.buffer is not None:
            tmp = self.buffer
            self.buffer = None
            return tmp

        traceline = self.trace.readline().split(' ')

        if traceline[0] == 'm':
            return ProcessEntry(int(traceline[2]))
        elif traceline[0] == 'r':
            self.buffer = ReadEntry(self.app_name + '.' + traceline[1],
                                    int(traceline[3]))
            return ProcessEntry(int(traceline[4]))
        elif traceline[0] == 'w':
            self.buffer = WriteEntry(self.app_name + '.' + traceline[1],
                                     int(traceline[2]))
            return ProcessEntry(int(traceline[3]))
        elif traceline[0] == 'e':
            return TerminateEntry()
        else:
            raise RuntimeError('Unexpected trace entry ' + traceline[0])

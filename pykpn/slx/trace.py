# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import os

from common import TraceReader
from common import ProcessEntry
from common import ReadEntry
from common import WriteEntry
from common import TerminateEntry


class SlxTraceReader(TraceReader):

    def __init__(self, traceDir, process, processor):
        file = os.path.join(traceDir, process + '.' + processor.type +
                            '.cpntrace')
        self.trace = open(file, 'r')
        assert self.trace is not None

        self.buffer = None

    def getNextEntry(self):
        if self.buffer is not None:
            tmp = self.buffer
            self.buffer = None
            return tmp

        traceline = self.trace.readline().split(' ')

        if traceline[0] == 'm':
            return ProcessEntry(int(traceline[2]))
        elif traceline[0] == 'r':
            self.buffer = ReadEntry(traceline[1], int(traceline[3]))
            return ProcessEntry(int(traceline[4]))
        elif traceline[0] == 'w':
            self.buffer = WriteEntry(traceline[1], int(traceline[2]))
            return ProcessEntry(int(traceline[3]))
        elif traceline[0] == 'e':
            return TerminateEntry()
        else:
            raise RuntimeError('Unexpected trace entry ' + traceline[0])

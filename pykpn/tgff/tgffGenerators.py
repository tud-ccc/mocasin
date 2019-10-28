# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.trace import TraceGenerator, TraceSegment
    
class tgffTraceGenerator(TraceGenerator):
    def __init__(self, peDict, processDict, repetition=1):
        self._peDict = peDict
        self._repetition = repetition
        self._processes = {}
        self._initializeProcessDict(processDict)
        
    def next_segment(self, process_name, processor_type):
        return
    
    def _initializeProcessDict(self, processDict):
        for process in processDict:
            pass
    
    
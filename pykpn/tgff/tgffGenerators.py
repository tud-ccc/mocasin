# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.trace import TraceGenerator, TraceSegment
    
class TgffTraceGenerator(TraceGenerator):
    def __init__(self, processor_dict, tgff_graph, repetition=1):
        self._processor_dict = processor_dict
        self._repetition = repetition
        self._trace_dict = {}
        self._initialize_trace_dict(tgff_graph)
        
    def next_segment(self, process_name, processor_type):
        if not process_name in self._trace_dict:
            raise RuntimeError("Unknown specified process!")
        
        if not processor_type in self._processor_dict:
            raise RuntimeError("Unknown specified processor")
    
        processor = self._processor_dict[processor_type]
        process = self._trace_dict[process_name]
        segment = TraceSegment()
        
        if process[0] == 0:
            segment.terminate = True
        else:
            if process[1] == len(process[2]):
                process[0] -= 1
                process[1] = 0
                return self.next_segment(process_name, processor_type)
            else:
                trace_parameter = process[2][process[1]]
                
                if trace_parameter[0] == 'r':
                    segment.n_tokens = 1
                    segment.read_from_channel = trace_parameter[1]
                elif trace_parameter[0] == 'e':
                    segment.processing_cycles = processor.getOperation(trace_parameter[1])
                elif trace_parameter[0] == 'w':
                    segment.n_tokens = 1
                    segment.write_to_channel = trace_parameter[1]
                
                process[1] += 1                
        
        return segment
    
    def _initialize_trace_dict(self, tgff_graph):
        for task in tgff_graph.tasks:
            self._trace_dict.update({task : [self._repetition, 0, tgff_graph.getExecutionOrder(task)]})
            
    
    
# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.trace import TraceGenerator, TraceSegment
 
class TgffTraceGenerator(TraceGenerator):
    """A trace generator based on the tgff representation.
    """
    
    def __init__(self, processor_list, tgff_graph, repetition=1):
        """ Initializes the generator
    
        :param processor_list: a list of all processors a
                                trace is available for.
        :type processor_list: list[TgffProcessor]
        :param tgff_graphs: A dictionary of TgffGraphs for which 
                            traces should be yielded.
        :type tgff_graphs: dict{string : TgffGraph}
        :param repetition: The amount of times the process is
                            executed before it terminates.
        """
        self._processor_list = processor_list
        self._repetition = repetition
        self._trace_dict = {}
        self._tgff_graph = tgff_graph
        for graph in tgff_graph.values():
            self._initialize_trace_dict(graph)
    
    def next_segment(self, process_name, processor_type):
        """Returns the next trace segment
        
        :param process_name: the name of the specific process 
        :type process_name: string
        :param processor_type: the name of the executing processor
        :type processor_type: string
        """
        
        if not process_name in self._trace_dict:
            raise RuntimeError("Unknown specified process!")
        
        #if not processor_type < len(self._processor_list) and processor_type >= 0:
            #raise RuntimeError("Unknown specified processor")
    
        processor = self._processor_list[processor_type]
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
                    segment.processing_cycles = processor.get_operation(trace_parameter[1])
                elif trace_parameter[0] == 'w':
                    segment.n_tokens = 1
                    segment.write_to_channel = trace_parameter[1]
                
                process[1] += 1                
        
        return segment
    
    def reset(self):
        """Resets the generator.
        
        This method resets the generator to its initial state. 
        Therefore it is not needed to instantiate a new generator
        if a trace has to be calculated twice.
        """
        self._trace_dict = {}
        for graph in self._tgff_graph.values():
            self._initialize_trace_dict(graph)
        
    
    def _initialize_trace_dict(self, tgff_graph):
        """Initializes an internal structure to keep track 
        of the current status for each trace.
        """
        for task in tgff_graph.tasks:
            self._trace_dict.update({tgff_graph.identifier+"."+task : [self._repetition, 0, tgff_graph.get_execution_order(task)]})
            
    
    
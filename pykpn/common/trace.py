# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Felix Teweleit

import networkx as nx
from enum import Enum

class TraceSegment(object):
    """Represents a segment in a process' execution trace

    :ivar processing_cycles:
        Duration (in cycles) of a processing segment. None if the segment does
        not contain any computations.
    :type processing_cycles: int or None
    :ivar read_from_channel:
        Name of the channel to read from at the end of the segment (after
        processing). None if no read access is to be performed. If not None,
        write_to_channel must be None.
    :type read_from_channel: str or None
    :ivar write_to_channel:
        Name of the channel to write to at the end of the segment (after
        processing). None if no write access is to be performed. If not None,
        read_from_channel must be None.
    :type write_to_channel: str or None
    :ivar n_tokens:
        Number of tokens to be read from or written to a channel. None if
        neither a write access nor a read access is to be performed at the end
        of the segment.
    :type n_tokens: int or None
    :ivar bool terminate:
        If True, this is the last segment of the execution trace.
    """

    def __init__(self):
        """Initialize a neutral (does not do anything) tracs segment)"""
        self.processing_cycles = None
        self.read_from_channel = None
        self.write_to_channel = None
        self.n_tokens = None
        self.terminate=False

    def sanity_check(self):
        """Perform a series of sanity checks on the object"""
        if (self.read_from_channel is not None and
            self.write_to_channel is not None):
            raise RuntimeError('A trace segment may not contain both a read '
                               'and a write access')
        if (self.n_tokens is None and (self.read_from_channel is not None or
                                       self.write_to_channel is not None)):
            raise RuntimeError('Trace segments contains a channel access but '
                               'the number of tokens is not specified!')


class TraceGenerator(object):
    """Creates trace segments

    This class is intended as a base class. A superclass could extend the
    functionality by generating random traces or reading traces from a file.
    """

    def next_segment(self, process_name, processor_type):
        """Return the next trace segment.

        Returns the next trace segment for a process running on a processor of
        the specified type (the segments could differ for different processor
        types). This should be overridden by a subclass. The default behaviuour
        is to return None

        :param str process_name:
            name of the process that a segment is requested for
        :param str processor_type:
            the processor type that a segment is requested for
        :returns: the next trace segment or None if there is none
        :rtype: TraceSegment or None
        """
        return None
 

class EdgeType(Enum):
    SEQUENTIAL_ORDER = 1
    READ_AFTER_COMPUTE = 2
    BLOCK_READ = 3
    UNBLOCK_READ = 4
    BLOCK_WRITE = 5
    ROOT_OR_LEAF = 6

   
class TraceGraph(nx.DiGraph):
    """
    """
    def __init__(self, kpn, trace_generator, processor_type):
        super(TraceGraph, self).__init__()
        self.add_nodes_from(["V_e", "V_s"])
        
        #captures the read and write accesses for each channel
        channel_dict = {}
        for channel in kpn.channels():
            channel_dict.update({channel.name : [0,0]})
        
        #captures the amount of executed segments and the last segment
        process_dict = {}
        for process in kpn.processes():
            process_dict.update({process.name : [0, None]})
            
        #Generate full trace for all processes
        all_terminated = False
        while not all_terminated:
            all_terminated = True
            
            for process_name in process_dict:
                try:
                    current_segment = trace_generator.next_segment(process_name, processor_type)
                except AttributeError:
                    continue
                last_segment_index = process_dict[process_name][0]
                last_segment = process_dict[process_name][1]
                
                process_dict[process_name][1] = current_segment
                
                if not current_segment.terminate:
                    all_terminated = False
                else:
                    continue
                
                
                if last_segment_index == 0:
                    #Adding dependencies from start node
                    self.add_edges_from([("V_s", "{}_1".format(process_name))], type=EdgeType.ROOT_OR_LEAF)
                else:
                    #Adding sequential order dependencies
                    self.add_edges_from([("{}_{}".format(process_name, last_segment_index),
                                          "{}_{}".format(process_name, last_segment_index+1))],
                                          type=EdgeType.SEQUENTIAL_ORDER)
                    
                process_dict[process_name][0] += 1

                #Adding unblock read dependencies
                if not last_segment == None and not last_segment.write_to_channel is None:
                    name = last_segment.write_to_channel
                        
                    self.add_edges_from([("r_{}_{}".format(name, channel_dict[name][1]-1),
                                    "{}_{}".format(process_name, last_segment_index+1))],
                                    type=EdgeType.UNBLOCK_READ)
                 
                #Adding block read dependencies
                if not current_segment.write_to_channel is None:
                    name = current_segment.write_to_channel
                    self.add_edges_from([("{}_{}".format(process_name, last_segment_index+1),
                                          "r_{}_{}".format(name, channel_dict[name][1]))],
                                          type=EdgeType.BLOCK_READ)
                    channel_dict[name][1] += 1
                
                #Adding read after compute dependencies
                if not current_segment.read_from_channel is None:
                    name = current_segment.read_from_channel
                    self.add_edges_from([("{}_{}".format(process_name, last_segment_index+1),
                                          "r_{}_{}".format(name, channel_dict[name][0]))],
                                          type=EdgeType.READ_AFTER_COMPUTE)
                    channel_dict[name][0] += 1
        
        #Adding dependencies to final node
        for node in self.nodes:
            if list(self.successors(node)) == [] and not node == "V_e":
                self.add_edges_from([(node, "V_e")],
                                    type=EdgeType.ROOT_OR_LEAF)


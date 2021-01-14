# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Felix Teweleit, Andres Goens

import networkx as nx
from enum import Enum
from mocasin.util import logging
import random

log = logging.getLogger(__name__)

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

    def __init__(self, process_cycles=None, read_from_channel=None,
                 write_to_channel=None, n_tokens=None, terminate=False):
        """Initialize a trace segment)"""
        self.processing_cycles = process_cycles
        self.read_from_channel = read_from_channel
        self.write_to_channel = write_to_channel
        self.n_tokens = n_tokens
        self.terminate = terminate

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
        types). This should be overridden by a subclass. The default behavior
        is to return None

        :param str process_name:
            name of the process that a segment is requested for
        :param str processor_type:
            the processor type that a segment is requested for
        :returns: the next trace segment or None if there is none
        :rtype: TraceSegment or None
        """
        return None
    
    def reset(self):
        """Resets the generator.
        
        Resets the generator to its initial state. In this way we
        can avoid to instantiate a new generator in case a trace
        has to be calculated multiple times.
        
        Returns:
            None: By default. Nothing should be returned by the
                implementation of any subclass.
        """
        return None

class EmptyTraceGenerator(TraceGenerator):
    def next_segment(self, process_name, processor_type):
        log.warning("Generating traces from empty trace. Did you forget to specify a trace configuration?")
        return TraceSegment(terminate=True)

class RandomTraceGenerator(TraceGenerator):

    def __init__(self,expected_num_executions=1000,
                 min_cycles=100,max_cycles=10000):
        self.firings = {}
        self.max_firings = {}
        self.num_firings = {}
        #suggestion: give min/max cycles per processor type?
        #perhaps also per process_name?
        self.min_cycles = min_cycles
        self.max_cycles = max_cycles
        self.expected_num_executions = expected_num_executions

    def next_segment(self, process_name, processor_type):
        #This will not produce any read/write events currently.
        #This can't be fixed without having information about
        #the application. If the need arises, we can change it.
        #Otherwise we don't need to change the initalization
        #of the trace generator.
        if process_name not in self.firings:
            sigma = 0.1 * self.expected_num_executions
            final = random.gauss(self.expected_num_executions,sigma)
            total = round(final)
            self.firings[process_name] = []
            self.num_firings[process_name] = 0
            self.max_firings[process_name] = total
            for i in range(total):
                exec_cycles = random.randint(self.min_cycles, self.max_cycles)
                self.firings[process_name].append(exec_cycles)
            log.info(f"Random trace for {process_name}: {final} executions.")

        exec_cycles = self.firings[process_name][self.num_firings[process_name]]
        log.debug(f"firing {process_name} for {exec_cycles} cycles.")
        self.num_firings[process_name] += 1
        if self.num_firings[process_name] == self.max_firings[process_name]:
            return TraceSegment(process_cycles=exec_cycles,terminate=True)
        elif self.num_firings[process_name] < self.max_firings[process_name]:
            return TraceSegment(process_cycles=exec_cycles)
        else:
            raise RuntimeError("Getting a segment from finished trace.")


    def reset(self,seed=None):
        if seed is not None:
            random.seed(seed)
        for proc in self.num_firings:
            self.num_firings[proc] = 0


# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from ..common import TraceGenerator
from ..common import TraceSegment


class SlxTraceReader(TraceGenerator):
    """A TraceGenerator that reads SLX trace files"""

    def __init__(self, trace_dir):
        """Initialize the trace reader

        :param str trace_dir: path to the directory containing all trace files
        """
        self._trace_dir = trace_dir

        self._trace_files = {}
        self._processor_types = {}

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
        if processor_type not in self._trace_files:
            fh = open('%s/%s.%s.cpntrace' % (self._trace_dir,
                                             process_name,
                                             processor_type))
            assert fh is not None
            self._trace_files[process_name] = fh
            self._processor_types[process_name] = processor_type
        else:
            fh = self._trace_files[process_name]

        if self._processor_types[process_name] != processor_type:
            raise RuntimeError('The SlxTraceReader does not support migration '
                               'of processes from one type of processor to '
                               'another!')

        traceline = self.trace.readline().split(' ')

        segment = TraceSegment()

        if traceline[0] == 'm':
            segment.processing_cycles = int(traceline[2])
        elif traceline[0] == 'r':
            segment.processing_cycles = int(traceline[4])
            segment.read_from_channel = traceline[1]
            segment.n_tokens = int(traceline[3])
        elif traceline[0] == 'w':
            segment.processing_cycles = int(traceline[3])
            segment.write_to_channel = traceline[1]
            segment.n_tokens = int(traceline[2])
        elif traceline[0] == 'e':
            segment.terminate = True
        else:
            raise RuntimeError('Unexpected trace entry ' + traceline[0])

        return segment

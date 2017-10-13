# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pykpn.common.trace import TraceGenerator, TraceSegment


class SlxTraceReader(TraceGenerator):
    """Base class for SLX trace generators"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def factory(trace_dir, prefix, version):
        """Factory method.

        Create a SlxTraceReader object according to version.

        :param str trace_dir: path to the directory containing all trace files
        :param str prefix: the prefix that is used for channel and process
            names
        :param str version: slx version
        """
        if version == '2017.04':
            return SlxTraceReader_2017_04(trace_dir, prefix)
        else:
            raise NotImplementedError(
                'The slx trace reader does not support version %s' % version)


class SlxTraceReader_2017_04(TraceGenerator):
    """A TraceGenerator that reads SLX 2017.04 trace files"""

    def __init__(self, trace_dir, prefix):
        """Initialize the trace reader

        :param str trace_dir: path to the directory containing all trace files
        :param str prefix: the prefix that is used for channel and process
            names
        """
        self._trace_dir = trace_dir

        self._trace_files = {}
        self._processor_types = {}
        self._prefix = prefix

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
        assert process_name.startswith(self._prefix)
        if process_name not in self._trace_files:
            fh = open('%s/%s.%s.cpntrace' % (self._trace_dir,
                                             process_name[len(self._prefix):],
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

        traceline = fh.readline().split(' ')
        segment = TraceSegment()

        if traceline[0] == 'm':
            segment.processing_cycles = int(traceline[2])
        elif traceline[0] == 'r':
            segment.processing_cycles = int(traceline[4])
            segment.read_from_channel = self._prefix + traceline[1]
            segment.n_tokens = int(traceline[3])
        elif traceline[0] == 'w':
            segment.processing_cycles = int(traceline[3])
            segment.write_to_channel = self._prefix + traceline[1]
            segment.n_tokens = int(traceline[2])
        elif traceline[0] == 'e':
            segment.terminate = True
        else:
            raise RuntimeError('Unexpected trace entry ' + traceline[0])

        return segment

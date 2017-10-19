# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import glob

from pykpn import slx
from pykpn.common import logging
from pykpn.common.trace import TraceGenerator, TraceSegment


log = logging.getLogger(__name__)


class SlxTraceReader(TraceGenerator):
    """Base class for SLX trace generators"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def factory(trace_dir, prefix):
        """Factory method.

        Create a SlxTraceReader object according to version.

        :param str trace_dir: path to the directory containing all trace files
        :param str prefix: the prefix that is used for channel and process
            names
        """
        version = slx.get_version()

        if version == '2017.04':
            return SlxTraceReader_2017_04(trace_dir, prefix)
        elif version == '2017.10':
            return SlxTraceReader_2017_10(trace_dir, prefix)
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

    def _open_trace_file(self, process_name, processor_type):
        assert process_name.startswith(self._prefix)
        return open('%s/%s.%s.cpntrace' % (self._trace_dir,
                                           process_name[len(self._prefix):],
                                           processor_type))

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
        if process_name not in self._trace_files:
            fh = self._open_trace_file(process_name, processor_type)
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
            # this was the last entry, thus we can and should close the file
            fh.close()
        else:
            raise RuntimeError('Unexpected trace entry ' + traceline[0])

        return segment


class SlxTraceReader_2017_10(SlxTraceReader_2017_04):
    """A TraceGenerator that reads SLX 2017.10 trace files"""

    def __init__(self, trace_dir, prefix):
        """Initialize the trace reader

        :param str trace_dir: path to the directory containing all trace files
        :param str prefix: the prefix that is used for channel and process
            names
        """
        super().__init__(trace_dir, prefix)

    def _open_trace_file(self, process_name, processor_type):
        assert process_name.startswith(self._prefix)
        trace_files = glob.glob('%s/%s.%s.*.cpntrace' % (
            self._trace_dir,
            process_name[len(self._prefix):],
            processor_type))

        if len(trace_files) == 0:
            raise RuntimeError(
                'No trace file for process %s on processor type %s found' % (
                    process_name, processor_type))
        elif len(trace_files) > 1:
            log.warn('More than one trace file found for process %s on '
                     'processor type %s. -> Choose %s' % (
                         process_name, processor_type, trace_files[0]))

        return open(trace_files[0])

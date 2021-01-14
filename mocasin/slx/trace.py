# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import glob

from mocasin.util import logging
from mocasin.common.trace import TraceGenerator, TraceSegment


log = logging.getLogger(__name__)


class SlxTraceReader(TraceGenerator):
    """A TraceGenerator that reads SLX trace files"""

    def __init__(self, trace_dir):
        """Initialize the trace reader

        :param str trace_dir: path to the directory containing all trace files
        """
        self._trace_dir = trace_dir

        self._trace_files = {}
        self._processor_types = {}

    def _open_trace_file(self, process_name, processor_type):
        trace_files = glob.glob(
            "%s/%s.%s.*cpntrace"
            % (self._trace_dir, process_name, processor_type)
        )

        if len(trace_files) == 0:
            raise RuntimeError(
                "No trace file for process %s on processor type %s found"
                % (process_name, processor_type)
            )
        elif len(trace_files) > 1:
            log.warning(
                "More than one trace file found for process %s on "
                "processor type %s. -> Choose %s"
                % (process_name, processor_type, trace_files[0])
            )

        return open(trace_files[0])

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
        if process_name not in self._trace_files:
            fh = self._open_trace_file(process_name, processor_type)
            assert fh is not None
            self._trace_files[process_name] = fh
            self._processor_types[process_name] = processor_type
        else:
            fh = self._trace_files[process_name]

        if self._processor_types[process_name] != processor_type:
            raise RuntimeError(
                "The SlxTraceReader does not support migration "
                "of processes from one type of processor to "
                "another!"
            )

        traceline = fh.readline().split(" ")
        segment = TraceSegment()

        if traceline[0] == "m":
            segment.processing_cycles = int(traceline[2])
        elif traceline[0] == "r":
            segment.processing_cycles = int(traceline[4])
            segment.read_from_channel = traceline[1]
            segment.n_tokens = int(traceline[3])
        elif traceline[0] == "w":
            segment.processing_cycles = int(traceline[3])
            segment.write_to_channel = traceline[1]
            segment.n_tokens = int(traceline[2])
        elif traceline[0] == "e":
            segment.terminate = True
            # this was the last entry, thus we can and should close the file
            fh.close()
            self._trace_files[process_name] = None
        else:
            raise RuntimeError("Unexpected trace entry " + traceline[0])

        return segment

    def reset(self):
        """Resets the generator.

        This method resets the generator to its initial state.
        Therefore it is not needed to instantiate a new generator
        if a trace has to be calculated twice.
        """
        for fh in self._trace_files.values():
            if fh:
                fh.close()
        self._trace_files = {}
        self._processor_types = {}

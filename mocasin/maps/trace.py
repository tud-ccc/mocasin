# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import contextlib
import glob
import logging
import os

from hydra.utils import to_absolute_path

from mocasin.common.trace import (
    DataflowTrace,
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)


log = logging.getLogger(__name__)


class MapsTrace(DataflowTrace):
    """Represents the  behavior of a MAPS (KPN) application

    See `~DataflowTrace`.

    Args:
        trace_dir (str): path to the directory containing all trace files
    """

    def __init__(self, trace_dir):
        self._trace_dir = to_absolute_path(trace_dir)

    def get_trace(self, process):
        """Get the trace for a specific process/actor in the dataflow app

        Args:
            process (str): Name of the process to get a trace for

        Yields:
            ComputeSegment: if the next segment is a compute segment
            ReadTokenSegment: if the next segment is a read segment
            WriteTokenSegment: if the next segment is a write segment
        """

        # use an exit stack to keep track of all files we open
        with contextlib.ExitStack() as stack:
            # open all matching trace files for the different processor types
            processor_types, trace_files = self._open_trace_files(
                stack, process
            )

            # iterate over all the lines in all the files simultaneously
            for lines in zip(*trace_files):
                log.debug(f"reading next trace lines for process {process}")
                # check if we received enough lines
                if len(lines) != len(trace_files):
                    raise RuntimeError(
                        f"The trace files for process {process} do not match!"
                    )

                marker = self._get_element(lines, 0)

                if marker == "m":
                    yield ComputeSegment(
                        self._get_processor_cycles(processor_types, lines, 2)
                    )
                elif marker == "r":
                    yield ComputeSegment(
                        self._get_processor_cycles(processor_types, lines, 4)
                    )
                    yield ReadTokenSegment(
                        channel=self._get_element(lines, 1),
                        num_tokens=int(self._get_element(lines, 3)),
                    )
                elif marker == "w":
                    yield ComputeSegment(
                        self._get_processor_cycles(processor_types, lines, 3)
                    )
                    yield WriteTokenSegment(
                        channel=self._get_element(lines, 1),
                        num_tokens=int(self._get_element(lines, 2)),
                    )
                elif marker == "e":
                    return
                else:
                    raise RuntimeError("Encountered an unknown line marker!")

    def _open_trace_files(self, stack, process):
        # find all trace files for the given process
        trace_file_paths = glob.glob(
            os.path.join(self._trace_dir, f"{process}.*.*.cpntrace")
        )
        if len(trace_file_paths) == 0:
            # try again with old naming scheme
            trace_file_paths = glob.glob(
                os.path.join(self._trace_dir, f"{process}.*.cpntrace")
            )
        if len(trace_file_paths) == 0:
            raise RuntimeError(
                f"There is no trace file for the process {process}!"
            )

        # open all files
        trace_files = []
        processor_types = []
        for path in trace_file_paths:
            processor_types.append(os.path.basename(path).split(".")[1])
            trace_files.append(stack.enter_context(open(path)))

        return processor_types, trace_files

    def _get_processor_cycles(self, processor_types, lines, index):
        cycles = (int(line.split()[index]) for line in lines)
        processor_cycles = {t: c for t, c in zip(processor_types, cycles)}
        return processor_cycles

    def _get_element(self, lines, index):
        elements = {line.split()[index] for line in lines}
        if len(elements) != 1:
            raise RuntimeError("The trace files do not match!")
        return elements.pop()

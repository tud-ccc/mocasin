# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Felix Teweleit, Andres Goens

import copy
import enum
import logging

log = logging.getLogger(__name__)


@enum.unique
class SegmentType(enum.Enum):
    """Enum indicating different types of trace segments"""

    COMPUTE = 1
    READ_TOKEN = 2
    WRITE_TOKEN = 3


class _BaseSegment:
    """A segment in the execution trace of a process (or dataflow actor)

    This is a base class that is not intended for direct use.

    Args:
       segment_type (SegmentType): The type of the segment to be created
    """

    def __init__(self, segment_type):
        self._segment_type = segment_type = segment_type

    @property
    def segment_type(self):
        """Get the segment type

        Returns:
            SegmentType: type of this segment
        """
        return self._segment_type


class ComputeSegment(_BaseSegment):
    """A trace segment representing computation

    Args:
        process_cycles (dict of str: int): A mapping of processor types to the
            respective number of computation cycles for this segment.
    """

    def __init__(self, processor_cycles):
        super().__init__(SegmentType.COMPUTE)
        self._processor_cycles = processor_cycles

    @property
    def processor_cycles(self):
        """Get expected computation cycles for all supported processor types

        Returns:
            (dict of str: int): A mapping of processor types to the
                respective number of computation cycles for this segment.
        """
        return self._processor_cycles


class ReadTokenSegment(_BaseSegment):
    """A trace segment representing a read operation from a dataflow channel

    Args:
        channel (str): The channel to read from
        num_tokens (int): The number of data tokens to read
    """

    def __init__(self, channel, num_tokens):
        super().__init__(SegmentType.READ_TOKEN)
        self._channel = channel
        self._num_tokens = num_tokens

    @property
    def channel(self):
        """Get the channel to read from

        Returns:
            str: the channel to read from
        """
        return self._channel

    @property
    def num_tokens(self):
        """Get number of tokens to read from channel

        Returns:
            int: number of tokens
        """
        return self._num_tokens


class WriteTokenSegment(_BaseSegment):
    """A trace segment representing a write operation to a dataflow channel

    Args:
        channel (str): The channel to write to
        num_tokens (int): The number of data tokens to write
    """

    def __init__(self, channel, num_tokens):
        super().__init__(SegmentType.WRITE_TOKEN)
        self._channel = channel
        self._num_tokens = num_tokens

    @property
    def channel(self):
        """Get the channel to write to

        Returns:
            str: the channel to write to
        """
        return self._channel

    @property
    def num_tokens(self):
        """Get number of tokens to write to channel

        Returns:
            int: number of tokens
        """
        return self._num_tokens


class DataflowTrace:
    """Represents one possible behavior of a dataflow application

    Provides traces for each process in a dataflow application. A trace
    is a sequence of trace segments, where each segment is either a
    `~ComputeSegment`, a `~ReadTokenSegment` or a `~WriteTokenSegment`.
    Thus a trace models the behavior of a trace as a sequence of compute, read
    and write operations.

    This class is intended as a base class. A superclass could extend the
    functionality by generating random trace segments or reading traces from a
    file.
    """

    def get_trace(self, process):
        """Get the trace for a specific process/actor in the dataflow app

        Args:
            process (str): Name of the process to get a trace for

        Yields:
            ComputeSegment: if the next segment is a compute segment
            ReadTokenSegment: if the next segment is a read segment
            WriteTokenSegment: if the next segment is a write segment
        """
        raise NotImplementedError(
            "get_trace() needs to be implemented by a superclass"
        )
        yield

    def accumulate_processor_cycles(self, process):
        """Calculate the total (accumulated) cycles of all compute segments

        Args:
            process (str): Name of the process to get accumulated cycles for

        Return
           (dict of str: int): A dict mapping processor types to the respective
                number of total computation cycles for the given process.
           None: If the trace for process does not contain any compute segments
        """
        trace = self.get_trace(process)

        # find all compute segments
        compute_segments = filter(
            lambda x: x.segment_type == SegmentType.COMPUTE, trace
        )

        # initialize acc_cycles with the cycles from the first compute segment
        try:
            acc_cycles = {}
            for k, v in next(compute_segments).processor_cycles.items():
                acc_cycles[k] = v
        except StopIteration:
            return None

        # iterate over the remaining compute segments while adding their
        # processor cycles to acc_cycles
        for s in compute_segments:
            for k, v in s.processor_cycles.items():
                acc_cycles[k] += v

        return acc_cycles


class EmptyTrace(DataflowTrace):
    """An empty application trace"""

    def get_trace(self, process):
        """Get an empty trace

        Args:
            process (str): Name of the process to get a trace for

        Yields: Nothing
        """
        log.warning(
            "Using empty trace. "
            "Did you forget to specify a trace configuration?"
        )
        return
        yield


# class RandomTraceGenerator(TraceGenerator):
#     def __init__(
#         self, expected_num_executions=1000, min_cycles=100, max_cycles=10000
#     ):
#         self.firings = {}
#         self.max_firings = {}
#         self.num_firings = {}
#         # suggestion: give min/max cycles per processor type?
#         # perhaps also per process_name?
#         self.min_cycles = min_cycles
#         self.max_cycles = max_cycles
#         self.expected_num_executions = expected_num_executions

#     def next_segment(self, process_name, processor_type):
#         # This will not produce any read/write events currently.
#         # This can't be fixed without having information about
#         # the application. If the need arises, we can change it.
#         # Otherwise we don't need to change the initalization
#         # of the trace generator.
#         if process_name not in self.firings:
#             sigma = 0.1 * self.expected_num_executions
#             final = random.gauss(self.expected_num_executions, sigma)
#             total = round(final)
#             self.firings[process_name] = []
#             self.num_firings[process_name] = 0
#             self.max_firings[process_name] = total
#             for i in range(total):
#                 exec_cycles = random.randint(self.min_cycles, self.max_cycles)
#                 self.firings[process_name].append(exec_cycles)
#             log.info(f"Random trace for {process_name}: {final} executions.")

#         exec_cycles = self.firings[process_name][self.num_firings[process_name]]
#         log.debug(f"firing {process_name} for {exec_cycles} cycles.")
#         self.num_firings[process_name] += 1
#         if self.num_firings[process_name] == self.max_firings[process_name]:
#             return TraceSegment(process_cycles=exec_cycles, terminate=True)
#         elif self.num_firings[process_name] < self.max_firings[process_name]:
#             return TraceSegment(process_cycles=exec_cycles)
#         else:
#             raise RuntimeError("Getting a segment from finished trace.")

#     def reset(self, seed=None):
#         if seed is not None:
#             random.seed(seed)
#         for proc in self.num_firings:
#             self.num_firings[proc] = 0

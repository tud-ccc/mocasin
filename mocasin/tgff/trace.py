# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Christian Menard

from mocasin.common.trace import (
    DataflowTrace,
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)


class TgffTrace(DataflowTrace):
    """Represents the  behavior of an SDF3 application

    See `~DataflowTrace`.

    Args:
        processor_list (list of TgffProcessor): a list of all processors the
            trace should be generated for
        tgff_graph (TgffGraph): The tgff graph for which traces should be
            generated
        repetitions (int): number of iterations in which the complete graph is
            executed
    """

    def __init__(self, processor_list, tgff_graph, repetitions):
        self._processor_list = processor_list
        self._repetitions = repetitions
        self._tgff_graph = tgff_graph

    def get_trace(self, process):
        """Get the trace for a specific task in the TGFF graph

        Args:
            process (str): Name of the task to get a trace for

        Yields:
            ComputeSegment, ReadTokenSegment, or WriteTokenSegment: The next
                segment in the process trace
        """
        task_name = process

        if task_name not in self._tgff_graph.tasks:
            raise RuntimeError(f"Unknown task! ({process})")

        # prepare a dict of computation cycles for all processor types
        processor_cycles = {}
        for processor in self._processor_list.values():
            processor_cycles[processor.type] = processor.get_operation(
                self._tgff_graph.tasks[task_name]
            )

        # iterate over all repetitions
        for _ in range(0, self._repetitions):
            # First, the task reads from all input channels
            for channel_name, properties in self._tgff_graph.channels.items():
                # properties[1] is the name of the channel's sink task
                # FIXME: This mechanism should be simplified or the variable
                # named property
                if task_name == properties[1]:
                    yield ReadTokenSegment(channel=channel_name, num_tokens=1)

            # Then, it computes
            yield ComputeSegment(processor_cycles)

            # Finally, it writes to all output channels
            for channel_name, properties in self._tgff_graph.channels.items():
                # properties[0] is the name of the channel's source task
                # FIXME: This mechanism should be simplified or the variable
                # named property
                if task_name == properties[0]:
                    yield WriteTokenSegment(channel=channel_name, num_tokens=1)

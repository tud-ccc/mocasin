# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

from mocasin.common.trace import TraceGenerator, TraceSegment


class ExampleTraceGenerator(TraceGenerator):
    def __init__(self):
        super().__init__()

    def next_segment(self, process_name, processor_type):
        if process_name == "a":
            return TraceSegment(
                process_cycles=1000,
                write_to_channel="c",
                n_tokens=2,
                terminate=True,
            )
        elif process_name == "b":
            return TraceSegment(
                process_cycles=1000,
                read_from_channel="c",
                n_tokens=2,
                terminate=True,
            )
        else:
            raise RuntimeError(f"Unexpected process name ({process_name})")

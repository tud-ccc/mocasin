# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

from mocasin.common.trace import (
    DataflowTrace,
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)


class ExampleTrace(DataflowTrace):
    def get_trace(self, process):
        if process == "a":
            yield ComputeSegment(
                processor_cycles={"proc_type_0": 1200, "proc_type_1": 1000}
            )
            yield WriteTokenSegment(channel="c", num_tokens=2)
        elif process == "b":
            yield ComputeSegment(
                processor_cycles={"proc_type_0": 1200, "proc_type_1": 1000}
            )
            yield ReadTokenSegment(channel="c", num_tokens=2)
        else:
            raise RuntimeError(f"Unexpected process name ({process})")

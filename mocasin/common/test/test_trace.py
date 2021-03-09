# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

from mocasin.common.trace import (
    DataflowTrace,
    EmptyTrace,
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)


def test_empty_trace():
    empty = EmptyTrace()
    trace = empty.get_trace("foo")
    assert len(list(trace)) == 0


def test_empty_accumulate_processor_cycles():
    empty = EmptyTrace()
    assert empty.accumulate_processor_cycles("foo") is None


class TestTrace(DataflowTrace):
    def get_trace(self, process):
        if process == "foo":
            yield ReadTokenSegment(None, None)
            yield WriteTokenSegment(None, None)
        if process == "bar":
            yield ReadTokenSegment(None, None)
            yield ComputeSegment({"A": 100, "B": 1000})
            yield WriteTokenSegment(None, None)
            yield ComputeSegment({"A": 50, "B": 500})
            yield ComputeSegment({"A": 30, "B": 300})
            yield ReadTokenSegment(None, None)
            yield ComputeSegment({"A": 20, "B": 200})
            yield WriteTokenSegment(None, None)
        if process == "baz":
            yield ReadTokenSegment(None, None)
            yield ComputeSegment({"A": 100, "B": 1000})
            yield WriteTokenSegment(None, None)


def test_accumulate_processor_cycles():
    trace = TestTrace()

    assert trace.accumulate_processor_cycles("empty") is None
    assert trace.accumulate_processor_cycles("baz") == {"A": 100, "B": 1000}
    assert trace.accumulate_processor_cycles("bar") == {"A": 200, "B": 2000}

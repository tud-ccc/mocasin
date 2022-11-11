# Copyright (C) 2022 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Julian Robledo

import pytest
from mocasin.common.graph import (
    DataflowGraph,
    DataflowChannel,
    DataflowProcess,
)


@pytest.fixture
def graph_acyclic():
    k = DataflowGraph("graph")
    process_a = DataflowProcess("a")
    process_b = DataflowProcess("b")
    process_c = DataflowProcess("c")
    channel_1 = DataflowChannel("ch1", 1)
    channel_2 = DataflowChannel("ch2", 1)
    process_a.connect_to_outgoing_channel(channel_1)
    process_b.connect_to_incomming_channel(channel_1)
    process_b.connect_to_outgoing_channel(channel_2)
    process_c.connect_to_incomming_channel(channel_2)
    k.add_channel(channel_1)
    k.add_channel(channel_2)
    k.add_process(process_a)
    k.add_process(process_b)
    k.add_process(process_c)
    return k


def test_graph_sort(graph_acyclic):
    processes, channels = graph_acyclic.sort()
    assert len(processes) == 3
    assert len(channels) == 2
    a = processes[0].name
    b = processes[1].name
    c = processes[2].name
    assert a == "a"
    assert b == "b"
    assert c == "c"

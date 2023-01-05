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

@pytest.fixture
def graph_cyclic():
    k = DataflowGraph("graph")
    process_a = DataflowProcess("a")
    process_b = DataflowProcess("b")
    process_c = DataflowProcess("c")
    channel_1 = DataflowChannel("ch1", 1)
    channel_2 = DataflowChannel("ch2", 1)
    channel_3 = DataflowChannel("ch3", 1)
    process_a.connect_to_outgoing_channel(channel_1)
    process_b.connect_to_incomming_channel(channel_1)
    process_b.connect_to_outgoing_channel(channel_2)
    process_b.connect_to_outgoing_channel(channel_3)
    process_c.connect_to_incomming_channel(channel_2)
    process_a.connect_to_incomming_channel(channel_3)
    k.add_channel(channel_1)
    k.add_channel(channel_2)
    k.add_channel(channel_3)
    k.add_process(process_a)
    k.add_process(process_b)
    k.add_process(process_c)
    return k


@pytest.fixture
def graph_multiple_roots():
    k = DataflowGraph("graph")

    root_one = DataflowProcess("a")
    root_two = DataflowProcess("b")

    a_one = DataflowProcess("a1")
    a_two = DataflowProcess("a2")
    a_three = DataflowProcess("a3")

    channel_1 = DataflowChannel("ch1", 1)
    channel_2 = DataflowChannel("ch2", 1)
    channel_3 = DataflowChannel("ch3", 1)

    root_one.connect_to_outgoing_channel(channel_1)
    root_one.connect_to_outgoing_channel(channel_2)
    a_one.connect_to_incomming_channel(channel_1)
    a_two.connect_to_incomming_channel(channel_2)
    a_two.connect_to_outgoing_channel(channel_3)
    a_three.connect_to_incomming_channel(channel_3)

    k.add_channel(channel_1)
    k.add_channel(channel_2)
    k.add_channel(channel_3)

    k.add_process(root_one)
    k.add_process(root_two)
    k.add_process(a_one)
    k.add_process(a_two)
    k.add_process(a_three)

    return k


def test_graph_sort_for_multiple_roots(graph_multiple_roots):

    processes, channels = graph_multiple_roots.sort()

    process_names = []
    for proc in processes:
        process_names.append(proc.name)

    assert len(processes) == 5
    assert len(channels) == 3

    assert process_names.index("a1") > process_names.index("a")
    assert process_names.index("a2") > process_names.index("a")
    assert process_names.index("a3") > process_names.index("a2")


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

def test_graph_cyclic(graph_cyclic, graph_acyclic):
    is_cyclic = graph_cyclic.isCyclic()
    assert is_cyclic == True

    is_cyclic = graph_acyclic.isCyclic()
    assert is_cyclic == False
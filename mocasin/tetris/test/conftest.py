# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

import pytest

from mocasin.common.graph import DataflowChannel, DataflowGraph, DataflowProcess
from mocasin.common.platform import Platform, Processor, Scheduler
from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper
from mocasin.platforms.odroid import DesignerPlatformOdroid
from mocasin.platforms.platformDesigner import genericProcessor


@pytest.fixture
def platform():
    pe_little = genericProcessor("proc_type_0")
    pe_big = genericProcessor("proc_type_1")
    p = DesignerPlatformOdroid(pe_little, pe_big)
    return p


@pytest.fixture
def graph():
    k = DataflowGraph("graph")
    channel = DataflowChannel("ch", 1)
    k.add_channel(channel)
    process_a = DataflowProcess("a")
    process_a.connect_to_outgoing_channel(channel)
    process_b = DataflowProcess("b")
    process_b.connect_to_incomming_channel(channel)
    k.add_process(DataflowProcess("a"))
    k.add_process(DataflowProcess("b"))
    return k


@pytest.fixture
def mapping(graph, platform):
    com_mapper = ComFullMapper(graph, platform)
    mapper = ProcPartialMapper(graph, platform, com_mapper)
    from_list = []
    # Map process "a"
    from_list.append(0)
    # Map process "b"
    from_list.append(1)
    mapping = mapper.generate_mapping(from_list)
    return mapping


@pytest.fixture
def pareto_mappings(platform, graph):
    com_mapper = ComFullMapper(graph, platform)
    mapper = ProcPartialMapper(graph, platform, com_mapper)

    mapping_tuples = [
        ([0, 0], 10.2, 21.45),
        ([0, 3], 5.2, 31.15),
        ([0, 2], 9.7, 23.45),
        ([1, 1], 6.0, 35.45),
        ([1, 3], 4.32, 39.1),
    ]

    mappings = []

    for tup in mapping_tuples:
        mapping = mapper.generate_mapping(tup[0])
        mapping.metadata.exec_time = tup[1]
        mapping.metadata.energy = tup[2]
        mappings.append(mapping)

    return mappings

# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

import pytest

from mocasin.common.graph import DataflowChannel, DataflowProcess, DataflowGraph
from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper
from mocasin.platforms.odroid import DesignerPlatformOdroid
from mocasin.platforms.platformDesigner import genericProcessor
from mocasin.representations import SymmetryRepresentation


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


def test_allEquivalent(platform, graph):
    com_mapper = ComFullMapper(platform)
    mapper = ProcPartialMapper(graph, platform, com_mapper)
    mapping = mapper.generate_mapping([0, 1])

    representation = SymmetryRepresentation(graph, platform)
    assert len(list(representation.allEquivalent(mapping))) == 12
    assert (
        len(list(representation.allEquivalent(mapping, only_support=True))) == 6
    )
    representation = SymmetryRepresentation(graph, platform, disable_mpsym=True)
    assert len(list(representation.allEquivalent(mapping))) == 12
    assert (
        len(list(representation.allEquivalent(mapping, only_support=True))) == 6
    )

# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.common.graph import DataflowChannel, DataflowProcess, DataflowGraph
from mocasin.util.mapping_table_reader import MappingTableReader
from mocasin.platforms.platformDesigner import genericProcessor
from mocasin.platforms.odroid import DesignerPlatformOdroid

from pathlib import Path
import pytest


@pytest.fixture
def table_file():
    return Path(__file__).parent.absolute().joinpath("mapping_table.csv")


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
def platform():
    pe_little = genericProcessor("proc_type_0")
    pe_big = genericProcessor("proc_type_1")
    p = DesignerPlatformOdroid(pe_little, pe_big)
    return p


def test_mapping_table_reader(platform, graph, table_file):
    reader = MappingTableReader(
        platform, graph, table_file, attributes=["attribute1"]
    )
    mappings = reader.form_mappings()
    assert len(mappings) == 4
    assert mappings[0][0].to_list() == [0, 1]
    assert mappings[0][0].metadata.exec_time == 10.23
    assert mappings[0][0].metadata.energy == 24.43
    assert mappings[0][1] == "a"
    assert mappings[1][0].to_list() == [0, 0]
    assert mappings[1][0].metadata.exec_time == 14.43
    assert mappings[1][0].metadata.energy == 21.56
    assert mappings[1][1] == "b"
    assert mappings[2][0].to_list() == [4, 0]
    assert mappings[2][1] == "c"
    assert mappings[3][0].to_list() == [4, 7]

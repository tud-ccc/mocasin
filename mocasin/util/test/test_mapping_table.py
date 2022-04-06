# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.common.graph import DataflowChannel, DataflowProcess, DataflowGraph
from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper
from mocasin.platforms.odroid import DesignerPlatformOdroid
from mocasin.platforms.platformDesigner import genericProcessor
from mocasin.util.mapping_table import MappingTableReader, MappingTableWriter

import filecmp
from pathlib import Path
import pytest


@pytest.fixture
def table_file():
    return Path(__file__).parent.absolute().joinpath("mapping_table.csv")


@pytest.fixture
def expected_csv():
    return (
        Path(__file__).parent.absolute().joinpath("expected_mapping_table.csv")
    )


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


def num_resources(mapping):
    return len(mapping.get_used_processors())


def test_mapping_table_writer(platform, graph, tmpdir, expected_csv):
    output_file = Path(tmpdir).joinpath("output_table.csv")
    com_mapper = ComFullMapper(graph, platform)
    mapper = ProcPartialMapper(graph, platform, com_mapper)

    mapping1 = mapper.generate_mapping([0, 0])
    mapping1.metadata.exec_time = 10.2
    mapping1.metadata.energy = 21.45

    mapping2 = mapper.generate_mapping([0, 3])
    mapping2.metadata.exec_time = 5.2
    mapping2.metadata.energy = 31.15

    attributes = {"num_resources": num_resources}
    writer = MappingTableWriter(
        platform, graph, output_file, attributes=attributes
    )
    writer.open()
    writer.write_header()
    writer.write_mapping(mapping1)
    writer.write_mapping(mapping2)
    writer.close()
    assert filecmp.cmp(output_file, expected_csv, shallow=False)


def test_mapping_table_writer_with(platform, graph, tmpdir, expected_csv):
    output_file = Path(tmpdir).joinpath("output_table.csv")
    com_mapper = ComFullMapper(graph, platform)
    mapper = ProcPartialMapper(graph, platform, com_mapper)

    mapping1 = mapper.generate_mapping([0, 0])
    mapping1.metadata.exec_time = 10.2
    mapping1.metadata.energy = 21.45

    mapping2 = mapper.generate_mapping([0, 3])
    mapping2.metadata.exec_time = 5.2
    mapping2.metadata.energy = 31.15

    attributes = {"num_resources": num_resources}
    with MappingTableWriter(
        platform, graph, output_file, attributes=attributes
    ) as writer:
        writer.write_header()
        writer.write_mapping(mapping1)
        writer.write_mapping(mapping2)
    assert filecmp.cmp(output_file, expected_csv, shallow=False)

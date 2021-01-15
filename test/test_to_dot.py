# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import filecmp
import pytest
import subprocess
import os


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_maps_graph_to_dot(datadir, expected_dir, maps_graph):
    dot_file = "%s.dot" % maps_graph
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "graph_to_dot",
            "graph=%s" % maps_graph,
            "output_file=%s" % out_file,
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_maps_platform_to_dot(datadir, expected_dir, maps_platform):
    dot_file = "%s.dot" % maps_platform
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "platform_to_dot",
            "platform=%s" % maps_platform,
            "output_file=%s" % out_file,
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_maps_mapping_to_dot(datadir, expected_dir, maps_graph_platform_pair):
    graph, platform = maps_graph_platform_pair
    dot_file = "%s_on_%s.dot" % (graph, platform)
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "mapping_to_dot",
            "graph=%s" % graph,
            "platform=%s" % platform,
            "mapper=maps_default",
            "output_file=%s" % out_file,
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


def test_tgff_graph_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.graph.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "graph_to_dot",
            "graph=tgff_reader",
            "tgff.file=%s.tgff" % tgff,
            "output_file=%s" % out_file,
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


def test_tgff_platform_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.platform.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "platform_to_dot",
            "platform=designer_bus",
            "tgff.file=%s.tgff" % tgff,
            "output_file=%s" % out_file,
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


def test_tgff_mapping_to_dot(datadir, expected_dir, tgff):
    dot_file = "%s.mapping.dot" % tgff
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "mapping_to_dot",
            "platform=designer_bus",
            "graph=tgff_reader",
            "mapper=random",
            "mapper.random_seed=42",
            "tgff.file=%s.tgff" % tgff,
            "output_file=%s" % out_file,
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


def test_sdf3_graph_to_dot(datadir, expected_dir):
    dot_file = "sdf3_medium_cyclic.dot"
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "graph_to_dot",
            "graph=sdf3_reader",
            "sdf3.file=../../../sdf3/medium_cyclic.xml",
            f"output_file={out_file}",
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )

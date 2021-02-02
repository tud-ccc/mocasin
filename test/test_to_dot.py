# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import filecmp
import subprocess
import os


def test_tgff_graph_to_dot(datadir, expected_dir):
    dot_file = "auto-indust-cords.dot"
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "graph_to_dot",
            "graph=tgff_reader",
            "tgff.file=auto-indust-cords.tgff",
            "tgff.directory=tgff/e3s-0.9",
            f"output_file={out_file}",
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


def test_platform_to_dot(datadir, expected_dir, large_platform):
    dot_file = f"{large_platform}.dot"
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "platform_to_dot",
            "platform=generic_bus",
            "tgff.file=auto-indust-cords",
            "tgff.directory=tgff/e3s-0.9",
            f"output_file={out_file}",
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )


def test_tgff_mapping_to_dot(datadir, expected_dir):
    dot_file = "auto-indust-cords.mapping.dot"
    out_file = os.path.join(datadir, dot_file)
    subprocess.check_call(
        [
            "mocasin",
            "mapping_to_dot",
            "platform=generic_bus",
            "graph=tgff_reader",
            "mapper=random",
            "mapper.random_seed=42",
            "tgff.file=auto-indust-cords.tgff",
            "tgff.directory=tgff/e3s-0.9",
            f"output_file={out_file}",
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
            "sdf3.file=sdf3/medium_cyclic.xml",
            f"output_file={out_file}",
        ],
        cwd=datadir,
    )
    assert filecmp.cmp(
        os.path.join(expected_dir, dot_file), out_file, shallow=False
    )

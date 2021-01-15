# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import pytest
import subprocess
import os


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_generate_mapping_maps(datadir, maps_mapper, maps_graph, representation):
    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=%s" % maps_graph,
            "platform=exynos",
            "representation=%s" % representation,
            "mapper=%s" % maps_mapper,
            "outdir=../../../",
            "trace=maps_default",
        ],
        cwd=datadir,
    )

    try:
        file_path = os.path.join(datadir, "mapping.pickle")
        file = open(file_path, "r")
        file.close()
    except FileNotFoundError:
        assert False


def test_generate_mapping_tgff(
    datadir, tgff_mapper, designer_platform, tgff, representation
):
    tgff_dir = os.path.join(datadir, "tgff/e3s-0.9")
    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=tgff_reader",
            "platform=%s" % designer_platform,
            "mapper=%s" % tgff_mapper,
            "tgff.directory=%s" % tgff_dir,
            "tgff.file=%s.tgff" % tgff,
            "outdir=../../../",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )
    try:
        file_path = os.path.join(datadir, "best_time.txt")
        file = open(file_path, "r")
        file.close()
    except FileNotFoundError:
        assert False

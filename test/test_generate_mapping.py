# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import pytest
import subprocess
import os


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_generate_mapping_maps(
    datadir, maps_mapper, maps_graph, representation
):
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

    file_path = os.path.join(datadir, "mapping.pickle")
    assert os.path.isfile(file_path)


def test_generate_mapping_tgff(datadir, tgff_mapper, designer_platform, tgff):
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

    file_path = os.path.join(datadir, "best_time.txt")
    assert os.path.isfile(file_path)

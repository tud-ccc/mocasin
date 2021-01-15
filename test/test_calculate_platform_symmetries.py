# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import filecmp
import os
import pytest


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_calculate_platform_symmetries_maps(
    datadir, expected_dir, maps_platform, mpsym
):
    file_name = "%s.autgrp" % maps_platform
    out_file = os.path.join(datadir, file_name)

    if mpsym:
        file_name += ".json"
        out_file += ".json"

    subprocess.check_call(
        [
            "mocasin",
            "calculate_platform_symmetries",
            "platform=%s" % maps_platform,
            "out_file=%s" % out_file,
            "mpsym=%s" % str(mpsym),
        ],
        cwd=datadir,
    )
    if not mpsym:
        file_name += ".out"
        out_file += ".out"
    assert filecmp.cmp(
        os.path.join(expected_dir, file_name), out_file, shallow=False
    )


def test_calculate_platform_symmetries_designer(
    datadir, expected_dir, designer_platform_small, mpsym
):
    file_name = "%s.autgrp" % designer_platform_small
    out_file = os.path.join(datadir, file_name)

    if mpsym:
        file_name += ".json"
        out_file += ".json"

    subprocess.check_call(
        [
            "mocasin",
            "calculate_platform_symmetries",
            "platform=%s" % designer_platform_small,
            "out_file=%s" % out_file,
            "mpsym=%s" % str(mpsym),
        ],
        cwd=datadir,
    )

    if not mpsym:
        file_name += ".out"
        out_file += ".out"
    assert filecmp.cmp(
        os.path.join(expected_dir, file_name), out_file, shallow=False
    )

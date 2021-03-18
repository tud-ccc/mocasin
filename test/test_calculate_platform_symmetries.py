# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import filecmp
import os
import pytest

# this comparison test is broken, as it will reject correctly calculated symmetries e.g.
# if a different but still valid BSGS is chosen. This should be fixed in !62
@pytest.mark.xfail
@pytest.mark.parametrize("mpsym", [True, False])
def test_calculate_platform_symmetries(
    datadir, expected_dir, small_platform, mpsym
):
    sfx = "json" if mpsym else "out"
    file_name = f"{small_platform}.autgrp.{sfx}"
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(
        [
            "mocasin",
            "calculate_platform_symmetries",
            f"platform={small_platform}",
            f"out_file={out_file}",
            f"mpsym={str(mpsym)}",
        ],
        cwd=datadir,
    )

    assert filecmp.cmp(
        os.path.join(expected_dir, file_name), out_file, shallow=False
    )

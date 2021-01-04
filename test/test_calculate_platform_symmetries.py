# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import filecmp
import os

def test_calculate_platform_symmetries_slx(datadir, expected_dir, slx_platform, mpsym):
    file_name = "%s.autgrp" % slx_platform
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(["pykpn", "calculate_platform_symmetries",
                           "platform=%s" % slx_platform,
                           "out_file=%s" % out_file,
                           "mpsym=%s" % str(mpsym)],
                          cwd=datadir)
    if mpsym:
        file_name += ".json"
        out_file += ".json"
    else:
        file_name += ".out"
        out_file += ".out"
    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file,
                       shallow=False)

def test_calculate_platform_symmetries_designer(datadir, expected_dir, designer_platform_small, mpsym):
    file_name = "%s.autgrp" % designer_platform_small
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(["pykpn", "calculate_platform_symmetries",
                           "platform=%s" % designer_platform_small,
                           "out_file=%s" % out_file,
                           "mpsym=%s" % str(mpsym)],
                          cwd=datadir)

    if mpsym:
        file_name += ".json"
        out_file += ".json"
    else:
        file_name += ".out"
        out_file += ".out"
    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file,
                       shallow=False)


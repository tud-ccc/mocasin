# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import filecmp
import os

def test_platform_to_autgrp_slx(datadir, expected_dir, slx_platform):
    file_name = "%s.autgrp.out" % slx_platform
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(["pykpn", "platform_to_autgrp",
                           "platform=%s" % slx_platform,
                           "out_file=%s" % out_file],
                          cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file,
                       shallow=False)

def test_platform_to_autgrp_tgff(datadir, expected_dir, tgff):
    file_name = "%s.autgrp.out" % tgff
    tgff_directory = os.path.join(datadir, "tgff/e3s-0.9")
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(["pykpn", "platform_to_autgrp",
                           "platform=designer_bus",
                           "tgff.directory=%s" % tgff_directory,
                           "tgff.file=%s.tgff" % tgff,
                           "out_file=%s" % out_file],
                          cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file,
                       shallow=False)


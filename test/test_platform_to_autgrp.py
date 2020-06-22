# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import filecmp
import os

def test_platform_to_autgrp(datadir, expected_dir, slx_version, slx_platform):
    file_name = "%s_%s.autgrp.out" % (slx_platform, slx_version)
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(["pykpn", "platform_to_autgrp",
                           "platform=%s" % slx_platform,
                           "slx.version=%s" % slx_version,
                           "out_file=%s" % out_file],
                          cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file)



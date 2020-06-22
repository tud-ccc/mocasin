# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens, Felix Teweleit

import os
import subprocess
import filecmp
import pytest

#TODO: Add test for parallella. But something seems to not work atm

@pytest.mark.parametrize("platform", ["exynos", "multidsp"])
def test_enumerate_equivalent_exynos(datadir, expected_dir, platform):
    file_name = "equivalent_mappings_audio_filter_%s.txt" % platform
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(["pykpn", "enumerate_equivalent",
                           "kpn=audio_filter",
                           "platform=%s" % platform,
                           "mapping=slx_default",
                           "output_file=%s" % out_file],
                          cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file)


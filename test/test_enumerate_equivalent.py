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
                           "mapper=default",
                           "output_file=%s" % out_file],
                          cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, file_name), out_file)

def test_enumerate_equivalent_tgff(datadir, tgff):
    file_name = "mappings_%s.txt" % tgff
    out_file = os.path.join(datadir, file_name)
    tgff_directory = os.path.join(datadir, 'tgff/e3s-0.9')

    subprocess.check_call(["pykpn", "enumerate_equivalent",
                           "kpn=tgff_reader",
                           "platform=tgff_reader",
                           "tgff.directory=%s" % tgff_directory,
                           "tgff.file=%s.tgff" % tgff,
                           "mapper=random",
                           "output_file=%s" % out_file],
                          cwd=datadir)

    #Todo: compare with expected result after merge with gbm_mapper branch
    assert os.stat(os.path.join(datadir, out_file)).st_size > 0

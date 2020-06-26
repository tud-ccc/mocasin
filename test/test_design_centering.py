# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import os
import pytest

thresholds = {
    "audio_filter": {
        "exynos": "37.3 ms",
        "multidsp": "800 ms",
        "parallella": "280 ms",
    },
    "hog": {"exynos": "880 ms"},
    "speaker_recognition": {"exynos": "38.3 ms"},
}


def test_dc_slx(datadir, slx_kpn_platform_pair):
    kpn, platform, version = slx_kpn_platform_pair

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=%s" % kpn,
                           "platform=%s" % platform,
                           "trace=slx_default",
                           "out_dir=%s" % datadir,
                           "threshold=%s" % thresholds[kpn][platform]],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0

@pytest.mark.skip(reason="What is a reasonable threshold for this test?")
def test_dc_tgff(datadir, tgff):
    tgff_directory = os.path.join(datadir, 'tgff/e3s-0.9')

    subprocess.check_call(["pykpn", "design_centering",
                           "kpn=tgff_reader",
                           "platform=tgff_reader",
                           "trace=tgff_reader",
                           "tgff.directory=%s" % tgff_directory,
                           "tgff.file=%s.tgff" % tgff,
                           "out_dir=%s" % datadir,
                           "threshold=100 ms"],
                          cwd=datadir)

    #TODO: check if generated json is actually parsable
    assert os.stat(os.path.join(datadir, "dc_out.json")).st_size > 0


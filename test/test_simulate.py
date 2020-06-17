# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import pytest
import subprocess


@pytest.fixture
def slx_expected_sim_time(slx_kpn_platform_pair):
    kpn, platform = slx_kpn_platform_tuple
    expected = {
        "audio_filter": {"exynos": "19.841971309 ms",
                         "multidsp": "95.811217897 ms",
                         "parallella": "193.346008966 ms"},
        "hog": {"exynos": "520.331958848 ms"},
        "speaker_recognition": {"exynos": "22.637929077 ms"},
    }
    return expected[kpn][platform]


def test_slx_simulate(datadir, slx_kpn_platform_pair, slx_expected_sim_time):
    kpn, platform = slx_kpn_platform_pair
    res = subprocess.run(["pykpn", "simulate",
                          f"kpn={kpn}",
                          f"platform={platform}",
                          "mapping=slx_default",
                          "trace=slx_default"],
                         cwd=datadir,
                         check=True,
                         stdout=subprocess.PIPE)

    found_line = False
    stdout = res.stdout.decode()
    for line in stdout.split('\n'):
        if line.startswith("Total simulated time: "):
            time = line[22:]
            assert time == slx_expected_sim_time
            found_line = True

    assert found_line


def test_tgff_simulate(datadir, tgff):
    subprocess.check_call(["pykpn", "simulate",
                           "platform=tgff_reader",
                           "kpn=tgff_reader",
                           "trace=tgff_reader",
                           "mapping=random_mapping",
                           "log_level=DEBUG",
                           f"tgff.file={tgff}.tgff"],
                          cwd=datadir)
    # Cannot validate random mappings

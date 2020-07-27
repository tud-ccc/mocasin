# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import subprocess


slx_expected_sim_time = {
    "audio_filter": {"exynos": "19.844971309 ms",
                     "multidsp": "95.812060002 ms",
                     "parallella": "193.346008966 ms"},
    "hog": {"exynos": "521.000341428 ms"},
    "speaker_recognition": {"exynos": "22.650786219 ms"},
}


def test_slx_simulate(datadir, slx_kpn_platform_pair):
    kpn, platform = slx_kpn_platform_pair
    res = subprocess.run(["pykpn", "simulate",
                          f"kpn={kpn}",
                          f"platform={platform}",
                          "mapper=slx_default",
                          "trace=slx_default"],
                         cwd=datadir,
                         check=True,
                         stdout=subprocess.PIPE)

    found_line = False
    stdout = res.stdout.decode()
    for line in stdout.split('\n'):
        if line.startswith("Total simulated time: "):
            time = line[22:]
            assert time == slx_expected_sim_time[kpn][platform]
            found_line = True

    assert found_line


tgff_expected_sim_time = {
    "auto-indust-cords": "524.6655 ms",
    "auto-indust-cowls": "530.327 ms",
    "auto-indust-mocsyn": "524.6655 ms",
    "auto-indust-mocsyn-asic": "524.6655 ms",
    "consumer-cords": "16093.52 ms",
    "networking-cowls": "7.0 ms",
    "office-automation-mocsyn-asic": "2797.52 ms",
    "telecom-mocsyn": "369.631 ms",
}


def test_tgff_simulate(datadir, tgff):
    res = subprocess.run(["pykpn", "simulate",
                          "platform=tgff_reader",
                          "kpn=tgff_reader",
                          "trace=tgff_reader",
                          "mapper=random",
                          "mapper.random_seed=42",
                          f"tgff.file={tgff}.tgff"],
                         cwd=datadir,
                         check=True,
                         stdout=subprocess.PIPE)
    found_line = False
    stdout = res.stdout.decode()
    for line in stdout.split('\n'):
        if line.startswith("Total simulated time: "):
            time = line[22:]
            assert time == tgff_expected_sim_time[tgff]
            found_line = True

    assert found_line

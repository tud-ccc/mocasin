# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import pytest
import subprocess


maps_expected_sim_time = {
    "audio_filter": {
        "exynos": "19.844971309 ms",
        "multidsp": "95.812062675 ms",
        "parallella": "193.346008966 ms",
    },
    "hog": {"exynos": "506.852794637 ms"},
    "speaker_recognition": {"exynos": "22.650786172 ms"},
}


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_maps_simulate(datadir, maps_graph_platform_pair):
    graph, platform = maps_graph_platform_pair
    res = subprocess.run(
        [
            "mocasin",
            "simulate",
            f"graph={graph}",
            f"platform={platform}",
            "mapper=maps_default",
            "trace=maps_default",
        ],
        cwd=datadir,
        check=True,
        stdout=subprocess.PIPE,
    )

    found_line = False
    stdout = res.stdout.decode()
    for line in stdout.split("\n"):
        if line.startswith("Total simulated time: "):
            time = line[22:]
            assert time == maps_expected_sim_time[graph][platform]
            found_line = True

    assert found_line


tgff_expected_sim_time = {
    "auto-indust-cords": "524.0033275 ms",
    "auto-indust-cowls": "530.327 ms",
    "auto-indust-mocsyn": "524.6655 ms",
    "auto-indust-mocsyn-asic": "524.0033275 ms",
    "consumer-cords": "16093.52 ms",
    "networking-cowls": "7.0 ms",
    "office-automation-mocsyn-asic": "2797.52 ms",
    "telecom-mocsyn": "369.631 ms",
}


def test_tgff_simulate(datadir, tgff):
    res = subprocess.run(
        [
            "mocasin",
            "simulate",
            "platform=designer_bus",
            "graph=tgff_reader",
            "trace=tgff_reader",
            "mapper=default",
            f"tgff.file={tgff}.tgff",
        ],
        cwd=datadir,
        check=True,
        stdout=subprocess.PIPE,
    )
    found_line = False
    stdout = res.stdout.decode()
    for line in stdout.split("\n"):
        if line.startswith("Total simulated time: "):
            time = line[22:]
            assert time == tgff_expected_sim_time[tgff]
            found_line = True

    assert found_line


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_sdf3_simulate(datadir):
    res = subprocess.run(
        [
            "mocasin",
            "simulate",
            "platform=exynos",
            "graph=sdf3_reader",
            "trace=sdf3_reader",
            "mapper=static_cfs",
            "sdf3.file=../../../sdf3/medium_cyclic.xml",
        ],
        cwd=datadir,
        check=True,
        stdout=subprocess.PIPE,
    )
    found_line = False
    stdout = res.stdout.decode()
    for line in stdout.split("\n"):
        if line.startswith("Total simulated time: "):
            time = line[22:]
            assert time == "1.340782929 ms"
            found_line = True

    assert found_line

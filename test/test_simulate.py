# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import subprocess


def test_tgff_simulate(datadir, tgff):
    res = subprocess.run(
        [
            "mocasin",
            "simulate",
            "platform=generic_bus",
            "graph=tgff_reader",
            "trace=tgff_reader",
            "mapper=default",
            "tgff.file=auto-indust-cords.tgff",
            "tgff.directory=tgff/e3s-0.9",
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
            assert time == "524.0033275 ms"
            found_line = True

    assert found_line


def test_sdf3_simulate(datadir):
    res = subprocess.run(
        [
            "mocasin",
            "simulate",
            "platform=odroid",
            "graph=sdf3_reader",
            "trace=sdf3_reader",
            "mapper=static_cfs",
            "sdf3.file=sdf3/medium_cyclic.xml",
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
            assert time == "26.434296828 ms"
            found_line = True

    assert found_line

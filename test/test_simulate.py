# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import subprocess


def test_tgff_simulate(datadir):
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
    found_flags = 0x0
    stdout = res.stdout.decode()
    for line in stdout.split("\n"):
        if line.startswith("Total simulated time: "):
            value = line[22:]
            assert value == "24.900902367 ms"
            found_flags |= 0x1
        if line.startswith("Total energy consumption: "):
            value = line[26:]
            assert value == "76.139183427 mJ"
            found_flags |= 0x2
        if line.startswith("      ---  static energy: "):
            value = line[26:]
            assert value == "54.376100499 mJ"
            found_flags |= 0x4
        if line.startswith("      --- dynamic energy: "):
            value = line[26:]
            assert value == "21.763082928 mJ"
            found_flags |= 0x8
        if line.startswith("Average power: "):
            value = line[15:]
            assert value == "3.057688 W"
            found_flags |= 0x10

    assert found_flags == 0x1F

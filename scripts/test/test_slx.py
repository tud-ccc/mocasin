# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import filecmp
import os
import pytest

from scripts.slx.kpn_to_dot import main as kpn_to_dot
from scripts.slx.mapping_to_dot import main as mapping_to_dot
from scripts.slx.platform_to_dot import main as platform_to_dot
from scripts.slx.random_walk import main as random_walk
from scripts.slx.simulate import main as simulate


slx_versions = ["2017.04", "2017.10"]


@pytest.mark.parametrize("platform", ["exynos", "multidsp", "parallella"])
@pytest.mark.parametrize("version", slx_versions)
def test_platform_to_dot(datadir, platform, version):
    xml = datadir.join("%s.platform" % platform)
    dot = datadir.join("%s.dot" % platform)
    expected = datadir.join("%s.dot.expected" % platform)
    platform_to_dot([str(xml), str(dot), "--slx-version=%s" % version])
    assert filecmp.cmp(dot, expected)


@pytest.mark.parametrize("version", slx_versions)
def test_kpn_to_dot(datadir, version):
    xml = datadir.join("audio_filter.cpn.xml")
    dot = datadir.join("audio_filter.dot")
    expected = datadir.join("audio_filter.dot.expected")
    kpn_to_dot([str(xml), str(dot), "--slx-version=%s" % version])
    assert filecmp.cmp(dot, expected)


# XXX The tests below can currently not be run for parallella as it imports
#     another version of the SLX bindings then exynos and multidsp. As this
#     leads to a conflict the test would alway fail...

@pytest.mark.parametrize("platform, expected", [
    ("exynos", "19.841971309 ms"),
    ("multidsp", "95.811217897 ms"),
])
def test_simulate(capfd, datadir, platform, expected):
    os.chdir(datadir)
    simulate([str("%s.ini" % platform)])
    out, err = capfd.readouterr()
    assert out.split('\n')[-3] == "Total simulated time: %s" % expected


@pytest.mark.parametrize("platform", ["exynos", "multidsp"])
def test_mapping_to_dot(datadir, platform):
    kpn_xml = datadir.join("audio_filter.cpn.xml")
    platform_xml = datadir.join("%s.platform" % platform)
    mapping_xml = datadir.join("%s.mapping" % platform)
    dot = datadir.join("%s-mapping.dot" % platform)
    expected = datadir.join("%s-mapping.dot.expected" % platform)
    mapping_to_dot([str(kpn_xml),
                    str(platform_xml),
                    str(mapping_xml),
                    str(dot),
                    "--slx-version=2017.10"])
    assert filecmp.cmp(dot, expected)


@pytest.mark.parametrize("platform", ["exynos", "multidsp"])
@pytest.mark.parametrize("option", [None, "-d", "-V", "-p", "--export-all"])
def test_random_walk(mocker, datadir, platform, option):
    mocker.patch("matplotlib.pyplot.show")  # suppress plots
    os.chdir(datadir)
    out_dir = datadir.join("out")
    cmd = [str("%s.ini" % platform), str(out_dir), "-n 100"]
    if option is not None:
        cmd.append(option)
    random_walk(cmd)

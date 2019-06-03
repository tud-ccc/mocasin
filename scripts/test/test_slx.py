# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import filecmp
import os
import pytest

from scripts.slx.platform_to_dot import main as platform_to_dot
from scripts.slx.kpn_to_dot import main as kpn_to_dot
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


# XXX This Test can currently not be run for parallella as it imports another
#     version of the SLX bindings then exynos and multidsp. As this leads to a
#     conflict the test would alway fail...
@pytest.mark.parametrize("platform, expected", [
    ("exynos", "19.841971309 ms"),
    ("multidsp", "95.811217897 ms"),
])
def test_simulate(capfd, datadir, platform, expected):
    os.chdir(datadir)
    simulate([str("%s.ini" % platform)])
    out, err = capfd.readouterr()
    assert out.split('\n')[-3] == "Total simulated time: %s" % expected

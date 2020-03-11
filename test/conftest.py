# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import pytest
import os


@pytest.fixture
def datadir(tmpdir):
    """
    Fixture that prepares a data directory for running tests. The resulting
    directory contains symbolic links to the examples directory.
    """
    module_path = os.path.dirname(__file__)
    examples_path = os.path.join(module_path, "..", "examples")

    os.symlink(os.path.join(examples_path, "conf"),
               os.path.join(tmpdir, "conf"))
    os.symlink(os.path.join(examples_path, "slx"),
               os.path.join(tmpdir, "slx"))
    os.symlink(os.path.join(examples_path, "tgff"),
               os.path.join(tmpdir, "tgff"))

    return tmpdir


@pytest.fixture
def expected_dir(request):
    module_path = os.path.dirname(request.module.__file__)
    module_name, _ = os.path.splitext(os.path.basename(request.module.__file__))
    return os.path.join(module_path, "expected_%s" % module_name)


@pytest.fixture(params=["exynos", "multidsp", "parallella"])
def slx_platform(request):
    return request.param


@pytest.fixture(params=["audio_filter", "hog", "speaker_recognition"])
def slx_kpn(request):
    return request.param


@pytest.fixture(params=[("audio_filter", "exynos", "'2017.10'"),
                        ("audio_filter", "multidsp", "'2017.10'"),
                        ("audio_filter", "parallella", "'2017.04'"),
                        ("hog", "exynos", "'2017.04'"),
                        ("speaker_recognition", "exynos", "'2017.04'")])
def slx_kpn_platform_pair(request):
    return request.param


@pytest.fixture(params=["auto-indust-cords",
                        "auto-indust-cowls"])
def tgff(request):
    return request.param

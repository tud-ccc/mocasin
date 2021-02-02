# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Felix Teweleit, Andres Goens


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

    os.symlink(
        os.path.join(examples_path, "tgff"), os.path.join(tmpdir, "tgff")
    )
    os.symlink(
        os.path.join(examples_path, "sdf3"), os.path.join(tmpdir, "sdf3")
    )
    os.symlink(os.path.join(examples_path, "csv"), os.path.join(tmpdir, "csv"))
    os.symlink(
        os.path.join(examples_path, "platform"),
        os.path.join(tmpdir, "platform"),
    )

    return tmpdir


@pytest.fixture
def expected_dir(request):
    module_path = os.path.dirname(request.module.__file__)
    module_name, _ = os.path.splitext(os.path.basename(request.module.__file__))
    return os.path.join(module_path, "expected_%s" % module_name)


@pytest.fixture(params=[True, False])
def mpsym(request):
    return request.param


@pytest.fixture(
    params=[
        "exynos990",
        "generic_bus",
        "generic_mesh",
        "multi_cluster",
        "odroid",
    ]
)
def small_platform(request):
    return request.param


@pytest.fixture(params=["haec", "mppa_coolidge"])
def large_platform(request):
    return request.param


@pytest.fixture(params=["random", "static_cfs"])
def fast_mapper(request):
    return request.param


@pytest.fixture(params=["SimpleVector", "MetricSpaceEmbedding", "Symmetries"])
def representation(request):
    return request.param

# Copyright (C) 2018 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

import pytest

from mocasin.maps.platform import MapsPlatform


@pytest.fixture
def exynos():
    return MapsPlatform("exynos", "examples/maps/platforms/exynos.platform")


@pytest.fixture
def parallella():
    return MapsPlatform(
        "parallella", "examples/maps/platforms/parallella.platform"
    )


@pytest.fixture
def multiDSP():
    return MapsPlatform("multiDSP", "examples/maps/platforms/multidsp.platform")

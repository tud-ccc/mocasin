# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest

from mocasin.slx.platform import SlxPlatform


@pytest.fixture
def exynos():
    return SlxPlatform('exynos',
                       'examples/slx/platforms/exynos.platform')


@pytest.fixture
def parallella():
    return SlxPlatform('parallella',
                       'examples/slx/platforms/parallella.platform')


@pytest.fixture
def multiDSP():
    return SlxPlatform(
        'multiDSP',
        'examples/slx/platforms/multidsp.platform')

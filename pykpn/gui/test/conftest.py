# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest

from pykpn.slx.platform import SlxPlatform

@pytest.fixture
def exynos():
    return SlxPlatform('SlxPlatform', '../../../apps/audio_filter/exynos/exynos.platform', '2017.04')

@pytest.fixture
def parallella():
    return  SlxPlatform('SlxPlatform', '../../../apps/audio_filter/parallella/parallella.platform', '2017.04')

@pytest.fixture
def multiDSP():
    return SlxPlatform('SlxPlatform', '../../../apps/audio_filter/multidsp/multidsp.platform', '2017.04')

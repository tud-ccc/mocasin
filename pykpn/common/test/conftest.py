# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
from pykpn.tgff.tgffSimulation import TraceGeneratorWrapper
from pykpn.slx.trace import SlxTraceReader

@pytest.fixture
def trace_generator_tgff():
    return TraceGeneratorWrapper('pykpn/tgff/graphs/auto-indust-cords.tgff', 'TASK_GRAPH_1')

@pytest.fixture
def trace_generator_slx():
    return SlxTraceReader('examples/slx/app/audio_filter/exynos/traces')

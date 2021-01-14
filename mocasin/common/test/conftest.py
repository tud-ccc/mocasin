# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
from mocasin.tgff.tgffSimulation import TraceGeneratorWrapper
from mocasin.slx.trace import SlxTraceReader

@pytest.fixture
def trace_generator_tgff():
    return TraceGeneratorWrapper('examples/tgff/e3s-0.9/auto-indust-cords.tgff', 'TASK_GRAPH_1')

@pytest.fixture
def trace_generator_slx():
    return SlxTraceReader('examples/slx/app/audio_filter/exynos/traces')

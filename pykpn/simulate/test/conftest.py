# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from unittest.mock import Mock

import simpy

import pytest
from pykpn.simulate.process import RuntimeKpnProcess, RuntimeProcess


@pytest.fixture
def env():
    return simpy.Environment()


@pytest.fixture
def base_process(env):
    return RuntimeProcess('test_proc', env)


@pytest.fixture
def kpn_process(env):
    return RuntimeKpnProcess('test_proc', Mock(), env, start_at_tick=1000)


@pytest.fixture
def processor():
    processor = Mock()
    processor.name = 'Test'
    processor.ticks = lambda x: x
    return processor

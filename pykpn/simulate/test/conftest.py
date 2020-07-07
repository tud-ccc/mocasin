# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import simpy

import pytest
from pykpn.common.mapping import ChannelMappingInfo
from pykpn.simulate.application import RuntimeApplication
from pykpn.simulate.channel import RuntimeChannel
from pykpn.simulate.process import RuntimeKpnProcess, RuntimeProcess


@pytest.fixture
def env():
    return simpy.Environment()


@pytest.fixture
def system(env, mocker):
    m = mocker.Mock()
    m.env = env
    return m


@pytest.fixture
def app(system):
    return RuntimeApplication("test_app", system)


@pytest.fixture
def base_process(app):
    return RuntimeProcess('test_proc', app)


@pytest.fixture
def kpn_process(app, mocker):
    return RuntimeKpnProcess('test_proc', mocker.Mock(), app)


@pytest.fixture
def channel(app, mocker):
    info = ChannelMappingInfo(mocker.Mock(), 4)
    return RuntimeChannel('test_chan', info, 8, app)


@pytest.fixture
def processor(mocker):
    processor = mocker.Mock()
    processor.name = 'Test'
    processor.ticks = lambda x: x
    return processor

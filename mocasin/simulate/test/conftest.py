# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import simpy
import pytest

from mocasin.common.mapping import ChannelMappingInfo
from mocasin.platforms.odroid import DesignerPlatformOdroid
from mocasin.platforms.platformDesigner import genericProcessor
from mocasin.simulate.application import RuntimeApplication
from mocasin.simulate.channel import RuntimeChannel
from mocasin.simulate.process import (
    RuntimeDataflowProcess,
    RuntimeProcess,
    ProcessState,
)


@pytest.fixture
def env():
    return simpy.Environment()


@pytest.fixture
def system(env, mocker):
    m = mocker.Mock()
    m.env = env
    return m


@pytest.fixture(params=ProcessState.__members__)
def state(request):
    return request.param


@pytest.fixture
def app(system, mocker):
    app = RuntimeApplication("test_app", system)
    app.trace = mocker.Mock()
    app.trace.get_trace = mocker.MagicMock(return_value=[])
    app.trace.accumulate_processor_cycles = mocker.MagicMock(
        return_value={"Test": 0, "Test2": 0}
    )
    return app


@pytest.fixture
def base_process(app):
    return RuntimeProcess("test_proc", app)


@pytest.fixture
def dataflow_process(app, mocker):
    return RuntimeDataflowProcess("test_proc", app)


@pytest.fixture
def channel(app, mocker):
    info = ChannelMappingInfo(primitive=mocker.Mock(), capacity=4)
    channel = RuntimeChannel("test_chan", 8, app)
    channel.update_mapping_info(info)
    return channel


@pytest.fixture
def processor(mocker):
    processor = mocker.Mock()
    processor.name = "Test"
    processor.type = "Test"
    processor.ticks = lambda x: x
    return processor


@pytest.fixture
def processor2(mocker):
    processor = mocker.Mock()
    processor.name = "Test2"
    processor.type = "Test2"
    processor.ticks = lambda x: x * 2
    return processor


@pytest.fixture(params=["base", "dataflow"])
def process(request, base_process, dataflow_process, mocker):
    if request.param == "base":
        proc = base_process
    elif request.param == "dataflow":
        proc = dataflow_process
    else:
        raise ValueError("Unexpected fixture parameter")

    proc.workload = mocker.Mock()
    return proc


@pytest.fixture
def platform():
    pe_little = genericProcessor("proc_type_0")
    pe_big = genericProcessor("proc_type_1")
    p = DesignerPlatformOdroid(pe_little, pe_big)
    return p


@pytest.fixture
def platform_power():
    pe_little = genericProcessor("proc_type_0", static_power=1, dynamic_power=3)
    pe_big = genericProcessor("proc_type_1", static_power=2, dynamic_power=7)
    p = DesignerPlatformOdroid(pe_little, pe_big)
    return p


@pytest.fixture
def platform_power_partial():
    pe_little = genericProcessor("proc_type_0", static_power=1, dynamic_power=3)
    pe_big = genericProcessor("proc_type_1", static_power=None, dynamic_power=None)
    p = DesignerPlatformOdroid(pe_little, pe_big)
    return p
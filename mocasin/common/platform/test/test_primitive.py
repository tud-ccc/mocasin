# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import pytest

from mocasin.common.platform import (
    CommunicationResource,
    CommunicationPhase,
    Primitive,
)


@pytest.fixture
def slow_resource(frequency_domain):
    return CommunicationResource(
        name="slow resource",
        frequency_domain=frequency_domain,
        resource_type=None,
        read_latency=100,  # cycles
        write_latency=200,  # cycles
        read_throughput=8,  # bytes per cycle
        write_throughput=8,  # bytes per cycle
    )


@pytest.fixture
def mediocre_resource(frequency_domain):
    return CommunicationResource(
        name="mediocre resource",
        frequency_domain=frequency_domain,
        resource_type=None,
        read_latency=10,  # cycles
        write_latency=20,  # cycles
        read_throughput=16,  # bytes per cycle
        write_throughput=16,  # bytes per cycle
    )


@pytest.fixture
def fast_resource(frequency_domain):
    return CommunicationResource(
        name="fast resource",
        frequency_domain=frequency_domain,
        resource_type=None,
        read_latency=2,  # cycles
        write_latency=2,  # cycles
        read_throughput=32,  # bytes per cycle
        write_throughput=32,  # bytes per cycle
    )


@pytest.fixture(params=["slow", "mediocre", "fast"])
def resource(request, slow_resource, mediocre_resource, fast_resource):
    if request.param == "slow":
        return slow_resource
    elif request.param == "mediocre":
        return mediocre_resource
    elif request.param == "fast":
        return fast_resource
    else:
        raise KeyError()


def test_slow_resource(slow_resource):
    assert slow_resource.read_latency() == 66667  # pico seconds (ps)
    assert slow_resource.write_latency() == 133333  # pico seconds (ps)

    assert slow_resource.read_throughput() == 8 / 667  # bytes per ps
    assert slow_resource.write_throughput() == 8 / 667  # bytes per ps


def test_mediocre_resource(mediocre_resource):
    assert mediocre_resource.read_latency() == 6667  # pico seconds (ps)
    assert mediocre_resource.write_latency() == 13333  # pico seconds (ps)

    assert mediocre_resource.read_throughput() == 16 / 667  # bytes per ps
    assert mediocre_resource.write_throughput() == 16 / 667  # bytes per ps


def test_fast_resource(fast_resource):
    assert fast_resource.read_latency() == 1333  # pico seconds (ps)
    assert fast_resource.write_latency() == 1333  # pico seconds (ps)

    assert fast_resource.read_throughput() == 32 / 667  # bytes per ps
    assert fast_resource.write_throughput() == 32 / 667  # bytes per ps


def test_single_resource_communication_phase(resource):
    read_phase = CommunicationPhase(
        name="read", resources=[resource], direction="read"
    )
    write_phase = CommunicationPhase(
        name="write", resources=[resource], direction="write"
    )

    assert resource.read_latency() == read_phase.get_costs(0)
    assert resource.write_latency() == write_phase.get_costs(0)

    assert int(
        round(resource.read_latency() + 100 / resource.read_throughput())
    ) == read_phase.get_costs(100)
    assert int(
        round(resource.write_latency() + 100 / resource.write_throughput())
    ) == write_phase.get_costs(100)


def test_multi_resource_communication_phase(
    slow_resource, mediocre_resource, fast_resource
):
    read_phase = CommunicationPhase(
        name="read",
        resources=[slow_resource, mediocre_resource, fast_resource],
        direction="read",
    )
    write_phase = CommunicationPhase(
        name="write",
        resources=[slow_resource, mediocre_resource, fast_resource],
        direction="write",
    )

    expected_read_latency = (
        slow_resource.read_latency()
        + mediocre_resource.read_latency()
        + fast_resource.read_latency()
    )
    expected_write_latency = (
        slow_resource.write_latency()
        + mediocre_resource.write_latency()
        + fast_resource.write_latency()
    )
    assert expected_read_latency == read_phase.get_costs(0)
    assert expected_write_latency == write_phase.get_costs(0)

    assert int(
        round(expected_read_latency + 100 / slow_resource.read_throughput())
    ) == read_phase.get_costs(100)
    assert int(
        round(expected_write_latency + 100 / slow_resource.write_throughput())
    ) == write_phase.get_costs(100)


def test_single_phase_primitive(resource, mocker):
    read_phase = CommunicationPhase(
        name="read", resources=[resource], direction="read"
    )
    write_phase = CommunicationPhase(
        name="write", resources=[resource], direction="write"
    )
    src = mocker.Mock(name="src")
    sink = mocker.Mock(name="sink")
    prim = Primitive("prim")
    prim.add_consumer(sink, [read_phase])
    prim.add_producer(src, [write_phase])

    with pytest.raises(RuntimeError):
        prim.add_consumer(sink, [])
    with pytest.raises(RuntimeError):
        prim.add_producer(src, [])

    with pytest.raises(RuntimeError):
        prim.add_producer(sink, [read_phase])
    with pytest.raises(RuntimeError):
        prim.add_consumer(src, [write_phase])

    assert prim.static_consume_costs(sink) == read_phase.get_costs(8)
    assert prim.static_consume_costs(sink, 100) == read_phase.get_costs(100)

    assert prim.static_produce_costs(src) == write_phase.get_costs(8)
    assert prim.static_produce_costs(src, 100) == write_phase.get_costs(100)

    expected_costs_8 = write_phase.get_costs(8) + read_phase.get_costs(8)
    expected_costs_100 = write_phase.get_costs(100) + read_phase.get_costs(100)
    assert prim.static_costs(src, sink) == expected_costs_8
    assert prim.static_costs(src, sink, 100) == expected_costs_100


def test_multi_phase_primitive(
    slow_resource, mediocre_resource, fast_resource, mocker
):
    src = mocker.Mock(name="src")
    sink = mocker.Mock(name="sink")

    read_phases = [
        CommunicationPhase("read_ph1", [fast_resource], "read"),
        CommunicationPhase("read_ph2", [mediocre_resource], "read"),
        CommunicationPhase("read_ph3", [slow_resource], "read"),
    ]
    write_phases = [
        CommunicationPhase("write_ph1", [fast_resource], "write"),
        CommunicationPhase("write_ph2", [mediocre_resource], "write"),
        CommunicationPhase("write_ph3", [slow_resource], "write"),
    ]

    prim = Primitive("prim")
    prim.add_consumer(sink, read_phases)
    prim.add_producer(src, write_phases)

    expected_consume_costs_8 = sum([p.get_costs(8) for p in read_phases])
    expected_consume_costs_100 = sum([p.get_costs(100) for p in read_phases])
    assert prim.static_consume_costs(sink) == expected_consume_costs_8
    assert prim.static_consume_costs(sink, 100) == expected_consume_costs_100

    expected_produce_costs_8 = sum([p.get_costs(8) for p in write_phases])
    expected_produce_costs_100 = sum([p.get_costs(100) for p in write_phases])
    assert prim.static_produce_costs(src) == expected_produce_costs_8
    assert prim.static_produce_costs(src, 100) == expected_produce_costs_100

    expected_costs_8 = expected_consume_costs_8 + expected_produce_costs_8
    expected_costs_100 = expected_consume_costs_100 + expected_produce_costs_100
    assert prim.static_costs(src, sink) == expected_costs_8
    assert prim.static_costs(src, sink, 100) == expected_costs_100
    assert prim.static_costs(src, sink, 8) <= prim.static_costs(src, sink, 16)

# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import pytest

from mocasin.simulate.energy import EnergyEstimator


def test_energy_estimation_none(env, platform, mocker):
    energy_estimator = EnergyEstimator(platform, env)
    assert not energy_estimator.enabled
    processors = list(platform.processors())
    process_a = mocker.Mock()
    energy_estimator.register_process_start(processors[0], process_a)
    env.run(1000)
    energy_estimator.register_process_end(processors[0], process_a)
    energy = energy_estimator.calculate_energy()
    assert not energy


def test_energy_estimation(env, platform_power, mocker):
    energy_estimator = EnergyEstimator(platform_power, env)
    assert energy_estimator.enabled
    assert energy_estimator._last_activity == 0
    processors = list(platform_power.processors())
    process_a = mocker.Mock()
    process_b = mocker.Mock()
    energy_estimator.register_process_start(processors[0], process_a)
    assert energy_estimator._last_activity == 0
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 1
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 0
    )
    env.run(1000)
    energy_estimator.register_process_start(processors[4], process_b)
    assert energy_estimator._last_activity == 1000
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 1
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 1
    )
    env.run(2000)
    energy_estimator.register_process_end(processors[0], process_a)
    assert energy_estimator._last_activity == 2000
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 0
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 1
    )
    env.run(3000)
    energy_estimator.register_process_end(processors[4], process_b)
    energy = energy_estimator.calculate_energy()
    assert energy_estimator._last_activity == 3000
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 0
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 0
    )
    assert energy == (36000, 20000)


def test_energy_estimation_raises(env, platform_power, mocker):
    energy_estimator = EnergyEstimator(platform_power, env)
    assert energy_estimator.enabled
    processors = list(platform_power.processors())
    process_a = mocker.Mock()
    process_b = mocker.Mock()

    with pytest.raises(RuntimeError):
        energy_estimator.register_process_end(processors[0], process_a)

    energy_estimator.register_process_start(processors[0], process_a)
    env.run(1000)

    with pytest.raises(RuntimeError):
        energy_estimator.register_process_start(processors[0], process_b)
    with pytest.raises(RuntimeError):
        energy_estimator.register_process_end(processors[0], process_b)


def test_energy_estimation_partial(env, platform_power_partial, mocker):
    energy_estimator = EnergyEstimator(platform_power_partial, env)
    assert energy_estimator.enabled
    assert energy_estimator._last_activity == 0
    processors = list(platform_power_partial.processors())
    process_a = mocker.Mock()
    process_b = mocker.Mock()
    energy_estimator.register_process_start(processors[0], process_a)
    assert energy_estimator._last_activity == 0
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 1
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 0
    )
    env.run(1000)
    energy_estimator.register_process_start(processors[4], process_b)
    assert energy_estimator._last_activity == 1000
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 1
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 1
    )
    env.run(2000)
    energy_estimator.register_process_end(processors[0], process_a)
    assert energy_estimator._last_activity == 2000
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 0
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 1
    )
    env.run(3000)
    energy_estimator.register_process_end(processors[4], process_b)
    energy = energy_estimator.calculate_energy()
    assert energy_estimator._last_activity == 3000
    assert (
        len(energy_estimator._process_registry[processors[0]]["processes"]) == 0
    )
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 0
    )
    assert energy == (12000, 6000)


def mock_process_calls(
    env, processor, process, energy_estimator, start_time, end_time
):
    yield env.timeout(start_time)
    energy_estimator.register_process_start(processor, process)
    yield env.timeout(end_time - start_time)
    energy_estimator.register_process_end(processor, process)


p1_start = 0
p2_start = 1
p1_end = 2
p2_end = 3
RUN_TIME = [p1_start, p2_start, p1_end, p2_end]


@pytest.fixture(params=RUN_TIME)
def run_time(request):
    return request.param


def test_energy_estimation_partial_2_threads(
    run_time, env, mocker, platform_power_partial_2_threads
):
    energy_estimator = EnergyEstimator(platform_power_partial_2_threads, env)
    processors = list(platform_power_partial_2_threads.processors())

    p1 = mocker.Mock()
    p1.run = mocker.Mock(
        side_effect=lambda: mock_process_calls(
            env, processors[0], p1, energy_estimator, p1_start, p1_end
        )
    )

    p2 = mocker.Mock()
    p2.run = mocker.Mock(
        side_effect=lambda: mock_process_calls(
            env, processors[0], p2, energy_estimator, p2_start, p2_end
        )
    )

    env.process(p1.run())
    env.process(p2.run())
    env.run(until=run_time + 0.1)

    energy = energy_estimator.calculate_energy()

    assert energy_estimator._last_activity == run_time
    assert (
        len(energy_estimator._process_registry[processors[4]]["processes"]) == 0
    )

    if run_time == p1_start:
        assert (
            len(energy_estimator._process_registry[processors[0]]["processes"])
            == 1
        )
        assert energy == (0, 0)

    elif run_time == p2_start:
        assert (
            len(energy_estimator._process_registry[processors[0]]["processes"])
            == 2
        )
        assert energy == (4, 3)

    elif run_time == p1_end:
        assert (
            len(energy_estimator._process_registry[processors[0]]["processes"])
            == 1
        )
        assert energy == (8, 6)

    elif run_time == p2_end:
        assert (
            len(energy_estimator._process_registry[processors[0]]["processes"])
            == 0
        )
        assert energy == (12, 9)

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
    assert len(energy_estimator._process_start_registry) == 1
    env.run(1000)
    energy_estimator.register_process_start(processors[4], process_b)
    assert energy_estimator._last_activity == 1000
    assert len(energy_estimator._process_start_registry) == 2
    env.run(2000)
    energy_estimator.register_process_end(processors[0], process_a)
    assert energy_estimator._last_activity == 2000
    assert len(energy_estimator._process_start_registry) == 1
    env.run(3000)
    energy_estimator.register_process_end(processors[4], process_b)
    energy = energy_estimator.calculate_energy()
    assert energy_estimator._last_activity == 3000
    assert not energy_estimator._process_start_registry
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

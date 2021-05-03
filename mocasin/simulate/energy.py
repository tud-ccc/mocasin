# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov


class EnergyEstimator:
    """Estimates the overall energy consumption during a simulation.

    Calculates both static and dynamic energy consumption.
    """

    def __init__(self, platform, env):
        self.platform = platform
        self.env = env
        self.enabled = platform.has_power_model()
        self._last_activity = 0
        self._accumulated_dynamic_energy = 0  # in pJ
        self._process_start_registry = {}

    def register_process_start(self, processor, process):
        """Register the start of a process running on a given processor to
        account for its dynamic energy."""
        self._last_activity = self.env.now

        assert processor not in self._process_start_registry
        self._process_start_registry[processor] = (process, self.env.now)

    def register_process_end(self, processor, process):
        """Register the end of a process running on a given processor to
        account for its dynamic energy."""
        self._last_activity = self.env.now

        assert processor in self._process_start_registry
        start_process, start_time = self._process_start_registry.pop(processor)
        assert start_process is process

        td = self.env.now - start_time
        power = processor.dynamic_power()
        self._accumulated_dynamic_energy += power * td

    def calculate_energy(self):
        """Calculate the energy consumption of the simulation.

        Returns the tuple (static_energy, dynamic_energy)
        """
        static_energy = 0  # in pJ
        total_time = self._last_activity
        for pe in self.platform.processors():
            static_energy += pe.static_power() * total_time

        return (static_energy, self._accumulated_dynamic_energy)

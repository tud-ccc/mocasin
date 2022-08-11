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
        self._process_registry = {
            processor: {"processes": set(), "last_update": 0}
            for processor in platform.processors()
        }
        self._accumulated_dynamic_energy = 0  # in pJ

    @property
    def _last_activity(self):
        """Return the latest activity among all processors."""
        return max(
            [
                self._process_registry[processor]["last_update"]
                for processor in self.platform.processors()
            ]
        )

    def register_process_start(self, processor, process):
        """Register the start of a process running on a given processor to
        account for its dynamic energy."""

        if (
            len(self._process_registry[processor]["processes"])
            >= processor.n_threads
        ):
            raise RuntimeError(
                "Failed to register the start of the segment: "
                f"processor {processor} is busy."
            )
        if self.enabled:
            self._accumulate_dynamic_energy(processor)

        self._process_registry[processor]["processes"].add(process)
        self._process_registry[processor]["last_update"] = self.env.now

    def register_process_end(self, processor, process):
        """Register the end of a process running on a given processor to
        account for its dynamic energy."""

        if process not in self._process_registry[processor]["processes"]:
            raise RuntimeError(
                f"Failed to register the end of the segment: "
                f"processor {processor} isn't running {process.full_name}"
            )

        if self.enabled:
            self._accumulate_dynamic_energy(processor)

        self._process_registry[processor]["processes"].remove(process)
        self._process_registry[processor]["last_update"] = self.env.now

    def _accumulate_dynamic_energy(self, processor):
        """Accumulate the dynamic energy consumed by the given processor
        from the last update up to now."""

        power = processor.dynamic_power()
        if power is not None:
            td = self.env.now - self._process_registry[processor]["last_update"]
            power_coeff = (
                1
                if len(self._process_registry[processor]["processes"]) > 0
                else 0
            )  # This will depend on the actual power model
            self._accumulated_dynamic_energy += td * power_coeff * power

    def calculate_energy(self):
        """Calculate the energy consumption of the simulation.

        Returns the tuple (static_energy, dynamic_energy)
        """
        if not self.enabled:
            return None

        static_energy = 0  # in pJ
        total_time = self._last_activity
        for pe in self.platform.processors():
            if pe.static_power() is not None:
                static_energy += pe.static_power() * total_time

        # Add peripheral static power on the platform
        if self.platform.peripheral_static_power:
            static_energy += self.platform.peripheral_static_power * total_time

        return (static_energy, self._accumulated_dynamic_energy)

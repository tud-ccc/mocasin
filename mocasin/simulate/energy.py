# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov


class EnergyEstimator:
    """A class which calculates the overall energy consumption of the trace.

    This class takes the simulation trace as input and evaluates the overall
    energy consumption as following:
        $$ E = \int P(t) \,dt $$
    Each core is assumed to have two possible states at every point in time,
    "active" and "idle". The idle power equals the static power, while the
    dynamic power is the sum of the idle and dynamic power consumptions. At each
    state the power consumption is assumed to be contant, $P_{active}$ and
    $P_{idle}$, correspondingly. So the energy consumption of each core is:
        $$ E_{PE} = \sum_{s \in S} P_{state_s} t_s $$
    The overall energy consumption is:
        $$ E = \sum_{p \in \Pi} E_p $$

    This class calculates both static and dynamic energy consumption.
    """

    def __init__(self, platform, trace_writer):
        self.platform = platform
        self._trace_writer = trace_writer
        self._tid_pe_map = {}
        pass

    def _energy_dynamic_segment(self, tid, start_ts, end_ts):
        pe = self._tid_pe_map[tid]
        power = pe.dynamic_power()
        if power is None:
            return 0
        td = end_ts - start_ts
        return power * td * 1000000

    def _energy_static_segment(self, tid, start_ts, end_ts):
        pe = self._tid_pe_map[tid]
        power = pe.static_power()
        if power is None:
            return 0
        td = end_ts - start_ts
        return power * td * 1000000

    def calculate_energy(self):
        """Calculate the energy consumption of the simulation.

        Returns the tuple (static_energy, dynamic_energy)
        """
        static_energy = 0  # in pJ
        dynamic_energy = 0  # in pJ
        trace = self._trace_writer._trace
        tids = set()
        platform_pid = None
        last_event_ts = {}

        for elem in trace:
            # Collect TID <-> PE map
            ph = elem["ph"]
            pid = elem["pid"]
            name = elem["name"]

            # Find a PID of the platform
            if ph == "M" and name == "process_name":
                args_name = elem["args"]["name"]
                if args_name == self.platform.name:
                    platform_pid = pid
                    continue

            # Register the processors
            if ph == "M" and pid == platform_pid and name == "thread_name":
                tid = elem["tid"]
                pe_name = elem["args"]["name"]
                pe = self.platform.find_processor(pe_name)
                self._tid_pe_map[tid] = pe
                last_event_ts[tid] = 0
                continue

            # Skip other metadata entries
            if ph == "M" or ph == "C":
                continue
            if "tid" not in elem:
                raise RuntimeError(f"Unknown event type: {elem}")
            # Skip non-processor's events
            if pid != platform_pid:
                continue

            # main calculation
            tid = elem["tid"]
            event_ts = elem["ts"]  # timestamp in us
            # Start of the segment
            if ph == "B":
                static_energy += self._energy_static_segment(
                    tid, last_event_ts[tid], event_ts
                )
                last_event_ts[tid] = event_ts
            elif ph == "E":
                static_energy += self._energy_static_segment(
                    tid, last_event_ts[tid], event_ts
                )
                dynamic_energy += self._energy_dynamic_segment(
                    tid, last_event_ts[tid], event_ts
                )
                last_event_ts[tid] = event_ts
            else:
                raise RuntimeError(f"Unknown event type: {elem}")

        # Calculate the idle power till the end
        end_ts = max(last_event_ts.values(), default=None)
        for tid, ts in last_event_ts.items():
            static_energy += self._energy_static_segment(tid, ts, end_ts)
            last_event_ts[tid] = end_ts
        return (static_energy, dynamic_energy)

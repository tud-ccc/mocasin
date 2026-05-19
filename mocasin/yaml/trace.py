# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import logging
import numpy as np

from dataclasses import dataclass, field
from fractions import Fraction as frac
from typing import Dict

from hydra.utils import to_absolute_path
from omegaconf import DictConfig, OmegaConf

from mocasin.common.trace import (
    DataflowTrace,
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)

log = logging.getLogger(__name__)


@dataclass
class _StaticFiringRule:
    """Helper class defining the firing rules of a static process."""

    reads: Dict[str, int] = field(default_factory=dict)
    writes: Dict[str, int] = field(default_factory=dict)
    initial_writes: Dict[str, int] = field(default_factory=dict)


class YamlTrace(DataflowTrace):
    """Represents the execution behavior of an application defined in YAML input.

    See `~DataflowTrace`.

    Args:
        yaml_file (str): YAML application file
        repetitions (int): number of times the graph execution should repeat.
    """

    def __init__(self, yaml_file: str, repetitions: int = 1):
        self._firing_rules: Dict[str, _StaticFiringRule] = {}
        self._repetition_vector: Dict[str, int] = {}
        self._process_processor_cycles: Dict[str, Dict[str, int]] = {}
        self._repetitions = repetitions

        log.info("Start parsing YAML trace")

        self.yaml_app = OmegaConf.load(to_absolute_path(yaml_file))
        if not isinstance(self.yaml_app, DictConfig):
            raise RuntimeError("Top-level YAML object must be a mapping")

        self._validate_yaml_trace(self.yaml_app)

        graph = self.yaml_app.graph
        execution = self.yaml_app.execution

        self.__init_firing_rules(graph, execution)
        self.__init_repetition_vector(graph, execution)
        self.__init_cycle_counts(execution)

        log.info("Done parsing YAML trace")

    def __init_firing_rules(self, graph: DictConfig, execution: DictConfig):
        """Collect firing rules for all static processes."""
        for process_name, process_cfg in execution.processes.instances.items():
            if process_cfg.model != "static":
                raise RuntimeError(
                    f"YAML trace currently only supports static processes. "
                    f"Process {process_name} uses model {process_cfg.model}."
                )

            rule = _StaticFiringRule()
            rates = process_cfg.get("rates", {})

            for channel_name, channel_cfg in graph.channels.items():
                if channel_cfg.src.process == process_name:
                    port = channel_cfg.src.port
                    rule.writes[channel_name] = int(rates[port])

                    initial_tokens = (
                        execution.get("channels", {})
                        .get(channel_name, {})
                        .get("initial_tokens", 0)
                    )
                    if initial_tokens:
                        rule.initial_writes[channel_name] = int(initial_tokens)

                if channel_cfg.dst.process == process_name:
                    port = channel_cfg.dst.port
                    rule.reads[channel_name] = int(rates[port])

            self._firing_rules[process_name] = rule

    def __init_repetition_vector(
        self,
        graph: DictConfig,
        execution: DictConfig,
    ) -> None:
        """Calculate the SDF-style repetition vector."""

        for process_name in graph.processes.keys():
            self._repetition_vector[process_name] = None

        rates = {
            process_name: process_cfg.get("rates", {})
            for process_name, process_cfg in execution.processes.instances.items()
        }

        def visit_process(process_name):
            assert self._repetition_vector[process_name] is not None

            for channel in graph.channels.values():
                src = channel.src.process
                dst = channel.dst.process
                src_port = channel.src.port
                dst_port = channel.dst.port

                if src == process_name:
                    production_rate = int(rates[src][src_port])
                    consumption_rate = int(rates[dst][dst_port])
                    factor = frac(production_rate, consumption_rate)
                    src_rate = self._repetition_vector[src]
                    dst_rate = src_rate * factor

                    if self._repetition_vector[dst] is None:
                        self._repetition_vector[dst] = dst_rate
                        visit_process(dst)
                    elif self._repetition_vector[dst] != dst_rate:
                        raise RuntimeError(
                            "Static YAML graph is not consistent!"
                        )

                elif dst == process_name:
                    production_rate = int(rates[src][src_port])
                    consumption_rate = int(rates[dst][dst_port])
                    factor = frac(production_rate, consumption_rate)
                    dst_rate = self._repetition_vector[dst]
                    src_rate = dst_rate / factor

                    if self._repetition_vector[src] is None:
                        self._repetition_vector[src] = src_rate
                        visit_process(src)
                    elif self._repetition_vector[src] != src_rate:
                        raise RuntimeError(
                            "Static YAML graph is not consistent!"
                        )

        start_process = next(iter(self._repetition_vector.keys()))
        self._repetition_vector[start_process] = frac(1, 1)
        visit_process(start_process)

        for rate in self._repetition_vector.values():
            if rate is None:
                raise RuntimeError(
                    "SDF graph contains processes that are not reachable!"
                )

        lcm = np.lcm.reduce(
            [x.denominator for x in self._repetition_vector.values()]
        )

        for process_name, rate in self._repetition_vector.items():
            self._repetition_vector[process_name] = int(rate * lcm)

        log.debug(
            "The repetition vector for YAML graph is %s",
            self._repetition_vector,
        )

    def __init_cycle_counts(self, execution: DictConfig) -> None:
        """Collect cycle counts for all static process instances."""

        profiles = execution.processes.get("profiles", {})

        for process_name, process_cfg in execution.processes.instances.items():
            profile_name = process_cfg.get("profile")
            if profile_name is None:
                raise RuntimeError(
                    f"Static process {process_name} is missing required key "
                    "'profile'"
                )

            if profile_name not in profiles:
                raise RuntimeError(
                    f"Process {process_name} references unknown profile "
                    f"{profile_name}"
                )

            processor_cycles = {}
            for processor_type, profile in profiles[profile_name].items():
                if "cycles" not in profile:
                    raise RuntimeError(
                        f"Profile {profile_name}.{processor_type} is missing "
                        "required key 'cycles'"
                    )
                processor_cycles[processor_type] = int(profile.cycles)

            self._process_processor_cycles[process_name] = processor_cycles

    def get_trace(self, process: str):
        """Get the trace for a specific process."""

        firings = self._firing_rules[process]

        for channel, count in firings.initial_writes.items():
            yield WriteTokenSegment(channel=channel, num_tokens=count)

        total_reps = self._repetition_vector[process] * self._repetitions

        for _ in range(0, total_reps):
            for channel, count in firings.reads.items():
                yield ReadTokenSegment(channel=channel, num_tokens=count)

            yield ComputeSegment(
                processor_cycles=self._process_processor_cycles[process]
            )

            for channel, count in firings.writes.items():
                yield WriteTokenSegment(channel=channel, num_tokens=count)

    def _validate_yaml_trace(self, app: DictConfig) -> None:
        self._require_key(app, "graph", "YAML application")
        self._require_key(app, "execution", "YAML application")
        self._require_key(app.execution, "processes", "YAML execution")

        self._validate_channels(app)
        self._validate_processes(app)

    def _validate_channels(self, app: DictConfig) -> None:
        graph_channels = set(app.graph.channels.keys())

        if "channels" not in app.execution:
            return

        execution_channels = set(app.execution.channels.keys())
        unknown_channels = execution_channels - graph_channels

        if unknown_channels:
            raise RuntimeError(
                "Execution references unknown channels: "
                + ", ".join(sorted(unknown_channels))
            )

    def _validate_processes(self, app: DictConfig) -> None:
        self._require_key(
            app.execution.processes,
            "instances",
            "YAML execution.processes",
        )

        graph_processes = set(app.graph.processes.keys())
        execution_processes = set(app.execution.processes.instances.keys())

        missing_processes = graph_processes - execution_processes
        if missing_processes:
            raise RuntimeError(
                "Missing execution definitions for processes: "
                + ", ".join(sorted(missing_processes))
            )

        unknown_processes = execution_processes - graph_processes
        if unknown_processes:
            raise RuntimeError(
                "Execution references unknown processes: "
                + ", ".join(sorted(unknown_processes))
            )

        self._validate_profiles(app)

        for (
            process_name,
            process_cfg,
        ) in app.execution.processes.instances.items():
            self._validate_process_instance(app, process_name, process_cfg)

    def _validate_profiles(self, app: DictConfig) -> None:
        if "profiles" not in app.execution.processes:
            return

        for (
            profile_name,
            profile_cfg,
        ) in app.execution.processes.profiles.items():
            if not profile_cfg:
                raise RuntimeError(f"Profile {profile_name} is empty")

            for processor_type, processor_profile in profile_cfg.items():
                self._require_key(
                    processor_profile,
                    "cycles",
                    f"profile {profile_name}.{processor_type}",
                )

    def _validate_process_instance(
        self,
        app: DictConfig,
        process_name: str,
        process_cfg: DictConfig,
    ) -> None:
        self._require_key(
            process_cfg,
            "model",
            f"execution.processes.instances.{process_name}",
        )

        if process_cfg.model != "static":
            raise RuntimeError(
                f"Unsupported process model {process_cfg.model} for "
                f"process {process_name}. Only 'static' is currently supported."
            )

        self._require_key(
            process_cfg,
            "rates",
            f"execution.processes.instances.{process_name}",
        )
        self._require_key(
            process_cfg,
            "profile",
            f"execution.processes.instances.{process_name}",
        )

        profile_name = process_cfg.profile
        if profile_name not in app.execution.processes.profiles:
            raise RuntimeError(
                f"Process {process_name} references unknown profile {profile_name}"
            )

        self._validate_process_rates(app, process_name, process_cfg)

    def _validate_process_rates(
        self,
        app: DictConfig,
        process_name: str,
        process_cfg: DictConfig,
    ) -> None:
        graph_process = app.graph.processes[process_name]

        in_ports = set(graph_process.ports.get("in", []))
        out_ports = set(graph_process.ports.get("out", []))

        expected_ports = in_ports | out_ports
        rate_ports = set(process_cfg.rates.keys())

        missing_ports = expected_ports - rate_ports
        if missing_ports:
            raise RuntimeError(
                f"Process {process_name} is missing rates for ports: "
                + ", ".join(sorted(missing_ports))
            )

        unknown_ports = rate_ports - expected_ports
        if unknown_ports:
            raise RuntimeError(
                f"Process {process_name} defines rates for unknown ports: "
                + ", ".join(sorted(unknown_ports))
            )

        for port_name, rate in process_cfg.rates.items():
            if not isinstance(rate, int):
                raise RuntimeError(
                    f"Rate for process {process_name}, port {port_name} "
                    "must be an integer"
                )

            if rate <= 0:
                raise RuntimeError(
                    f"Rate for process {process_name}, port {port_name} "
                    "must be positive"
                )

    @staticmethod
    def _require_key(obj: DictConfig, key: str, context: str) -> None:
        if key not in obj:
            raise RuntimeError(f"{context} is missing required key '{key}'")

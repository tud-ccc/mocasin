# Copyright (C) 2024 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov, Jiahong Bi

import logging
from typing import List, Optional, Set, Tuple

from hydra.utils import to_absolute_path
from mocasin.common.graph import DataflowChannel, DataflowGraph, DataflowProcess
from omegaconf import OmegaConf, DictConfig

log = logging.getLogger(__name__)

PortKey = Tuple[str, str, str]  # (process_name, direction, port_name)


class YamlGraph(DataflowGraph):
    """Graph representation of a YAML application

    Args:
        yaml_file (str): the YAML file to read from
        name (str): the name to use for the application
    """

    def __init__(self, yaml_file: str, name: Optional[str] = None):
        log.info("Start parsing application graph from YAML")

        self.yaml_graph = OmegaConf.load(to_absolute_path(yaml_file))
        log.debug(self.yaml_graph)

        graph_name = name or self.yaml_graph.get("name")
        if graph_name is None:
            raise RuntimeError("YAML graph is missing required key 'name'")

        self._validate_application(self.yaml_graph)

        graph = self.yaml_graph.graph

        super().__init__(graph_name)

        for process_name, process_cfg in graph.processes.items():
            log.debug(f"Add process {graph_name}.{process_name}")
            self.add_process(DataflowProcess(process_name))

        for channel_name, channel_cfg in graph.channels.items():
            log.debug(f"Add channel {graph_name}.{channel_name}")
            df_channel = DataflowChannel(channel_name, channel_cfg.token_size)
            self.add_channel(df_channel)

            src_process = self.find_process(channel_cfg.src.process)
            src_process.connect_to_outgoing_channel(df_channel)
            log.debug(
                f"Process {graph_name}.{src_process.name} writes to channel "
                f"{graph_name}.{channel_name}"
            )

            dst_process = self.find_process(channel_cfg.dst.process)
            dst_process.connect_to_incomming_channel(df_channel)
            log.debug(
                f"Process {graph_name}.{dst_process.name} reads from channel "
                f"{graph_name}.{channel_name}"
            )

        log.info("Done parsing graph from YAML")

    def _validate_application(self, app: DictConfig) -> None:
        self._require_key(app, "graph", "YAML application")
        self._validate_graph(app.graph)

        if "execution" in app:
            self._validate_execution(app.graph, app.execution)

    def _validate_graph(self, graph: DictConfig) -> None:
        self._require_key(graph, "processes", "YAML graph")
        self._require_key(graph, "channels", "YAML graph")

        process_names: Set[str] = set()
        declared_ports: Set[PortKey] = set()

        for process_name, process_cfg in graph.processes.items():
            self._validate_process(process_name, process_cfg, declared_ports)

        channel_names: Set[str] = set()
        connected_ports: Set[PortKey] = set()

        for channel_name, channel_cfg in graph.channels.items():
            self._validate_channel(
                channel_name, channel_cfg, declared_ports, connected_ports
            )

        missing_ports = declared_ports - connected_ports
        if missing_ports:
            formatted = ", ".join(
                f"{process}.{port} ({direction})"
                for process, direction, port in sorted(missing_ports)
            )
            raise RuntimeError(
                f"Some declared ports are not connected: {formatted}"
            )

    def _validate_process(
        self,
        process_name: str,
        process_cfg: DictConfig,
        declared_ports: Set[PortKey],
    ):
        self._require_key(process_cfg, "ports", f"process {process_name}")

        in_ports = process_cfg.ports.get("in", [])
        out_ports = process_cfg.ports.get("out", [])

        self._validate_port_list(process_name, "in", in_ports, declared_ports)
        self._validate_port_list(process_name, "out", out_ports, declared_ports)

    def _validate_port_list(
        self,
        process_name: str,
        direction: str,
        ports: List[str],
        declared_ports: Set[PortKey],
    ) -> None:
        seen_ports: Set[str] = set()

        for port in ports:
            if port in seen_ports:
                raise RuntimeError(
                    f"Duplicate {direction} port {process_name}.{port}"
                )
            seen_ports.add(port)

            key = (process_name, direction, port)
            declared_ports.add(key)

    def _validate_channel(
        self,
        channel_name: str,
        channel_cfg: DictConfig,
        declared_ports: Set[PortKey],
        connected_ports: Set[PortKey],
    ) -> None:
        self._require_key(channel_cfg, "src", f"channel {channel_name}")
        self._require_key(channel_cfg, "dst", f"channel {channel_name}")
        self._require_key(channel_cfg, "token_size", f"channel {channel_name}")

        src_key = self._validate_endpoint(
            channel_name,
            "src",
            channel_cfg.src,
            "out",
            declared_ports,
        )
        dst_key = self._validate_endpoint(
            channel_name,
            "dst",
            channel_cfg.dst,
            "in",
            declared_ports,
        )

        for key in (src_key, dst_key):
            if key in connected_ports:
                process_name, direction, port_name = key
                raise RuntimeError(
                    f"Port {process_name}.{port_name} ({direction}) is connected "
                    "to more than one channel"
                )
            connected_ports.add(key)

    def _validate_endpoint(
        self,
        channel_name: str,
        endpoint_name: str,
        endpoint: DictConfig,
        expected_direction: str,
        declared_ports: Set[PortKey],
    ) -> PortKey:
        self._require_key(
            endpoint, "process", f"channel {channel_name}.{endpoint_name}"
        )
        self._require_key(
            endpoint, "port", f"channel {channel_name}.{endpoint_name}"
        )

        key = (endpoint.process, expected_direction, endpoint.port)

        if key not in declared_ports:
            raise RuntimeError(
                f"Channel {channel_name} uses invalid {endpoint_name} endpoint "
                f"{endpoint.process}.{endpoint.port}: expected an "
                f"{expected_direction} port"
            )

        return key

    def _validate_execution(
        self,
        graph: DictConfig,
        execution: DictConfig,
    ) -> None:
        """Validate optional execution annotations.

        The graph parser does not use execution data directly, but validating
        references here helps catch malformed application files early.
        """
        graph_processes = set(graph.processes.keys())
        graph_channels = set(graph.channels.keys())

        if "processes" in execution and "instances" in execution.processes:
            for process_name in execution.processes.instances.keys():
                if process_name not in graph_processes:
                    raise RuntimeError(
                        f"Execution references unknown process {process_name}"
                    )

        if "channels" in execution:
            for channel_name in execution.channels.keys():
                if channel_name not in graph_channels:
                    raise RuntimeError(
                        f"Execution references unknown channel {channel_name}"
                    )

    @staticmethod
    def _require_key(obj: DictConfig, key: str, context: str) -> None:
        if key not in obj:
            raise RuntimeError(f"{context} is missing required key '{key}'")

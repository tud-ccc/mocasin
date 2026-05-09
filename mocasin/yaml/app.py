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

PortKey = Tuple[str, str, str]  # (node_name, direction, port_name)


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

        self._validate_graph(self.yaml_graph)

        super().__init__(graph_name)

        for node in self.yaml_graph.nodes:
            log.debug(f"Add process {name}.{node.name}")
            self.add_process(DataflowProcess(node.name))

        for channel in self.yaml_graph.channels:
            token_size = channel.get("token_size")

            log.debug(f"Add channel {name}.{channel.name}")
            df_channel = DataflowChannel(channel.name, token_size)
            self.add_channel(df_channel)

            src_process = self.find_process(channel.src.node)
            src_process.connect_to_outgoing_channel(df_channel)
            log.debug(
                f"Process {graph_name}.{src_process.name} writes to channel "
                f"{graph_name}.{channel.name}"
            )

            dst_process = self.find_process(channel.dst.node)
            dst_process.connect_to_incomming_channel(df_channel)
            log.debug(
                f"Process {graph_name}.{dst_process.name} reads from channel "
                f"{graph_name}.{channel.name}"
            )

        log.info("Done parsing graph from YAML")

    def _validate_graph(self, graph: DictConfig) -> None:
        self._require_key(graph, "nodes", "YAML graph")
        self._require_key(graph, "channels", "YAML graph")

        node_names: Set[str] = set()
        declared_ports: Set[PortKey] = set()

        for node in graph.nodes:
            self._validate_node(node, node_names, declared_ports)

        channel_names: Set[str] = set()
        connected_ports: Set[PortKey] = set()

        for channel in graph.channels:
            self._validate_channel(
                channel, declared_ports, channel_names, connected_ports
            )

        missing_ports = declared_ports - connected_ports
        if missing_ports:
            formatted = ", ".join(
                f"{node}.{port} ({direction})"
                for node, direction, port in sorted(missing_ports)
            )
            raise RuntimeError(
                f"Some declared ports are not connected: {formatted}"
            )

    def _validate_node(
        self,
        node: DictConfig,
        node_names: Set[str],
        declared_ports: Set[PortKey],
    ):
        self._require_key(node, "name", "node")
        self._require_key(node, "ports", f"node {node.name}")

        if node.name in node_names:
            raise RuntimeError(f"Duplicate node name: {node.name}")
        node_names.add(node.name)

        in_ports = node.ports.get("in", [])
        out_ports = node.ports.get("out", [])

        self._validate_port_list(node.name, "in", in_ports, declared_ports)
        self._validate_port_list(node.name, "out", out_ports, declared_ports)

    def _validate_port_list(
        self,
        node_name: str,
        direction: str,
        ports: List[str],
        declared_ports: Set[PortKey],
    ) -> None:
        seen_ports: Set[str] = set()

        for port in ports:
            if port in seen_ports:
                raise RuntimeError(
                    f"Duplicate {direction} port {node_name}.{port}"
                )
            seen_ports.add(port)

            key = (node_name, direction, port)
            declared_ports.add(key)

    def _validate_channel(
        self,
        channel: DictConfig,
        declared_ports: Set[PortKey],
        channel_names: Set[str],
        connected_ports: Set[PortKey],
    ) -> None:
        self._require_key(channel, "name", "channel")

        if channel.name in channel_names:
            raise RuntimeError(f"Duplicate channel name: {channel.name}")
        channel_names.add(channel.name)

        self._require_key(channel, "src", f"channel {channel.name}")
        self._require_key(channel, "dst", f"channel {channel.name}")

        src_key = self._validate_endpoint(
            channel.name,
            "src",
            channel.src,
            "out",
            declared_ports,
        )
        dst_key = self._validate_endpoint(
            channel.name,
            "dst",
            channel.dst,
            "in",
            declared_ports,
        )

        for key in (src_key, dst_key):
            if key in connected_ports:
                node_name, direction, port_name = key
                raise RuntimeError(
                    f"Port {node_name}.{port_name} ({direction}) is connected "
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
            endpoint, "node", f"channel {channel_name}.{endpoint_name}"
        )
        self._require_key(
            endpoint, "port", f"channel {channel_name}.{endpoint_name}"
        )

        key = (endpoint.node, expected_direction, endpoint.port)

        if key not in declared_ports:
            raise RuntimeError(
                f"Channel {channel_name} uses invalid {endpoint_name} endpoint "
                f"{endpoint.node}.{endpoint.port}: expected an "
                f"{expected_direction} port"
            )

        return key

    @staticmethod
    def _require_key(obj: DictConfig, key: str, context: str) -> None:
        if key not in obj:
            raise RuntimeError(f"{context} is missing required key '{key}'")

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import hydra


def graph_to_dot(cfg):
    """Generate a dot graph from dataflow graph

    This simple task produces a dot graph that visualizes a given dataflow
    graph. It expects two hydra parameters to be available.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **graph:** the input dataflow graph. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.graph.DataflowGraph` object.
        * **dot:** the output file
    """
    graph = hydra.utils.instantiate(cfg["graph"])
    graph.to_pydot().write_raw(cfg["output_file"])


def platform_to_dot(cfg):
    """Generate a dot graph from a Platform

    This simple task produces a dot graph that visualizes a given Platform. It
    expects two hydra parameters to be available.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **dot:** the output file
    """
    platform = hydra.utils.instantiate(cfg["platform"])
    platform.to_pydot().write_raw(cfg["output_file"])


def mapping_to_dot(cfg):
    """Generate a dot graph representing the mapping of a dataflow application
    to a platform.

    This task expects four hydra parameters to be available.

    **Hydra Parameters**:
        * **graph:** the input dataflow graph. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.graph.DataflowGraph` object.
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **mapping:** the input mapping. The task expects a configuration dict
          that can be instantiated to a :class:`~mocasin.common.mapping.Mapping`
          object.
        * **dot:** the output file
    """
    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    mapper = hydra.utils.instantiate(cfg["mapper"], platform)
    mapping = mapper.generate_mapping(
        graph, trace=trace, representation=representation
    )

    mapping.to_pydot().write_raw(cfg["output_file"])

# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard, Robert Khasanov

import logging
from pathlib import Path

import hydra

from mocasin.util.mapping_table import MappingTableWriter

log = logging.getLogger(__name__)


@hydra.main(config_path="../conf/", config_name="pareto_front.yaml")
def pareto_front(cfg):
    """Pareto Front Task.

    This task produces a pareto front of mappings using the genetic algorithms
    task.

    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **graph:** the input datafloe graph. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.graph.DataflowGraph` object.
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~mocasin.common.trace.TraceGenerator` object.
        * **representation:** the representation. The task expects a
          configuration dict that can be instantiated to a
          :class:`~mocasin.representations.MappingRepresentation` object.
        * **mapper:** the mapper.
        * **evaluate_metadata:** the flag to force the evaluation of the mapping
          metadata if the mapper does not evaluate them.
        * **mapping_table:** the output path for the mapping table.
    """
    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    mapper = hydra.utils.instantiate(cfg["mapper"], platform)
    evaluate_metadata = cfg["evaluate_metadata"]

    # Run genetic algorithm
    if not hasattr(mapper, "generate_pareto_front") or not callable(
        getattr(mapper, "generate_pareto_front")
    ):
        raise RuntimeError(
            "The method 'generate_pareto_front' is not implemented"
        )

    pareto_front = mapper.generate_pareto_front(
        graph,
        trace=trace,
        representation=representation,
        evaluate_metadata=evaluate_metadata,
    )

    # export the pareto front
    mapping_table_path = Path(cfg["mapping_table"])

    with MappingTableWriter(platform, graph, mapping_table_path) as writer:
        writer.write_header()
        for m in pareto_front:
            writer.write_mapping(m)

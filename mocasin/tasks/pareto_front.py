# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard, Robert Khasanov

import hydra
import logging
from pathlib import Path

from mocasin.mapper.utils import SimulationManager
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
        * **export_all:** a flag indicating whether all mappings should be
          exported. If ``false`` only the best mapping will be exported.
        * **graph:** the input datafloe graph. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.graph.DataflowGraph` object.
        * **outdir:** the output directory
        * **progress:** a flag indicating whether to show a progress bar with
          ETA
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~mocasin.common.trace.TraceGenerator` object.
        * **mapping_table:** the ouput path for the mapping table.
    """
    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    mapper = hydra.utils.instantiate(
        cfg["mapper"], graph, platform, trace, representation
    )

    # Run genetic algorithm
    pareto_front = mapper.generate_pareto_front()

    # obtain simulation values
    simulation_manager = SimulationManager(
        representation, trace, jobs=None, parallel=True
    )
    simulation_manager.simulate(pareto_front)

    # export the pareto front
    mapping_table_path = Path(cfg["mapping_table"])

    with MappingTableWriter(platform, graph, mapping_table_path) as writer:
        writer.write_header()
        for m in pareto_front:
            writer.write_mapping(m)

# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard, Robert Khasanov

import logging
import hydra
from pathlib import Path

from mocasin.mapper.genetic import GeneticMapper
from mocasin.tgff.tgffSimulation import TgffReferenceError
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
    try:
        graph = hydra.utils.instantiate(cfg["graph"])
        platform = hydra.utils.instantiate(cfg["platform"])
        trace = hydra.utils.instantiate(cfg["trace"])
        representation = hydra.utils.instantiate(
            cfg["representation"], graph, platform
        )
        if (
            cfg["mapper"]._target_ != "mocasin.mapper.genetic.GeneticMapper"
            and cfg["mapper"]._target_ != "mocasin.mapper.fair.StaticCFSMapper"
        ):
            raise RuntimeError(
                "The pareto front task needs to be called with the genetic "
                "mapper or the static cfs mapper. Called with "
                f"{cfg['mapper']._target_}"
            )
        mapper = hydra.utils.instantiate(
            cfg["mapper"], graph, platform, trace, representation
        )
    except TgffReferenceError:
        # Special exception indicates a bad combination of tgff components
        # can be thrown during multiruns and should not stop the hydra
        # execution
        log.warning("Referenced non existing tgff component!")
        return

    # Run genetic algorithm
    results = mapper.generate_pareto_front()

    # export the pareto front
    mapping_table_path = Path(cfg["mapping_table"])
    with MappingTableWriter(platform, graph, mapping_table_path) as writer:
        writer.write_header()
        for m in results:
            writer.write_mapping(m)

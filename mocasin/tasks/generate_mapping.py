#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra
import os
import pickle

from mocasin.maps.mapping import export_maps_mapping
from mocasin.simulate import DataflowSimulation

log = logging.getLogger(__name__)


@hydra.main(config_path="../conf", config_name="generate_mapping")
def generate_mapping(cfg):
    """Mapper Task

    This task produces a mapping using one of multiple possible mapping algorithms.


    Args:
        cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object

    **Hydra Parameters**:
        * **mapper:** the mapper (mapping algorithm) to be used.
        * **export_all:** a flag indicating whether all mappings should be
          exported. If ``false`` only the best mapping will be exported.
        * **graph:** the input dataflow graph. The task expects a configuration dict
          that can be instantiated to a :class:`~mocasin.common.graph.DataflowGraph`
          object.
        * **outdir:** the output directory
        * **progress:** a flag indicating whether to show a progress bar with
          ETA
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **plot_distribution:** a flag indicating whether to plot the
          distribution of simulated execution times over all mapping
        * **trace:** the input trace. The task expects a configuration dict
          that can be instantiated to a
          :class:`~mocasin.common.trace.TraceGenerator` object.

    It is recommended to use the silent all logginf o (``-s``) to suppress all logging
    output from the individual simulations."""
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    graph = hydra.utils.instantiate(cfg["graph"])
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    mapper = hydra.utils.instantiate(
        cfg["mapper"], graph, platform, trace, representation
    )

    # Run mapper
    result = mapper.generate_mapping()

    # export the best mapping
    outdir = cfg["outdir"]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    with open(outdir + "/mapping.pickle", "wb") as f:
        p = pickle.Pickler(f)
        p.dump(result)

    if cfg["simulate_best"]:
        trace = hydra.utils.instantiate(cfg["trace"])
        simulation = DataflowSimulation(
            result.platform, result.graph, result, trace
        )
        with simulation as s:
            s.run()

        exec_time = float(simulation.exec_time) / 1000000000.0
        log.info("Best mapping simulated time: " + str(exec_time) + " ms")
        with open(outdir + "best_time.txt", "w") as f:
            f.write(str(exec_time))

    if cfg["graph"]["_target_"] == "mocasin.maps.graph.MapsDataflowGraph":
        export_maps_mapping(
            result, os.path.join(outdir, "generated_mapping.mapping")
        )

    hydra.utils.call(cfg["cleanup"])
    del mapper

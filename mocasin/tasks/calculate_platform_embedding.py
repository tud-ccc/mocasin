# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Andres Goens

import hydra
import logging
from mocasin.common.graph import DataflowGraph
import os

log = logging.getLogger(__name__)


@hydra.main(config_path="../conf", config_name="calculate_platform_embedding")
def calculate_platform_embedding(cfg):
    """Calculate the embedding for a Platform Graph

    This task expects two hydra parameters to be available, for the platform and
    for the representation. The representation has to be an embedding
    representation (MetricSpaceEmbedding or SymmetryEmbedding).
    The options are taken from the metric space embedding representation.
    The file is written to the path defined in the configuration under:
     `platform.embedding_json`

    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **representation:** the mapping representation to find the embedding.
        This can be either MetricSpaceEmbedding or SymmetryEmbedding.

    """
    platform = hydra.utils.instantiate(cfg["platform"])
    json_file = cfg["platform"]["embedding_json"]
    if json_file is not None and os.path.exists(json_file):
        log.info("JSON file already found. Removing and recalculating")
        os.remove(json_file)
    elif json_file is None:
        log.warning(
            "No path specified for storing the file. Embedding won't be stored."
            "\n You can specify it with: platform.embedding_json "
            "= <output-file-path>"
        )
    if (
        cfg["representation"]._target_
        != "mocasin.representations.MetricEmbeddingRepresentation"
        and cfg["representation"]._target_
        != "mocasin.representations.SymmetryEmbedding"
    ):
        raise RuntimeError(
            "The calculate platform embedding task needs to be called "
            "w/ the MetricSpaceEmbedding or SymmetryEmbedding representation."
            f" Called with {cfg['representation']._target_}"
        )
    graph = DataflowGraph(name="EmptyGraph")
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    out_filename = str(cfg["out_file"])
    representation.dump_json(out_filename)

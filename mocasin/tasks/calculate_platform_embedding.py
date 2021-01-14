#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import hydra
import logging
from mocasin.common.kpn import KpnGraph
import os

log = logging.getLogger(__name__)


@hydra.main(config_path="../conf", config_name="calculate_platform_embedding")
def calculate_platform_embedding(cfg):
    """Calculate the Automorphism Group of a Platform Graph

    This task expects three hydra parameters to be available.


    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~mocasin.common.platform.Platform` object.
        * **out:** the output file (extension will be added)
        * **mpsym:** a boolean value selecting mpsym as backend (and JSON as output)
        Otherwise it outputs plaintext from the python implementation.
    """
    platform = hydra.utils.instantiate(cfg["platform"])
    json_file = cfg["platform"]["embedding_json"]
    if json_file is not None and os.path.exists(json_file):
        log.info("JSON file already found. Removing and recalculating")
        os.remove(json_file)
    if (
        cfg["representation"]._target_
        != "mocasin.representations.MetricEmbeddingRepresentation"
    ):
        raise RuntimeError(
            f"The enumerate equvialent task needs to be called "
            f"with the MetricSpaceEmbeddings representation."
            f" Called with {cfg['representation']._target_}"
        )
    kpn = KpnGraph(name="EmptyGraph")
    representation = hydra.utils.instantiate(
        cfg["representation"], kpn, platform
    )

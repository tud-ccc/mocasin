# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Andres Goens

import logging
import hydra

log = logging.getLogger(__name__)


@hydra.main(config_path="../conf", config_name="enumerate_equivalent")
def enumerate_equivalent(cfg):
    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    if (
        cfg["representation"]._target_
        != "mocasin.representations.SymmetryRepresentation"
    ):
        raise RuntimeError(
            f"The enumerate equvialent task needs to be called with the Symmetry representation. Called with {cfg['representation']._target_}"
        )
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    mapping = hydra.utils.instantiate(
        cfg["mapper"], graph, platform, trace, representation
    ).generate_mapping()

    log.info(("calculating orbit for mapping:" + str(mapping.to_list())))
    with open(cfg["output_file"], "w") as output_file:
        i = 0
        for i, elem in enumerate(representation.allEquivalent(mapping)):
            output_file.write(f"\n mapping {i}:\n")
            log.debug(f"mapping {i}: {elem.to_list()}")
            output_file.write(elem.to_string())
    log.info(f"orbit of size: {i}")

#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Gerald Hempel, Andres Goens

import os
import json
import logging
import random
import hydra
import numpy as np
import sys

from mocasin.design_centering import sample as dc_sample
from mocasin.design_centering import util as dc_util

log = logging.getLogger(__name__)


@hydra.main(config_path="../conf", config_name="find_design_center")
def dc_task(cfg):
    tp = dc_util.ThingPlotter()
    random.seed(cfg["random_seed"])
    np.random.seed(cfg["random_seed"])
    log.info(
        "Initialized random number generator. Seed: {"
        + str(cfg["random_seed"])
        + "}"
    )
    json_dc_dump = {}

    threshold = cfg["threshold"]
    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    oracle = hydra.utils.instantiate(
        cfg["design_centering"]["oracle"], graph, platform, trace, threshold
    )

    # starting volume (init):
    # this should be doable via hydra too
    if "starting_center" in cfg["design_centering"]["volume"]:
        starting_center = cfg["design_centering"]["volume"]["starting_center"]
    else:
        timeout = 0
        while timeout < cfg["design_centering"]["perturbation"]["max_iters"]:
            starting_center = representation.uniform()
            starting_center_sample = dc_sample.Sample(
                sample=representation.toRepresentation(starting_center),
                representation=representation,
            )
            oracle.validate_set([starting_center_sample])

            if starting_center_sample.getFeasibility():
                break
            else:
                timeout += 1

    if timeout == cfg["design_centering"]["perturbation"]["max_iters"]:
        log.error(
            f"could not find a feasible starting center after {timeout} iterations"
        )
        sys.exit(1)

    log.info(f"Starting with center: {starting_center.to_list()}")
    # center = dc_sample.Sample(center)

    v = hydra.utils.instantiate(
        cfg["design_centering"]["volume"],
        graph,
        platform,
        representation,
        starting_center,
    )
    sg = hydra.utils.instantiate(
        cfg["design_centering"]["sample_generator"], representation
    )
    dc = hydra.utils.instantiate(
        cfg["design_centering"]["algorithm"], v, oracle, sg, representation
    )
    center, history = dc.ds_explore()
    centers = history["centers"]
    samples = history["samples"]
    radii = history["radii"]
    # plot explored design space (in 2D)
    # if True:
    #    tp.plot_samples(dc.samples)
    log.info("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
    log.info("==== Design Centering done ====")

    json_dc_dump["center"] = {}
    json_dc_dump["center"]["mapping"] = center.getMapping().to_list()
    json_dc_dump["center"]["feasible"] = center.getFeasibility()
    json_dc_dump["center"]["runtime"] = (
        center.getSimContext().exec_time / 1000000000.0
    )
    # FIXME: This crashs with index out of range:
    # json_dc_dump['center']['radius'] = radii[-1]

    if cfg["record_samples"]:
        json_dc_dump["samples"] = {}

        for cent_idx, cent in enumerate(centers):
            json_dc_dump["samples"][cent_idx] = {"center": {}}
            json_dc_dump["samples"][cent_idx]["center"][
                "mapping"
            ] = cent.getMapping().to_list()
            json_dc_dump["samples"][cent_idx]["center"][
                "feasible"
            ] = cent.getFeasibility()
            json_dc_dump["samples"][cent_idx]["center"]["runtime"] = (
                cent.getSimContext().exec_time / 1000000000.0
            )
            json_dc_dump["samples"][cent_idx]["center"]["radius"] = radii[
                cent_idx
            ]

        n = cfg["adapt_samples"]

        for i, sample in enumerate(samples):
            idx = int(i / n)
            json_dc_dump["samples"][idx][i % n] = {
                "mapping": sample.getMapping().to_list()
            }
            json_dc_dump["samples"][idx][i % n][
                "feasible"
            ] = sample.getFeasibility()
            json_dc_dump["samples"][idx][i % n]["runtime"] = (
                sample.getSimContext().exec_time / 1000000000.0
            )

    # run perturbation test

    if cfg["run_perturbation"]:
        log.info("==== Run Perturbation Test ====")

        pm = hydra.utils.instantiate(
            cfg["design_centering"]["perturbation"],
            graph,
            platform,
            trace,
            representation,
            threshold,
        )

        map_set = pm.create_randomMappings()

        pert_res = []
        s, c = pm.run_perturbation(center.getMapping())
        pert_res.append(s)

        json_dc_dump["center"]["pert"] = c
        json_dc_dump["center"]["passed"] = s

        for i, m in enumerate(map_set):
            s, c = pm.run_perturbation(m)
            pert_res.append(s)
            json_dc_dump["rand mapping" + str(i)] = {}
            json_dc_dump["rand mapping" + str(i)]["mapping"] = m.to_list()
            json_dc_dump["rand mapping" + str(i)]["pert"] = c
            json_dc_dump["rand mapping" + str(i)]["passed"] = s

        if (
            bool(cfg["plot_perturbations"])
            and not os.environ.get("DISPLAY", "") == ""
        ):
            tp.plot_perturbations(pert_res, cfg["perturbations_out"])

        log.info("==== Perturbation Test done ====")

    log.info(f"total simulations from cache: {oracle.total_cached}")
    if not os.path.exists(cfg["out_dir"]):
        os.mkdir(cfg["out_dir"])
    with open(cfg["out_dir"] + "/dc_out.json", "w+") as dump:
        json.dump(json_dc_dump, dump, indent=4)

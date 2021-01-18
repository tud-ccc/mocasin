# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

import hydra

from mocasin.util.logging import getLogger
from mocasin.ontologies.solver import Solver

logger = getLogger(__name__)


@hydra.main(config_path="../conf", config_name="solve_query.yaml")
def solve_query(cfg):
    # TODO:
    # find a way to hand in a set of mappings on which equal_operations can be applied

    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    query = cfg["query"]
    vector = cfg["vector"]
    if (
        cfg["representation"]._target_
        != "mocasin.representations.SimpleVectorRepresentation"
    ):
        raise RuntimeError(
            f"The solve_query task needs to be called with the SimpleVector representation. Called with {cfg['representation']._target_}"
        )
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )

    solver = Solver(graph, platform, cfg)

    if not vector == "None":
        starting_vector = []

        for element in vector.split(","):
            starting_vector.append(int(element))

        result = solver.request(query, vec=starting_vector)

    else:
        result = solver.request(query)

    if not cfg["output_file"] == "None":
        # write result to file in simple vector representation
        output_file = open(cfg["output_file"], "w+")
        if not result:
            output_file.write("False")
        else:
            output_file.write("[")

            for processor in representation.toRepresentation(result):
                output_file.write(str(processor) + ", ")

            output_file.write("]")
        output_file.close()

    else:
        if not result:
            print("No result found.")
        else:
            print(representation.toRepresentation(result))

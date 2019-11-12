#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import hydra
import logging
import pynauty

import pykpn.representations.automorphisms as aut

log = logging.getLogger(__name__)


def platform_to_autgrp(cfg):
    """Calculate the Automorphism Group of a Platform Graph

    This task expects two hydra parameters to be available.


    **Hydra Parameters**:
        * **platform:** the input platform. The task expects a configuration
          dict that can be instantiated to a
          :class:`~pykpn.common.platform.Platform` object.
        * **out:** the output file
    """
    platform = hydra.utils.instantiate(cfg['platform'])
    log.info("start converting platform to edge graph for automorphisms.")
    plat_graph = platform.to_adjacency_dict()

    adjacency_dict, num_vertices, coloring, nodes_correspondence = aut.to_labeled_edge_graph(plat_graph)
    log.info("done converting platform to edge graph for automorphisms.")
    #print(nodes_correspondence)
    #print(coloring)
    #print(len(coloring))
    #print(str(edge_graph))
    log.info("start calculating the automorphism group of the (edge) graph with " + str(num_vertices) +  " nodes using nauty.")
    nautygraph = pynauty.Graph(num_vertices,True,adjacency_dict, coloring)
    autgrp_edges = pynauty.autgrp(nautygraph)
    log.info("done calculating the automorphism group of the (edge) graph using nauty.")

    log.info("start coverting automorhpism of edges to nodes.")
    autgrp, new_nodes_correspondence = aut.edge_to_node_autgrp(autgrp_edges[0],nodes_correspondence)
    permutations_lists = map(aut.list_to_tuple_permutation,autgrp)
    #permutations = map(perm.Permutation,permutations_lists)
    #permgrp = perm.PermutationGroup(list(permutations))
    #print(permgrp.point_orbit(0))
    log.info("done coverting automorhpism of edges to nodes.")

    log.info("start writing to file.")
    with open(cfg['out'], 'w') as f:
        f.write("Platform Graph:")
        f.write(str(plat_graph))
        #f.write("Edge Group with ~" + str(autgrp_edges[1]) + " * 10^" + str(autgrp_edges[2]) + " elements.\n")
        f.write("Symmetry group generators:")
        f.write(str(list(permutations_lists)))
        f.write("\nCorrespondence:")
        f.write(str(new_nodes_correspondence))
    log.info("done writing to file.")

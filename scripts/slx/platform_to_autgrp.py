#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens
"""Calculate the Automorphism Group of a Platform Graph

This script takes expects to positional arguments: an xml file describing a
platform in the SLX format, e.g. apps/audio_filter/exynos/exynos.platform
and an output file, where the automorphism group of the platform graph will be
placed. 
"""


import argparse
import sys

import pynauty as pynauty

from pykpn.util import logging
from pykpn.slx.platform import SlxPlatform
import pykpn.representations.automorphisms as aut


log = logging.getLogger(__name__)


def main(argv):
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('platform', help="xml platform description", type=str)
    parser.add_argument('out', help="output file for automorphism group", type=str)
    parser.add_argument('--slx-version', help="silexica version", type=str,
                        default='2017.04')

    args = parser.parse_args(argv)

    logging.setup_from_args(args)
    cfg = {
        'platform_xml': args.platform,
        'slx_version' : args.slx_version,
        'out' : args.out
    }
    log.warning('Using this script is deprecated. Use the pykpn_manager instead.')
    platform_to_autgrp(cfg)

def platform_to_autgrp(cfg):
    platform = SlxPlatform('SlxPlatform', cfg['platform_xml'], cfg['slx_version'])
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


if __name__ == '__main__':
    main(sys.argv[1:])

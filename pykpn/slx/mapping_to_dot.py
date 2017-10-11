#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse

from pykpn.common import logging
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.mapping import SlxMapping
from pykpn.slx.platform import SlxPlatform


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('graph', help="xml description of the kpn graph",
                        type=str)
    parser.add_argument('platform', help="xml description of the platform",
                        type=str)
    parser.add_argument('mapping', help="xml description of the mapping",
                        type=str)
    parser.add_argument('dot', help="dot output file", type=str)

    args = parser.parse_args()

    logging.setup_from_args(args)

    graph = SlxKpnGraph('app', args.graph)
    platform = SlxPlatform(args.platform)
    mapping = SlxMapping(graph, platform, args.mapping)
    dot = mapping.to_pydot()
    dot.write_raw(args.dot)


if __name__ == '__main__':
    main()

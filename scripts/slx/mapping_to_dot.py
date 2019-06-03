#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import sys

from pykpn.util import logging
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.mapping import SlxMapping
from pykpn.slx.platform import SlxPlatform


log = logging.getLogger(__name__)


def main(argv):
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('graph', help="xml description of the kpn graph",
                        type=str)
    parser.add_argument('platform', help="xml description of the platform",
                        type=str)
    parser.add_argument('mapping', help="xml description of the mapping",
                        type=str)
    parser.add_argument('dot', help="dot output file", type=str)
    parser.add_argument('--slx-version', help="dot output file", type=str,
                        default='2017.04')

    args = parser.parse_args(argv)

    logging.setup_from_args(args)

    graph = SlxKpnGraph('app', args.graph, args.slx_version)
    platform = SlxPlatform('platform', args.platform, args.slx_version)
    mapping = SlxMapping(graph, platform, args.mapping, args.slx_version)
    dot = mapping.to_pydot()
    dot.write_raw(args.dot)


if __name__ == '__main__':
    main(sys.argv[1:])

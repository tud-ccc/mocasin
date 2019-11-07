#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


"""Generate a dot graph representing the mapping of a KPN application to a platform

This script expects four positional arguments: a KPN graph xml file, a platform
xml, a mapping xml file and the output file.
"""


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
                        default='2017.10')

    args = parser.parse_args(argv)

    logging.setup_from_args(args)
    log.warn('Using this script is deprecated. Use the pykpn_manager instead.')
    cfg = {
        'cpn_xml' : args.graph,
        'platform_xml' : args.platform,
        'mapping_xml' : args.mapping,
        'slx_version' : args.slx_version,
        'dot' : args.dot
    }
    mapping_to_dot(cfg)

def mapping_to_dot(cfg):
    print(cfg['cpn_xml'])
    print(cfg['slx_version'])
    print(cfg['platform_xml'])
    print(cfg['mapping_xml'])

    graph = SlxKpnGraph('app', cfg['cpn_xml'], cfg['slx_version'])
    platform = SlxPlatform('platform', cfg['platform_xml'], cfg['slx_version'])
    mapping = SlxMapping(graph, platform, cfg['mapping_xml'], cfg['slx_version'])
    dot = mapping.to_pydot()
    dot.write_raw(cfg['dot'])


if __name__ == '__main__':
    main(sys.argv[1:])

#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import argparse

from pykpn.util import logging
from pykpn.representations.representations import RepresentationType
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
    parser.add_argument('out', help="output file",
                        type=str)
    parser.add_argument('--slx-version', help="SLX Version", type=str,
                        default='2017.10')

    args = parser.parse_args()

    logging.setup_from_args(args)
    log.warn('Using this script is deprecated. Use the pykpn_manager instead.')
    cfg = {
        'cpn_xml'  : args.graph,
        'platform_xml'  : args.platform,
        'mapping_xml'  : args.mapping,
        'slx_version': args.slx_version,
        'out': args.out
    }
    enumerate_equivalent(cfg)

def enumerate_equivalent(cfg):
    kpn = SlxKpnGraph('app', cfg['cpn_xml'], cfg['slx_version'])
    platform = SlxPlatform('platform', cfg['platform_xml'], cfg['slx_version'])
    mapping = SlxMapping(kpn, platform, cfg['mapping_xml'], cfg['slx_version'])
    representation = RepresentationType['Symmetries'].getClassType()(kpn,platform)
    log.info(("calculating orbit for mapping:" + str(mapping.to_list())))
    orbit = representation.allEquivalent(mapping.to_list())
    log.info("orbit of size: " + str(len(orbit)))
    with open(cfg['out'],'w') as output_file:
        for i,elem in enumerate(orbit):
            output_file.write(f"\n mapping {i}:\n")
            output_file.write(mapping.to_string())


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""Generate a dot graph from a SLX platform xml

This script expects two positional arguments: a platform xml file such as
apps/audio_filter/exynos/exynos.platform and an output file. The script parses
the xml file and produces a dot graph that visualizes the given platform.
"""

import argparse
import sys

from pykpn.util import logging
from pykpn.slx.platform import SlxPlatform


log = logging.getLogger(__name__)


def main(argv):
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('platform', help="xml platform description", type=str)
    parser.add_argument('dot', help="dot output file", type=str)
    parser.add_argument('--slx-version', help="silexica version", type=str,
                        default='2017.04')

    args = parser.parse_args(argv)

    logging.setup_from_args(args)

    cfg = {
        'platform_xml'  : args.platform,
        'slx_version'  : args.slx_version,
        'dot' : args.dot
    }
    log.warn('Using this script is deprecated. Use the pykpn_manager instead.')
    platform_to_dot(cfg)

def platform_to_dot(cfg):

    platform = SlxPlatform('SlxPlatform', cfg['platform_xml'], cfg['slx_version'])
    dot = platform.to_pydot()
    dot.write_raw(cfg['dot'])


if __name__ == '__main__':
    main(sys.argv[1:])

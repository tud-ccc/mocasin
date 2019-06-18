#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""Generate a dot graph from a SLX cpn xml

This script expects two positional arguments: a cpn xml file such as
apps/audio_filter.cpn.xml and an output file. The script parses the xml file
and produces a dot graph that visualizes the given KPN application.
"""


import argparse
import sys

from pykpn.util import logging
from pykpn.slx.kpn import SlxKpnGraph


log = logging.getLogger(__name__)


def main(argv):
    parser = argparse.ArgumentParser(
        description="Generate a dot graph visualizing a KPN application")

    logging.add_cli_args(parser)

    parser.add_argument('kpn', help="xml kpn graph description", type=str)
    parser.add_argument('dot', help="dot output file", type=str)
    parser.add_argument('--slx-version', help="dot output file", type=str,
                        default='2017.04')

    args = parser.parse_args(argv)

    logging.setup_from_args(args)

    kpn = SlxKpnGraph('app', args.kpn, args.slx_version)
    dot = kpn.to_pydot()
    dot.write_raw(args.dot)


if __name__ == '__main__':
    main(sys.argv[1:])
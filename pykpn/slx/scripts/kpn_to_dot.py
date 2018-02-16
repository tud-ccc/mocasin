#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse

from pykpn.common import logging
from pykpn.slx.kpn import SlxKpnGraph


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('kpn', help="xml kpn graph description", type=str)
    parser.add_argument('dot', help="dot output file", type=str)
    parser.add_argument('--slx-version', help="dot output file", type=str,
                        default='2017.04')

    args = parser.parse_args()

    logging.setup_from_args(args)

    kpn = SlxKpnGraph('app', args.kpn, args.slx_version)
    dot = kpn.to_pydot()
    dot.write_raw(args.dot)


if __name__ == '__main__':
    main()

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

    parser.add_argument(
        '-v',
        '--verbosity',
        action="count",
        help="increase output verbosity (e.g., -vv is more than -v)",
        dest='verbosity')

    parser.add_argument('kpn', help="xml kpn graph description", type=str)
    parser.add_argument('dot', help="dot output file", type=str)

    args = parser.parse_args()

    if args.verbosity is not None:
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbosity >= 1:
            logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    kpn = SlxKpnGraph('app', args.kpn)
    dot = kpn.to_pydot()
    dot.write_raw(args.dot)


if __name__ == '__main__':
    main()

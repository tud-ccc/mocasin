#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import logging

import simpy

from platforms import Tomahawk2Platform
from . import System
from slx import SlxKpnGraph
from slx import SlxMapping
from slx import SlxTraceReader


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v',
        '--verbosity',
        action="count",
        help="increase output verbosity (e.g., -vv is more than -v)",
        dest='verbosity')

    parser.add_argument('mapping')
    parser.add_argument('pngraph')
    parser.add_argument('tracedir')

    args = parser.parse_args()

    if args.verbosity is not None:
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbosity >= 1:
            logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Create a simpy environment
    env = simpy.Environment()

    # Create the platform
    platform = Tomahawk2Platform(env)

    # Create an Application
    application = SlxKpnGraph('app', args.pngraph)

    # Creat the mapping
    mapping = SlxMapping(args.mapping)

    # Create the system
    system = System(env, platform, application, mapping, args.tracedir,
                    SlxTraceReader)

    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import argparse
import logging

from slx import SlxMapping
from tomahawk import Tomahawk2Platform
from slx import SlxApplication
from pytrm import System


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

    # Create the platform
    platform = Tomahawk2Platform()

    # Create an Application
    application = SlxApplication('app', args.pngraph)

    # Creat the mapping
    mapping = SlxMapping(args.mapping)

    # Create the system
    system = System(platform, application, mapping, args.tracedir)

    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

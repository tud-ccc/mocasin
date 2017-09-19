#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import logging

from pykpn.simulate import RuntimeApplication
from pykpn.simulate import RuntimeSystem
from pykpn.slx import SlxConfig


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v',
        '--verbosity',
        action="count",
        help="increase output verbosity (e.g., -vv is more than -v)",
        dest='verbosity')

    parser.add_argument('configFile', nargs=1,
                        help="input configuration file", type=str)

    args = parser.parse_args()

    if args.verbosity is not None:
        if args.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbosity >= 1:
            logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Declare the list of applications
    applications = []

    # parse the config file
    config = SlxConfig(args.configFile)

    for an in config.app_names:
        app = RuntimeApplication(
            an, config.graphs[an], config.mappings[an],
            config.trace_readers[an], config.start_times[an])
        applications.append(app)

        if config.mapping_to_dot[an] is not None:
            config.mappings[an].outputDot(config.mapping_to_dot[an])
    # Create the system
    system = RuntimeSystem(config.vcd_file_name, config.platform,
                           config.graphs, applications)
    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

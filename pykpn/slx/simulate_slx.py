#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import simpy

from pykpn.simulate import RuntimeKpnApplication
from pykpn.simulate import RuntimeSystem
from pykpn.slx import SlxConfig
import pykpn.common.logging as logging


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('configFile', nargs=1,
                        help="input configuration file", type=str)

    args = parser.parse_args()

    logging.setup_from_args(args)

    # Declare the list of applications
    applications = []

    # parse the config file
    config = SlxConfig(args.configFile)

    env = simpy.Environment()

    for an in config.app_names:
        app = RuntimeKpnApplication(
            an, config.graphs[an], config.mappings[an],
            env, config.start_times[an])
        applications.append(app)

    # Create the system
    system = RuntimeSystem(config.platform, applications, env)
    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

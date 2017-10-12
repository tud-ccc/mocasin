#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse

import simpy

from pykpn.common import logging
from pykpn.slx.config import SlxSimulationConfig
from pykpn.slx.system import SlxRuntimeSystem


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('configFile', nargs=1,
                        help="input configuration file", type=str)

    args = parser.parse_args()

    logging.setup_from_args(args)

    # parse the config file
    config = SlxSimulationConfig(args.configFile)

    # Create the system
    env = simpy.Environment()
    system = SlxRuntimeSystem(config, env)

    # Run the simulation
    system.simulate()

    system.check_errors()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import timeit

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

    try:
        # parse the config file
        config = SlxSimulationConfig(args.configFile)

        # Create the system
        env = simpy.Environment()
        system = SlxRuntimeSystem(config, env)

        # Run the simulation
        start = timeit.default_timer()
        system.simulate()
        stop = timeit.default_timer()

        exec_time = float(env.now) / 1000000000.0
        print('Total simulated time: ' + str(exec_time) + ' ms')
        print('Total simulation time: ' + str(stop - start) + ' s')

        system.check_errors()
    except Exception as e:
        log.exception(str(e))
        if hasattr(e, 'details'):
            log.info(e.details())


if __name__ == '__main__':
    main()

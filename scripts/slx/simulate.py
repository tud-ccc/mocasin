#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import argparse
import sys
import timeit

import simpy

from pykpn.util import logging
from pykpn.slx.config import SlxSimulationConfig
from pykpn.slx.system import SlxRuntimeSystem


log = logging.getLogger(__name__)


"""Run simulation based on a config file.

This script expects a configuration file as the first positional argument.
It constructs a system according to this configuration and simulates
it. Finally, the script reports the simulated execution time.

See apps/audio_filter/exynos/config.ini for an example configuration.
"""


def main(argv):

    parser = argparse.ArgumentParser(
        description="Run simulation based on a config file")

    logging.add_cli_args(parser)

    parser.add_argument('configFile', nargs=1,
                        help="input configuration file", type=str)

    args = parser.parse_args(argv)

    logging.setup_from_args(args)
    log.warning('Using this script is deprecated. Use the pykpn_manager instead.')
    simulate(args.configFile)

def simulate(config_dict=None, config_file=None):
    try:
        # parse the config file
        config = SlxSimulationConfig(config_file,config_dict)

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
    main(sys.argv[1:])

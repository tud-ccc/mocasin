#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel

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
            log.info(e.details()
            )

def run_simulation(sim_context):
    #Create simulation environment
    env = simpy.Environment()

    #Create applications
    applications = []
    mappings = {}
    for ac in sim_context.app_context:
        app = RuntimeKpnApplication(ac.name, ac.kpn, ac.mapping, ac.trace_reader, env, ac.start_time)
        applications.append(app)
        mappings[ac.name] = ac.mapping

    #Create the system
    system = RuntimeSystem(sim_context.platform, applications, env)

    #Run simulation
    system.simulate()
    system.check_errors()

    sim_context.exec_time = env.now

    return sim_context


if __name__ == '__main__':
    main()


#/slx_random_walk -V ~/misc_code/kpn-apps/audio_filter/parallella/config.ini /tmp -n5000

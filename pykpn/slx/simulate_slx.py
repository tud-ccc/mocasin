#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse

import simpy

import pykpn.common.logging as logging
from pykpn.simulate import RuntimeKpnApplication, RuntimeSystem
from pykpn.simulate.process import ProcessState
from pykpn.slx import SlxConfig


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
            config.trace_readers[an], env, config.start_times[an])
        applications.append(app)

    # Create the system
    system = RuntimeSystem(config.platform, applications, env)
    # Run the simulation
    system.simulate()

    for app in applications:
        some_blocked = False
        for p in app.processes():
            if p.check_state(ProcessState.BLOCKED):
                log.error('The process %s is blocked', p.name)
                some_blocked = True
            elif not p.check_state(ProcessState.FINISHED):
                log.warn('The process %s did not finish its execution!',
                         p.name)
        if some_blocked:
            log.error('The application %s is deadlocked!', app.name)


if __name__ == '__main__':
    main()

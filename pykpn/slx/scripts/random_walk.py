#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import os
import timeit

import simpy

from ..kpn import SlxKpnGraph
from ..platform import SlxPlatform
from ..trace import SlxTraceReader
from pykpn import slx
from pykpn.common import logging
from pykpn.mapper.random import RandomMapping
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
from pykpn.slx.config import SlxSimulationConfig


import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('configFile', nargs=1,
                        help="input configuration file", type=str)

    parser.add_argument(
        '-n',
        '--num-iterations',
        type=int,
        help='number of iterations to perform (default: 1000)',
        dest='num_iterations',
        default=1000)

    args = parser.parse_args()

    logging.setup_from_args(args)

    num_iterations = args.num_iterations

    try:
        # parse the config file
        config = SlxSimulationConfig(args.configFile)

        slx.set_version(config.slx_version)

        # create the platform
        platform_name = os.path.splitext(
            os.path.basename(config.platform_xml))[0]
        platform = SlxPlatform(platform_name, config.platform_xml)

        # create all graphs
        kpns = {}
        for app_config in config.applications:
            app_name = app_config.name
            kpns[app_name] = SlxKpnGraph(app_name, app_config.cpn_xml)

        results = []
        start = timeit.default_timer()
        for i in range(0, num_iterations):
            # create the mappings
            mappings = {}
            for app_config in config.applications:
                app_name = app_config.name
                mappings[app_name] = RandomMapping(kpns[app_name], platform)

            # Simulation Environment
            env = simpy.Environment()

            # create the applications
            applications = []
            for app_config in config.applications:
                app_name = app_config.name
                trace_reader = SlxTraceReader.factory(
                    app_config.trace_dir, '%s.' % (app_config.name))
                app = RuntimeKpnApplication(app_name, kpns[app_name],
                                            mappings[app_name], trace_reader,
                                            env, app_config.start_at_tick)
                applications.append(app)

            # Create the system
            system = RuntimeSystem(platform, applications, env)

            # Run the simulation
            system.simulate()

            system.check_errors()

            results.append((env.now, mappings))

        best_result = results[0]
        for r in results:
            if r[0] < best_result[0]:
                best_result = r

        stop = timeit.default_timer()
        print('Tried %d random mappings in %0.1fs' %
              (num_iterations, stop - start))
        exec_time = float(best_result[0] / 1000000000.0)
        print('Best simulated execution time: %0.1fms' % (exec_time))

    except Exception as e:
        log.exception(str(e))
        if hasattr(e, 'details'):
            log.info(e.details())


if __name__ == '__main__':
    main()

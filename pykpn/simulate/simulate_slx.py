#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import logging
import simpy
import os
import configparser

from pykpn.platforms import Tomahawk2Platform
from pykpn.platforms import GenericNocPlatform
from pykpn.simulate import System
from pykpn.simulate import Application
from pykpn.simulate import SlxConfig
from pykpn.slx import SlxKpnGraph
from pykpn.slx import SlxMapping
from pykpn.slx import SlxTraceReader


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v',
        '--verbosity',
        action="count",
        help="increase output verbosity (e.g., -vv is more than -v)",
        dest='verbosity')

    reqNamed = parser.add_argument_group('required named arguments')

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
    # Declare the list of applications
    applications=[]
    # Create the platform
    config=SlxConfig('config.ini')
    for i in config.applications:
        if i not in config.conf:
            raise ValueError("application name does not match to the section key")
        # Create a graph
        graph = SlxKpnGraph(i+'_graph', config.get_graph(i))

        # Create the mapping
        mapping = SlxMapping(graph, config.get_platform(), config.get_mapping(i))

        # Create the application
        readers = {}
        for pm in mapping.processMappings:
            name = pm.kpnProcess.name

            processors = pm.scheduler.processors
            type = processors[0].type

            for p in processors:
                if p.type != type:
                    log.warn(pm.kpnProcess.scheduler + ' schedules on ' +
                             'processors of different types. Use ' + type +
                             'for reading the process trace of ' + name)

            path = os.path.join(config.get_trace(i),
                                name + '.' + type + '.cpntrace')
            assert os.path.isfile(path)
            readers[name] = SlxTraceReader(path, i)
        app = Application(i, graph, mapping, readers, config.get_ini_time(i))
        applications.append(app)

        if config.get_mappingout(i):
            mapping.outputDot(config.get_mappingout(i))
        else:
            config.conf[i]['mappingout']=''

    # Create the system
    system = System(env, config, applications)
    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

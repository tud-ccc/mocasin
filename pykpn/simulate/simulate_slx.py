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
    config=configparser.ConfigParser()
    config.read('config.ini')

    # Declare the list of applications
    applications=[]
    # Create the platform
    if config['simulation']['platform'] is None:
        raise ValueError('Define the platform')

    elif config['simulation']['platform'][0:config['simulation']['platform'].find('_')]=='generic':
        temp1=config['simulation']['platform'].find('_')
        temp2=config['simulation']['platform'][temp1+1:].find('_')
        architecture=config['simulation']['platform'][temp1+1:temp1+temp2+1]
        x=int(config['simulation']['platform'][-1])
        y=int(config['simulation']['platform'][-3])
        platform = GenericNocPlatform(env, architecture, x, y)

    elif config['simulation']['platform']=='tomahawk2':
        platform = Tomahawk2Platform(env)

    else:
        raise ValueError('Platform does not exist')

    apps=config['simulation']['applications'].split(",")
    for i in range(len(apps)):
        if apps[i] not in config:
            raise ValueError("application name does not match to the section key")
        # Create a graph
        graph = SlxKpnGraph('graph'+str(i), config[apps[i]]['graph'])

        # Create the mapping
        mapping = SlxMapping(graph, platform, config[apps[i]]['mapping'])

        # Create the application
        app_name = apps[i]

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

            path = os.path.join(config[apps[i]]['trace'],
                                name + '.' + type + '.cpntrace')
            assert os.path.isfile(path)
            readers[name] = SlxTraceReader(path, app_name)

        app = Application(app_name, graph, mapping, readers)
        applications.append(app)

        if 'mappingout' not in config[apps[i]]:
            config[apps[i]]['mappingout']=''
        if config[apps[i]]['mappingout']:
            mapping.outputDot(config[apps[i]]['mappingout'] + '.' + app_name + '.dot')

    # Create the system
    system = System(env, platform, applications, config['simulation']['vcd'])
    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

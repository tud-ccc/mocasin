#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import logging
import simpy

from pykpn.platforms import Tomahawk2Platform
from pykpn.platforms import GeneralPlatform
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

    reqNamed.add_argument('-g', '--graph', nargs='+',
                          help='List of SLX PN graph descriptor files',
                          required=True)
    reqNamed.add_argument('-m', '--mapping', nargs='+',
                          help='List of SLX mapping descriptor files',
                          required=True)
    reqNamed.add_argument('-t', '--tracedir', nargs='+',
                          help='List of directories conataing SLX trace files',
                          required=True)
    parser.add_argument("--mappingout", metavar="PREFIX", type=str,
                        help="Graphviz output for mapping visualization")
    parser.add_argument('--vcd', type=str,
                        help="dump simulation state to a vcd file")
    parser.add_argument('--platform', type=str,
                        help="Platform name and dimensions")

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
    if args.platform is None:
        raise ValueError('Define the platform')

    elif args.platform[0:args.platform.find('_')]=='generic':
        temp1=args.platform.find('_')
        temp2=args.platform[temp1+1:].find('_')
        architecture=args.platform[temp1+1:temp1+temp2+1]
        x=int(args.platform[-1])
        y=int(args.platform[-3])
        platform = GeneralPlatform(env, architecture, x, y)

    elif args.platform=='tomahawk2':
        platform = Tomahawk2Platform(env)

    else:
        raise ValueError('Platform does not exist')

    for i in range(len(args.mapping)):

        # Create a graph
        graph = SlxKpnGraph('graph'+str(i), args.graph[i])

        # Create the mapping
        mapping = SlxMapping(args.mapping[i])

        # Create the application
        app_name = 'app'+str(i)
        app = Application(app_name, graph, mapping, args.tracedir[i], SlxTraceReader)
        applications.append(app)

        if args.mappingout:
            mapping.outputDot(graph, args.mappingout + '.' + app_name + '.dot')
    # Create the system
    system = System(env, platform, applications, args.vcd)
    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

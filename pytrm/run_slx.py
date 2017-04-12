#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import argparse
import logging
import simpy

from platforms import Tomahawk2Platform
from pytrm import System
from pytrm import Application
from slx import SlxKpnGraph
from slx import SlxMapping
from slx import SlxTraceReader


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
    platform = Tomahawk2Platform(env)

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

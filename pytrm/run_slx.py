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

    parser.add_argument('-mapping', nargs='+')
    parser.add_argument('-pngraph', nargs='+')
    parser.add_argument('-tracedir', nargs='+')
    parser.add_argument("--mappingout", metavar="mapping output dot", type=str,
                           help = "Graphviz output for mapping visualization")
    parser.add_argument('-dump_on', dest='dump', action='store_true')
    parser.add_argument('-dump_off', dest='dump', action='store_false')
    parser.set_defaults(dump=True)

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
        graph = SlxKpnGraph('graph'+str(i), args.pngraph[i])

        # Create the mapping
        mapping = SlxMapping(args.mapping[i])

        # Create the application
        app_name = 'app'+str(i)
        app = Application(app_name, graph, mapping, args.tracedir[i], SlxTraceReader)
        applications.append(app)

        if args.mappingout:
            mapping.outputDot(app, args.mappingout + app_name + '.dot')

    # Create the system
    system = System(env, platform, applications, args.dump)
    # Run the simulation
    system.simulate()


if __name__ == '__main__':
    main()

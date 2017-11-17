#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


import argparse
import multiprocessing as mp
import os
import timeit

import simpy

from ..config import SlxSimulationConfig
from ..kpn import SlxKpnGraph
from ..mapping import export_slx_mapping
from ..platform import SlxPlatform
from ..trace import SlxTraceReader
from pykpn import slx
from pykpn.common import logging
from pykpn.mapper.random import RandomMapping
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
from pykpn.util import plot


log = logging.getLogger(__name__)


class ApplicationContext(object):

    def __init__(self, name=None, kpn=None, mapping=None, trace_reader=None,
                 start_time=None):
        self.name = name
        self.kpn = kpn
        self.mapping = mapping
        self.trace_reader = trace_reader
        self.start_time = start_time


class SimulationContext(object):

    def __init__(self, platform=None, app_contexts=None):
        self.platform = platform
        if app_contexts is None:
            self.app_contexts = []
        else:
            self.app_contexts = app_contexts
        self.exec_time = None


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('config', nargs=1,
                        help="input configuration file", type=str)

    parser.add_argument('outdir',
                        help="output directory", type=str)

    parser.add_argument(
        '-j',
        '--jobs',
        type=int,
        help='number of parallel jobs',
        dest='jobs',
        default=mp.cpu_count())

    parser.add_argument(
        '-n',
        '--num-iterations',
        type=int,
        help='number of iterations to perform (default: 1000)',
        dest='num_iterations',
        default=1000)

    parser.add_argument(
        '-d',
        '--plot-distribution',
        action='store_true',
        help='plot the distribution of execution times (requires matplotlib)',
        dest='plot_distribution')

    parser.add_argument(
        '-p',
        '--progess',
        action='store_true',
        help='show a progress bar and ETA (requires tqdm)',
        dest='progress')

    parser.add_argument(
        '-V',
        '--visualize',
        action='store_true',
        help='show a visualization of the searched space using t-SNE',
        dest='visualize')

    parser.add_argument(
        '--export-all',
        action='store_true',
        help='export all random mappings to <outdir>',
        dest='export_all')

    args = parser.parse_args()

    logging.setup_from_args(args)

    num_iterations = args.num_iterations

    try:
        # parse the config file
        config = SlxSimulationConfig(args.config)

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

        start = timeit.default_timer()

        # Create a list of 'simulations'. These are later executed by multiple
        # worker processes.
        simulations = []
        for i in range(0, num_iterations):

            # create a simulation context
            sim_context = SimulationContext(platform)

            # create the application contexts
            for app_config in config.applications:
                name = app_config.name
                kpn = kpns[name]
                app_context = ApplicationContext(name, kpn)

                app_context.start_time = app_config.start_at_tick

                # generate a random mapping
                app_context.mapping = RandomMapping(kpn, platform)

                # create the trace reader
                app_context.trace_reader = SlxTraceReader.factory(
                    app_config.trace_dir, '%s.' % (name))

                sim_context.app_contexts.append(app_context)

            simulations.append(sim_context)

        # run the simulations and search for the best mapping
        pool = mp.Pool(processes=args.jobs)

        # execute the simulations in parallel
        if args.progress:
            import tqdm
            results = list(tqdm.tqdm(pool.imap(run_simualtion, simulations,
                                               chunksize=10),
                                     total=num_iterations))
        else:
            results = list(pool.map(run_simualtion, simulations, chunksize=10))

        # calculate the execution times in milliseconds and look for the best
        # result
        best_result = results[0]
        exec_times = []  # keep a list of exec_times for later
        for r in results:
            exec_times.append(float(r.exec_time / 1000000000.0))
            if r.exec_time < best_result.exec_time:
                best_result = r

        # When we reach this point, all simulations completed

        stop = timeit.default_timer()
        print('Tried %d random mappings in %0.1fs' %
              (len(results), stop - start))
        exec_time = float(best_result.exec_time / 1000000000.0)
        print('Best simulated execution time: %0.1fms' % (exec_time))

        # export the best mapping
        outdir = args.outdir
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        for ac in best_result.app_contexts:
            mapping_name = '%s.best.mapping' % (ac.name)
            export_slx_mapping(ac.mapping, os.path.join(outdir, mapping_name))

        # export all mappings if requested
        idx = 1
        if args.export_all:
            for r in results:
                for ac in r.app_contexts:
                    mapping_name = '%s.rnd_%08d.mapping' % (ac.name, idx)
                    export_slx_mapping(ac.mapping,
                                       os.path.join(outdir, mapping_name))
                idx += 1

        # plot result distribution
        if args.plot_distribution:
            import matplotlib.pyplot as plt
            # exec time in milliseconds
            plt.hist(exec_times, bins=int(num_iterations/20), normed=True)
            plt.yscale('log', nonposy='clip')
            plt.title("Mapping Distribution")
            plt.xlabel("Execution Time [ms]")
            plt.ylabel("Probability")
            plt.show()

        # visualize searched space
        if args.visualize:
            if len(results[0].app_contexts) > 1:
                raise RuntimeError('Search space visualization only works '
                                   'for single application mappings')
            mappings = [r.app_contexts[0].mapping for r in results]
            plot.visualize_mapping_space(mappings, exec_times)

    except Exception as e:
        log.exception(str(e))
        if hasattr(e, 'details'):
            log.info(e.details())


def run_simualtion(sim_context):
    # Create simulation environment
    env = simpy.Environment()

    # create the applications
    applications = []
    mappings = {}
    for ac in sim_context.app_contexts:
        app = RuntimeKpnApplication(ac.name, ac.kpn, ac.mapping,
                                    ac.trace_reader, env, ac.start_time)
        applications.append(app)
        mappings[ac.name] = ac.mapping

    # Create the system
    system = RuntimeSystem(sim_context.platform, applications, env)

    # run the simulation
    system.simulate()
    system.check_errors()

    sim_context.exec_time = env.now

    return sim_context


if __name__ == '__main__':
    main()

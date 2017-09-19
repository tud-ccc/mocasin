# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
import timeit
import os
import simpy

from operator import itemgetter
from vcd import VCDWriter
from .channel import Channel
from .process import Process
from .scheduler import RuntimeScheduler

from simpy.resources.resource import Resource

log = logging.getLogger(__name__)


class RuntimeSystem:
    '''
    This is the central class for managing a simulation. It contains the
    simulation environment, the entire platform, and all applications running
    on top of it.
    '''

    def __init__(self, vcd, platform, graphs, applications):
        self.env = simpy.Environment()
        self.platform = platform
        self.applications = applications
        self.schedulers = []
        self.channels = {}
        self.start_times = []
        self.pair = {}
        self.graphs = graphs

        if vcd:
            self.vcd_writer = VCDWriter(
                open(vcd, 'w'), timescale='1 ps', date='today')
        else:
            self.vcd_writer = VCDWriter(
                open(os.devnull, 'w'), timescale='1 ps', date='today')
            self.vcd_writer.dump_off(self.env.now)

        log.info('Start initializing the system.')

        for app in self.applications:
            self.start_times.append([app, int(app.start_at_tick)])
            log.debug('  Load application: ' + app.name)
            for cm in app.mapping.channelMappings:
                name = app.name + '.' + cm.kpnChannel.name
                log.debug('    Create channel: ' + name)
                self.channels[name] = Channel(name, self, cm, self.graphs[app.name])

            for pm in app.mapping.processMappings:
                name = app.name + '.' + pm.kpnProcess.name
                log.debug('    Create process: ' + name)
                process = Process(name, self, pm,
                                  app.trace_readers[pm.kpnProcess.name])

                log.debug('      it uses the scheduler ' + pm.scheduler.name)

                scheduler = self.findScheduler(pm.scheduler.name)
                if scheduler is not None:
                    log.debug('      The scheduler was already created -> ' +
                              'append process')

                    if scheduler.policy != pm.policy:
                        log.warn('The scheduler ' + pm.scheduler.name +
                                 ' was already created but uses the ' +
                                 scheduler.policy + ' instead of the ' +
                                 'requested ' + pm.policy + ' policy')
                    self.pair[scheduler].append(process)
                else:
                    log.debug('    Create scheduler: ' + pm.scheduler.name)
                    scheduler = RuntimeScheduler(self, [], pm.policy,
                                                 pm.scheduler)
                    self.schedulers.append(scheduler)
                    self.pair[scheduler] = [process]

        # We iterate over all channels and their cost models to get all
        # communication resources that are required for simulation. For each
        # communication resource we create a simpy resource object and extend
        # the communication reource by an attribute 'simpy_resource' that
        # points to the simpy resource.
        #
        # This is not the best solution (TM) but does the job of decoupling
        # the platform description and simulation.
        for key, c in self.channels.items():
            for phase in c.primitive.consume + c.primitive.produce:
                for r in phase.resources:
                    if r.exclusive and not hasattr(r, 'simpy_resource'):
                        r.simpy_resource = Resource(self.env, capacity=1)

        log.info('Done initializing the system.')

    def simulate(self):
        print('=== Start Simulation ===')
        start = timeit.default_timer()

        self.env.process(self.run())

        # start the schedulers
        for scheduler in self.schedulers:
            self.env.process(scheduler.run())

        self.env.run()

        stop = timeit.default_timer()

        print('=== End Simulation ===')
        exec_time = float(self.env.now) / 1000000000.0
        print('Total execution time: ' + str(exec_time) + ' ms')
        print('Total simulation time: ' + str(stop - start) + ' s')
        self.vcd_writer.close()

    def findScheduler(self, name):
        for s in self.schedulers:
            if s.name == name:
                return s
        return None

    def run(self):
        self.start_times = sorted(self.start_times, key=itemgetter(1))
        # applications sorted according to their initialization times in a list
        # [application, initialization time]

        time_delay = [self.start_times[0][1]] + \
                     [self.start_times[i][1] - self.start_times[i - 1][1]
                      for i in range(1, len(self.start_times))]
        # the differences in the initialization times of succesive applications

        for i in time_delay:
            yield(self.env.timeout(i))  # delay till the start time is reached
            log.info('{0:19}'.format(self.env.now)
                     + ": Start application " +
                     self.start_times[0][0].name)
            for s in self.pair:
                # self.pair contains scheduler and processes key value pair
                # **scheduler={process1, process2,...}
                for l in self.pair[s]:  # l is the process
                    if l.name[0:4] == self.start_times[0][0].name:
                        # check if process name has the application name
                        # as in the start_times list
                        s.assignProcess(l)
            self.start_times.pop(0)

    def Migrate_ProcessToScheduler(self, process, scheduler):
        for s in self.pair:
            if s.name == scheduler:
                scheduler = s

        for s in self.pair:
            for l in self.pair[s]:
                if l.name == process:
                    self.pair[scheduler].append(l)
                    scheduler.assignProcess(l)
                    self.pair[s].remove(l)
                    if l in s.processes:
                        s.processes.remove(l)
                    else:
                        raise ValueError("The process hasn't initiated yet")

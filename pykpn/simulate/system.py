# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
import timeit
import os
from vcd import VCDWriter
from .channel import Channel
from .process import Process
from .scheduler import Scheduler

from simpy.resources.resource import Resource

log = logging.getLogger(__name__)


class System:
    '''
    This is the central class for managing a simulation. It contains the
    entire platform and all applications running on it.
    '''

    def __init__(self, env, platform, applications, dump):
        self.env = env
        self.platform = platform
        self.applications = applications
        self.schedulers = []
        self.channels = {}

        if dump:
            self.vcd_writer=VCDWriter(open(dump,'w'), timescale='1 ps', date='today')
        else:
            self.vcd_writer=VCDWriter(open(os.devnull,'w'), timescale='1 ps', date='today')
            self.vcd_writer.dump_off(self.env.now)

        log.info('Start initializing the system.')
        for app in self.applications:
            log.debug('  Load application: ' + app.name)
            for cm in app.mapping.channelMappings:
                name = app.name + '.' + cm.kpnChannel.name
                log.debug('    Create channel: ' + name)
                self.channels[name] = Channel(name, self, cm)

            for pm in app.mapping.processMappings:
                name = app.name + '.' + pm.kpnProcess.name
                log.debug('    Create process: ' + name)
                process = Process(name, self, pm,
                                  app.traceReaders[pm.kpnProcess.name])

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

                    scheduler.processes.append(process)
                else:
                    log.debug('    Create scheduler: ' + pm.scheduler.name)
                    scheduler = Scheduler(self, [process], pm.policy,
                                          pm.scheduler)
                    self.schedulers.append(scheduler)

        # We iterate over all channels and their cost models to get all
        # platform resources that are required for simulation. For each
        # platform resource we create a simpy resource object and extend the
        # platform reource by an attribute 'res' that points to the simpy
        # resource.
        #
        # This is not the best solution (TM) but does the job of decoupling
        # the platform description and simulation.
        for key, c in self.channels.items():
            for model in c.primitive.consume + c.primitive.produce:
                for r in model.resources:
                    if not hasattr(r, 'res'):
                        r.res = Resource(env, capacity=r.capacity)

        log.info('Done initializing the system.')

    def simulate(self):
        print('=== Start Simulation ===')
        start = timeit.default_timer()

        # start the schedulers
        for scheduler in self.schedulers:
            self.env.process(scheduler.run())

        self.env.run()

        stop = timeit.default_timer()

        print('=== End Simulation ===')
        exec_time = float(self.env.now) / 1000000000.0
        print('Total execution time: ' + str(exec_time) + ' ms')
        print('Total simulation time: ' + str(stop-start) + ' s')
        self.vcd_writer.close()

    def findScheduler(self, name):
        for s in self.schedulers:
            if s.name == name:
                return s
        return None

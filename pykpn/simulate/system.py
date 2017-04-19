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
                log.debug('    Create process: ' + pm.kpnProcess.name)
                process = Process(self.env,
                                  pm.kpnProcess.name,
                                  self.channels,
                                  app,
                                  self.vcd_writer)

                log.debug('      it uses the scheduler ' + pm.scheduler.name)

                scheduler = self.findScheduler(pm.scheduler.name)
                if scheduler is not None:
                    log.debug('      The scheduler was already created -> ' +
                              'append process')
                    scheduler.processes.append(process)
                else:
                    log.debug('    Create scheduler: ' + pm.scheduler.name)
                    scheduler = Scheduler(self.env,
                                          pm.scheduler.name,
                                          pm.scheduler.processors,
                                          [process],
                                          pm.policy,
                                          self.vcd_writer)
                    self.schedulers.append(scheduler)

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

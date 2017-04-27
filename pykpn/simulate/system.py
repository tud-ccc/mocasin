# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
import timeit
import os

from operator import itemgetter
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

    def __init__(self, env, config, applications):
        self.env = env
        self.platform = config.get_platform()
        self.applications = applications
        self.schedulers = []
        self.channels = {}
        dump=config.get_vcd()
        self.ini_times=[]
        self.pair={}

        if dump:
            self.vcd_writer=VCDWriter(open(dump,'w'), timescale='1 ps', date='today')
        else:
            self.vcd_writer=VCDWriter(open(os.devnull,'w'), timescale='1 ps', date='today')
            self.vcd_writer.dump_off(self.env.now)

        log.info('Start initializing the system.')
        for app in self.applications:
            self.ini_times.append([app,int(app.ini_time)])
            log.info(' Start application: '+app.name)
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
                    self.pair[scheduler].append(process)
                else:
                    log.debug('    Create scheduler: ' + pm.scheduler.name)
                    scheduler = Scheduler(self, [], pm.policy,
                                          pm.scheduler)
                    self.schedulers.append(scheduler)
                    self.pair[scheduler]=[process]

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
        print('Total simulation time: ' + str(stop-start) + ' s')
        self.vcd_writer.close()

    def findScheduler(self, name):
        for s in self.schedulers:
            if s.name == name:
                return s
        return None

    def run(self):
        self.ini_times=sorted(self.ini_times, key=itemgetter(1)) # applications sorted according to their initialization times in a list [application, initialization time]
        time_delay=[self.ini_times[0][1]]+[self.ini_times[i][1]-self.ini_times[i-1][1] for i in range(1, len(self.ini_times))] #the differences in the initialization times of succesive applications 

        for i in time_delay: 
            yield(self.env.timeout(i)) #delay till the initialization time is reached
            log.info("           "+str(self.env.now)+": Start application "+self.ini_times[0][0].name)
            for s in self.pair: #self.pair contains scheduler and processes key value pair **scheduler={process1, process2,...}
                for l in self.pair[s]: #l is the process
                    if l.name[0:4]==self.ini_times[0][0].name: #check if process name has the application name as in the ini)times list
                            s.assignProcess(l)
            self.ini_times.pop(0)

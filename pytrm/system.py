# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import itertools
import logging
import timeit
import sys
from vcd import VCDWriter
from pytrm import application
from .channel import Channel
from .process import Process
from .scheduler import Scheduler


log = logging.getLogger(__name__)


class System:

    schedulers =[]

    def __init__(self, env, platform, applications):
        self.vcd_writer=VCDWriter(open('dump.vcd','w'), timescale='1 ps', date='today')
        self.env = env
        self.platform = platform
        self.applications = applications
        log.info('Initialize the system.')
        self.channels = []
        for app in self.applications:
            log.debug('Found application  '+ app.name)
            for c in app.mapping.channels:
                log.debug(''.join([
                    'Found channel ', c.name, ' from ', c.processorFrom, ' to ',
                    c.processorTo, ' via ', c.viaMemory]))
                log.debug(''.join([
                    'The channel is bound to ', str(c.capacity),
                    ' tokens and uses the ', c.primitive,
                    ' communication primitive']))

                kpn_channel = None
                for app_chan in app.graph.channels:
                    if app_chan.name == c.name:
                        kpn_channel = app_chan
                if kpn_channel is None:
                    raise RuntimeError('The mapping references the channel ' +
                                       c.name + ' that is not defined in the ' +
                                       'graph')

                primitive = None
                for p in platform.primitives:
                    if p.typename == c.primitive and \
                       p.from_.name == c.processorFrom and \
                       p.via.name == c.viaMemory and \
                       p.to.name == c.processorTo:
                        primitive = p
                if primitive is None:
                    raise RuntimeError('Requested a communication primitive that' +
                                       ' the platform does not provide!')

                self.channels.append(Channel(self.env, c.name, c.capacity,
                                             kpn_channel.token_size, primitive))

            for s in app.mapping.schedulers:
                log.debug(''.join([
                    'Found the ', str(s.policy), ' scheduler ', s.name,
                    ' that schedules ', str(s.processNames), ' on ',
                    str(s.processorNames)]))

                processes = []
                for pn in s.processNames:
                    processes.append(Process(self.env, pn, self.channels, app, self.vcd_writer))

                processors = []
                for pn in s.processorNames:
                    for processor in self.platform.processors:
                        if pn == processor.name:
                            processors.append(processor)

                flag = [] # flag stores the information if all the processors are same as processsors of the scheduler
                f = 0
                I=[]
                for i in System.schedulers:
                    if processors == i.processors:
                        f=1
                        I.append(i)
                        break

                flag.append(f)

                if sum(flag) == 0: # if none of the processors match a new scheduler is created
                    System.schedulers.append(Scheduler(self.env, s.name, processors, processes, s.policy))
                    log.debug('Creating a new scheduler  '+ s.name)

                elif sum(flag) != len(flag): # if some of the processors match but not all error is raised
                    raise RuntimeError('Scheduler cannot be alloted to this process')

                elif sum(flag)==len(flag):
                    log.debug('Using the old scheduler  '+ s.name)
                    for i in I:
                        i.processes.append(processes[0])

        log.info('Done reading the applications')

    def simulate(self):
        print('=== Start Simulation ===')
        start = timeit.default_timer()

        # start the schedulers
        for scheduler in System.schedulers:
            self.env.process(scheduler.run())

        self.env.run()

        stop = timeit.default_timer()

        print('=== End Simulation ===')
        exec_time = float(self.env.now) / 1000000000.0
        print('Total execution time: ' + str(exec_time) + ' ms')
        print('Total simulation time: ' + str(stop-start) + ' s')
        self.vcd_writer.close()

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import itertools
import logging
import timeit
from pytrm import application
from .channel import Channel
from .process import Process
from .scheduler import Scheduler


log = logging.getLogger(__name__)


class System:

    schedulers =[]

    def __init__(self, env, platform, applications):

        self.env = env
        self.platform = platform
        self.applications = applications
        log.info('Initialize the system. Read the mapping.')

        self.channels = []

        for app in self.applications:
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
                    processes.append(Process(self.env, pn, self.channels,
                                             app.TraceReader))

                processors = []
                for pn in s.processorNames:
                    for processor in self.platform.processors:
                        if pn == processor.name:
                            processors.append(processor)

                flag = []
                f = 0
                for i in System.schedulers:
                    if processors == i.processors:
                        f=1
                        break

                flag.append(f)

                if sum(flag) == 0:
                    System.schedulers.append(Scheduler(self.env, s.name, processors, processes, s.policy))

                elif sum(flag) != len(flag):
                    raise RuntimeError('Scheduler allotment not valid')

                log.info('Done reading the mapping.')

    def simulate(self):
        print('=== Start Simulation ===')
        start = timeit.default_timer()

        # start the schedulers
        for scheduler in System.schedulers:
            #for app in self.applications:
                #TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO 
                scheduler.setTraceDir(self.applications[0].tracedir)
                self.env.process(scheduler.run())

        self.env.run()

        stop = timeit.default_timer()

        print('=== End Simulation ===')
        exec_time = float(self.env.now) / 1000000000.0
        print('Total execution time: ' + str(exec_time) + ' ms')
        print('Total simulation time: ' + str(stop-start) + ' s')

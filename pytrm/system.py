# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
import timeit
import simpy

from .channel import Channel
from .process import Process
from .scheduler import Scheduler


log = logging.getLogger(__name__)


class System:

    def __init__(self, platform, application, mapping, tracedir, TraceReader):

        # Create a simpy environment
        self.env = simpy.Environment()

        self.platform = platform
        self.application = application
        self.mapping = mapping
        self.tracedir = tracedir

        log.info('Initialize the system. Read the mapping.')

        self.channels = []

        for c in mapping.channels:
            log.debug(''.join([
                'Found channel ', c.name, ' from ', c.processorFrom, ' to ',
                c.processorTo, ' via ', c.viaMemory]))
            log.debug(''.join([
                'The channel is bound to ', str(c.capacity),
                ' tokens and uses the ', c.primitive,
                ' communiction primitive']))

            kpn_channel = None
            for app_chan in self.application.channels:
                if app_chan.name == c.name:
                    kpn_channel = app_chan
            if kpn_channel is None:
                raise RuntimeError('The mapping references the channel ' +
                                   c.name + ' that is not defined in the ' +
                                   'application')

            primitive = None
            for p in platform.primitives:
                if p.typename == c.primitive and \
                   p._from.name == c.processorFrom and \
                   p._via.name == c.viaMemory and \
                   p._to.name == c.processorTo:
                    primitive = p
            if primitive is None:
                raise RuntimeError('Requested a communication primitive that' +
                                   ' the platform does not provide!')

            self.channels.append(Channel(self.env, c.name, c.capacity,
                                         kpn_channel.token_size, primitive))

        self.schedulers = []

        for s in mapping.schedulers:
            log.debug(''.join([
                'Found the ', str(s.policy), ' scheduler ', s.name,
                ' that schedules ', str(s.processNames), ' on ',
                str(s.processorNames)]))

            processes = []
            for pn in s.processNames:
                processes.append(Process(self.env, pn, self.channels,
                                         TraceReader))

            processors = []
            for pn in s.processorNames:
                for processor in self.platform.processors:
                    if pn == processor.name:
                        processors.append(processor)

            self.schedulers.append(
                    Scheduler(self.env, s.name, processors, processes,
                              s.policy))

            log.info('Done reading the mapping.')

    def simulate(self):
        print('=== Start Simulation ===')
        start = timeit.default_timer()

        # start the schedulers
        for scheduler in self.schedulers:
            scheduler.setTraceDir(self.tracedir)
            self.env.process(scheduler.run())

        self.env.run()

        stop = timeit.default_timer()

        print('=== End Simulation ===')
        print('needed ' + str(stop-start) + ' seconds for simulation')

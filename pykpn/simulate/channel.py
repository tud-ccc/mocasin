# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

log = logging.getLogger(__name__)


class RuntimeChannel(object):
    '''
    Represents the runtime instance of a KPN channel.
    '''

    def __init__(self, name, system, mappingInfo, graph):
        self.env = system.env
        self.name = name
        self.graph = graph
        self.capacity = mappingInfo.capacity
        for c in graph.channels:
            if c.name in name:
                self.to_process=c.sinks
        self.primitive = mappingInfo.primitive
        self.token_size = mappingInfo.kpnChannel.token_size
        self.filled={}
        for p in self.to_process:
            self.filled[p]=0
        self.vcd_writer = system.vcd_writer
        self.filled_var = self.vcd_writer.register_var(
                'system.channels.' + name,
                'filling_level',
                'integer',
                size=self.capacity,
                init=0)

        self.event_produce = self.env.event()
        self.event_consume = self.env.event()

    def canProduceTokens(self, num):
        for p in self.filled:
            if self.filled[p] + num > self.capacity:
                return False
        return True

    def produceTokens(self, num):
        for p in self.filled:
            assert self.filled[p] + num <= self.capacity, \
            'produce called but buffer is full!'
            self.filled[p] = self.filled[p] + num

        self.vcd_writer.change(self.filled_var,
                self.env.now, list(self.filled.values())[0])

        log.debug(''.join([
                '{0:16}'.format(self.env.now), ': producing ', str(num),
                ' tokens on channel ', self.name,
                ' succeeded. New filling level: ',
                str(list(self.filled.values())[0]), '/',
                str(self.capacity)]))

        if len(self.event_produce.callbacks) > 0:
            self.event_produce.succeed()
            self.event_produce = self.env.event()

    def canConsumeTokens(self, num):
        for p in self.filled:
            if self.filled[p] - num < 0:
                return False
        return True

    def consumeTokens(self, num, process):
        for p in self.to_process:
            if p.name in process.name:
                assert self.filled[p] - num >= 0, 'consume called but buffer is empty!'
                self.filled[p] = self.filled[p] - num
        self.vcd_writer.change(self.filled_var,
                self.env.now, list(self.filled.values())[0])

        log.debug(''.join([
            '{0:16}'.format(self.env.now), ': consuming ', str(num),
            ' tokens on channel ', self.name,
            ' succeeded. New filling level: ',
            str(list(self.filled.values())[0]), '/',
            str(self.capacity)]))

            # notify waiting processes and recreate the event
        if len(self.event_consume.callbacks) > 0:
            self.event_consume.succeed()
            self.event_consume = self.env.event()

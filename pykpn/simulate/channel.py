# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

log = logging.getLogger(__name__)


class Channel(object):

    def __init__(self, name, system, mappingInfo):
        self.env = system.env
        self.name = name
        self.capacity = mappingInfo.capacity
        self.primitive = mappingInfo.primitive
        self.token_size = mappingInfo.kpnChannel.token_size
        self.filled = 0
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
        if self.filled + num <= self.capacity:
            return True
        else:
            return False

    def produceTokens(self, num):
        assert self.filled + num <= self.capacity, \
            'produce called but buffer is full!'

        self.filled = self.filled + num
        log.debug(''.join([
            '{0:16}'.format(self.env.now), ': producing ', str(num),
            ' tokens on channel ', self.name,
            ' succeeded. New filling level: ', str(self.filled), '/',
            str(self.capacity)]))

        self.vcd_writer.change(self.filled_var, self.env.now, self.filled)
        if len(self.event_produce.callbacks) > 0:
            self.event_produce.succeed()
            self.event_produce = self.env.event()

    def canConsumeTokens(self, num):
        if self.filled - num >= 0:
            return True
        else:
            return False

    def consumeTokens(self, num):
        assert self.filled - num >= 0, 'consume called but buffer is empty!'

        self.filled = self.filled - num
        log.debug(''.join([
            '{0:16}'.format(self.env.now), ': consuming ', str(num),
            ' tokens on channel ',self.application.name+'.'+ self.name,
            ' succeeded. New filling level: ', str(self.filled), '/',
            str(self.capacity)]))
        self.vcd_writer.change(self.filled_var, self.env.now, self.filled)

        # notify waiting processes and recreate the event
        if len(self.event_consume.callbacks) > 0:
            self.event_consume.succeed()
            self.event_consume = self.env.event()

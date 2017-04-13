# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

log = logging.getLogger(__name__)


class Channel(object):

    def __init__(self, env, name, capacity, token_size, primitive, application, vcd_writer):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.primitive = primitive
        self.token_size = token_size
        self.application=application
        self.filled = 0
        self.vcd_writer=vcd_writer
        self.channel=self.vcd_writer.register_var('system.'+ application.name+'.' + 'channels.'+name, 'filling_level', 'integer', size=capacity, init=0)
        self.event_produce = env.event()
        self.event_consume = env.event()

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
            ' tokens on channel ', self.application.name+'.'+self.name,
            ' succeeded. New filling level: ', str(self.filled), '/',
            str(self.capacity)]))

        self.vcd_writer.change(self.channel, self.env.now, self.filled)
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
        self.vcd_writer.change(self.channel, self.env.now, self.filled)

        # notify waiting processes and recreate the event
        if len(self.event_consume.callbacks) > 0:
            self.event_consume.succeed()
            self.event_consume = self.env.event()
# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

log = logging.getLogger(__name__)


class Channel(object):

    def __init__(self, env, name, capacity, token_size, primitive):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.primitive = primitive
        self.token_size = token_size

        self.producer_filled = 0
        self.consumer_filled = 0

        self.event_produce = env.event()
        self.event_consume = env.event()

    def canProduceTokens(self, num):
        if self.producer_filled + num <= self.capacity:
            return True
        else:
            return False

    def getDelayProduceTokens(self, num):
        return self.primitive.getProduceCosts(num)

    def produceTokens(self, num):

        assert self.producer_filled + num <= self.capacity, \
            'produce called but buffer is full!'

        self.producer_filled = self.producer_filled + num
        log.debug(''.join([
            '{0:16}'.format(self.env.now), ': producing ', str(num),
            ' tokens on channel ', self.name,
            ' succeeded. New filling level: ', str(self.producer_filled), '/',
            str(self.capacity)]))

    def getDelayTransferTokens(self, num):
        return self.primitive.getTransportCosts(num)

    def transferTokens(self, num):
        assert self.consumer_filled + num <= self.capacity, \
            'transfer called but buffer is full!'

        self.consumer_filled = self.consumer_filled + num
        log.debug(''.join([
            '{0:16}'.format(self.env.now), ': transfer of ', str(num),
            ' tokens on channel ', self.name, ' finished.']))

        if len(self.event_produce.callbacks) > 0:
            self.event_produce.succeed()
            self.event_produce = self.env.event()

    def canConsumeTokens(self, num):
        if self.consumer_filled - num >= 0:
            return True
        else:
            return False

    def getDelayConsumeTokens(self, num):
        return self.primitive.getConsumeCosts(num)

    def consumeTokens(self, num):

        assert self.consumer_filled - num >= 0, \
            'consume called but buffer is empty!'
        assert self.producer_filled - num >= 0, \
            'consume called but buffer is empty!'

        self.consumer_filled = self.consumer_filled - num
        self.producer_filled = self.producer_filled - num
        log.debug(''.join([
            '{0:16}'.format(self.env.now), ': consuming ', str(num),
            ' tokens on channel ', self.name,
            ' succeeded. New filling level: ', str(self.consumer_filled), '/',
            str(self.capacity)]))

        # notify waiting processes and recreate the event
        if len(self.event_consume.callbacks) > 0:
            self.event_consume.succeed()
            self.event_consume = self.env.event()

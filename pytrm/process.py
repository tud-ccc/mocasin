# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

from .trace import ProcessEntry
from .trace import ReadEntry
from .trace import WriteEntry
from .trace import TerminateEntry

from enum import Enum

log = logging.getLogger(__name__)


class ProcessState(Enum):
    Ready = 0
    Running = 1
    Blocked = 2
    Finished = 3


class Process(object):
    """
    Represents a KPN process.
    """

    traceDir = None
    processor = None
    trace = None
    resume = None
    traceReader = None

    def __init__(self, env, name, channels, TraceReaderClass):
        """
        Constructor

        :param env A SimPy Environment
        :param name The process' name
        """
        self.env = env
        self.name = name
        self.state = ProcessState.Ready

        self.event_unblock = env.event()

        self.channels = {}
        for c in channels:
            self.channels[c.name] = c

        self.TraceReaderClass = TraceReaderClass

    def unblock(self, event):
        assert self.state == ProcessState.Blocked
        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' unblocked')
        self.state = ProcessState.Ready

        self.event_unblock.succeed()
        self.event_unblock = self.env.event()

    def assignProcessor(self, processor):
        assert self.processor is None
        self.processor = processor

    def setTraceDir(self, traceDir):
        assert self.traceDir is None
        self.traceDir = traceDir

    def doTransport(self, ticks, channel, tokens):
        cm = channel.primitive.interconnectTransport

        # request all resources
        requests = []
        for r in cm.resources:
            req = r.request()
            requests.append(req)
            yield req

        yield self.env.timeout(ticks)
        channel.transferTokens(tokens)

        # release all resources
        for (res, req) in zip(cm.resources, requests):
            res.release(req)

    def run(self):
        """
        A SimPy process that replays the process trace
        """

        if self.traceReader is None:
            assert self.traceDir is not None
            assert self.processor is not None

            self.traceReader = self.TraceReaderClass(self.traceDir,
                                                     self.name,
                                                     self.processor)

        self.state = ProcessState.Running

        if self.resume is None:
            log.debug('{0:16}'.format(self.env.now) + ': process ' +
                      self.name + ' starts execution')
        else:
            log.debug('{0:16}'.format(self.env.now) + ': process ' +
                      self.name + ' resumes execution')

        delay = 0

        while not self.state == ProcessState.Finished:

            entry = None
            if self.resume is None:
                entry = self.traceReader.getNextEntry()
            else:
                entry, self.resume = self.resume, None

            if isinstance(entry, ProcessEntry):
                cycles = entry.cycles
                ticks = self.processor.cyclesToTicks(cycles)
                log.debug('{0:16}'.format(self.env.now + delay) +
                          ': process ' + self.name + ' processes for ' +
                          str(cycles) + ' cycles (' + str(ticks) + ' ticks)')

                # When we process we don't have to synchronize and simply
                # advance in local time
                delay += ticks
            elif isinstance(entry, ReadEntry):
                channel = self.channels[entry.channel]

                log.debug('{0:16}'.format(self.env.now + delay) +
                          ': process ' + self.name + ' reads ' +
                          str(entry.tokens) + ' tokens from channel ' +
                          entry.channel)

                if channel.canConsumeTokens(entry.tokens):
                    # we need to pay for the delay here, since we will request
                    # resources
                    yield self.env.timeout(delay)
                    delay = 0

                    size = entry.tokens * channel.token_size

                    pcm = channel.primitive.consumePrepare
                    rcm = channel.primitive.consumeRequest
                    tcm = channel.primitive.consumeTransport

                    # Do the prepare part of the consume, ...
                    cycles = round(pcm.getCosts(x=size))
                    ticks = self.processor.cyclesToTicks(cycles)

                    # request all resources
                    requests = []
                    for r in pcm.resources:
                        req = r.request()
                        requests.append(req)
                        yield req

                    yield self.env.timeout(ticks)

                    # release all resources
                    for (res, req) in zip(pcm.resources, requests):
                        res.release(req)

                    # ... the request part, ...
                    cycles = round(rcm.getCosts(x=size))
                    ticks = self.processor.cyclesToTicks(cycles)

                    # request all resources
                    requests = []
                    for r in rcm.resources:
                        req = r.request()
                        requests.append(req)
                        yield req

                    yield self.env.timeout(ticks)

                    # release all resources
                    for (res, req) in zip(rcm.resources, requests):
                        res.release(req)

                    # ... and the tranport part
                    cycles = round(tcm.getCosts(x=size))
                    ticks = self.processor.cyclesToTicks(cycles)

                    # request all resources
                    requests = []
                    for r in tcm.resources:
                        req = r.request()
                        requests.append(req)
                        yield req

                    yield self.env.timeout(ticks)

                    # release all resources
                    for (res, req) in zip(tcm.resources, requests):
                        res.release(req)

                    channel.consumeTokens(entry.tokens)
                else:
                    log.debug('                  Not enough tokens in ' +
                              'channel -> block')
                    self.state = ProcessState.Blocked
                    self.resume = entry
                    channel.event_produce.callbacks.append(self.unblock)
                    return
            elif isinstance(entry, WriteEntry):
                channel = self.channels[entry.channel]

                log.debug('{0:16}'.format(self.env.now + delay) +
                          ': process ' + self.name + ' writes ' +
                          str(entry.tokens) + ' tokens to channel ' +
                          entry.channel)

                if channel.canProduceTokens(entry.tokens):
                    # we need to pay for the delay here, since we will request
                    # resources
                    yield self.env.timeout(delay)
                    delay = 0

                    size = entry.tokens * channel.token_size

                    pcm = channel.primitive.producePrepare
                    tcm = channel.primitive.produceTransport
                    rcm = channel.primitive.produceResponse

                    # Do the produce prepare, ...
                    cycles = round(pcm.getCosts(x=size))
                    ticks = self.processor.cyclesToTicks(cycles)

                    # request all resources
                    requests = []
                    for r in pcm.resources:
                        req = r.request()
                        requests.append(req)
                        yield req

                    yield self.env.timeout(ticks)

                    # release all resources
                    for (res, req) in zip(pcm.resources, requests):
                        res.release(req)

                    # ... the transport, ...
                    cycles = round(tcm.getCosts(x=size))
                    ticks = self.processor.cyclesToTicks(cycles)

                    # request all resources
                    requests = []
                    for r in tcm.resources:
                        req = r.request()
                        requests.append(req)
                        yield req

                    yield self.env.timeout(ticks)

                    # release all resources
                    for (res, req) in zip(tcm.resources, requests):
                        res.release(req)

                    # ... and the response.
                    cycles = round(rcm.getCosts(x=size))
                    ticks = self.processor.cyclesToTicks(cycles)

                    # request all resources
                    requests = []
                    for r in rcm.resources:
                        req = r.request()
                        requests.append(req)
                        yield req

                    yield self.env.timeout(ticks)

                    # release all resources
                    for (res, req) in zip(rcm.resources, requests):
                        res.release(req)

                    channel.produceTokens(entry.tokens)
                else:
                    log.debug('                  Not enough free slots ' +
                              'in channel -> block')
                    self.state = ProcessState.Blocked
                    self.resume = entry
                    channel.event_consume.callbacks.append(self.unblock)
                    return
            elif isinstance(entry, TerminateEntry):
                yield self.env.timeout(delay)
                self.state = ProcessState.Finished
            else:
                assert False, "found an unexpected trace entry"

        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' finished execution')

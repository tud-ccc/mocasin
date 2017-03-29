# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

from common.trace import ProcessEntry
from common.trace import ReadEntry
from common.trace import WriteEntry
from common.trace import TerminateEntry

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
        
        self.time=0
        self.channels = {}
        for c in channels:
            self.channels[c.name] = c

        self.TraceReaderClass = TraceReaderClass

    def unblock(self, event):
        assert self.state == ProcessState.Blocked
        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' unblocked')
        self.time=format(self.env.now)
        self.state = ProcessState.Ready

        self.event_unblock.succeed()
        self.event_unblock = self.env.event()

    def assignProcessor(self, processor):
        assert self.processor is None
        self.processor = processor

    def setTraceDir(self, traceDir):
        assert self.traceDir is None
        self.traceDir = traceDir

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

        while not self.state == ProcessState.Finished:

            entry = None
            if self.resume is None:
                entry = self.traceReader.getNextEntry()
            else:
                entry, self.resume = self.resume, None

            if isinstance(entry, ProcessEntry):
                cycles = entry.cycles
                ticks = self.processor.cyclesToTicks(cycles)
                log.debug('{0:16}'.format(self.env.now) +
                          ': process ' + self.name + ' processes for ' +
                          str(cycles) + ' cycles (' + str(ticks) + ' ticks)')

                yield self.env.timeout(ticks)
            elif isinstance(entry, ReadEntry):
                channel = self.channels[entry.channel]

                log.debug('{0:16}'.format(self.env.now) +
                          ': process ' + self.name + ' reads ' +
                          str(entry.tokens) + ' tokens from channel ' +
                          entry.channel)

                if channel.canConsumeTokens(entry.tokens):
                    size = entry.tokens * channel.token_size

                    consume = channel.primitive.consume


                    for c in consume:
                        cycles = round(c.getCosts(x=size))
                        ticks = self.processor.cyclesToTicks(cycles)
                        # request all resources
                        requests = []
                        for r in c.resources:
                            req = r.request()
                            requests.append(req)
                            yield req
                        yield self.env.timeout(ticks)

                        # release all resources
                        for (res, req) in zip(c.resources, requests):
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

                log.debug('{0:16}'.format(self.env.now) +
                          ': process ' + self.name + ' writes ' +
                          str(entry.tokens) + ' tokens to channel ' +
                          entry.channel)

                if channel.canProduceTokens(entry.tokens):
                    size = entry.tokens * channel.token_size

                    produce = channel.primitive.produce

                    for p in produce:
                        cycles = round(p.getCosts(x=size))
                        ticks = self.processor.cyclesToTicks(cycles)
                        # request all resources
                        requests = []
                        for r in p.resources:
                            req = r.request()
                            requests.append(req)
                            yield req

                        yield self.env.timeout(ticks)

                        # release all resources
                        for (res, req) in zip(p.resources, requests):
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
                self.state = ProcessState.Finished
            else:
                assert False, "found an unexpected trace entry"

        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' finished execution')

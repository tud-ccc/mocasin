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

    def finishTransfer(self, event):
        event.channel.transferTokens(event.num)
        event._ok = True

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
                ticks = int(cycles / float(self.processor.frequency) * 1000000)
                log.debug('{0:16}'.format(self.env.now) + ': process ' +
                          self.name + ' processes for ' + str(cycles) +
                          ' cycles (' + str(ticks) + ' ticks)')
                yield self.env.timeout(ticks)
            elif isinstance(entry, ReadEntry):
                channel = self.channels[entry.channel]

                cycles = channel.getDelayProduceTokens(entry.tokens)
                ticks = int(cycles / float(self.processor.frequency) * 1000000)

                log.debug('{0:16}'.format(self.env.now) + ': process ' +
                          self.name + ' reads ' + str(entry.tokens) +
                          ' tokens from channel ' + entry.channel)

                if channel.canConsumeTokens(entry.tokens):
                    yield self.env.timeout(ticks)
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

                produceCycles = channel.getDelayProduceTokens(entry.tokens)
                produceTicks = int(produceCycles /
                                   float(self.processor.frequency) * 1000000)
                transferCycles = channel.getDelayTransferTokens(entry.tokens)
                transferTicks = int(transferCycles /
                                    float(self.processor.frequency) * 1000000)

                log.debug('{0:16}'.format(self.env.now) + ': process ' +
                          self.name + ' writes ' + str(entry.tokens) +
                          ' tokens to channel ' + entry.channel)

                if channel.canProduceTokens(entry.tokens):
                    yield self.env.timeout(produceTicks)
                    channel.produceTokens(entry.tokens)

                    # schedule an event at the end of the transfer
                    event = self.env.event()
                    event.channel = channel
                    event.num = entry.tokens
                    event.callbacks.append(self.finishTransfer)
                    self.env.schedule(event, delay=transferTicks)
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

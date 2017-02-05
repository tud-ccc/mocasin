# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
import os

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

    def __init__(self, env, name, channels):
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
        assert self.traceDir is not None
        self.processor = processor
        traceFile = os.path.join(self.traceDir, self.name + '.' +
                                 processor.type + '.cpntrace')
        self.trace = open(traceFile, 'r')
        assert self.trace is not None

    def setTraceDir(self, traceDir):
        assert self.traceDir is None
        self.traceDir = traceDir

    def run(self):
        """
        A SimPy process that replays the process trace
        """

        self.state = ProcessState.Running

        if self.resume is None:
            log.debug('{0:16}'.format(self.env.now) + ': process ' +
                      self.name + ' starts execution')
        else:
            log.debug('{0:16}'.format(self.env.now) + ': process ' +
                      self.name + ' resumes execution')

        if self.resume is not None:
            # retry
            if self.resume[0] == 'r':
                num = int(self.resume[3])
                log.debug('{0:16}'.format(self.env.now) + ': process ' +
                          self.name + ' reads ' + str(num) +
                          ' tokens from channel ' + self.resume[1])

                channel = self.channels[self.resume[1]]

                if channel.canConsumeTokens(num):
                    delay = channel.getDelayConsumeTokens(num)
                    t = int(delay / float(self.processor.frequency) * 1000000)
                    yield self.env.timeout(t)
                    channel.consumeTokens(num)
                else:
                    log.debug('                  Not enough tokens in' +
                              'channel -> block')
                    self.state = ProcessState.Blocked
                    channel.event_produce.callbacks.append(self.unblock)
                    return
            elif self.resume[0] == 'w':
                num = int(self.resume[2])
                log.debug('{0:16}'.format(self.env.now) + ': process ' +
                          self.name + ' writes ' + str(num) +
                          ' tokens to channel ' + self.resume[1])

                channel = self.channels[self.resume[1]]

                if channel.canProduceTokens(num):
                    delay = channel.getDelayProduceTokens(num)
                    t = int(delay / float(self.processor.frequency) * 1000000)
                    yield self.env.timeout(t)
                    channel.produceTokens(num)

                    transferCycles = channel.getDelayTransferTokens(num)
                    delay = int(transferCycles /
                                float(self.processor.frequency) * 1000000)
                    event = self.env.event()
                    event.channel = channel
                    event.num = num
                    event.callbacks.append(self.finishTransfer)
                    self.env.schedule(event, delay=delay)
                else:
                    log.debug('                  Not enough free slots in' +
                              ' channel -> block')
                    self.state = ProcessState.Blocked
                    channel.event_consume.callbacks.append(self.unblock)
                    return
            else:
                assert False, "found an unexpected trace entry"

        self.resume = None

        while not self.state == ProcessState.Finished:
            traceline = self.trace.readline().split(' ')

            entry_type = traceline[0]

            if entry_type == 'm':
                cycles = int(traceline[2])
                ticks = int(cycles / float(self.processor.frequency) * 1000000)
                log.debug('{0:16}'.format(self.env.now) + ': process ' +
                          self.name + ' processes for ' + str(cycles) +
                          ' cycles (' + str(ticks) + ' ticks)')
                yield self.env.timeout(ticks)
            elif entry_type == 'r':
                channel = self.channels[traceline[1]]

                num = int(traceline[3])
                processCycles = int(traceline[4])
                processTicks = int(processCycles /
                                   float(self.processor.frequency) * 1000000)
                consumeCycles = channel.getDelayProduceTokens(num)
                consumeTicks = int(consumeCycles /
                                   float(self.processor.frequency) * 1000000)

                # If we know already that we can produce a token, we merge the
                # delay for processing and produce operation
                if channel.canConsumeTokens(num):
                    log.debug('{0:16}'.format(self.env.now) + ': process ' +
                              self.name + ' processes for ' +
                              str(processCycles) + ' cycles (' +
                              str(processTicks) + ' ticks)')
                    log.debug('                 ... and then reads ' +
                              str(num) + ' tokens to channel ' + traceline[1])

                    yield self.env.timeout(processTicks+consumeTicks)
                    channel.consumeTokens(num)
                else:
                    log.debug('{0:16}'.format(self.env.now) + ': process ' +
                              self.name + ' processes for ' +
                              str(processCycles) + ' cycles (' +
                              str(processTicks) + ' ticks)')
                    yield self.env.timeout(processTicks)
                    log.debug('{0:16}'.format(self.env.now) + ': process ' +
                              self.name + ' reads ' + str(num) +
                              ' tokens from channel ' + traceline[1])

                    if channel.canConsumeTokens(num):
                        yield self.env.timeout(consumeTicks)
                        channel.consumeTokens(num)
                    else:
                        log.debug('                  Not enough tokens in ' +
                                  'channel -> block')
                        self.state = ProcessState.Blocked
                        self.resume = traceline
                        channel.event_produce.callbacks.append(self.unblock)
                        return

            elif entry_type == 'w':
                channel = self.channels[traceline[1]]

                num = int(traceline[2])
                processCycles = int(traceline[3])
                processTicks = int(processCycles /
                                   float(self.processor.frequency) * 1000000)
                produceCycles = channel.getDelayProduceTokens(num)
                produceTicks = int(produceCycles /
                                   float(self.processor.frequency) * 1000000)
                transferCycles = channel.getDelayTransferTokens(num)
                transferTicks = int(transferCycles /
                                    float(self.processor.frequency) * 1000000)

                # If we know already that we can produce a token, we merge the
                # delay for processing and produce operation
                if channel.canProduceTokens(num):
                    log.debug('{0:16}'.format(self.env.now) + ': process ' +
                              self.name + ' processes for ' +
                              str(processCycles) + ' cycles (' +
                              str(processTicks) + ' ticks)')
                    log.debug('                 ... and then writes ' +
                              str(num) + ' tokens to channel ' + traceline[1])

                    yield self.env.timeout(processTicks+produceTicks)
                    channel.produceTokens(num)

                    event = self.env.event()
                    event.channel = channel
                    event.num = num
                    event.callbacks.append(self.finishTransfer)

                    self.env.schedule(event, delay=transferTicks)
                else:
                    log.debug('{0:16}'.format(self.env.now) + ': process ' +
                              self.name + ' processes for ' +
                              str(processCycles) + ' cycles (' +
                              str(processTicks) + ' ticks)')

                    yield self.env.timeout(processTicks)

                    log.debug('{0:16}'.format(self.env.now) + ': process ' +
                              self.name + ' writes ' + str(num) +
                              ' tokens to channel ' + traceline[1])

                    if channel.canProduceTokens(num):
                        yield self.env.timeout(produceTicks)
                        channel.produceTokens(num)

                        event = self.env.event()
                        event.channel = channel
                        event.num = num
                        event.callbacks.append(self.finishTransfer)
                        self.env.schedule(event, delay=transferTicks)
                    else:
                        log.debug('                  Not enough free slots ' +
                                  'in channel -> block')
                        self.state = ProcessState.Blocked
                        self.resume = traceline
                        channel.event_consume.callbacks.append(self.unblock)
                        return
            elif traceline[0] == 'e':
                self.state = ProcessState.Finished
            else:
                assert False, "found an unexpected trace entry"

        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' finished execution')

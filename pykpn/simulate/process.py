# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
from ..common.trace import ProcessEntry
from ..common.trace import ReadEntry
from ..common.trace import WriteEntry
from ..common.trace import TerminateEntry
from enum import Enum

log = logging.getLogger(__name__)


class ProcessState(Enum):
    Ready = 0
    Running = 1
    Blocked = 2
    Finished = 3


class Process(object):

    traceDir = None
    processor = None
    trace = None
    resume = None
    traceReader = None

    def __init__(self, name, system, processMapping, traceReader):
        self.env = system.env
        self.name = name
        self.channels = system.channels
        self.traceReader = traceReader

        self.state = ProcessState.Ready

        self.event_unblock = self.env.event()

        self.vcd_writer = system.vcd_writer
        self.running_var = self.vcd_writer.register_var(
                'system.processes.' + name,
                'running',
                'integer',
                size=1,
                init=0)

        # ASCII encoded name for display in VCD traces
        self.vcd_id = ''.join(['{0:08b}'.format(ord(c)) for c in self.name])

    def unblock(self, event):
        assert self.state == ProcessState.Blocked
        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' unblocked')
        self.state = ProcessState.Ready

        self.event_unblock.succeed()
        self.event_unblock = self.env.event()

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

        self.vcd_writer.change(self.running_var, self.env.now, 1)

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
                    self.vcd_writer.change(self.running_var, self.env.now, 0)
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
                    self.vcd_writer.change(self.running_var, self.env.now, 0)
                    return
            elif isinstance(entry, TerminateEntry):
                self.state = ProcessState.Finished
            else:
                assert False, "found an unexpected trace entry"
        log.debug('{0:16}'.format(self.env.now) + ': process ' + self.name +
                  ' finished execution')

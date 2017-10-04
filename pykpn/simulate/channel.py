# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

from pykpn.simulate.adapter import SimulateLoggerAdapter


log = logging.getLogger(__name__)


class RuntimeChannel(object):
    """Represents the runtime instance of a KPN channel.

    This implements a multiple reader channel, meaning that a channel may have
    multiple consumers. This is an optimization to the more restrictive KPN
    channel that only allows one reader. The channel ensures that each consumer
    receives a copy of each token written to the channel. This implementation
    keeps a FIFO for every sink process and copies the tokens upon production.

    :ivar name:   the channel name
    :type name:   str
    :ivar _env:   the simpy environment
    :ivar _src:   the source process of this channel
    :type _src:   RuntimeProcess
    :ivar _sinks: list of sink processes of this channel
    :type _sinks: list[RuntimeProcess]
    :ivar _fifo_state: A dictionary of sink process names (keys) and the number
                       of tokens currently stored in the FIFO as values.
    :type _fifo_state: dict[str, int]
    :ivar _capacity: maximum number of tokens that can be stored in a FIFO
    :type _capacity: int
    :ivar tokens_produced: a simpy event triggered when new tokens where witten
        to this channel
    :type tokens_produced: simpy.events.Event
    :ivar tokens_consumed: a simpy event triggered when tokens where read from
        the channel
    :type tokens_consumed: simpy.events.Event
    """

    def __init__(self, name, mapping_info, env):
        """Initialize a runtime channel.

        :param str name: the channel name
        :param mapping_info: a channel mapping info object
        :type mapping_info: ChannelMappingInfo
        :param env: the simpy environment
        """
        log.debug('initialize new runtime channel: (%s)', name)

        self._log = SimulateLoggerAdapter(log, name, env)

        self.name = name
        self._env = env
        self._src = None
        self._sinks = []
        self._fifo_state = {}
        self._capacity = mapping_info.capacity

        self.tokens_produced = env.event()
        self.tokens_consumed = env.event()

    def set_src(self, process):
        """Set the source process

        :param process: the process to become source to this channel
        :type process: RuntimeProcess
        """
        assert self._src is None
        self._src = process

    def add_sink(self, process):
        """Register a process as sink

        :param process: the process to become a sink to this channel
        :type process: RuntimeProcess
        """
        self._sinks.append(process)
        self._fifo_state[process.name] = 0

    def _can_consume(self, process, num):
        """Check if a number of tokens can be consumed.

        Check if at least ``num`` tokens are stored in the FIFO for the sink
        process ``process``.

        :param process: the process that tries to consume tokens
        :type process: RuntimeKpnProcess
        :param num: number of tokens to be consumed
        :type num: int
        :returns: ``True`` if the process can consume ``num`` tokens
        :rtype: bool
        """
        assert len(self._sinks) > 1
        return bool(self._fifo_state[process.name] >= num)

    def _can_produce(self, num):
        """Check if a number of tokens can be produced

        Check if all FIFO have at least ``num`` empty slots.

        :param num: number of tokens to be produced
        :type num: int
        :returns: ``True`` if the process can consume ``num`` tokens
        :rtype: bool
        """
        return all([(self._fifo_state[p.name] + num) <= self._capacity
                    for p in self._sinks])

    def consume(self, process, num):
        """Consume tokens

        :param process: the process that consumes tokens
        :type process: RuntimeKpnProcess
        :param num: number of tokens to be consumed
        :type num: int
        """
        assert process in self._sinks

        self._log.debug('%s starts a consume operation requesting %d tokens.',
                        process.name, num)

        # wait until there are enough tokens available
        blocked = False
        while True:
            if self._can_consume(process, num):
                self._log.debug('consume successful')
                break
            else:
                self._log.debug('not enough tokens available')
                if not blocked:
                    blocked = True
                    process.block()
                yield self.tokens_produced

        # If we blocked the process, we need to unblock it and wait until it is
        # running again.
        if blocked:
            process.unblock()
            yield process.running
            self._log.debug('continue consume after process was blocked')

        # update the state
        new_state = self._fifo_state[process.name] - num
        self._fifo_state[process.name] = new_state

        self._log.debug('consume operation completed')

    def produce(self, process, num):
        assert self._src is process

        self._log.debug('%s starts a produce operation writing %d tokens.',
                        process.name, num)

        # wait until there are enough tokens available
        blocked = False
        while True:
            if self._can_produce(num):
                self._log.debug('produce successful')
                break
            else:
                self._log.debug('not enough free slots available')
                if not blocked:
                    blocked = True
                    process.block()
                yield self.tokens_consumed

        # If we blocked the process, we need to unblock it and wait until it is
        # running again.
        if blocked:
            process.unblock()
            yield process.running
            self._log.debug('continue consume after process was blocked')

        # update the state
        for p in self._fifo_state:
            self._fifo_state[p] += num

        self._log.debug('produce operation completed')

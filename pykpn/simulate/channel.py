# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pykpn.common import logging
from pykpn.simulate.adapter import SimulateLoggerAdapter
from pykpn.simulate.process import ProcessState


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
    :ivar _primitive: The communication primitive this channel is mmapped to
    :type _primitive: PrimitiveGroup
    :ivar tokens_produced: a simpy event triggered when new tokens where witten
        to this channel
    :type tokens_produced: simpy.events.Event
    :ivar tokens_consumed: a simpy event triggered when tokens where read from
        the channel
    :type tokens_consumed: simpy.events.Event
    :ivar int _token_size: size of one data token in bytes
    """

    def __init__(self, name, mapping_info, token_size, env):
        """Initialize a runtime channel.

        :param str name: the channel name
        :param mapping_info: a channel mapping info object
        :type mapping_info: ChannelMappingInfo
        :param int token_size: size of one data token in bytes
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
        self._primitive = mapping_info.primitive
        self._token_size = token_size

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

    def can_consume(self, process, num):
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
        assert process in self._sinks
        return bool(self._fifo_state[process.name] >= num)

    def can_produce(self, process, num):
        """Check if a number of tokens can be produced

        Check if all FIFO have at least ``num`` empty slots.

        :param process: the process that tries to produce tokens
        :type process: RuntimeKpnProcess
        :param num: number of tokens to be produced
        :type num: int
        :returns: ``True`` if the process can consume ``num`` tokens
        :rtype: bool
        """
        assert self._src is process
        return all([(self._fifo_state[p.name] + num) <= self._capacity
                    for p in self._sinks])

    def wait_for_tokens(self, process, num):
        """A simpy process that waits for tokens.

        Wait until the process ``process`` can consume ``num`` tokens. Then,
        unblock the process.
        :param process: the process that waits
        :type process: RuntimeKpnProcess
        :param num: number of tokens to wait for
        :type num: int
        """
        assert process.check_state(ProcessState.BLOCKED)

        self._log.debug('wait until %s can consume %d tokens', process.name,
                        num)

        while True:
            yield self.tokens_produced
            if self.can_consume(process, num):
                break

        self._log.debug('enough tokens available -> unblock %s', process.name)
        process.unblock()

    def wait_for_slots(self, process, num):
        """A simpy process that waits for free slots.

        Wait until the process ``process`` can produce ``num`` tokens. Then,
        unblock the process.
        :param process: the process that waits
        :type process: RuntimeKpnProcess
        :param num: number of free slots to wait for
        :type num: int
        """
        assert process.check_state(ProcessState.BLOCKED)

        self._log.debug('wait until %s can produce %d tokens', process.name,
                        num)

        while True:
            yield self.tokens_consumed
            if self.can_produce(process, num):
                break

        self._log.debug('enough slots available -> unblock %s', process.name)
        process.unblock()

    def consume(self, process, num):
        """Consume tokens

        :param process: the process that consumes tokens
        :type process: RuntimeKpnProcess
        :param num: number of tokens to be consumed
        :type num: int
        :returns: a simpy Event that is triggered after the consume operation
            completed.
        :rtype: simpy.events.Event
        """
        assert self.can_consume(process, num)

        sink = process.processor
        prim = self._primitive
        log = self._log

        log.debug('start a consume operation reading %d tokens using %s',
                  num, prim.name)

        # update the state
        new_state = self._fifo_state[process.name] - num
        self._fifo_state[process.name] = new_state

        if sink not in prim.consumers:
            raise RuntimeError(
                'processor %s cannot consume tokens using the primitive %s' %
                (sink.name, prim.name))

        for phase in prim.consume_phases[sink.name]:
            log.debug('start communication phase "%s"', phase.name)

            # 1. request all resouces
            requests = []
            for r in phase.resources:
                log.debug('via resource: %s', r.name)
                if hasattr(r, 'simpy_resource'):
                    req = r.simpy_resource.request()
                    requests.append(req)
                    log.debug('request resource %s', r.name)
                    yield req
                else:
                    requests.append(None)

            # pay for the delay
            size = num * self._token_size
            ticks = phase.get_costs(size)
            yield self._env.timeout(ticks)

            # release all resources that we requested before
            for (res, req) in zip(phase.resources, requests):
                if req is not None:
                    log.debug('release resource %s', r.name)
                    res.simpy_resource.release(req)

            log.debug('communication phase completed')

        log.debug('consume operation completed')

        # notify waiting processes
        self.tokens_consumed.succeed()
        self.tokens_consumed = self._env.event()

    def produce(self, process, num):
        """Produce tokens

        :param process: the process that produces tokens
        :type process: RuntimeKpnProcess
        :param num: number of tokens to be produced
        :type num: int
        :returns: a simpy Event that is triggered after the produce operation
            completed.
        :rtype: simpy.events.Event
        """
        assert self.can_produce(process, num)

        src = process.processor
        prim = self._primitive
        log = self._log

        log.debug('start a produce operation writing %d tokens using %s',
                  num, prim.name)

        # update the state
        for p in self._fifo_state:
            self._fifo_state[p] += num

        if src not in prim.producers:
            raise RuntimeError(
                'processor %s cannot produce tokens using the primitive %s' %
                (src.name, prim.name))

        for phase in prim.produce_phases[src.name]:
            log.debug('start communication phase "%s"', phase.name)

            # 1. request all resouces
            requests = []
            for r in phase.resources:
                log.debug('via resource: %s', r.name)
                if hasattr(r, 'simpy_resource'):
                    req = r.simpy_resource.request()
                    requests.append(req)
                    log.debug('request resource %s', r.name)
                    yield req
                else:
                    requests.append(None)

            # pay for the delay
            size = num * self._token_size
            ticks = phase.get_costs(size)
            yield self._env.timeout(ticks)

            # release all resources that we requested before
            for (res, req) in zip(phase.resources, requests):
                if req is not None:
                    log.debug('release resource %s', r.name)
                    res.simpy_resource.release(req)

            log.debug('communication phase completed')

        log.debug('produce operation completed')

        # notify waiting processes
        self.tokens_produced.succeed()
        self.tokens_produced = self._env.event()

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""Contains the :class:`RuntimeChannel` class which manages the simulation of
KPN channels."""


from pykpn.util import logging
from pykpn.simulate.adapter import SimulateLoggerAdapter
from pykpn.simulate.process import ProcessState


log = logging.getLogger(__name__)


class RuntimeChannel(object):
    """Represents the runtime instance of a KPN channel.

    Implements the semantics of a multiple reader channel. This means that a
    channel may have multiple consumers. This is an optimization to the more
    restrictive KPN channel that only allows one reader. The channel ensures
    that each consumer receives a copy of each token written to the channel.
    This implementation keeps a FIFO for each consumer and copies tokens when
    produced. Initially all FIFOs are empty.

    Attributes:
        name (str): the channel name
        tokens_consumed (~simpy.events.Event): a simpy event triggered when
            tokens where read from the channel
        tokens_produced (~simpy.events.Event): a simpy event triggered when new
            tokens where written to this channel
        app (RuntimeApplication): the application this process is part of
        _src (RuntimeProcess): the source process
        _sinks (list[RuntimeProcess]): the sink processes
        _fifo_state (dict[str, int]): A dictionary of sink process names (keys)
            and the number of tokens currently stored in the FIFO as values.
        _capacity (int): maximum number of tokens that can be stored in a FIFO
        _primitive (Primitive): The communication primitive this channel is
            mmapped to

    Args:
        name (str): the channel name
        mapping_info (ChannelMappingInfo): a channel mapping info object
        token_size(int): size of one data token in bytes
        app (RuntimeApplication): the application this process is part of
    """
    def __init__(self, name, mapping_info, token_size, app):
        self.name = name
        self.app = app

        log.debug(f"initialize new runtime channel: ({self.full_name})")

        self._log = SimulateLoggerAdapter(log, name, self.env)
        self._src = None
        self._sinks = []
        self._fifo_state = {}
        self._capacity = mapping_info.capacity
        self._primitive = mapping_info.primitive
        self._token_size = token_size

        self.tokens_produced = self.env.event()
        self.tokens_consumed = self.env.event()

    @property
    def env(self):
        """The simpy environment"""
        return self.app.env

    @property
    def full_name(self):
        """Full name including the application name"""
        return f"{self.app.name}.{self.name}"

    @property
    def trace_writer(self):
        """The system's trace writer"""
        return self.app.system.trace_writer

    def set_src(self, process):
        """Set the source process.

        Args:
            process (RuntimeProcess): the process to become source
        Raises:
            AssertionError: if the source was already set
        """
        assert self._src is None
        self._src = process

    def add_sink(self, process):
        """Add a sink process.

        Args:
            process (RuntimeProcess): the process to become a sink
        Warning:
            Adding a sink during a simulation might have unexpected effects.
        """
        self._sinks.append(process)
        self._fifo_state[process.name] = 0

        # record the channel creation in the simulation trace
        self.trace_writer.update_counter(self.app.name,
                                         self.name,
                                         self._fifo_state.copy(),
                                         category="Channel")

    def can_consume(self, process, num):
        """Check if a process can consume a number of tokens.

        Args:
            process (RuntimeProcess): the process that tries to consume tokens
            num (int): number of tokens to be consumed (>0)
        Returns:
            bool: ``True`` if the process can consume `num` tokens
        Raises:
            ValueError: if the process is not registered as a sink
            ValueError: if `num` is not an integer greater than 0
            RuntimeError: if no source is registered to the channel
        """
        if process not in self._sinks:
            raise ValueError('Process %s is not a sink' % process.full_name)
        if (not isinstance(num, int)) or num < 1:
            raise ValueError('num must be an integer greater than 0')
        if self._src is None:
            raise RuntimeError('No source registered to the channel')
        return bool(self._fifo_state[process.name] >= num)

    def can_produce(self, process, num):
        """Check if a process can produce a number of tokens.

        Args:
            process (RuntimeProcess): the process that tries to produce tokens
            num (int): number of tokens to be produced
        Returns:
            bool: ``True`` if the process can produce `num` tokens
        Raises:
            ValueError: if the process is not registered as a source
            ValueError: if `num` is not an integer greater than 0
            RuntimeError: if no sinks are registered to the channel
        """
        if process is not self._src:
            raise ValueError(f"Process {process.full_name} is not the source")
        if (not isinstance(num, int)) or num < 1:
            raise ValueError('num must be an integer greater than 0')
        if len(self._sinks) == 0:
            raise RuntimeError('No sinks registered to the channel')
        return all([(self._fifo_state[p.name] + num) <= self._capacity
                    for p in self._sinks])

    def wait_for_tokens(self, process, num):
        """An event generator that waits for tokens.

        Wait until `process` can consume `num` tokens. Then, unblock `process`
        and return.

        Note:
            The process must be in the
            :const:`~pykpn.simulate.process.ProcessState.BLOCKED` state!

        Args:
            process (RuntimeProcess): the process that waits for tokens
            num (int): number of tokens to wait for

        Yields:
            ~simpy.events.Event: a series of events until `process`
            can consume `num` tokens
        """
        assert process.check_state(ProcessState.BLOCKED)

        self._log.debug('wait until %s can consume %d tokens',
                        process.full_name, num)

        while True:
            yield self.tokens_produced
            if self.can_consume(process, num):
                break

        self._log.debug('enough tokens available -> unblock %s',
                        process.full_name)
        process.unblock()

    def wait_for_slots(self, process, num):
        """An event generator that waits for empty slots.

        Wait until `process` can produce `num` tokens. Then, unblock `process`
        and return.

        Note:
            The process must be in the
            :const:`~pykpn.simulate.process.ProcessState.BLOCKED` state!

        Args:
            process (RuntimeProcess): the process that waits for tokens
            num (int): number of tokens to wait for

        Yields:
            ~simpy.events.Event: a series of events until `process`
            can produce `num` tokens
        """
        assert process.check_state(ProcessState.BLOCKED)

        self._log.debug('wait until %s can produce %d tokens',
                        process.full_name, num)

        while True:
            yield self.tokens_consumed
            if self.can_produce(process, num):
                break

        self._log.debug('enough slots available -> unblock %s',
                        process.full_name)
        process.unblock()

    def consume(self, process, num):
        """An event generator that models a consume operation.

        Models the consume operation according to the associated primitive
        (:attr:`_primitive`). It iterates over all communication phases and
        pays for the communication costs as calculated by the phase object.
        For each phase, it also iterates over all resources and checks for the
        ``simpy_resource`` attribute. If present, the resource is requested at
        the start of the phase and released at its end.

        Note:
            The process must be in the
            :const:`~pykpn.simulate.process.ProcessState.RUNNING` state!
        Args:
            process (RuntimeProcess): the process that waits for tokens
            num (int): number of tokens to wait for
        Yields:
            ~simpy.events.Event: a series of events until `process`
            completes the consume operation
        Raises:
            ValueError: if the process is not registered as a sink
            ValueError: if `num` is not an integer greater than 0
            RuntimeError: if no source is registered to the channel
            RuntimeError: if `process` cannot access the communication
                primitive
        """
        assert self.can_consume(process, num)
        assert process.check_state(ProcessState.RUNNING)

        sink = process.processor
        prim = self._primitive
        log = self._log

        log.debug('start a consume operation reading %d tokens using %s',
                  num, prim.name)

        if sink not in prim.consumers:
            raise RuntimeError(
                'processor %s cannot consume tokens using the primitive %s' %
                (sink.name, prim.name))

        # update the state
        new_state = self._fifo_state[process.name] - num
        self._fifo_state[process.name] = new_state

        # record the consume operation in the simulation trace
        self.trace_writer.update_counter(self.app.name,
                                         self.name,
                                         self._fifo_state.copy(),
                                         category="Channel")

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
            yield self.env.timeout(ticks)

            # release all resources that we requested before
            for (res, req) in zip(phase.resources, requests):
                if req is not None:
                    log.debug('release resource %s', r.name)
                    res.simpy_resource.release(req)

            log.debug('communication phase completed')

        log.debug('consume operation completed')

        # notify waiting processes
        self.tokens_consumed.succeed()
        self.tokens_consumed = self.env.event()

    def produce(self, process, num):
        """An event generator that models a produce operation.

        Models the produce operation according to the associated primitive
        (:attr:`_primitive`). It iterates over all communication phases and
        pays for the communication costs as calculated by the phase object.
        For each phase, it also iterates over all resources and checks for the
        ``simpy_resource`` attribute. If present, the resource is requested at
        the start of the phase and released at its end.

        Note:
            The process must be in the
            :const:`~pykpn.simulate.process.ProcessState.RUNNING` state!
        Args:
            process (RuntimeProcess): the process that waits for tokens
            num (int): number of tokens to wait for
        Yields:
            ~simpy.events.Event: a series of events until `process`
            completes the produce operation
        Raises:
            ValueError: if the process is not registered as a sink
            ValueError: if `num` is not an integer greater than 0
            RuntimeError: if no source is registered to the channel
            RuntimeError: if `process` cannot access the communication
                primitive
        """
        assert self.can_produce(process, num)
        assert process.check_state(ProcessState.RUNNING)

        src = process.processor
        prim = self._primitive
        log = self._log

        log.debug('start a produce operation writing %d tokens using %s',
                  num, prim.name)

        if src not in prim.producers:
            raise RuntimeError(
                'processor %s cannot produce tokens using the primitive %s' %
                (src.name, prim.name))

        # update the state
        for p in self._fifo_state:
            self._fifo_state[p] += num

        # record the produce operation in the simulation trace
        self.trace_writer.update_counter(self.app.name,
                                         self.name,
                                         self._fifo_state.copy(),
                                         category="Channel")

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
            yield self.env.timeout(ticks)

            # release all resources that we requested before
            for (res, req) in zip(phase.resources, requests):
                if req is not None:
                    log.debug('release resource %s', r.name)
                    res.simpy_resource.release(req)

            log.debug('communication phase completed')

        log.debug('produce operation completed')

        # notify waiting processes
        self.tokens_produced.succeed()
        self.tokens_produced = self.env.event()

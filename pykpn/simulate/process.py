# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


"""Contains classes that manage simulation of (KPN) processes.

**Classes:**
    * :class:`ProcessState`: an enumeration of process states
    * :class:`RuntimeProcess`: base process model
    * :class:`RuntimeKpnProcess`: KPN process model
"""


from enum import Enum

from pykpn.common import logging
from pykpn.simulate.adapter import SimulateLoggerAdapter


log = logging.getLogger(__name__)


class ProcessState(Enum):
    """Denotes the state of a runtime process object.

    :cvar int CREATED: The process is instantiated but not started yet.
    :cvar int READY:       The process is ready and waits to be scheduled.
    :cvar int RUNNING:     The process is currently being executed.
    :cvar int BLOCKED:     The process is blocked and waits for a resource to
                           become available.
    :cvar int FINISHED:    The process completed its execution.
    """
    CREATED = 0
    READY = 1
    RUNNING = 2
    BLOCKED = 3
    FINISHED = 4


class RuntimeProcess(object):
    """Runtime instance of a process.

    Implements the process state machine and provides an API for triggering
    valid transitions from outside (e.g. by a scheduler). This class is
    designed to be a base class and does not provide any
    functionality. Subclasses should override :func:`workload` to implement the
    process functionality.

    :ivar str name: the process name
    :ivar ~simpy.core.Environment _env: the simpy environment
    :ivar ProcessState _state: The current process state.
    :ivar SimulateLoggerAdapter _log:
        an logger adapter to print messages with simulation context
    :ivar Processor processor: the processor that the processes currently runs
        on. This attribute is only valid in the :const:`~ProcessState.RUNNING`
        state.

    :ivar created: An event that triggers on entering the
        :const:`~ProcessState.CREATED` state.
    :ivar ready: An event that triggers on entering the
        :const:`~ProcessState.READY` state.
    :ivar running: An event that triggers on entering the
        :const:`~ProcessState.RUNNING` state.
    :ivar finished: An event that triggers on entering the
        :const:`~ProcessState.FINISHED` state.
    :ivar blocked: An event that triggers on entering the
        :const:`~ProcessState.BLOCKED` state.
    :vartype created: ~simpy.events.Event
    :vartype ready: ~simpy.events.Event
    :vartype running: ~simpy.events.Event
    :vartype blocked: ~simpy.events.Event
    :vartype finished: ~simpy.events.Event

    **State Machine:**

        **States:** See :class:`ProcessState`.

        **Events:**
          * :attr:`~created`: Triggered on entering the
            :const:`~ProcessState.CREATED` state.
          * :attr:`~ready`: Triggered on entering the
            :const:`~ProcessState.READY` state.
          * :attr:`~running`: Triggered on entering the
            :const:`~ProcessState.RUNNING` state.
          * :attr:`~finished`: Triggered on entering the
            :const:`~ProcessState.FINISHED` state.
          * :attr:`~blocked`: Triggered on entering the
            :const:`~ProcessState.BLOCKED` state.

        **Entry Actions:**
          * :func:`_cb_created`:  Callback of :attr:`created`
          * :func:`_cb_ready`:  Callback of :attr:`ready`
          * :func:`_cb_running`:  Callback of :attr:`running`
          * :func:`_cb_finished`: Callback of :attr:`finished`
          * :func:`_cb_blocked`: Callback of :attr:`blocked`

        **Transitions:**
          * :func:`start`: Transition from :const:`~ProcessState.CREATED` to
            :const:`~ProcessState.READY`
          * :func:`activate`: Transition from :const:`~ProcessState.READY` to
            :const:`~ProcessState.RUNNING`
          * :func:`finish`: Transition from :const:`~ProcessState.RUNNING` to
            :const:`~ProcessState.FINISHED`
          * :func:`block`: Transition from :const:`~ProcessState.RUNNING` to
            :const:`~ProcessState.BLOCKED`
          * :func:`unblock`: Transition from :const:`~ProcessState.BLOCKED` to
            :const:`~ProcessState.READY`
    """

    def __init__(self, name, env):
        """Initialize a runtime process.

        This is not intended to be used directly and should always be called
        by a subclass.

        :param name: The process name. This should be unique within the system.
        :param env: the simpy environment
        :type name: str
        :type env: simpy.core.Environment
        :type start_event: simpy.events.Event
        """
        self.name = name
        self._env = env
        self._state = ProcessState.CREATED
        self.processor = None
        self._log = SimulateLoggerAdapter(log, name, env)

        # setup the events
        self.created = self._env.event()
        self.created.callbacks.append(self._cb_created)
        self.ready = self._env.event()
        self.ready.callbacks.append(self._cb_ready)
        self.running = self._env.event()
        self.running.callbacks.append(self._cb_running)
        self.finished = self._env.event()
        self.finished.callbacks.append(self._cb_finished)
        self.blocked = self._env.event()
        self.blocked.callbacks.append(self._cb_blocked)

    def _transition(self, state_name):
        """Helper function for convenient state transitions.

        This updates the process state (:attr:`_state`), triggers the
        corresponding event, and reinitializes the event.

        :param str state_name: name of the state to be transitioned to
        """
        if not hasattr(ProcessState, state_name):
            raise RuntimeError(
                'Tried to transition to an invalid state (%s)' % (state_name))

        event_name = state_name.lower()
        cb_name = '_cb_' + state_name.lower()
        assert hasattr(self, event_name)
        assert hasattr(self, cb_name)

        # update the state
        self._state = getattr(ProcessState, state_name)

        old_event = getattr(self, event_name)
        old_event.succeed(self)

        new_event = self._env.event()
        new_event.callbacks.append(getattr(self, '_cb_' + event_name))
        setattr(self, event_name, new_event)

    def check_state(self, state):
        """Compare to internal state

        :param ProcessState state: the state to compare to
        :rtype bool:
        """
        return self._state == state

    def start(self, event=None):
        """Start the process.

        Start the process by transitioning to the :const:`~ProcessState.READY`
        state. This function may be called directly, but can also be registered
        as a callback to a simpy event.

        :param event: unused (only required for usage as a simpy callback)
        :type event: ~simpy.events.Event
        """
        assert(self._state == ProcessState.CREATED)
        self._log.debug('Process starts.')
        self.processor = None
        self._transition('READY')

    def activate(self, processor):
        """Start the process execution.

        Start the workload execution by transitioning to the
        :const:`~ProcessState.RUNNING` state.

        :param processor: The processor that executes the workload
        :type processor: Processor
        """
        assert(self._state == ProcessState.READY)
        self._log.debug('Start workload execution on processor %s',
                        processor.name)
        self.processor = processor
        self._transition('RUNNING')

    def finish(self):
        """Terminate the process.

        Terminate the process execution by transitioning to the
        :const:`~ProcessState.FINISHED` state.
        """
        assert(self._state == ProcessState.RUNNING)
        self._log.debug('Workload execution finished.')
        self.processor = None
        self._transition('FINISHED')

    def block(self):
        """Block the process.

        Interrupt the process execution by transitioning to the
        :const:`~ProcessState.BLOCKED` state.
        """
        assert(self._state == ProcessState.RUNNING)
        self._log.debug('Process blocks')
        self.processor = None
        self._transition('BLOCKED')

    def unblock(self):
        """Unblock the process.

        Mark the process as ready for execution by transitioning to the
        :const:`~ProcessState.READY` state.
        """
        assert(self._state == ProcessState.BLOCKED)
        self._log.debug('Process unblocks')
        self.processor = None
        self._transition('READY')

    def _cb_ready(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.READY`
        state.

        :param event: unused (only required to provide the callback interface)
        :type event: ~simpy.events.Event
        """
        assert(self._state == ProcessState.READY)
        self._log.debug('Entered READY state')

    def _cb_running(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.RUNNING`
        state.

        Starts a simpy process that executes :func:`workload`

        :param event: unused (only required to provide the callback interface)
        :type event: ~simpy.events.Event
        """
        assert(self._state == ProcessState.RUNNING)
        self._log.debug('Entered RUNNING state')
        self._env.process(self.workload())

    def _cb_finished(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.FINISHED`
        state.

        :param event: unused (only required to provide the callback interface)
        :type event: ~simpy.events.Event
        """
        assert(self._state == ProcessState.FINISHED)
        self._log.debug('Entered FINISHED state')

    def _cb_blocked(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.BLOCKED`
        state.

        :param event: unused (only required to provide the callback interface)
        :type event: ~simpy.events.Event
        """
        assert(self._state == ProcessState.BLOCKED)
        self._log.debug('Entered BLOCKED state')

    def _cb_created(self, event):
        """Callback invoked upon entering the :const:`~ProcessState.CREATED`
        state.

        :param event: unused (only required to provide the callback interface)
        :type event: ~simpy.events.Event
        """
        assert(self._state == ProcessState.CREATED)
        self._log.debug('Entered CREATED state')
        print('created')

    def workload(self):
        """Implements the process functionality.

        This is just a stub and may not be called. This has to be overridden by
        a subclass.

        :raises: NotImplementedError
        """
        raise NotImplementedError(
            'This function does not provide any functionality and should '
            'never be called. Override it in a subclass!')


class RuntimeKpnProcess(RuntimeProcess):
    """Runtime instance of a KPN process.

    :ivar _channels: Dictionary of channel names and there corresponding
        runtime object. This only includes channels that may be accessed by
        this process.
    :vartype _channels: dict[str, RuntimeChannel]
    :ivar _trace_generator: a trace generator object
    :vartype _trace_generator: TraceGenerator
    :ivar _start: a timeout event that triggers the start of this process
    :vartype _start: ~simpy.events.Timeout
    :ivar _current_segment: The trace segment that is currently processed
    :vartype _current_segment: TraceSegment
    """

    def __init__(self, name, trace_generator, env, start_at_tick=0):
        """Initialize a kpn runtime process

        :param name: The process name. This should be unique across
            applications within the same system.
        :type name: str
        :param trace_generator: a trace generator object
        :type trace_generator: TraceGenerator
        :param env: the simpy environment
        :type env: ~simpy.core.Environment
        :param start_at_tick: tick at which the process execution should start
        :type start_at_tick: int
        """
        log.debug('initialize new KPN runtime process (%s)', name)

        super().__init__(name, env)

        self._channels = {}
        self._trace_generator = trace_generator

        self._start = env.timeout(start_at_tick)
        self._start.callbacks.append(self.start)

        self._current_segment = None

    def connect_to_incomming_channel(self, channel):
        """Connect the process to an incoming runtime channel

        Makes the process a sink of the channel.

        :param RuntimeChannel channel:
            the channel to connect to
        """
        self._channels[channel.name] = channel
        channel.add_sink(self)

    def connect_to_outgoing_channel(self, channel):
        """Connect the process to an outgoing runtime channel

        Makes the process the source of the channel.

        :param RuntimeChannel channel:
            the channel to connect to
        """
        self._channels[channel.name] = channel
        channel.set_src(self)

    def workload(self):
        """Replay a KPN execution trace

        Iterates over all segments in the execution trace and performs actions
        as specified by the segments. By returning, the execution
        terminates. However, this does not mean that it is actually complete. A
        process may also return when it blocks. Then the execution is resumed
        on the next call of this method.
        """

        if self._current_segment is None:
            self._log.debug('start workload execution')
        else:
            self._log.debug('resume workload execution')

        while True:
            if self._current_segment is None:
                self._current_segment = self._trace_generator.next_segment(
                    self.name, self.processor.type)
            s = self._current_segment
            s.sanity_check()
            if s.processing_cycles is not None:
                cycles = s.processing_cycles
                self._log.debug('process for %d cycles', cycles)
                ticks = self.processor.ticks(cycles)
                s.processing_cycles = None
                yield self._env.timeout(ticks)
            if s.read_from_channel is not None:
                c = self._channels[s.read_from_channel]
                self._log.debug('read %d tokens from channel %s', s.n_tokens,
                                c.name)
                if not c.can_consume(self, s.n_tokens):
                    self._log.debug('not enough tokens available -> block')
                    self.block()
                    self._env.process(c.wait_for_tokens(self, s.n_tokens))
                    return
                else:
                    s.read_from_channel = None
                    yield self._env.process(c.consume(self, s.n_tokens))
            if s.write_to_channel is not None:
                c = self._channels[s.write_to_channel]
                self._log.debug('write %d tokens to channel %s', s.n_tokens,
                                c.name)
                if not c.can_produce(self, s.n_tokens):
                    self._log.debug('not enough slots available -> block')
                    self.block()
                    self._env.process(c.wait_for_slots(self, s.n_tokens))
                    return
                else:
                    s.write_to_channel = None
                    yield self._env.process(c.produce(self, s.n_tokens))
            if s.terminate:
                self._log.debug('process terminates')
                break

            self._current_segment = None

        self.finish()

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
from enum import Enum

from .adapter import SimulateLoggerAdapter

log = logging.getLogger(__name__)


class ProcessState(Enum):
    """Denotes the state of a runtime process object.
    :cvar int NOT_STARTED: The process is instantiated but not started yet.
    :cvar int READY:       The process is ready and waits to be scheduled.
    :cvar int RUNNING:     The process is currently being executed.
    :cvar int BLOCKED:     The process is blocked and waits for a resource to
                           become available.
    :cvar int FINISHED:    The process completed its execution.
    """
    NOT_STARTED = 0
    READY = 1
    RUNNING = 2
    BLOCKED = 3
    FINISHED = 4


class RuntimeProcess(object):
    """Runtime instance of a process.

    This class implements the process state machine and provides an API for
    managing the process from outside (e.g. by a scheduler). It is designed to
    be a base class and does not provide any functionality. In order to be
    useful, subclasses need to override the :func:`workload` method.

    :ivar name: the process name
    :type name: str
    :ivar _env: the simpy environment
    :type _env: simpy.core.Environment
    :ivar _state: The current process state.
    :type _state: ProcessState
    :ivar _log: an logger adapter to print messages with simulation context
    :type _log: SimulateLoggerAdapter

    :ivar running: An event that triggers on entering the ``RUNNING`` state.
    :ivar finished: An event that triggers on entering the ``FINISHED`` state.
    :type running: :class:`simpy.events.Event`
    :type finished: :class:`simpy.events.Event`

    State Machine
    =============
    This section describes the state machine that this class implements.

    States
    ------
    See :class:`ProcessState`.

    Events
    ------
    * :attr:`running`:  Triggered on entering the ``RUNNING`` state.
    * :attr:`finished`: Triggered on entering the ``FINISHED`` state.

    Entry Actions
    -------------
    * :func:`_cb_running`:  Callback of :attr:`running`
    * :func:`_cb_finished`: Callback of :attr:`finished`

    Transitions
    -----------
    * :func:`start`:  Transition from ``NOT_STARTED`` to ``RUNNING``
    * :func:`finish`: Transition from ``RUNNING`` to ``FINISHED``
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
        self._state = ProcessState.NOT_STARTED
        self._log = SimulateLoggerAdapter(log, name, env)

        # setup the events
        self.running = self._env.event()
        self.running.callbacks.append(self._cb_running)
        self.finished = self._env.event()
        self.finished.callbacks.append(self._cb_finished)

    def start(self, event=None):
        """Start the process execution.

        Start the process execution and transition to the ``RUNNING``
        state. This function may be called directly or be registered as a
        callback to a simpy event.
        :param event: unused (only required for usage as a simpy ecallback)
        """
        assert(self._state == ProcessState.NOT_STARTED)
        log.debug('Process starts its execution.')
        self._state = ProcessState.RUNNING
        self.running.succeed(self)

    def finish(self, event=None):
        """Finish the process execution.

        Finish the process execution and transition to the ``FINISHED``
        state. This function may be called directly or be registered as a
        callback to a simpy event.
        :param event: unused (only required for usage as a simpy ecallback)
        """
        assert(self._state == ProcessState.RUNNING)
        self._log.debug('Process finishes its execution.')
        self._state = ProcessState.FINISHED

    def _cb_running(self, event):
        """Callback invoked upon entering the ``RUNNING`` state

        Starts a simpy process that executes :func:`workload`
        :param event: unused (only required to provide the callback interface)
        """
        assert(self._state == ProcessState.RUNNING)
        self._log.debug('Entered RUNNING state')
        self._env.process(self.workload())

    def _cb_finished(self, event):
        """Callback invoked upon entering the ``FINISHED`` state

        Does not do anything useful yet
        :param event: unused (only required to provide the callback interface)
        """
        assert(self._state == ProcessState.FINISHED)
        self._log.debug('Entered FINISHED state')
        # TODO do smth useful

    def workload(self):
        """Implements the functionality of this process

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
    :type _channels: dict[str, RuntimeChannel]
    """

    def __init__(self, name, mapping_info, env, start_at_tick=0):
        """Initialize a kpn runtime process

        :param name: The process name. This should be unique across
            applications within the same system.
        :type name: str
        :param mapping_info: the mapping info object for this process
        :type mapping_info: ProcessMappingInfo
        :param env: the simpy environment
        :type env: simpy.core.Environment
        :param start_at_tick: tick at which the process execution should start
        :type start_at_tick: int
        """
        log.debug('initialize new KPN runtime process (%s)', name)

        super().__init__(name, env)

        self._channels = {}

        self._start = env.timeout(start_at_tick)
        self._start.callbacks.append(self.start)

    def connect_to_incomming_channel(self, channel):
        """Connect the process to a incoming runtime channel

        This makes this process a sink of the channel.

        :param RuntimeChannel channel:
            the channel to connect to
        """
        self._channels[channel.name] = channel
        channel.add_sink(self)

    def connect_to_outgoing_channel(self, channel):
        """Connect the process to a outgoing runtime channel

        This makes this process the source of the channel.

        :param RuntimeChannel channel:
            the channel to connect to
        """
        self._channels[channel.name] = channel
        channel.set_src(self)

    def workload(self):
        self._log.debug('workload')

        for i in range(0, 10):
            self._log.debug('process i=%d', i)
            yield self._env.timeout(20)  # dummy workload

        self.finish()

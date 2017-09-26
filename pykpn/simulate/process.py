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
    """Represents the runtime instance of a KPN process.

    :ivar str name:
        the process name
    :ivar _env:
        the simpy environment
    :ivar dict[str, RuntimeChannel] _channels:
        Dictionary of channel names and there corresponding runtime
        object. This only includes channels that may be accessed by this
        process.
    :ivar ProcessState _state:
        The current process state.
    """

    def __init__(self, name, mapping_info, env, start_at_tick=0):
        """Initialize a runtime process

        :param str name:
            The process name. This should be unique across applications within
            the same system.
        :param ProcessMappingInfo mapping_info:
            the mapping info object for this process
        :param env:
            the simpy environment
        :param int start_at_tick:
            delay the process start to this tick
        """
        log.debug('initialize new runtime process: %s', name)

        self.name = name     #: the process name
        self._env = env      #: the simpy environment
        self._channels = {}  #: a dict of channel names and channel objects
        self._state = ProcessState.NOT_STARTED

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

    def run(self):
        """SimPy process

        Replays the execution trace of a kpn process.
        """
        assert self._state == ProcessState.NOT_STARTED
        pass

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging

log = logging.getLogger(__name__)


class RuntimeChannel(object):
    """Represents the runtime instance of a KPN channel.

    :ivar name:   the channel name
    :type name:   str
    :ivar _env:   the simpy environment
    :ivar _src:   the source process of this channel
    :type _src:   RuntimeProcess
    :ivar _sinks: list of sink processes of this channel
    :type _sinks: list[RuntimeProcess]
    """

    def __init__(self, name, mapping_info, env):
        """Initialize a runtime channel.

        :param str name: the channel name
        :param mapping_info: a channel mapping info object
        :type mapping_info: ChannelMappingInfo
        :param env: the simpy environment
        """
        log.debug('initialize new runtime channel: (%s)', name)

        self.name = name
        self._env = env
        self._src = None
        self._sinks = []

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

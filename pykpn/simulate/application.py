# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pykpn.util import logging
from pykpn.simulate.channel import RuntimeChannel
from pykpn.simulate.process import RuntimeKpnProcess


log = logging.getLogger(__name__)


class RuntimeApplication(object):
    """Represents the runtime instance of an application.

    Attributes:
        name (str): the application name
    """

    def __init__(self, name):
        """Initialize a RuntimeApplication

        Args:
            name (str): the application name
        """
        self.name = name


class RuntimeKpnApplication(RuntimeApplication):
    """Represents the runtime instance of a kpn application.

    :ivar Mapping mapping:
        mapping object for this application
    :ivar list[RuntimeProcess] _pocesses:
        a list of runtime processes that belong to this application
    :ivar list[RuntimeChannel] _channels:
        a list of runtime channels that belong to this application
    """

    def __init__(self, name, kpn_graph, mapping, trace_generator, env,
                 start_at_tick=0):
        """Initialize a RuntimeKpnApplication.

        :param name: name of the application
        :type name: str
        :param kpn_graph: the corresponding KpnGraph object
        :type kpn_graph: KpnGraph
        :param mapping: the corresponding Mapping object
        :type mapping: Mapping
        :param trace_generator: the trace generator object to be used by the
            processes belonging to this application
        :type trace_generator: TraceGenerator
        :param env: the simpy environment object
        :param start_at_tick: delay the application start to this tick
        :type start_at_tick: int
        """
        super().__init__(name)
        self.mapping = mapping
        if mapping.kpn != kpn_graph:
            log.error("KPN and mapping incompatible in RuntimeKpnApplication")

        log.info('initialize new runtime application: %s', name)
        logging.inc_indent()

        # Instantiate all channels
        self._channels = {}
        for c in kpn_graph.channels():
            c_name = '%s.%s' % (name, c.name)
            mapping_info = mapping.channel_info(c)
            self._channels[c.name] = RuntimeChannel(
                c_name, mapping_info, c.token_size, env)

        # Instantiate all processes
        self._processes = {}
        for p in kpn_graph.processes():
            p_name = '%s.%s' % (name, p.name)
            mapping_info = mapping.process_info(p)
            proc = RuntimeKpnProcess(p_name, trace_generator, env,
                                     start_at_tick)
            self._processes[p.name] = proc
            logging.inc_indent()
            for c in p.incoming_channels:
                rc = self._channels[c.name]
                log.debug('make process %s a sink to %s', p_name, rc.name)
                proc.connect_to_incomming_channel(rc)
            for c in p.outgoing_channels:
                rc = self._channels[c.name]
                log.debug('make process %s a source to %s', p_name, rc.name)
                proc.connect_to_outgoing_channel(rc)
            logging.dec_indent()

        logging.dec_indent()

    def processes(self):
        """Get a list of all processes

        :returns: a list of the application's processes
        :rtype: list[RuntimeProcess]
        """
        return self._processes.values()

    def channels(self):
        """Get a list of all channels

        :returns: a list of the application's channels
        :rtype: list[RuntimeChannel]
        """
        return self._channels.values()

    def find_process(self, process_name):
        """Find a process by name"""
        return self._processes[process_name]

    def find_channel(self, channel_name):
        """Find a channel by name"""
        return self._channeles[channel_name]

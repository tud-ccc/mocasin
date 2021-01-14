# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from mocasin.util import logging
from mocasin.simulate.channel import RuntimeChannel
from mocasin.simulate.process import RuntimeKpnProcess
from mocasin.simulate.adapter import SimulateLoggerAdapter


log = logging.getLogger(__name__)


class RuntimeApplication(object):
    """Represents the runtime instance of an application.

    Attributes:
        name (str): the application name
        system (System): the system the application is supposed to be
            executed on
    """

    def __init__(self, name, system):
        """Initialize a RuntimeApplication

        Args:
            name (str): the application name
            system (System): the system the application is supposed to be
                executed on
        """
        self.name = name
        self.system = system

    @property
    def env(self):
        """The simpy environment"""
        return self.system.env


class RuntimeKpnApplication(RuntimeApplication):
    """Represents the runtime instance of a kpn application.

    :ivar Mapping mapping:
        mapping object for this application
    :ivar list[RuntimeProcess] _pocesses:
        a list of runtime processes that belong to this application
    :ivar list[RuntimeChannel] _channels:
        a list of runtime channels that belong to this application
    """

    def __init__(self, name, kpn_graph, mapping, trace_generator, system):
        """Initialize a RuntimeKpnApplication.

        Args:
            name (str): the application name
            kpn_graph (KpnGraph): the graph denoting the KPN application
            mapping (Mapping): a mapping to the platform implemented by system
            trace_generator (TraceGenerator): the trace generator that
                represents the execution trace of the application trace
            system (System): the system the application is supposed to be
                executed on
        """
        super(RuntimeKpnApplication, self).__init__(name, system)
        self.mapping = mapping
        if mapping.kpn != kpn_graph:
            raise RuntimeError("KPN and mapping incompatible")
        if mapping.platform != system.platform:
            raise RuntimeError(f"Mapping {name} to an incompatible platform")

        log.debug('initialize new runtime application: %s', name)
        logging.inc_indent()

        # Instantiate all channels
        self._channels = {}
        for c in kpn_graph.channels():
            mapping_info = mapping.channel_info(c)
            self._channels[c.name] = RuntimeChannel(
                c.name, mapping_info, c.token_size, self)

        # Instantiate all processes
        self._processes = {}
        self._mapping_infos = {}
        for p in kpn_graph.processes():
            mapping_info = mapping.process_info(p)
            proc = RuntimeKpnProcess(p.name, trace_generator, self)
            self._processes[p.name] = proc
            self._mapping_infos[proc] = mapping_info
            logging.inc_indent()
            for c in p.incoming_channels:
                rc = self._channels[c.name]
                log.debug('make process %s a sink to %s', proc.full_name,
                          rc.name)
                proc.connect_to_incomming_channel(rc)
            for c in p.outgoing_channels:
                rc = self._channels[c.name]
                log.debug('make process %s a source to %s', proc.full_name,
                          rc.name)
                proc.connect_to_outgoing_channel(rc)
            logging.dec_indent()
        logging.dec_indent()

        self._log = SimulateLoggerAdapter(log, self.name, self.env)

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

    def run(self):
        """Start execution of this application

        Yields:
            ~simpy.events.Event: an event that is triggered when the
                application finishes execution.
        """
        self._log.info(f"Application {self.name} starts")
        for process, mapping_info in self._mapping_infos.items():
            self.system.start_process(process, mapping_info)
        finished = self.env.all_of([p.finished for p in self.processes()])
        finished.callbacks.append(lambda _: self._log.info(
            f"Application {self.name} terminates"))
        yield finished

    def kill(self):
        """Stop execution of this application

        This method kills each running process of this application. The
        processes might not stop immediately as operations such as producing
        or consuming tokens are considered atomic an cannot be interrupted.
        The simpy process managing run will terminate as soon as all processes
        terminated.

        Examples:
            Usage::

                app_finished = env.process(app.run())
                yield env.timeout(1000000000)  # wait 1ms
                app.kill()
                yield app_finished  # wait until the application stopped completely

        """
        for p in self.processes():
            p.kill()

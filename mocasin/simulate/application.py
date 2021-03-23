# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


from mocasin.util import logging
from mocasin.simulate.channel import RuntimeChannel
from mocasin.simulate.process import RuntimeDataflowProcess
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


class RuntimeDataflowApplication(RuntimeApplication):
    """Represents the runtime instance of a dataflow application.

    Attributes:
        mapping (Mapping): a mapping object for this application
        _pocesses (list of RuntimeProcess): a list of runtime processes that
            belong to this application
        _channeles (list of RuntimeChannel): a list of runtime channels that
        belong to this application

    Args:
        name (str): the application name
        graph (DataflowGraph): the graph denoting the dataflow application
        mapping (Mapping): a mapping to the platform implemented by system
        trace (DataflowTrace): the trace representing the execution
            behavior of the application
        system (System): the system the application is supposed to be
            executed on
    """

    def __init__(self, name, graph, app_trace, system):
        super().__init__(name, system)
        self.graph = graph
        self.trace = app_trace

        self._is_running = False
        self._is_finished = False

        # a dict mapping each process to a processor/scheduler
        # leave it uninitialized for now, it will set by calling run()
        self._process_mappings = None

        log.debug("initialize new runtime application: %s", name)

        # Instantiate all channels
        self._channels = {}
        for c in graph.channels():
            self._channels[c.name] = RuntimeChannel(
                c.name, c.token_size, self
            )

        # Instantiate all processes
        self._processes = {}
        for p in graph.processes():
            proc = RuntimeDataflowProcess(
                p.name, app_trace.get_trace(p.name), self
            )
            self._processes[p.name] = proc
            for c in p.incoming_channels:
                rc = self._channels[c.name]
                proc.connect_to_incomming_channel(rc)
            for c in p.outgoing_channels:
                rc = self._channels[c.name]
                proc.connect_to_outgoing_channel(rc)

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
        return self._channels[channel_name]

    def run(self, mapping):
        """Start execution of this application

        Yields:
            ~simpy.events.Event: an event that is triggered when the
                application finishes execution.
        """
        assert not (self._is_running or self._is_finished)
        assert not self._process_mappings
        self._is_running = True

        self._log.info(f"Application {self.name} starts")

        # map all processes and channels

        # first some sanity checks
        if mapping.graph != self.graph:
            raise RuntimeError("dataflow graph and mapping incompatible")
        if mapping.platform != self.system.platform:
            raise RuntimeError(f"Mapping {self.name} to an incompatible platform")

        # map all channels:
        for channel in self.graph.channels():
            info = mapping.channel_info(channel)
            self.find_channel(channel.name).update_mapping_info(info)

        # map all processes
        self._process_mappings = {}
        for process in self.graph.processes():
            info = mapping.process_info(process)
            runtime_process = self.find_process(process.name)
            self._process_mappings[runtime_process] = info.affinity

        # start all the processes
        for process, processor in self._process_mappings.items():
            self.system.start_process(process, processor)
        # create an event that is triggered when all processes completed and
        # wait for this event
        finished = self.env.all_of([p.finished for p in self.processes()])
        finished.callbacks.append(self._app_finished_callback)
        yield finished

    def _app_finished_callback(self, event):
        self._log.info(f"Application {self.name} terminates")
        self._running = False
        self._finished = True

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

    def is_running(self):
        """Check if the application is running."""
        assert not (self._is_running and self._is_finished)
        return self._is_running

    def is_finished(self):
        """Check if the application is finished."""
        assert not (self._is_running and self._is_finished)
        return self._is_finished

    def update_mapping(self, mapping):
        """Update the mapping used by this application, causing a migration of
           processes.

        Args:
             Mapping: an updated mapping to be used by the application
        """
        assert self.is_running()

        self._log.debug(f"Update mapping of application {self.name}")

        # iterate over all proceses
        for process in self._process_mappings.keys():
            current_processor = self._process_mappings[process]
            dataflow_process = self.graph.find_process(process.name)
            new_processor = mapping.process_info(dataflow_process).affinity

            # move the process
            if current_processor != new_processor:
                self._log.debug(
                    f"Move process {process.full_name} from {current_processor}"
                    f" to {new_processor}"
                )
                self._process_mappings[process] = new_processor
                self.system.move_process(
                    process, current_processor, new_processor
                )

        # iterate over all channels
        for name, channel in self._channels.items():
            dataflow_channel = self.graph.find_channel(name)
            mapping_info = mapping.channel_info(dataflow_channel)
            self._log.debug(
                f"Update channel primitive to {mapping_info.primitive.name}"
            )
            channel.update_mapping_info(mapping_info)

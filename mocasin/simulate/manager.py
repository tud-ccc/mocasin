# Copyright (C) 2021 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov, Christian Menard

import logging

from mocasin.simulate.adapter import SimulateLoggerAdapter

log = logging.getLogger(__name__)


class RuntimeManager:
    def __init__(self, system):
        self.system = system

        # a special logger that allows printing timestamped messages
        self._log = SimulateLoggerAdapter(log, self.name, self.env)

        # an event indicating that runtime manager should shut down
        self._request_shutdown = self.env.event()

    @property
    def name(self):
        """The runtime manager name."""
        raise NotImplementedError(
            "This property needs to be overridden by a subclass"
        )

    @property
    def env(self):
        """The simpy environment."""
        return self.system.env

    def run(self):
        """Start a simpy process modelling the runtime manager."""
        raise NotImplementedError(
            "This method needs to be overridden by a subclass"
        )

    def shutdown(self):
        """Terminate the runtime manager.

        The runtime manager will not stop immediately but wait until all
        currently running applications terminate.
        """
        self._log.debug("Shutdown was requested")
        self._request_shutdown.succeed()

    def start_applications(self, graphs, traces):
        """Start new applications.

        The runtime manager expects arguments graphs and traces be lists of the
        equal size.
        """
        raise NotImplementedError(
            "This method needs to be overridden by a subclass"
        )

# Copyright (C) 2021 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov, Christian Menard

import csv
from dataclasses import asdict, dataclass, field
import logging

from mocasin.simulate.adapter import SimulateLoggerAdapter

log = logging.getLogger(__name__)


@dataclass
class ManagerStatisticsApplicationEntry:
    """A log entry of the application scheduling with the runtime manager."""

    name: str
    arrival: int
    deadline: int

    accepted: bool = field(default=None, init=False)
    expected_end_time: float = field(default=None, init=False)

    start_time: int = field(default=None, init=False)
    end_time: int = field(default=None, init=False)
    missed_deadline: bool = field(default=None, init=False)

    def to_dict(self):
        """Get the dict representation."""
        return asdict(self)


@dataclass
class ManagerStatisticsActivationEntry:
    """A log entry of the runtime manager activation."""

    activation_time: int
    num_new_apps: int
    num_accepted_apps: int
    num_prev_apps: int
    scheduling_time: int

    def to_dict(self):
        """Get the dict representation."""
        return asdict(self)


class ManagerStatistics:
    """Collection and export of statistics after simulation."""

    def __init__(self):
        self.applications = {}
        self.activations = []

    def new_application(self, graph, arrival=None, deadline=None):
        """Create an application entry."""
        # TODO: Change the argument graph to runtime application.
        entry = ManagerStatisticsApplicationEntry(
            name=graph.name, arrival=arrival, deadline=deadline
        )
        self.applications[entry.name] = entry
        return entry

    def new_activation(
        self, activation_time, num_new, num_accepted, num_prev, scheduling_time
    ):
        """Create an activation entry."""
        entry = ManagerStatisticsActivationEntry(
            activation_time=activation_time,
            num_new_apps=num_new,
            num_accepted_apps=num_accepted,
            num_prev_apps=num_prev,
            scheduling_time=scheduling_time,
        )
        self.activations.append(entry)
        return entry

    def total_applications(self):
        """Returns the total number of applications."""
        return len(self.applications)

    def total_accepted(self):
        """Returns the number of accepted applications."""
        return sum([1 for x in self.applications.values() if x.accepted])

    def total_rejected(self):
        """Returns the number of rejected applications."""
        return self.total_applications() - self.total_accepted()

    def total_missed(self):
        """Returns the number of applications missed the deadline."""
        return sum([1 for x in self.applications.values() if x.missed_deadline])

    def total_activations(self):
        """Returns the total number of activations."""
        return len(self.activations)

    def total_scheduling_time(self):
        """Returns the total scheduling time."""
        return sum(x.scheduling_time for x in self.activations)

    def average_scheduling_time(self):
        """Returns the average scheduling time."""
        return self.total_scheduling_time() / self.total_activations()

    def find_application(self, name):
        """Find the entry by the applications name."""
        return self.applications.get(name, None)

    def dump_applications(self, filename):
        """Dump application entries to a CSV file."""
        if not self.applications:
            log.warning(
                "No records of applications in the manager statistics. "
                "Skip dumping."
            )
            return
        elem = next(iter(self.applications.values()))
        fieldnames = list(elem.to_dict().keys())
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.applications.values():
                writer.writerow(entry.to_dict())

    def dump_activations(self, filename):
        """Dump activation entries to a CSV file."""
        if not self.activations:
            log.warning(
                "No records of activations in the manager statistics. "
                "Skip dumping."
            )
            return
        elem = next(iter(self.activations))
        fieldnames = list(elem.to_dict().keys())
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.activations:
                writer.writerow(entry.to_dict())


class RuntimeManager:
    """Base class for runtime managers.

    The runtime manager is used in the multi-application simulations. To start
    the applications, the method `start_applications` should be called.

    Args:
        system (System): the system
    """

    def __init__(self, system):
        self.system = system
        self.statistics = ManagerStatistics()

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

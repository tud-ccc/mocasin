# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov
import logging
import os
import time

from mocasin.simulate.manager import ManagerStatistics
from mocasin.tetris.job_request import JobRequestStatus


log = logging.getLogger(__name__)


class TracePlayer:
    """Trace player.

    This class simulates a trace scenario, which consists of events of
    applications arrival. The trace is read from CSV file.

    FIXME: Now we supply input events in the forms of the requests, in the
    resource manager we create also requests.

    Args:
        resource_manager (ResourceManager): A resource manager
        events (list of JobRequestInfo): List of input requests
        dump_summary (bool): A flag to dump the summary (default: False)
        dump_path (str): A path to summary file
    """

    def __init__(
        self, resource_manager, events, dump_summary=False, dump_path=""
    ):
        self.resource_manager = resource_manager

        # Read scenario from file
        self._events = events
        self._requests = []

        # Initialize time
        self._time = 0.0

        # Statistics
        self.stats = ManagerStatistics()

        # Initialize dump paramerers
        self._dump_summary = dump_summary
        self._dump_path = dump_path

    def _simulate_to(self, new_time):
        assert isinstance(new_time, (int, float))
        assert new_time >= self._time

        if new_time > self._time:
            # Update manager's state
            self.resource_manager.advance_to_time(new_time)

        self._time = new_time

    def run(self):
        """Run the simulation."""
        self._simulation_start_time = time.time()
        log.info("Simulation started")

        for event_no, event in enumerate(self._events):
            log.debug(f"Handling request {event.to_str()}")
            graph = event.app
            mappings = event.mappings
            arrival = event.arrival
            deadline = event.deadline
            self._simulate_to(arrival)

            num_prev_apps = len(self.resource_manager.requests)

            request = self.resource_manager.new_request(
                graph, mappings, deadline - arrival
            )
            stats_entry = self.stats.new_application(
                graph, arrival=arrival, deadline=deadline
            )

            self._requests.append(request)
            (
                schedule,
                scheduling_time,
            ) = self.resource_manager.generate_schedule()

            accepted = schedule is not None

            if accepted:
                # Job is accepted
                accepted_str = "ACCEPTED"
                stats_entry.accepted = True
                num_accepted = 1
            else:
                # Job is refused
                accepted_str = "REFUSED"
                stats_entry.accepted = False
                num_accepted = 0

            self.stats.new_activation(
                arrival, 1, num_accepted, num_prev_apps, scheduling_time
            )

            log.info(
                f"T={arrival:8.2f}: "
                f"Req#{event_no + 1:02} {graph.name:4} dl={deadline:8.3f} | "
                f"ARs={len(self.resource_manager.requests)} "
                f"st={scheduling_time:.3f}s "
                f"=> {accepted_str}"
            )

        while self.resource_manager.schedule:
            self.resource_manager.advance_segment()

        new_time = self.resource_manager.state_time
        self._time = new_time
        log.info("Simulation finished at time {:.2f}".format(self._time))
        self._simulation_end_time = time.time()

        # TODO: Create methods is_new, is_arrived, ...
        assert all(r.status != JobRequestStatus.NEW for r in self._requests)
        assert all(r.status != JobRequestStatus.ARRIVED for r in self._requests)
        assert all(
            r.status != JobRequestStatus.ACCEPTED for r in self._requests
        )

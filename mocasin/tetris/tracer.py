# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov
import csv
import logging
import os
import time

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
            request = self.resource_manager.new_request(
                graph, mappings, deadline - arrival
            )
            self._requests.append(request)
            schedule, sched_time = self.resource_manager.generate_schedule()
            accepted_str = "ACCEPTED" if schedule else "REFUSED"

            log.info(
                f"T={arrival:8.2f}: "
                f"Req#{event_no+1:02} {graph.name:4} dl={deadline:8.3f} | "
                f"ARs={len(self.resource_manager.requests)} "
                f"st={sched_time:.3f}s "
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

        self._generate_stats()
        self._print_stats()
        self._dump_stats()

    def _generate_stats(self):
        self._stats = {
            "requests": len(self._requests),
            "accepted": sum(
                r.status == JobRequestStatus.FINISHED for r in self._requests
            ),
            "dynamic_energy": self.resource_manager.dynamic_energy,
            "scheduler": self.resource_manager.scheduler.name,
        }

    def _print_stats(self):
        log.info("==================================")
        log.info("Results:")
        log.info("Total requests: {}".format(self._stats["requests"]))
        log.info(
            "Accepted requests (rate): {} ({:.2f}%)".format(
                self._stats["accepted"],
                100 * self._stats["accepted"] / self._stats["requests"],
            )
        )
        log.info(f"Dynamic energy: {self._stats['dynamic_energy']:.3f}J")
        log.info("Simulated time: {:.2f}s".format(self._time))
        log.info(
            "Simulation time: {:.2f}s".format(
                self._simulation_end_time - self._simulation_start_time
            )
        )

    def _dump_stats(self):
        if not self._dump_summary:
            return
        if os.path.exists(self._dump_path):
            assert os.path.isfile(self._dump_path)
            mod = "a"
        else:
            mod = "w"

        with open(self._dump_path, mod) as f:
            if mod == "w":
                print(
                    "input_scenario,scheduler,requests,accepted,energy,"
                    "time_simulated,time_simulation",
                    file=f,
                )
            print(
                "{},{},{},{},{},{},{}".format(
                    self._scenario,
                    self._stats["scheduler"],
                    self._stats["requests"],
                    self._stats["accepted"],
                    self._stats["energy"],
                    self._time,
                    self._simulation_end_time - self._simulation_start_time,
                ),
                file=f,
            )

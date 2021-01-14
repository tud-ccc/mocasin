# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov
import csv
import os
import time

from mocasin.tetris.manager import ResourceManager

import logging
log = logging.getLogger(__name__)


class TracePlayer:
    """Trace player.

    This class simulates a trace scenario, which consists of events of
    applications arrival. The trace is read from CSV file.

    Args:
        manager (ResourceManager): A resource manager
        scenario (str): Path to scenario
        dump_summary (bool): A flag to dump the summary (default: False)
        dump_path (str): A path to summary file
    """
    def __init__(self, manager, requests, dump_summary=False, dump_path=""):
        assert isinstance(manager, ResourceManager)
        self.__manager = manager

        # Read scenario from file
        self.__events = requests

        # Initialize time
        self.__time = 0.0

        # Initialize dump paramerers
        self.__dump_summary = dump_summary
        self.__dump_path = dump_path

    def __simulate_to(self, new_time):
        assert isinstance(new_time, (int, float))
        assert new_time >= self.__time

        if new_time > self.__time:
            # Update manager's state
            self.__manager.simulate_to(new_time)

        self.__time = new_time

    def run(self):
        """Run the simulation."""
        self.__simulation_start_time = time.time()
        log.info("Simulation started")
        self.__manager.start()

        for request in self.__events:
            arr = request.arrival
            self.__simulate_to(arr)
            self.__manager.new_request(request)

        new_time = self.__manager.finish()
        self.__time = new_time
        log.info("Simulation finished at time {:.2f}".format(self.__time))
        self.__simulation_end_time = time.time()

        self.__print_stats()
        self.__dump_stats()

    def __print_stats(self):
        stats = self.__manager.stats()
        log.info("==================================")
        log.info("Results:")
        log.info("Total requests: {}".format(stats['requests']))
        log.info("Accepted requests (rate): {} ({:.2f}%)".format(
            stats['accepted'], 100 * stats['accepted'] / stats['requests']))
        log.info("Energy consumption: {:.3f}J".format(stats['energy']))
        log.info("Simulated time: {:.2f}s".format(self.__time))
        log.info(
            "Simulation time: {:.2f}s".format(self.__simulation_end_time -
                                              self.__simulation_start_time))

    def __dump_stats(self):
        if not self.__dump_summary:
            return
        if os.path.exists(self.__dump_path):
            assert os.path.isfile(self.__dump_path)
            mod = 'a'
        else:
            mod = 'w'

        stats = self.__manager.stats()

        with open(self.__dump_path, mod) as f:
            if mod == 'w':
                print(
                    "input_scenario,scheduler,requests,accepted,energy,"
                    "time_simulated,time_simulation", file=f)
            print(
                "{},{},{},{},{},{},{}".format(
                    self.__scenario, stats['scheduler'], stats['requests'],
                    stats['accepted'], stats['energy'], self.__time,
                    self.__simulation_end_time - self.__simulation_start_time),
                file=f)

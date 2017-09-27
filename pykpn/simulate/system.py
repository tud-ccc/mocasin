# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import timeit

from .scheduler import RuntimeScheduler
from ..common import logging

from simpy.resources.resource import Resource

log = logging.getLogger(__name__)


class RuntimeSystem:
    """The central class for managing a simulation.

    This class contains the simulation environment, the entire platform with
    instances of schedulers, and all applications running on top of it.

    :ivar _env: the simpy environment
    :ivar schedulers: list of all runtime schedulers
    :type schedulers: list[RuntimeScheduler]
    """

    def __init__(self, platform, applications, env):
        """Initialize a runtime system.

        :param platform: the platform to be simulated
        :type platform: Platform
        :param applications: list of applications to be run on the system
        :type applications: list[RuntimeApplication]
        :param env: the simpy environment
        """
        log.info('Initialize the system')
        logging.inc_indent()

        self._env = env

        # initialize all schedulers
        self._schedulers = []
        for s in platform.schedulers:
            scheduler = RuntimeScheduler(s, env)
            logging.inc_indent()
            for app in applications:
                mapping_info = app.mapping.scheduler_info(s)
                scheduler.add_application(app, mapping_info)
            logging.dec_indent()
            self._schedulers.append(scheduler)

        # Since the platform classes are designed such that they are
        # independent of the simulation implementation, the communication
        # resources do not have any notion of simpy resources. However, to
        # simulate the exclusiveness of resources correctly, we need simpy
        # resources that correspond to the communication resources. The best
        # way (TM) of doing this would be to create a runtime represantation of
        # the entire communicarion system (similar to Scheduler ->
        # RuntimeScheduler). However, since this would be quite extensive, we
        # use the following workaround.
        #
        # We iterate over all channels and their cost models to get all
        # communication resources that are required for simulation. For each
        # communication resource we create a simpy resource object and extend
        # the communication reource by an attribute 'simpy_resource' that
        # points to the simpy resource.
        for r in platform.communication_resources:
            if r.exclusive and not hasattr(r, 'simpy_resource'):
                r.simpy_resource = Resource(self.env, capacity=1)

        logging.dec_indent()
        return

    def simulate(self):
        log.info('Start the simulation')
        start = timeit.default_timer()

        # start all the schedulers
        for s in self._schedulers:
            self._env.process(s.run())

        self._env.run()

        stop = timeit.default_timer()

        log.info('Simulation done')
        exec_time = float(self._env.now) / 1000000000.0
        print('Total simulated time: ' + str(exec_time) + ' ms')
        print('Total simulation time: ' + str(stop - start) + ' s')

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from simpy.resources.resource import Resource

from pykpn.util import logging
from pykpn.simulate.process import ProcessState
from pykpn.simulate.scheduler import create_scheduler


log = logging.getLogger(__name__)


class RuntimeSystem:
    """The central class for managing a simulation.

    This class contains the simulation environment, the entire platform with
    instances of schedulers, and all applications running on top of it.

    :ivar _env: the simpy environment
    :ivar schedulers: list of all runtime schedulers
    :type schedulers: list[RuntimeScheduler]
    :ivar _applications: list of all applications
    :type _applications: list[RuntimeKpnApplication]
    """

    def __init__(self, platform, applications, env):
        """Initialize a runtime system.

        Most importantly, this sets up all the schedulers in the system.

        :param platform: the platform to be simulated
        :type platform: Platform
        :param applications: list of applications to be run on the system
        :type applications: list[RuntimeKpnApplication]
        :param env: the simpy environment
        """
        log.info('Initialize the system')
        logging.inc_indent()

        self._env = env
        self._applications = applications
        for app in applications:
            if app.mapping.platform != platform:
                log.error(f"Application {app.name} is mapped into a different platform than the system")


        # initialize all schedulers
        self._schedulers = []
        for sched in platform.schedulers():
            policy, policy_param = self._find_scheduler_policy(sched,
                                                               applications)
            if len(sched.processors) == 1:
                scheduler = create_scheduler(sched.name, sched.processors[0],
                                             policy, policy_param, env)
                self._schedulers.append(scheduler)

                for app in applications:
                    for p in app.mapping.scheduler_processes(sched):
                        scheduler.add_process(app.find_process(p.name))
            else:
                log.warning('True multi-processor scheduling is not supported '
                            'yet! -> split the %s scheduler into multiple '
                            'single-processor schedulers', sched.name)
                for proc in sched.processors:
                    name = '%s_%s' % (sched.name, proc.name)
                    scheduler = create_scheduler(name, proc, policy,
                                                 policy_param, env)
                    self._schedulers.append(scheduler)

                    for app in applications:
                        for p in app.mapping.scheduler_processes(sched):
                            affinity = app.mapping.affinity(p)
                            assert affinity in sched.processors
                            if affinity == proc:
                                scheduler.add_process(app.find_process(p.name))

        # Since the platform classes are designed such that they are
        # independent of the simulation implementation, the communication
        # resources do not have any notion of simpy resources. However, to
        # simulate the exclusiveness of resources correctly, we need simpy
        # resources that correspond to the communication resources. The best
        # way (TM) of doing this would be to create a runtime representation of
        # the entire communication system (similar to Scheduler ->
        # RuntimeScheduler). However, since this would be quite extensive, we
        # use the following workaround.
        #
        # We iterate over all channels and their cost models to get all
        # communication resources that are required for simulation. For each
        # communication resource we create a simpy resource object and extend
        # the communication resource by an attribute 'simpy_resource' that
        # points to the simpy resource.
        for r in platform.communication_resources():
            if r.exclusive and not hasattr(r, 'simpy_resource'):
                r.simpy_resource = Resource(self.env, capacity=1)

        logging.dec_indent()
        return

    def _find_scheduler_policy(self, scheduler, applications):
        policy = None
        policy_param = None
        for app in applications:
            mapping_info = app.mapping.scheduler_info(scheduler)
            if policy is None:
                policy = mapping_info.policy
                policy_param = mapping_info.param
                log.debug('The scheduler %s uses the policy %s',
                          scheduler.name, policy.name)
            else:
                if policy.name != mapping_info.policy.name:
                    log.warning(
                        '%s: The scheduling policy was already set' ' to %s '
                        'but the application %s requested a different policy '
                        '(%s) -> force old policy', self.name, policy.name,
                        app.name, mapping_info.policy.name)
                elif policy_param != mapping_info.param:
                    log.warning(
                        '%s: The application %s requested a different '
                        'scheduling policy parameter than the application '
                        'before -> use old parameter', self.name, app.name)
        return policy, policy_param

    def simulate(self):
        log.info('Start the simulation')

        for s in self._schedulers:
            self._env.process(s.run())

        self._env.run()

        log.info('Simulation done')

    def check_errors(self):
        for app in self._applications:
            some_blocked = False
            for p in app.processes():
                if p.check_state(ProcessState.BLOCKED):
                    log.error('The process %s is blocked', p.name)
                    some_blocked = True
                elif not p.check_state(ProcessState.FINISHED):
                    log.warning('The process %s did not finish its execution!',
                                p.name)
            if some_blocked:
                log.error('The application %s is deadlocked!', app.name)

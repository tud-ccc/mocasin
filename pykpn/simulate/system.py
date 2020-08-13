# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from simpy.resources.resource import Resource

from pykpn.util import logging
from pykpn.simulate.process import ProcessState
from pykpn.simulate.scheduler import create_scheduler
from pykpn.simulate.trace_writer import TraceWriter


log = logging.getLogger(__name__)


class SimulationError(Exception):
    pass


class RuntimeSystem:
    """The central class for managing a simulation.

    This class contains the simulation environment, the entire platform with
    instances of schedulers, and all applications running on top of it.

    Attributes:
        platform (Platform): the underlying platform of the system
        trace_writer (TraceWriter): a trace writer to record simulation traces
        _env: the simpy environment
        _processes (set(RuntimeProcess)): set of all processes that where
            executed by the system
        _schedulers (list(RuntimeScheduler)): list of all runtime schedulers that
            are part of the system
        _processors_to_schedulers (dict(Processor, RuntimeScheduler)): mapping
            of processors to their schedulers
    """

    def __init__(self, platform, env):
        """Initialize a runtime system.

        Most importantly, this sets up all the schedulers in the system.

        Args:
            platform (Platform): the platform to be simulated
            env: the simpy environment
        """
        log.info('Initialize the system')
        logging.inc_indent()

        self._env = env
        self.platform = platform

        self._processes = set()

        self.trace_writer = TraceWriter(env)

        # initialize all schedulers

        # list of all schedulers
        self._schedulers = []
        # a mapping of all processors to their schedulers
        self._processors_to_schedulers = {}
        for sched in platform.schedulers():
            if len(sched.processors) == 1:
                proc = sched.processors[0]
                scheduler = create_scheduler(sched.name, proc, sched.policy,
                                             self)
                self._schedulers.append(scheduler)
                self._processors_to_schedulers[proc] = scheduler
            else:
                log.warning('True multi-processor scheduling is not supported '
                            'yet! -> split the %s scheduler into multiple '
                            'single-processor schedulers', sched.name)
                for proc in sched.processors:
                    name = '%s_%s' % (sched.name, proc.name)
                    scheduler = create_scheduler(name, proc, sched.policy,
                                                 self)
                    self._schedulers.append(scheduler)
                    self._processors_to_schedulers[proc] = scheduler

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

    def start_process(self, process, mapping_info):
        """Start execution of a process.

        This should only be called by a RuntimeApplication.

        Args:
            process (RuntimeProcess): the runtime process to be started
            mapping_info (ProcessMappingInfo): object that specifies where to
                start the process
        """
        if process in self._processes:
            raise RuntimeError(
                f"The process {process.name} was already started!")
        self._processes.add(process)
        processor = mapping_info.affinity
        scheduler = self._processors_to_schedulers[processor]
        scheduler.add_process(process)
        process.start()

    def start_schedulers(self):
        for s in self._schedulers:
            self._env.process(s.run())

        self._env.run()

        self.check_errors()

    def check_errors(self):
        some_blocked = False
        for p in self._processes:
            if p.check_state(ProcessState.BLOCKED):
                log.error('The process %s is blocked', p.name)
                some_blocked = True
            elif not p.check_state(ProcessState.FINISHED):
                log.warning('The process %s did not finish its execution!',
                            p.name)
        if some_blocked:
            raise SimulationError('There is a deadlock!')

    @property
    def env(self):
        """The simpy environment"""
        return self._env

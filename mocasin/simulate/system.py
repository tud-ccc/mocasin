# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from simpy.resources.resource import Resource

from mocasin.util import logging
from mocasin.simulate.process import ProcessState
from mocasin.simulate.scheduler import create_scheduler
from mocasin.simulate.trace_writer import TraceWriter


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
        self.app_trace_enabled = False
        self.platform_trace_enabled = False
        self.load_trace_cfg = None

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

    def record_system_load(self):
        # create an init event in order to give the trace viewer a hint
        # on the maximum value
        for s in self._schedulers:
            self.trace_writer.update_counter("load",
                                             s._processor.name,
                                             [1.0],
                                             category="Load")

        granularity, time_frame = self.load_trace_cfg
        while True:
            for s in self._schedulers:
                load = s.average_load(time_frame),
                self.trace_writer.update_counter("load",
                                                 s._processor.name,
                                                 load,
                                                 category="Load")
            yield self.env.timeout(granularity)

    def start_schedulers(self):
        for s in self._schedulers:
            self._env.process(s.run())
        # trace the system load
        if self.load_trace_cfg is not None:
            self._env.process(self.record_system_load())

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

    def get_scheduler(self, processor):
        """Look up the scheduler for a given processor

        Args:
            processor (Processor): the processor to find the scheduler foreach

        Returns:
            (Scheduler) A scheduler object
        """
        return self._processors_to_schedulers[processor]

    @property
    def env(self):
        """The simpy environment"""
        return self._env

    def write_simulation_trace(self, path):
        """Write a json trace of the simulated system to ``path``

        The generated trace can be opened with Chrome's or Chromiums builtin
        trace viewer at ``about://tracing/``.
        Args:
            path (str): path to the file that should be generated
        """
        self.trace_writer.write_trace(path)

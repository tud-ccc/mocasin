# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import logging

from simpy.resources.resource import Resource

from mocasin.simulate.energy import EnergyEstimator
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
        log.info("Initialize the system")

        self._env = env
        self.platform = platform

        self._processes = set()

        self.trace_writer = TraceWriter(env)
        self.app_trace_enabled = False
        self.platform_trace_enabled = False
        self.load_trace_cfg = None

        self.energy_estimator = EnergyEstimator(platform, env)

        # initialize all schedulers

        # list of all schedulers
        self._schedulers = []
        # a mapping of all processors to their schedulers
        self._processors_to_schedulers = {}
        for sched in platform.schedulers():
            if len(sched.processors) == 1:
                proc = sched.processors[0]
                scheduler = create_scheduler(
                    sched.name, proc, sched.policy, self
                )
                self._schedulers.append(scheduler)
                self._processors_to_schedulers[proc] = scheduler
            else:
                log.warning(
                    "True multi-processor scheduling is not supported "
                    "yet! -> split the %s scheduler into multiple "
                    "single-processor schedulers",
                    sched.name,
                )
                for proc in sched.processors:
                    name = "%s_%s" % (sched.name, proc.name)
                    scheduler = create_scheduler(name, proc, sched.policy, self)
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
            if r.exclusive and not hasattr(r, "simpy_resource"):
                r.simpy_resource = Resource(self.env, capacity=1)

        return

    def start_process(self, process, processor):
        """Start execution of a process.

        This should only be called by a RuntimeApplication.

        Args:
            process (RuntimeProcess): the runtime process to be started
            processor (str): name of the processor to run the process on
            mapping_info (ProcessMappingInfo): object that specifies where to
                start the process
        """
        if process in self._processes:
            raise RuntimeError(
                f"The process {process.name} was already started!"
            )
        self._processes.add(process)
        process.finished.callbacks.append(self._process_finished_cb)

        scheduler = self._processors_to_schedulers[processor]
        scheduler.add_process(process)
        process.start()

    def _process_finished_cb(self, event):
        """Callback for the finished event of runtime processes

        Makes sure that the process is removed from the internal set of all
        processes.
        """
        process = event.value
        assert process.check_state(ProcessState.FINISHED)
        self._processes.remove(process)

    def move_process(self, process, from_processor, to_processor):
        """Move a running process from one processor to another

        Args:
            process (RuntimeProcess): the runtime process to be moved
            from_processor (str): name of the processor the process is currently
                running on
            to_processor (str): name of the processor the process should be
                moved to
        """
        # nothing to do if the process is already finished
        if process.check_state(ProcessState.FINISHED):
            return

        # remove the process from its current scheduler
        event = self.pause_process(process, from_processor)

        # The remove call above may return an event that indicates the
        # completion of the process removal. This is necessary in cases where
        # the process is currently running and first needs to be deactivated.
        if event:
            # if we got an event, add a callback that adds the process to the
            # new scheduler as soon as the event is triggered (i.e. as soon
            # as the process is removed completely)
            event.callbacks.append(
                lambda _: self.resume_process(process, to_processor)
            )
        else:
            # otherwise, resume the process on the new scheduler immediately
            self.resume_process(process, to_processor)

    def pause_process(self, process, current_processor):
        """Pause a running process

        Removes the process from its current processor and pauses its execution
        until it is resumed on the same or another processor.

        Args:
            process (RuntimeProcess): the runtime process to be moved
            current_processor (str): name of the processor the process is
                currently running on
        Returns:
            None: if the process was removed immediately
            simpy.events.Event: An event indicating completion of the removal
                if the process cannot be removed immediately (sine it is
                currently running)
        """
        # nothing to do if the process is already finished
        if process.check_state(ProcessState.FINISHED):
            return

        assert process in self._processes

        # Remove the process from its scheduler. If the process is currently
        # running, then it needs to be preempted. This might take a while, and
        # in this case remove_process() returns an event indicating when
        # preemption completed. We simply return this event here to indicate
        # when the process has paused.
        scheduler = self._processors_to_schedulers[current_processor]
        event = scheduler.remove_process(process)
        return event

    def resume_process(self, process, processor):
        """Resume a paused process on a given processor

        Args:
            process (RuntimeProcess): the runtime process to be moved
            processor (str): name of the processor the process is
                should resume its execution on
        """
        # nothing to do if the process is already finished
        if process.check_state(ProcessState.FINISHED):
            return

        assert process in self._processes

        scheduler = self._processors_to_schedulers[processor]
        scheduler.add_process(process)

    def record_system_load(self):
        # create an init event in order to give the trace viewer a hint
        # on the maximum value
        for s in self._schedulers:
            self.trace_writer.update_counter(
                "load", s._processor.name, [1.0], category="Load"
            )

        granularity, time_frame = self.load_trace_cfg
        while True:
            for s in self._schedulers:
                load = (s.average_load(time_frame),)
                self.trace_writer.update_counter(
                    "load", s._processor.name, load, category="Load"
                )
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
                log.error("The process %s is blocked", p.name)
                some_blocked = True
            elif not p.check_state(ProcessState.FINISHED):
                log.warning(
                    "The process %s did not finish its execution!", p.name
                )
        if some_blocked:
            raise SimulationError("There is a deadlock!")

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

    def check_power_model(self):
        return self.energy_estimator.check_power_model()

    def calculate_energy(self):
        return self.energy_estimator.calculate_energy()

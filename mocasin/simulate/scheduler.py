# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Felix Teweleit


from collections import deque
from enum import Enum

from mocasin.util import logging
from mocasin.simulate.adapter import SimulateLoggerAdapter
from mocasin.simulate.process import ProcessState, RuntimeProcess


log = logging.getLogger(__name__)


_MAX_DEQUE_LEN = 1000


class ContextSwitchMode(Enum):
    """Indicates when a scheduler should perform a context switch

    :cvar int ALWAYS: Always perform a context switch. Process blocks/finishes
        -> store context -> schedule -> load context -> activate process
    :cvar int AFTER_SCHEDULING: Only perform a context switch when the
        scheduler decides to load another process. Process blocks/finishes ->
        schedule -> (store context -> load context) -> activate process)
    :cvar int NEVER: Never perform a context switch. For instance, this is
        useful to model protothreads. Process blocks/finishes -> schedule ->
        activate process
    """

    ALWAYS = 0
    AFTER_SCHEDULING = 1
    NEVER = 2


class RuntimeScheduler(object):
    """The simulated runtime instance of a scheduler.

    This is a base class that implements common scheduler
    functionality. Derived subclasses implement the actual scheduling policies.

    :ivar str name: the scheduler name
    :ivar _processor: the processor managed by this scheduler
    :type _processor: Processor
    :ivar _context_switch_mode: the mode to be used for context switches
    :type _context_switch_mode: ContextSwitchMode
    :ivar int _scheduling_cycles: number of cycles required to reach a
        scheduling decision
    :ivar _system: the runtime system
    :ivar _log: an logger adapter to print messages with simulation context
    :type _log: SimulateLoggerAdapter
    :ivar _processes: list of runtime processes managed by this scheduler
    :type _processes: list[RuntimeProcess]
    :ivar _ready_queue: list of runtime processes that are ready. Process in
        the front of the list became ready earlier than the processes at the
        end.
    :type _ready_queue: list[RuntimeProcess]
    :ivar current_process: the process that is currently executed
    :type current_process: RuntimeProcess
    """

    def __init__(
        self,
        name,
        processor,
        context_switch_mode,
        scheduling_cycles,
        time_slice,
        system,
    ):
        """Initialize a runtime scheduler.

        :param str name: the scheduler name
        :param processor: the processor managed by this scheduler
        :type processor: Processor
        :param context_switch_mode: the mode to be used for context switches
        :type context_switch_mode: ContextSwitchMode
        :param int scheduling_cycles: number of cycles required to reach a
            scheduling decision
        :param system:  the runtime system this scheduler belongs to
        """

        self.name = name
        self._processor = processor
        self._context_switch_mode = context_switch_mode
        self._scheduling_cycles = scheduling_cycles
        self._time_slice = time_slice
        self._system = system

        self._log = SimulateLoggerAdapter(log, self.name, self.env)

        self._processes = deque()
        self._ready_queue = deque()

        self.current_process = None

        self.process_ready = self.env.event()

        # keep track of processor load, maxlen ensures that memory does not
        # grow arbitrarily large
        self._load_trace = deque(maxlen=_MAX_DEQUE_LEN)

        # An event that is only valid during removal of a process and that
        # is triggered when the removal completed
        self._process_removal_complete = None

    @property
    def env(self):
        """The simpy environment"""
        return self._system.env

    @property
    def trace_writer(self):
        """The system's trace writer"""
        return self._system.trace_writer

    def average_load(self, time_frame):
        """Calculate the average load over a given time frame.

        This will analyse the execution trace and process all events between
        now and ``time_frame`` pico seconds in the past to determine the
        average load in this time_frame. Note that ``_load_trace`` only
        keeps a total of 1000 entries. Thus, ``time_frame`` cannot be
        arbitrarily large.

        Args:
            time_frame (int): size of the time frame to consider in pico
                seconds
        """
        if len(self._load_trace) == 0:
            return 0.0

        active_time = 0
        now = self.env.now
        stop = now - time_frame
        reached_stop = False
        for timestamp, event in self._load_trace:
            if timestamp < stop:
                if event == 1:
                    active_time += now - stop
                reached_stop = True
                break
            else:
                if event == 1:
                    active_time += now - timestamp
            now = timestamp
        if not reached_stop and len(self._load_trace) == _MAX_DEQUE_LEN:
            log.warn(
                "Cannot calculate load accurately as the trace data is "
                "not long enough."
            )
        return float(active_time) / float(time_frame)

    def add_process(self, process):
        """Add a process to this scheduler.

        Append the process to the :attr:`_processes` list and register all
        required event callbacks.

        Args:
            process (RuntimeDataflowProcess): the process to be added
        """
        self._log.debug("add process %s", process.full_name)
        if process.check_state(ProcessState.FINISHED) or process.check_state(
            ProcessState.RUNNING
        ):
            raise RuntimeError(
                "Processes that are running or finished cannot be "
                "added to a scheduler"
            )
        assert process not in self._processes
        self._processes.append(process)
        process.ready.callbacks.append(self._cb_process_ready)
        process.finished.callbacks.append(self._cb_process_finished)
        # if the process is ready, also add it to the ready queue
        if process.check_state(ProcessState.READY):
            self._ready_queue.append(process)
            if len(self._ready_queue) == 1:
                # notify the process ready event
                self.process_ready.succeed()
                self.process_ready = self.env.event()

    def remove_process(self, process):
        """Remove a process from this scheduler.

        This will usually be called in the context of a process migration,
        where a process is moved from one scheduler to another.

        Args:
            process (RuntimeDataflowProcess): the process to be removed

        Raises:
            ValueError: if the process is not int the :attr:`_processes` list

        Returns:
            None: if the process was removed immediately
            simpy.events.Event: An event indicating completion of the removal
                if the process cannot be removed immediately (since it is
                currently running)
        """
        # there is nothing to do if the process already finished
        if process.check_state(ProcessState.FINISHED):
            return

        if process not in self._processes:
            raise ValueError("Attempted to remove an unknown process")

        # remove any registered callbacks
        process.ready.callbacks.remove(self._cb_process_ready)
        process.finished.callbacks.remove(self._cb_process_finished)

        # remove process from _processes list and ready queue
        self._processes.remove(process)
        if process in self._ready_queue:
            self._ready_queue.remove(process)

        # if the process is running, we need to preempt it and wait for its
        # context to be stored
        if process.check_state(ProcessState.RUNNING):
            assert process is self.current_process

            # prepare an event that will be notified once the process
            # is preempted and completely removed
            self._process_removal_complete = self.env.event()

            # preempt the process
            process.preempt()

            # return the event so that a caller can wait for it
            return self._process_removal_complete

        # in some seldom cases it could happen that the removed process
        # is still marked as the current process. In this case we reset
        # the current process
        if process is self.current_process:
            self.current_process = None

    def _cb_process_ready(self, event):
        """Callback for the ready event of runtime processes

        Append process to the ready queue and call :func:`schedule`.

        :param event: The event calling the callback. This function expects \
            ``event.value`` to be a valid RuntimeProcess object.
        """
        if not isinstance(event.value, RuntimeProcess):
            raise ValueError(
                "Expected a RuntimeProcess to be passed as value "
                "of the triggering event!"
            )
        process = event.value
        if process not in self._ready_queue:
            self._ready_queue.append(process)
        process.ready.callbacks.append(self._cb_process_ready)

        self._log.debug(f"process {process.name} became ready")

        # notify the process ready event
        self.process_ready.succeed()
        self.process_ready = self.env.event()

    def _cb_process_finished(self, event):
        """Callback for the finished event of runtime processes

        Makes sure that the process is removed from the ready queue.

        :param event: The event calling the callback. This function expects \
            ``event.value`` to be a valid RuntimeProcess object.
        """
        if not isinstance(event.value, RuntimeProcess):
            raise ValueError(
                "Expected a RuntimeProcess to be passed as value "
                "of the triggering event!"
            )
        process = event.value
        assert process.check_state(ProcessState.FINISHED)
        try:
            self._ready_queue.remove(process)
        except ValueError:
            pass

    def schedule(self):
        """Perform the scheduling.

        This should return the next process and the time (in ticks) taken to
        reach the decision.

        :raises: NotImplementedError
        :rtype: (RuntimeDataflowProcess, int)
        """
        raise NotImplementedError(
            "This method needs to be overridden by a subclass"
        )

    def _load_context(self, last_process, next_process):
        """A simpy process modeling the context loading for next_process

        Yields:
            ~simpy.events.Event: a series of events until the context is loaded
        """

        # In case of the AFTER_SCHEDULING context switch mode, the context
        # switch is deferred until absolutely necessary. This means we first
        # have to store the old context before we can load the new context
        # here.
        if self._context_switch_mode == ContextSwitchMode.AFTER_SCHEDULING:
            # there is nothing to do if last and next process are identical
            if last_process is next_process:
                return
            if last_process is not None:
                self._log.debug(
                    f"store the context of process {next_process.full_name}"
                )
                # wait until the store operation is complete
                ticks = self._processor.context_store_ticks()
                yield self.env.timeout(ticks)

        # load context of the new process
        if self._context_switch_mode != ContextSwitchMode.NEVER:
            self._log.debug(f"load context of process {next_process.full_name}")
            # wait until the load operation is complete
            ticks = self._processor.context_load_ticks()
            self._log.debug(f"before timeout {(ticks)}")
            yield self.env.timeout(ticks)
            self._log.debug(f"after timeout")

    def _store_context(self, process, always=False):
        """A simpy process modeling the context storing for process

        Yields:
            ~simpy.events.Event: a series of events until the context is loaded
        """
        if self._context_switch_mode == ContextSwitchMode.NEVER:
            return

        if always or self._context_switch_mode == ContextSwitchMode.ALWAYS:
            self._log.debug(f"store the context of process {process.full_name}")
            yield self.env.timeout(self._processor.context_store_ticks())

    def run(self):
        self._log.debug("scheduler starts")

        while True:
            self._log.debug("run scheduling algorithm")
            yield from self._schedule_next_process()

    def _wait_for_ready_process(self):
        """A simpy process for waiting until a new process becomes ready"""
        self._log.debug("There is no ready process -> sleep")
        # Record the idle event in our internal load trace
        if len(self._load_trace) == 0 or self._load_trace[0][1] == 1:
            self._load_trace.appendleft((self.env.now, 0))
        # wait until a process becomes ready
        yield self.process_ready

    def _schedule_next_process(self):
        next_process = self.schedule()

        # Found no process to be scheduled? Then, wait for a process to become
        # ready and then try again.
        if next_process is None:
            yield from self._wait_for_ready_process()
            # by returning, we trigger the algorithm again
            return

        # record the activation event in our internal load trace
        if len(self._load_trace) == 0 or self._load_trace[0][1] == 0:
            self._load_trace.appendleft((self.env.now, 1))

        # pay for the scheduling delay
        ticks = self._processor.ticks(self._scheduling_cycles)
        yield self.env.timeout(ticks)

        self._log.debug("schedule process %s next", next_process.full_name)

        # pay for context switching
        yield from self._load_context(self.current_process, next_process)

        # it could happen, that the process gets killed or removed
        # before the context was loaded completely. In this case we
        # just return and the algorithm will be run again
        if next_process not in self._processes or next_process.check_state(
            ProcessState.FINISHED
        ):
            self._log.debug(
                f"process {next_process.name} was migrated or killed before its"
                " context could be loaded"
            )
            return

        self._log.debug("activate process %s", next_process.full_name)
        # activate the process and remove it from the ready queue
        self.current_process = next_process
        next_process.activate(self._processor)
        # make sure the activation is processed completely before
        # continuing
        yield self.env.timeout(0)

        self._log.debug("run workload of process %s", next_process.full_name)
        # model the actual workload execution of the process
        yield from self._execute_process_workload(self.current_process)

        self._log.debug("after workload of process %s", next_process.full_name)

        # check if the process is being removed
        if self.current_process not in self._processes:
            self._log.debug("Cleaning up after removing a running process")
            # first store the context
            yield from self._store_context(self.current_process, always=True)
            # reset current process
            self.current_process = None
            # notify the event to indicate that migration completed
            assert self._process_removal_complete is not None
            self._process_removal_complete.succeed()
        else:
            # Otherwise, just pay for context switching
            yield from self._store_context(self.current_process)

    def _execute_process_workload(self, process):
        # record the process activation in the simulation trace
        if self._system.platform_trace_enabled or self._system.power_enabled:
            self.trace_writer.begin_duration(
                self._system.platform.name,
                self._processor.name,
                process.full_name,
                category="Schedule",
            )

        # execute the process workload
        workload = self.env.process(process.workload())
        if self._time_slice is not None:
            timeout = self.env.timeout(self._time_slice)
            yield self.env.any_of([timeout, workload])
            if timeout.processed:
                process.preempt()
                # Although we requested to preempt the process, it may
                # still continue running in order to finish any atomic
                # operations it might be processing at the moment. Thus
                # we wait for the workload process to terminate before
                # continuing
                yield workload
                assert not process.check_state(ProcessState.RUNNING)
        else:
            yield workload

        # record the process halting in the simulation trace
        if self._system.platform_trace_enabled or self._system.power_enabled:
            self.trace_writer.end_duration(
                self._system.platform.name,
                self._processor.name,
                process.full_name,
                category="Schedule",
            )

    def ready_queue_length(self):
        """Get the current length of the ready queue"""
        return len(self._ready_queue)


class FifoScheduler(RuntimeScheduler):
    """A FIFO Scheduler.

    Always schedules the process that became ready first
    """

    def __init__(
        self, name, processor, context_switch_mode, scheduling_cycles, env
    ):
        """Initialize a FIFO scheduler

        Calls :func:`RuntimeScheduler.__init__`.
        """
        super().__init__(
            name, processor, context_switch_mode, scheduling_cycles, None, env
        )

    def schedule(self):
        """Perform the scheduling.

        Returns the next ready process.
        """

        # Schedule next ready process if there are any ready processes
        if len(self._ready_queue) > 0:
            return self._ready_queue.popleft()

        # sleep otherwise
        return None


class RoundRobinScheduler(RuntimeScheduler):
    """A RoundRobin Scheduler

    Schedules ready processes in round robin manner.
    """

    def __init__(
        self,
        name,
        processor,
        context_switch_mode,
        scheduling_cycles,
        time_slice,
        env,
    ):
        """Initialize a RoundRobin scheduler

        Calls :func:`RuntimeScheduler.__init__`.
        """
        if time_slice is None:
            raise RuntimeError(
                "time_slice must be defined for a RoundRobin scheduler"
            )
        super(RoundRobinScheduler, self).__init__(
            name,
            processor,
            context_switch_mode,
            scheduling_cycles,
            time_slice,
            env,
        )

    def schedule(self):
        """Perform the scheduling.

        Returns returns the first ready process found while iterating over
        all processes in round robin manner.
        """

        # Abort if there are no ready processes
        if len(self._ready_queue) == 0:
            return None
        assert len(self._processes) > 0

        # keep track of the process where we start searching
        stop_at = self._processes[-1]

        while True:
            # check if the first process in the deque is ready
            process = self._processes[0]
            if process in self._ready_queue:
                # if it is ready, then remove it from the ready queue and
                # return it
                self._ready_queue.remove(process)
                return process

            # check if we already iterated over the complete process queue
            if stop_at is process:
                raise RuntimeError(
                    "Did not find a ready process although the ready queue is "
                    "not empty"
                )

            # rotate the deque by one to the left and try again
            self._processes.rotate(-1)


def create_scheduler(name, processor, policy, env):
    """Factory method for RuntimeScheduler

    Creates a RuntimeScheduler depending on the policy passed to this function.

    Args:
        name (str): name of the new scheduler
        processor (Processor): the processor that the scheduler manages
        policy (SchedulingPolicy): the policy implemented by the new scheduler

    Returns:
        RuntimeScheduler: a runtime scheduler object
    """
    if policy.name == "FIFO":
        log.debug(f"Initialize new FIFO scheduler ({name})")
        s = FifoScheduler(
            name,
            processor,
            ContextSwitchMode.AFTER_SCHEDULING,
            policy.scheduling_cycles,
            env,
        )
    elif policy.name == "RoundRobin":
        log.debug(f"Initialize new RoundRobin scheduler ({name})")
        s = RoundRobinScheduler(
            name,
            processor,
            ContextSwitchMode.AFTER_SCHEDULING,
            policy.scheduling_cycles,
            policy.time_slice,
            env,
        )
    else:
        raise NotImplementedError(
            "The simulation module does not implement the %s scheduling "
            "policy" % (policy.name)
        )

    return s

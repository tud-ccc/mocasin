# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from enum import Enum

from pykpn.util import logging
from pykpn.simulate.adapter import SimulateLoggerAdapter
from pykpn.simulate.process import ProcessState, RuntimeProcess


log = logging.getLogger(__name__)


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
    :ivar _env: the simpy environment
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

    def __init__(self, name, processor, context_switch_mode, scheduling_cycles,
                 env):
        """Initialize a runtime scheduler.

        :param str name: the scheduler name
        :param processor: the processor managed by this scheduler
        :type processor: Processor
        :param context_switch_mode: the mode to be used for context switches
        :type context_switch_mode: ContextSwitchMode
        :param int scheduling_cycles: number of cycles required to reach a
            scheduling decision
        :param env: the simpy environment
        """
        log.debug('Initialize new scheduler (%s)', name)

        self.name = name
        self._processor = processor
        self._context_switch_mode = context_switch_mode
        self._scheduling_cycles = scheduling_cycles
        self._env = env

        self._log = SimulateLoggerAdapter(log, self.name, env)

        self._processes = []
        self._ready_queue = []

        self.current_process = None

    def add_process(self, process):
        """Add a process to this scheduler.

        Append the process to the :attr:`_processes` list and register all
        required event callbacks. This may not be called after the simulation
        started.
        :param process: the process to be added
        :type process: RuntimeProcess
        """
        assert self._env.now == 0
        self._log.debug('add process %s', process.name)
        if not process.check_state(ProcessState.CREATED):
            raise RuntimeError('Processes that are already started cannot be '
                               'added to a scheduler')
        self._processes.append(process)
        process.ready.callbacks.append(self._cb_process_ready)

    def _cb_process_ready(self, event):
        """Callback for the ready event of runtime processes

        Append process to the ready queue and call :func:`schedule`.

        :param event: The event calling the callback. This function expects \
            ``event.value`` to be a valid RuntimeProcess object.
        """
        if not isinstance(event.value, RuntimeProcess):
            raise ValueError('Expected a RuntimeProcess to be passed as value '
                             'of the triggering event!')
        process = event.value
        self._ready_queue.append(event.value)
        process.ready.callbacks.append(self._cb_process_ready)

    def schedule(self):
        """Perform the scheduling.

        This should return the next process and the time (in ticks) taken to
        reach the decision.

        :raises: NotImplementedError
        :rtype: (RuntimeKpnProcess, int)
        """
        raise NotImplementedError(
            'This method needs to be overridden by a subclass')

    def run(self):
        log = self._log

        log.debug('scheduler starts')

        if len(self._processes) == 0:
            log.debug('Scheduler has no assigned processes -> terminate')
            return

        while True:
            log.debug('run scheduling algorithm')

            cp = self.current_process
            np = self.schedule()

            # Found a process to be scheduled?
            if np is not None:
                # pay for the scheduling delay
                ticks = self._processor.ticks(self._scheduling_cycles)
                yield self._env.timeout(ticks)

                log.debug('schedule process %s next', np.name)

                # pay for context switching
                mode = self._context_switch_mode
                if mode == ContextSwitchMode.ALWAYS:
                    log.debug('load context of process %s', np.name)
                    ticks = self._processor.context_load_ticks()
                    yield self._env.timeout(ticks)
                elif (mode == ContextSwitchMode.AFTER_SCHEDULING and
                      np is not self.current_process):
                    if cp is not None:
                        log.debug('store the context of process %s', cp.name)
                        ticks = self._processor.context_store_ticks()
                        yield self._env.timeout(ticks)
                    log.debug('load context of process %s', np.name)
                    ticks = self._processor.context_load_ticks()
                    yield self._env.timeout(ticks)

                # activate the process
                self.current_process = np
                self._ready_queue.remove(np)
                np.activate(self._processor)
                # wait until the process stops its execution
                yield self._env.any_of([np.blocked, np.finished])

                # pay for context switching
                if self._context_switch_mode == ContextSwitchMode.ALWAYS:
                    self._log.debug('store the context of process %s', np.name)
                    yield self._env.timeout(
                        self._processor.context_store_ticks())
            else:
                # Wait for ready events if the scheduling algorithm did not
                # find a process that is ready for execution
                self._log.debug('There is no ready process -> sleep')
                ready_events = [p.ready for p in self._processes]
                yield self._env.any_of(ready_events)


class DummyScheduler(RuntimeScheduler):
    """A Dummy Scheduler.

    This scheduler does not implement any policy and is intended to be used
    when there is no scheduler in the platform. This scheduler simply runs all
    processes sequentially. It always waits until the current process finishes
    before starting a new one.
    """

    def __init__(self, name, processor, context_switch_mode, scheduling_cycles,
                 env):
        """Initialize a dummy scheduler

        Calls :func:`RuntimeScheduler.__init__`.
        """
        super().__init__(name, processor, context_switch_mode,
                         scheduling_cycles, env)

    def schedule(self):
        """Perform the scheduling.

        Returns the next process from the ready queue if the current process is
        finished or no process is currently being executed. Returns the
        current_process if it is ready. Returns None in all other cases.
        """
        cp = self.current_process

        if cp is None:
            # Schedule next ready process if no process was loaded before
            if len(self._ready_queue) > 0:
                return self._ready_queue[0]
        elif cp.check_state(ProcessState.FINISHED):
            # Schedule next ready process if current process finished
            if len(self._ready_queue) > 0:
                return self._ready_queue[0]
        elif cp.check_state(ProcessState.READY):
            # Schedule the current process if it became ready again
            return cp

        # sleep otherwise
        return None


class FifoScheduler(RuntimeScheduler):
    """A FIFO Scheduler.

    Always schedules the process that became ready first
    """

    def __init__(self, name, processor, context_switch_mode, scheduling_cycles,
                 env):
        """Initialize a FIFO scheduler

        Calls :func:`RuntimeScheduler.__init__`.
        """
        super().__init__(name, processor, context_switch_mode,
                         scheduling_cycles, env)

    def schedule(self):
        """Perform the scheduling.

        Returns the next ready process or the current process if it is ready.
        """
        cp = self.current_process

        if cp is None:
            # Schedule next ready process if no process was loaded before
            if len(self._ready_queue) > 0:
                return self._ready_queue[0]
        elif (cp.check_state(ProcessState.FINISHED) or
              cp.check_state(ProcessState.BLOCKED)):
            # Schedule next ready process if current process finished or is
            # blocked
            if len(self._ready_queue) > 0:
                return self._ready_queue[0]
        elif cp.check_state(ProcessState.READY):
            # Schedule the current process if it became ready again
            return cp

        # sleep otherwise
        return None


def create_scheduler(name, processor, policy, param, env):
    if policy.name == 'Dummy':
        s = DummyScheduler(name, processor, ContextSwitchMode.NEVER,
                           policy.scheduling_cycles, env)
    if policy.name == 'FIFO':
        s = FifoScheduler(name, processor, ContextSwitchMode.AFTER_SCHEDULING,
                          policy.scheduling_cycles, env)
    elif policy.name == 'RoundRobin':
        # TODO Actually implement RoundRobin
        log.warning('RoundRobin scheduler is not yet implemented -> Fall back '
                    'to FIFO')
        s = FifoScheduler(name, processor, ContextSwitchMode.AFTER_SCHEDULING,
                          policy.scheduling_cycles, env)
    else:
        raise NotImplementedError(
            'The simulation module does not implement the %s scheduling '
            'policy' % (policy.name))

    return s

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from .adapter import SimulateLoggerAdapter
from .process import RuntimeProcess
from .process import ProcessState
from ..common import logging


log = logging.getLogger(__name__)


class RuntimeScheduler(object):
    """The simulated runtime instance of a scheduler.

    This is a base class that implements common scheduler
    functionality. Derived subclasses implement the actual scheduling policies.

    :ivar str name: the scheduler name
    :ivar _env: the simpy environment
    :ivar _log: an logger adapter to print messages with simulation context
    :type _log: SimulateLoggerAdapter
    :ivar _processes: list of runtime processes managed by this scheduler
    :type _processes: list[RuntimeProcess]
    :ivar _ready_queue: list of runtime processes that are ready. Process in
        the front of the list became ready earlier than the processes at the
        end.
    :type _ready_queue: list[RuntimeProcess]
    """

    def __init__(self, name, env):
        """Initialize a runtime scheduler.

        :param platform_scheduler: scheduler object as defined by the platform
        :type platform_scheduler: Scheduler
        :param env: the simpy environment
        """
        self.name = name

        self._env = env
        self._log = SimulateLoggerAdapter(log, name, env)

        self._processes = []
        self._ready_queue = []

    def add_process(self, process):
        """Add a process to this scheduler.

        Append the process to the :attr:`_processes` list and register all
        required event callbacks
        :param process: the process to be added
        :type process: RuntimeProcess
        """
        self._log.debug('add process %s', process.name)
        if not process.check_state(ProcessState.NOT_STARTED):
            raise RuntimeError('Processes that are already started cannot be '
                               'added to a scheduler')
        self._processes.append(process)
        process.ready.callbacks.append(self._cb_process_ready)
        process.finished.callbacks.append(self._cb_process_finished)

    def _cb_process_ready(self, event):
        """Callback for the ready event of runtime processes

        Append process to the ready queue and call :func:`schedule`.
        :param event: The event calling the callback. This function expects
            ``event.value`` to be a valid RuntimeProcess object.
        """
        if not isinstance(event.value, RuntimeProcess):
            raise ValueError('Expected a RuntimeProcess to be passed as value '
                             'of the triggering event!')
        process = event.value
        self._ready_queue.append(event.value)
        process.ready.callbacks.append(self._cb_process_ready)
        self.schedule()

    def _cb_process_finished(self, event):
        """Callback for the finished event of runtime processes

        Call :func:`schedule`.
        :param event: The event calling the callback. This function expects
            ``event.value`` to be a valid RuntimeProcess object.
        """
        if not isinstance(event.value, RuntimeProcess):
            raise ValueError('Expected a RuntimeProcess to be passed as value '
                             'of the triggering event!')
        self.schedule()

    def schedule(self):
        """Perform the scheduling.

        Do nothing. This should be overridden by subclasses.
        """
        pass


class DummyScheduler(RuntimeScheduler):
    """A Dummy Scheduler.

    This scheduler does not implement any policy and is intended to be used
    when there is no scheduler in the platform. This scheduler simply runs all
    processes sequentially. It always waits until the current process finishes
    before starting a new one.

    :ivar _processor: the processor managed by this scheduler
    :type _processor: Processor
    :ivar _current_process: the process that is currently executed
    :type _current_process: RuntimeProcess
    """

    def __init__(self, platform_scheduler, env):
        """Initialize a runtime scheduler.

        :param platform_scheduler: scheduler object as defined by the platform
        :type platform_scheduler: Scheduler
        :param env: the simpy environment
        """
        super().__init__(platform_scheduler.name, env)
        log.debug('Initialize new FIFO scheduler (%s)' % self.name)

        # TODO implement multi-processor scheduling
        if len(platform_scheduler.processors) > 1:
            raise RuntimeError(
                'Multi-processor scheduling is not yet supported!')
        self._processor = platform_scheduler.processors[0]

        self._current_process = None

    def schedule(self):
        """Perform the scheduling.

        Activate the next process from the ready queue if the current process
        is finished or no process is currently being executed.
        """
        self._log.debug('scheduler runs')
        if len(self._ready_queue) > 0:
            if (self._current_process is None or
                    self._current_process.check_state(ProcessState.FINISHED)):
                self._current_process = self._ready_queue.pop(0)
                self._log.debug('activate process %s',
                                self._current_process.name)
                self._current_process.activate()


def create_scheduler(platform_scheduler, policy, param, env):
    if policy.name == 'Dummy':
        s = DummyScheduler(platform_scheduler, env)
    if policy.name == 'FIFO':
        # TODO Actually implement FIFO
        s = DummyScheduler(platform_scheduler, env)
    elif policy.name == 'RoundRobin':
        # TODO Actually implement RoundRobin
        s = DummyScheduler(platform_scheduler, env)
    else:
        raise NotImplementedError(
            'The simulation module does not implement the %s scheduling '
            'policy' % (policy.name))

    return s

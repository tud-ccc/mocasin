# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
import simpy
import sys

from .process import ProcessState

log = logging.getLogger(__name__)


class RuntimeScheduler(object):
    """
    Represents the simulated runtime instance of a scheduler.
    """

    def __init__(self, system, processes, policy_name, platform_scheduler):
        '''
        Initialize a RuntimeScheduler.
        :param system: the simulation system object
        :param processes: a list of processes to be scheduled by this Scheduler
        :param policy_name: name of the scheduling policy used by this
                            Scheduler
        :param platform_scheduler: The platform Scheduler object that should be
                                   instanciated
        '''

        # TODO implement multi-processor scheduling
        assert len(platform_scheduler.processors) == 1, (
            'only single processor scheduling supported')

        self.env = system.env
        self.name = platform_scheduler.name
        self.processor = platform_scheduler.processors[0]
        self.processes = processes

        self.policy = None
        for p in platform_scheduler.policies:
            if p.name == policy_name:
                self.policy = p
        if self.policy is None:
            raise RuntimeError('The scheduling policy %s is not supported by '
                               'the scheduler %s!', policy_name, self.name)

        self.prev_process = None
        self.first_iteration = False

        self.vcd_writer = system.vcd_writer
        self.process_var = self.vcd_writer.register_var(
            'system.' + 'schedulers.' + self.name, 'process', 'integer',
            size=128, init=None)
        self.wake_up = self.env.event()

    def assignProcess(self, process):
        self.processes.append(process)
        process.assignProcessor(self.processor)
        log.info('{0:16}'.format(self.env.now) + ": " +
                 process.name + " added to " + self.name)
        self.wake_up.succeed()
        self.wake_up = self.env.event()

    def run(self):
        log.info('{0:16}'.format(self.env.now) + ': scheduler ' +
                 self.name + ' starts execution')
        while(True):
            log.info('{0:16}'.format(self.env.now) + ': scheduler ' +
                     self.name + ' woke up')

            while True:
                p, allProcessesFinished = self.scheduling()
                if p is not None:
                    delay = self.scheduling_cycles(p)
                    yield self.env.timeout(self.processor.ticks(delay))

                    self.vcd_writer.change(self.process_var, self.env.now,
                                           int(p.vcd_id[0:128], 2))
                    yield self.env.process(p.run())
                else:
                    self.vcd_writer.change(self.process_var, self.env.now,
                                           None)

                    if allProcessesFinished:
                        break

                    # collect unblock events
                    events = []
                    for pro in self.processes:
                        events.append(pro.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)
            log.info('{0:16}'.format(self.env.now) +
                     ': scheduler ' + self.name + " going to sleep")
            yield self.wake_up

    def scheduling(self):
        if self.policy.name == 'None':
            return self.none_sched()
        elif self.policy.name == 'FIFO':
            return self.fifo_sched()
        elif self.policy.name == 'RoundRobin':
            return self.roundrobin_sched()
        else:
            raise RuntimeError('The scheduling policy ' + self.policy +
                               ' is not supported')

    def scheduling_cycles(self, p):
        if self.policy.name == 'None':
            return 0
        elif self.policy.name == 'FIFO':
            return self.scheduling_cycles_fifo(p)
        elif self.policy.name == 'RoundRobin':
            return self.scheduling_cycles_roundrobin()
        else:
            raise RuntimeError('The scheduling policy ' + self.policy +
                               ' is not supported')

    def none_sched(self):
        if self.prev_process is None and self.processes:
            # if prev_process is empty allot a process from the list
            self.prev_process = self.processes[0]
        elif self.prev_process is None:
            # if prev_process is empty and there are no available processes
            # return None processes and allProcessesFinished is True
            return None, True
        assert not self.prev_process.state == ProcessState.Running
        if self.prev_process.state == ProcessState.Blocked:
            # if the process is blocked allProcessFinished is false
            return None, False
        elif self.prev_process.state == ProcessState.Finished:
            if self.processes.index(self.prev_process) + 1 == \
               len(self.processes):
                # the process is finished and there are no more processes
                return None, True
            else:
                # the processs is finished so allot next process to the
                # previous process
                self.prev_process = self.processes[
                    self.processes.index(self.prev_process) + 1]
                return self.prev_process, False
        elif self.prev_process.state == ProcessState.Ready:
            return self.prev_process, False

    def roundrobin_sched(self):
        allProcessesFinished = True
        for process in self.processes:
            assert not process.state == ProcessState.Running
            if process.state == ProcessState.Blocked:
                # if the current process is blocked
                allProcessesFinished = False
            elif process.state == ProcessState.Finished:
                # if thr current process is finished move on to the next one
                continue
            elif process.state == ProcessState.Ready:
                allProcessesFinished = False
                return process, allProcessesFinished
            else:
                assert False, 'unknown process state'
        return None, allProcessesFinished

    def fifo_sched(self):
        allProcessesFinished = True
        min = sys.maxsize
        p = None
        for process in self.processes:
            if process.state == ProcessState.Blocked:
                allProcessesFinished = False
            elif process.state == ProcessState.Finished:
                continue
            elif process.state == ProcessState.Ready:
                allProcessesFinished = False

                if int(process.time) < min:
                    # the process that has been waiting the longest
                    # should be run first
                    min = int(process.time)
                    p = process
                    return p, allProcessesFinished
            else:
                assert False, 'unknown process state'
        return None, allProcessesFinished

    def scheduling_cycles_fifo(self, p):
        cycles = self.policy.scheduling_cycles
        if self.prev_process is None:
            # we need to load the first process
            cycles += self.processor.context_load_cycles
        elif p != self.prev_process:
            cycles += (self.processor.context_load_cycles +
                       self.processor.context_store_cycles)
        self.prev_process = p  # XXX Why is this set here?
        return cycles

    def scheduling_cycles_roundrobin(self):
        cycles = self.policy. scheduling_cycles
        if self.first_iteration:
            # Nothing to switch out on first iteration
            cycles += self.processor.context_load_cycles
            self.first_iteration = False
        else:
            cycles += (self.processor.context_load_cycles +
                       self.processor.context_store_cycles)
        return cycles

    def setTraceDir(self, dir):
        for process in self.processes:
            process.setTraceDir(dir)

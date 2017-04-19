# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
import simpy
import sys

from .process import ProcessState

log = logging.getLogger(__name__)


class Scheduler(object):
    """
    Represents a scheduler in the target Platform
    """

    def __init__(self, system, processes, policy, info):

        assert len(info.processors) == 1, \
            'only single processor scheduling supported'

        self.env = system.env
        self.name = info.name
        self.processor = info.processors[0]
        self.processes = processes
        self.policy = policy

        self.schedulingDelay = info.policies[policy]

        self.vcd_writer = system.vcd_writer
        self.process_var = self.vcd_writer.register_var(
                'system.' + 'schedulers.' + self.name, 'process', 'integer',
                size=128, init=None)

    def run(self):
        log.info('{0:16}'.format(self.env.now) + ': scheduler ' +
                 self.name + ' starts execution')

        for p in self.processes:
            p.assignProcessor(self.processor)

        if self.policy == "None":
            # if scheduling is disabled, we run the processes after each other
            for process in self.processes:
                while True:
                    assert not process.state == ProcessState.Running
                    self.vcd_writer.change(self.process_var, self.env.now,
                                           int(process.vcd_id[0:128], 2))
                    yield self.env.process(process.run())

                    if process.state == ProcessState.Finished:
                        break
                    elif process.state == ProcessState.Blocked:
                        self.vcd_writer.change(self.process_var, self.env.now,
                                               None)
                        yield process.event_unblock
            self.vcd_writer.change(self.process_var, self.env.now, None)

        elif self.policy == "RoundRobin":
            while True:
                first_iteration=True
                allProcessesFinished = True
                allProcessesBlocked = True
                for process in self.processes:
                    assert not process.state == ProcessState.Running
                    if process.state == ProcessState.Blocked:
                        allProcessesFinished = False
                    elif process.state == ProcessState.Finished:
                        continue
                    elif process.state == ProcessState.Ready:
                        prev_process=process
                        allProcessesBlocked = False
                        allProcessesFinished = False
                        self.vcd_writer.change(self.process_var, self.env.now,
                                               int(process.vcd_id[0:128],2))
                        yield self.env.process(process.run())

                        # pay for the scheduling delay
                        delay = 0
                        if first_iteration:
                            # Nothing to switch out on first iteration
                            delay = self.schedulingDelay + \
                                    self.processor.contextSwitchInDelay
                            first_iteration = False
                        else:
                            delay = self.schedulingDelay + \
                                    self.processor.contextSwitchInDelay + \
                                    self.processor.contextSwitchOutDelay
                        yield self.env.timeout(
                                self.processor.cyclesToTicks(delay))
                    else:
                        assert False, 'unknown process state'

                if allProcessesFinished:
                    self.vcd_writer.change(self.process_var, self.env.now,
                                           None)
                    break

                if allProcessesBlocked:
                    self.vcd_writer.change(self.process_var, self.env.now,
                                           None)
                    # collect unblock events
                    events = []
                    for p in self.processes:
                        events.append(p.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)

        elif self.policy == 'FIFO':
            prev_process = None
            while True:
                allProcessesFinished = True
                allProcessesBlocked = True
                min=sys.maxsize
                p=None
                for process in self.processes:
                    if process.state == ProcessState.Blocked:
                        allProcessesFinished = False
                    elif process.state == ProcessState.Finished:
                        continue
                    elif process.state == ProcessState.Ready:
                        allProcessesBlocked = False
                        allProcessesFinished = False

                        if int(process.time) < min:
                            min=int(process.time)
                            p=process
                    else:
                        assert False, 'unknown process state'

                if p is not None:
                    delay = self.schedulingDelay
                    if prev_process is None:
                        # we need to load the first process
                        delay = delay + self.processor.contextSwitchInDelay
                    elif p != prev_process:
                        delay = delay + self.processor.contextSwitchInDelay + \
                                self.processor.contextSwitchOutDelay
                    yield self.env.timeout(self.processor.cyclesToTicks(delay))

                    self.vcd_writer.change(self.process_var, self.env.now,
                                           int(p.vcd_id[0:128], 2))
                    yield self.env.process(p.run())
                    prev_process = p

                if allProcessesFinished:
                    self.vcd_writer.change(self.process_var, self.env.now,
                                           None)
                    break

                if allProcessesBlocked:
                    # collect unblock events
                    self.vcd_writer.change(self.process_var, self.env.now,
                                           None)
                    events = []
                    for pro in self.processes:
                        events.append(pro.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)
        else:
            raise RuntimeError('The scheduling policy ' + self.policy +
                               ' is not supported')

        log.info('{0:16}'.format(self.env.now) + ': scheduler ' + self.name +
                 ' finished execution')

    def setTraceDir(self, dir):
        for process in self.processes:
            process.setTraceDir(dir)

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
import simpy
import sys

from enum import Enum

from .process import ProcessState
from ..common import SchedulingPolicy

log = logging.getLogger(__name__)


class Scheduler(object):
    """
    Represents a scheduler in the target Platform
    """

    def __init__(self, env, name, processors, processes, policy, vcd_writer):
        """
        Constructor

        :param env The SimPy environment
        :param name Scheduler name
        :param processors List of processors manged by the scheduler
        :param processes Initial list of processes managed by the scheduler
        :param policy The scheduling policy
        """

        assert len(processors) > 0, \
            'each scheduler needs at least one processor'

        self.env = env
        self.name = name
        self.processors = processors
        self.processes = processes
        self.policy = policy
        self.vcd_writer=vcd_writer
        self.scheduler=self.vcd_writer.register_var('system.'+'scheduler.'+name, 'process', 'integer', size=128, init=None)

    def run(self):
        assert len(self.processors) == 1, \
            'only single processor scheduling supported'

        log.info('{0:16}'.format(self.env.now) + ': scheduler ' +
                self.name + ' starts execution')

        for process in self.processes:
            process.assignProcessor(self.processors[0])


        if self.policy==SchedulingPolicy.RoundRobin:
            while True:
                first_process=True
                allProcessesFinished = True
                allProcessesBlocked = True
                for process in self.processes:
                    delay=0
                    assert not process.state == ProcessState.Running
                    if process.state == ProcessState.Blocked:
                        allProcessesFinished = False
                    elif process.state == ProcessState.Finished:
                        continue
                    elif process.state == ProcessState.Ready:
                        prev_process=process
                        allProcessesBlocked = False
                        allProcessesFinished = False
                        self.vcd_writer.change(self.scheduler, self.env.now, int(process.vcd_id[0:128],2))
                        yield self.env.process(process.run())
                        if first_process:
                            delay=self.processors[0].scheduling_penalty+self.processors[0].switching_in
                            first_process=False
                        else:
                            delay=self.processors[0].scheduling_penalty+self.processors[0].switching_in+self.processors[0].switching_out
                        yield self.env.timeout(delay)

                    else:
                        assert False, 'unknown process state'


                if allProcessesFinished:
                    self.vcd_writer.change(self.scheduler, self.env.now, None)
                    break


                if allProcessesBlocked:
                    self.vcd_writer.change(self.scheduler, self.env.now, None)
                    # collect unblock events
                    events = []
                    for p in self.processes:
                        events.append(p.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)

        elif self.policy == SchedulingPolicy.FIFO:
            prev_process = None
            while True:
                allProcessesFinished = True
                allProcessesBlocked = True
                min=sys.maxsize
                p=None
                delay=0
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
                    if prev_process==None:
                        delay=self.processors[0].scheduling_penalty+self.processors[0].switching_in
                    elif p!=prev_process:
                        delay=self.processors[0].scheduling_penalty+self.processors[0].switching_in+self.processors[0].switching_out
                    else:
                        delay= self.processors[0].scheduling_penalty
                    yield self.env.timeout(delay)

                    self.vcd_writer.change(self.scheduler, self.env.now, int(p.vcd_id[0:128],2))
                    yield self.env.process(p.run())
                    prev_process = p

                if allProcessesFinished:
                    self.vcd_writer.change(self.scheduler, self.env.now, None)
                    break

                if allProcessesBlocked:
                    # collect unblock events
                    self.vcd_writer.change(self.scheduler, self.env.now, None)
                    events = []
                    for pro in self.processes:
                        events.append(pro.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)



        log.info('{0:16}'.format(self.env.now) + ': scheduler ' + self.name +
                 ' finished execution')

    def setTraceDir(self, dir):
        for process in self.processes:
            process.setTraceDir(dir)

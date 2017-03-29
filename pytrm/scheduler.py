# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import logging
import simpy

from enum import Enum

from .process import ProcessState
from common import SchedulingPolicy

log = logging.getLogger(__name__)


class Scheduler(object):
    """
    Represents a scheduler in the target Platform
    """

    def __init__(self, env, name, processors, processes, policy):
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
        #assert policy == SchedulingPolicy.FIFO, \
        #   'Only FIFO scheduling supported'

        self.env = env
        self.name = name
        self.processors = processors
        self.processes = processes
        self.policy = policy

    def run(self):
        assert len(self.processors) == 1, \
            'only single processor scheduling supported'

   #     assert self.policy == SchedulingPolicy.FIFO, \
#        'only FIFO scheduling is supported'

        log.info('{0:16}'.format(self.env.now) + ': scheduler ' +
                 self.name + ' starts execution')

        for process in self.processes:
            process.assignProcessor(self.processors[0])


        if self.policy==SchedulingPolicy.RoundRobin:
            while True:
                allProcessesFinished = True
                allProcessesBlocked = True
                for process in self.processes:
                    assert not process.state == ProcessState.Running
                    if process.state == ProcessState.Blocked:
                        allProcessesFinished = False
                    elif process.state == ProcessState.Finished:
                        continue
                    elif process.state == ProcessState.Ready:
                        allProcessesBlocked = False
                        allProcessesFinished = False
                        yield self.env.process(process.run())
                    else:
                        assert False, 'unknown process state'

                if allProcessesFinished:
                    break

                if allProcessesBlocked:
                    # collect unblock events
                    events = []
                    for p in self.processes:
                        events.append(p.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)

        elif self.policy == SchedulingPolicy.FIFO:
            while True:
                allProcessesFinished = True
                allProcessesBlocked = True
                min=999999999999
                p=None
                for process in self.processes:
                    if process.state == ProcessState.Blocked:
                        allProcessesFinished = False
                    elif process.state == ProcessState.Finished:
                        continue
                    elif process.state == ProcessState.Ready:
                        allProcessesBlocked = False
                        allProcessesFinished = False
                        process.name

                        if int(process.time) < min:
                            min=int(process.time)
                            p=process
                    else:
                        assert False, 'unknown process state'


                if p is not None:
                    print(p.name)
                    yield self.env.process(p.run())

                if allProcessesFinished:
                    break

                if allProcessesBlocked:
                    # collect unblock events
                    events = []
                    for pro in self.processes:
                        events.append(pro.event_unblock)
                    yield simpy.events.AnyOf(self.env, events)



        log.info('{0:16}'.format(self.env.now) + ': scheduler ' + self.name +
                 ' finished execution')

    def setTraceDir(self, dir):
        for process in self.processes:
            process.setTraceDir(dir)

#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import simpy
import logging
import os

from ...common import FrequencyDomain
from ...common import Mapping
from ...common import ChannelMappingInfo
from ...common import ProcessMappingInfo
from ...common import KpnGraph
from ...common import KpnChannel
from ...common import KpnProcess
from ...common import TraceReader
from ...common import ProcessEntry
from ...common import ReadEntry
from ...common import WriteEntry
from ...common import TerminateEntry
from ...common import Primitive
from ...common import Processor
from ...simulate import Channel
from ..process import ProcessState
from unittest import TestCase

from pykpn.platforms import GenericNocPlatform
from pykpn.platforms import Tomahawk2Platform
from pykpn.simulate import System
from pykpn.simulate import Process
from pykpn.simulate import Scheduler
from pykpn.simulate import Application
from vcd import VCDWriter

log = logging.getLogger(__name__)



class TestChannel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestChannel, self).__init__(*args, **kwargs)
        self.system, self.mappingInfo = common_sys()
        self.c=Channel('app.c1', self.system, self.mappingInfo)

    def test_initialized(self):
        #Channel capacity is 4, so a channel can produce maximum of 4 packets
        self.assertTrue(self.c.canProduceTokens(4))
        self.assertTrue(self.c.canConsumeTokens(0))

    def test_consume_limit(self):
        self.c.produceTokens(4)
        self.assertFalse(self.c.canConsumeTokens(5))
        self.assertTrue(self.c.canConsumeTokens(4))

    def test_produce_limit(self):
        self.assertFalse(self.c.canProduceTokens(5))
        self.assertTrue(self.c.canProduceTokens(4))

    def test_ConsumeAndProduceTokens(self):
        self.c.produceTokens(4)
        self.c.consumeTokens(4)

    def test_overflowTokens(self):
        #since the channel can only produce maximum of 4 tokens
        #excepttion is thrown
        try:
            assert self.c.produceTokens(100)
        except:
            True

    def test_consume(self):
        self.c.produceTokens(4)
        try:
            assert self.c.consumeTokens(100)
        except:
            True


class TestProcess(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestProcess, self).__init__(*args, **kwargs)
        self.system, self.mappingInfo = common_sys()
        self.system.channels={'app.c1': Channel('app.c1', self.system, self.mappingInfo)}
        self.name='w1'
        self.traceReader=DummyTraceReader(self.name)
        self.p=Process(self.name, self.system, None, self.traceReader)
        fd = FrequencyDomain('fd_test', 200000000)
        self.processor=Processor('PE1', 'RISC', fd)

    def test_RunProcess(self):
        self.p.assignProcessor(self.processor)
        self.system.env.process(self.p.run())
        self.p.env.run()
        assert self.p.env.now==10180000


class TestScheduler(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScheduler, self).__init__(*args, **kwargs)
        self.system, self.mappingInfo = common_sys()
        self.policy='FIFO'
        self.info=Empty()
        self.info.name='SchedulerForProcessor(PE1)'
        fd = FrequencyDomain('fd_test', 200000000)
        self.info.processors=[Processor('PE1', 'RISC', fd)]
        self.info.policies={'FIFO':100}
        self.system.channels={'app.c1': Channel('app.c1', self.system, self.mappingInfo)\
                , 'app.c2': Channel('app.c2', self.system, self.mappingInfo)}
        self.traceReader1=DummyTraceReader('w1')
        self.traceReader2=DummyTraceReader('w2')
        self.p=Process('w1', self.system, None, self.traceReader1)
        self.P=Process('w2', self.system, None, self.traceReader2)
        self.s=Scheduler(self.system, [], self.policy, self.info)

    def test_SchedulingDelay(self):
        assert self.s.scheduling_delay(self.P)==100

    def test_RoundRobin(self):
        assert self.s.roundrobin_sched()==(None,True)
        assert self.s.delay_roundrobin()==100
        self.s.assignProcess(self.P)
        self.s.assignProcess(self.p)
        assert self.s.roundrobin_sched()==(self.P,False)
        self.P.state=ProcessState.Blocked
        assert self.s.roundrobin_sched()==(self.p,False)
        self.P.state=ProcessState.Finished
        assert self.s.roundrobin_sched()==(self.p,False)
        self.p.state=ProcessState.Finished
        assert self.s.roundrobin_sched()==(None,True)
        self.P.state=ProcessState.Ready
        assert self.s.fifo_sched()==(self.P,False)

    def test_FIFO(self):
        assert self.s.fifo_sched()==(None,True)
        assert self.s.delay_fifo(self.P)==100
        assert self.s.delay_fifo(self.p)==100
        self.s.assignProcess(self.p)
        self.s.assignProcess(self.P)
        assert self.s.fifo_sched()==(self.p,False)
        self.P.state=ProcessState.Blocked
        assert self.s.fifo_sched()==(self.p,False)
        self.P.state=ProcessState.Finished
        assert self.s.fifo_sched()==(self.p,False)
        self.p.state=ProcessState.Finished
        assert self.s.fifo_sched()==(None,True)
        self.P.state=ProcessState.Ready
        assert self.s.fifo_sched()==(self.P,False)

    def test_NoneScheduler(self):
        #there are no processes assigned so no process is returned
        #and allProcessesFinished is True
        assert self.s.none_sched()==(None,True)
        assert self.s.delay_none()==0
        self.s.assignProcess(self.p)
        self.s.assignProcess(self.P)
        # the process that was assigned first is returned and since there is
        #still one process that needs to be scheduled allProcessesFinished is
        #False
        assert self.s.none_sched()==(self.p,False)
        #the second process is blocked, thus sheduler returns the process p 
        #and all process finished is False
        self.P.state=ProcessState.Blocked
        assert self.s.none_sched()==(self.p,False)
        #process P is finshed but p still can be scheduled
        self.P.state=ProcessState.Finished
        assert self.s.none_sched()==(self.p,False)
        #process p is finished so P is scheduled
        self.p.state=ProcessState.Finished
        assert self.s.none_sched()==(self.P, False)
        self.P.state=ProcessState.Ready
        assert self.s.none_sched()==(self.P,False)

class TestSystem(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSystem, self).__init__(*args, **kwargs)
        env = simpy.Environment()
        platform=Tomahawk2Platform()
        graph = DummyKpnGraph()
        mapping = DummyMapping(graph,
                            platform)
        readers = {}
        for pm in mapping.processMappings:
            name = pm.kpnProcess.name
            processors = pm.scheduler.processors
            readers[name] = DummyTraceReader(name)
        app = Application('app', graph, mapping, readers,0)
        self.system = System('dump.vcd', platform, [app])
        #add processes to the schedulers
        self.system.schedulers[0].assignProcess(self.system.pair[self.system.schedulers[0]][0])
        self.system.schedulers[1].assignProcess(self.system.pair[self.system.schedulers[1]][0])
        self.system.schedulers[2].assignProcess(self.system.pair[self.system.schedulers[2]][0])


    def test_simulate(self):
        self.system.simulate()

    def test_findScheduler(self):
        assert self.system.findScheduler('SchedulerForProcessor(PE3)').name=='SchedulerForProcessor(PE3)'

    def test_run(self):
        self.system.run()

    def test_Migrate(self):
        #Move process app.w3 from Scheduler3 to Scheduler2
        #Now there should be 2 processes allotted to scheduler 2
        #and none to scheduler3
        self.system.Migrate_ProcessToScheduler('app.w3','SchedulerForProcessor(PE2)')
        assert self.system.schedulers[0].processes[0].name == 'app.w2'
        assert self.system.schedulers[0].processes[1].name == 'app.w3'
        assert len(self.system.pair[self.system.schedulers[1]]) == 0
        self.system.Migrate_ProcessToScheduler('app.w2','SchedulerForProcessor(PE4)')
        #Move process app.w2 to scheduler 4
        assert self.system.schedulers[2].processes[0].name == 'app.w4'
        assert self.system.schedulers[2].processes[1].name == 'app.w2'

class Empty:
    pass

def common_sys():
    #create a dummy system object
    system=Empty()
    system.env=simpy.Environment()
    system.vcd_writer=VCDWriter(open(os.devnull,'w'), timescale='1 ps', date='today')
    system.vcd_writer.dump_off(system.env.now)
    kpnchannel=Empty()
    kpnchannel.token_size=4

    mappingInfo=Empty()
    mappingInfo.capacity=4
    mappingInfo.kpnChannel=kpnchannel
    mappingInfo.primitive=Primitive('dummy_cp', None, None, None)
    return system,mappingInfo

class DummyKpnGraph(KpnGraph):
    def __init__(self):
        KpnGraph.__init__(self)

        for i in range(2,5):
            self.channels.append(KpnChannel('c'+str(i), 4096))

        for i in range(2,5):
            self.processes.append(KpnProcess('w'+str(i)))
            self.connectProcessToOutgoingChannel(KpnProcess('w'+str(i)),KpnChannel('c'+str(i),4096))
            self.connectProcessToIncomingChannel(KpnProcess('w'+str(i)),KpnChannel('c'+str(i-1),4096))


class DummyMapping(Mapping):
    def __init__(self, kpn, platform):
        Mapping.__init__(self, kpn, platform)

        for i in range(2,5):
            scheduler=platform.findScheduler("SchedulerForProcessor(PE"+str(i)+")")
            scheduler.policies['FIFO']=100
            self.processMappings.append(ProcessMappingInfo(kpn.findProcess('w'+str(i)), scheduler, 'FIFO'))

        for i in range(2,5):
            kpnChannel=kpn.findChannel('c'+str(i))
            processorFrom=platform.findProcessor("PE"+str(i))
            processorTo=platform.findProcessor("PE"+str(i+1))
            viaMemory=platform.findMemory("sp"+str(i+1))
            primitive = platform.findPrimitive("consumer_cp",
                                               processorFrom,
                                               processorTo,
                                               viaMemory)
            self.channelMappings.append(ChannelMappingInfo(kpnChannel,
                                                           4,
                                                           primitive))

class DummyTraceReader(TraceReader):
    def __init__(self, process_name):
        super().__init__(process_name, None)
        self.traces=[ProcessEntry(12), ProcessEntry(1000), ProcessEntry(12),\
                ProcessEntry(1000), ProcessEntry(12), TerminateEntry()]
        self.i=-1

    def getNextEntry(self):
        self.i+=1
        return self.traces[self.i]

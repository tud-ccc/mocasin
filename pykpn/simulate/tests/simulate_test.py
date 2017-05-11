#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import simpy
import logging
import os

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

from unittest import TestCase

from pykpn.platforms import GenericNocPlatform
from pykpn.platforms import Tomahawk2Platform
from pykpn.simulate import System
from pykpn.simulate import Process
from pykpn.simulate import Scheduler
from pykpn.simulate import Application
from vcd import VCDWriter

log = logging.getLogger(__name__)



class TestSimulate(TestCase):
    def test_system(self):
        system=create_system()
        system.simulate()
        k=0
        I=0
        for i in system.pair:
            k+=1
            if k==1:I=i
            if k==2:system.Migrate_ProcessToScheduler(system.pair[I][0],i)
            system.findScheduler(i)
        system.run()

class TestChannel(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestChannel, self).__init__(*args, **kwargs)
        self.system, self.mappingInfo = common_sys()
        self.c=Channel('app.c1', self.system, self.mappingInfo)

    def test_initialized(self):
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
        self.processor=Processor('PE1', 'RISC', 200000000)

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
        self.info.processors=[Processor('PE1', 'RISC', 200000000)]
        self.info.policies={'FIFO':100}
        self.processes=[]
        self.s=Scheduler(self.system, [], self.policy, self.info)

    def test_RunScheduler(self):
        self.s.run()

class Empty:
        pass

def common_sys():
    system=Empty()
    system.env=simpy.Environment()
    system.vcd_writer=VCDWriter(open(os.devnull,'w'), timescale='1 ps', date='today')
    system.vcd_writer.dump_off(system.env.now)
    kpnchannel=Empty()
    kpnchannel.token_size=4

    mappingInfo=Empty()
    mappingInfo.capacity=4
    mappingInfo.kpnChannel=kpnchannel
    mappingInfo.primitive=Primitive()
    return system,mappingInfo


def create_system():
    env = simpy.Environment()
    platform = Tomahawk2Platform()
    graph = DummyKpnGraph()
    mapping = DummyMapping(graph,
                          platform)

    readers = {}
    for pm in mapping.processMappings:
        name = pm.kpnProcess.name
        processors = pm.scheduler.processors
        readers[name] = DummyTraceReader(name)
    app = Application('app', graph, mapping, readers,0)
    system = System('dump.vcd', platform, [app])
    return system

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

    def __init__(self, ProcessName):
        self.ProcessName =ProcessName
        self.buffer = None
        self.traces=[ProcessEntry(12), ProcessEntry(1000), ProcessEntry(12), ProcessEntry(1000), ProcessEntry(12), TerminateEntry()]
        self.i=-1

    def getNextEntry(self):
        if self.buffer is not None:
            tmp = self.buffer
            self.buffer = None
            return tmp
        self.i+=1
        return self.traces[self.i]


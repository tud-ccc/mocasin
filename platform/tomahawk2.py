# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pytrm import CostModel
from pytrm import Memory
from pytrm import Platform
from pytrm import Primitive
from pytrm import Processor

from simpy.resources.resource import Resource


class Tomahawk2Platform(Platform):

    def createRamPrimitive(self, from_, to, via):
        p = Primitive()
        p.typename = "global_ram_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        p.consume = CostModel("299+0.128*x")
        p.produce = CostModel("209.5 + 0.3179*x")

        return p

    def createConsumerPrimitive(self, from_, to, via):
        p = Primitive()
        p.typename = "consumer_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        p.produce = CostModel("299", bw=8.0)
        p.producerTransport = CostModel("x/bw", bw=8.0)
        p.consume = CostModel("164")

        p.producerTransport.resources.append(self.nis[from_])
        p.producerTransport.resources.append(self.nis[to])

        return p

    def createProducerPrimitive(self, from_, to, via, hops):
        p = Primitive()
        p.typename = "producer_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        p.produce = CostModel("205")
        p.consumerTransport = CostModel("15.4*hops+x/bw", bw=8.0, hops=hops)
        p.consume = CostModel("242")

        p.consumerTransport.resources.append(self.nis[from_])
        p.consumerTransport.resources.append(self.nis[to])

        return p

    def __init__(self, env):
        super(Platform, self).__init__()
        self.env = env

        self.nis = []

        for i in range(0, 8):
            processor = Processor("PE" + str(i), 'RISC', 200000000)
            self.processors.append(processor)
            memory = Memory("sp" + str(i), 32768)
            self.memories.append(memory)

            ni = Resource(env, capacity=1)
            self.nis.append(ni)

        self.ram = Memory("ram", 268435456)
        self.memories.append(self.ram)

        for i in range(0, 8):
            for j in range(0, 8):
                p = self.createRamPrimitive(i, j, 8)
                self.primitives.append(p)
                p = self.createConsumerPrimitive(i, j, j)
                self.primitives.append(p)

        for i in range(0, 4):
            for j in range(0, 4):
                p = self.createProducerPrimitive(i, j, i, 1)
                self.primitives.append(p)

        for i in range(4, 8):
            for j in range(4, 8):
                p = self.createProducerPrimitive(i, j, i, 1)
                self.primitives.append(p)

        for i in range(0, 4):
            for j in range(4, 8):
                p = self.createProducerPrimitive(i, j, i, 3)
                self.primitives.append(p)

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

    def createConsumerPrimitive(self, from_, to, via):
        p = Primitive()
        p.typename = "consumer_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        p.producePrepare = CostModel("299", bw=8.0)
        p.produceTransport = CostModel("x/bw", bw=8.0)
        p.consumePrepare = CostModel("164")

        p.produceTransport.resources.append(self.nis_out[from_])

        if from_ < 4 and to >= 4:
            p.produceTransport.resources.append(self.link_10_to_11)
            p.produceTransport.resources.append(self.link_11_to_01)
        if from_ >= 4 and to < 4:
            p.produceTransport.resources.append(self.link_01_to_11)
            p.produceTransport.resources.append(self.link_11_to_10)

        p.produceTransport.resources.append(self.nis_in[to])

        return p

    def createProducerPrimitive(self, from_, to, via):
        p = Primitive()
        p.typename = "producer_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        hops = 1
        if (from_ < 4 and to >= 4) or (from_ >= 4 and to < 4):
            hops = 3

        p.producePrepare = CostModel("205")
        p.consumePrepare = CostModel("242")
        p.consumeRequest = CostModel("8*hops", bw=8.0, hops=hops)
        p.consumeTransport = CostModel("8*hops+x/bw", bw=8.0, hops=hops)

        p.consumeRequest.resources.append(self.nis_out[to])
        p.consumeTransport.resources.append(self.nis_out[from_])

        if from_ < 4 and to >= 4:
            p.consumeTransport.resources.append(self.link_10_to_11)
            p.consumeTransport.resources.append(self.link_11_to_01)
        if from_ >= 4 and to < 4:
            p.consumeTransport.resources.append(self.link_01_to_11)
            p.consumeTransport.resources.append(self.link_11_to_10)

        p.consumeRequest.resources.append(self.nis_in[from_])
        p.consumeTransport.resources.append(self.nis_in[to])

        return p

    def __init__(self, env):
        Platform.__init__(self)
        #super(Platform, self).__init__()
        self.env = env

        self.nis_in = []
        self.nis_out = []

        for i in range(0, 8):
            processor = Processor("PE" + str(i), 'RISC', 200000000)
            self.processors.append(processor)
            memory = Memory("sp" + str(i), 32768)
            self.memories.append(memory)

            ni = Resource(env, capacity=1)
            no = Resource(env, capacity=1)
            self.nis_in.append(ni)
            self.nis_out.append(no)

        self.link_00_to_10 = Resource(env)
        self.link_10_to_11 = Resource(env)
        self.link_11_to_01 = Resource(env)
        self.link_01_to_00 = Resource(env)

        self.link_00_to_01 = Resource(env)
        self.link_01_to_11 = Resource(env)
        self.link_11_to_10 = Resource(env)
        self.link_10_to_00 = Resource(env)

        for i in range(0, 8):
            for j in range(0, 8):
                p = self.createConsumerPrimitive(i, j, j)
                self.primitives.append(p)
                p = self.createProducerPrimitive(i, j, i)
                self.primitives.append(p)

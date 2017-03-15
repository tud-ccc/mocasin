# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pytrm import CostModel
from pytrm import Memory
from pytrm import Platform
from pytrm import Primitive
from pytrm import Processor
from pytrm import Noc

from simpy.resources.resource import Resource


class Tomahawk2Platform(Platform):


    def createConsumerPrimitive(self, m, from_, to, via):
        p = Primitive()
        p.typename = "consumer_cp"
        p.from_ = self.processors[int(from_[2])]
        p.to = self.processors[int(to[2])]
        p.via = self.memories[int(via[2])]

        producePrepare = CostModel("299", bw=8.0)
        produceTransport = CostModel("x/bw", bw=8.0)
        consumePrepare = CostModel("164")

        R=m.get_route(from_, to)
        produceTransport.resources.extend(R)

        p.produce.append(producePrepare)
        p.produce.append(produceTransport)
        p.consume.append(consumePrepare)

        return p

    def createProducerPrimitive(self, m, from_, to, via):
        p = Primitive()
        p.typename = "producer_cp"
        p.from_ = self.processors[int(from_[2])]
        p.to = self.processors[int(to[2])]
        p.via = self.memories[int(via[2])]

        R_r=m.get_route(to, from_) # request
        R_t=m.get_route(from_, to) # transport
        producePrepare = CostModel("205")
        consumePrepare = CostModel("242")
        consumeRequest = CostModel("8*hops", bw=8.0, hops=len(R_r)-1)
        consumeTransport = CostModel("8*hops+x/bw", bw=8.0, hops=len(R_t)-1)

        consumeRequest.resources.append(R_r[0])
        consumeRequest.resources.append(R_r[-1])
        consumeTransport.resources.extend(R_t)

        p.produce.append(producePrepare)
        p.consume.append(consumePrepare)
        p.consume.append(consumeRequest)
        p.consume.append(consumeTransport)
        return p

    def __init__(self, env):
        Platform.__init__(self)
        #super(Platform, self).__init__()
        self.env = env
        m=Noc(self.env,"yx")
        m.meshNoc(2,2)

        for i in range(0, 8):
            processor = Processor("PE" + str(i), 'RISC', 200000000)
            self.processors.append(processor)
            memory = Memory("sp" + str(i), 32768)
            self.memories.append(memory)
            m.create_ni([memory, processor], int(i/4), int(i/4))

        for i in range(0, 8):
            for j in range(0, 8):
                p = self.createConsumerPrimitive(m, "PE"+str(i), "PE"+str(j), "sp"+str(j))
                self.primitives.append(p)
                p = self.createProducerPrimitive(m, "PE"+str(i), "PE"+str(j), "sp"+str(i))
                self.primitives.append(p)

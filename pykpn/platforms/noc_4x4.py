# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from common import CostModel
from common import Memory
from common import Platform
from common import Primitive
from common import Processor

from simpy.resources.resource import Resource


class Noc4x4Platform(Platform):

    def getRoute(self, pe_from, pe_to):
        from_x = int(pe_from / 4)
        from_y = pe_from % 4
        to_x = int(pe_to / 4)
        to_y = pe_to % 4

        route = []

        pos_x = from_x
        pos_y = from_y

        while pos_x != to_x:
            if pos_x < to_x:
                next_pos_x = pos_x + 1
            else:
                next_pos_x = pos_x - 1
            link_name = "%d%d_to_%d%d" % (pos_x, pos_y, next_pos_x, pos_y)
            route.append(self.links[link_name])
            pos_x = next_pos_x
        while pos_y != to_y:
            if pos_y < to_y:
                next_pos_y = pos_y + 1
            else:
                next_pos_y = pos_y - 1
            link_name = "%d%d_to_%d%d" % (pos_x, pos_y, pos_x, next_pos_y)
            route.append(self.links[link_name])
            pos_y = next_pos_y

        return route

    def createConsumerPrimitive(self, from_, to, via):
        p = Primitive()
        p.typename = "consumer_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        p.producePrepare = CostModel("299", bw=8.0)
        p.produceTransport = CostModel("x*20/bw", bw=8.0)
        p.consumePrepare = CostModel("164")

        route = self.getRoute(from_, to)

        p.produceTransport.resources.append(self.nis_out[from_])
        p.produceTransport.resources.extend(route)
        p.produceTransport.resources.append(self.nis_in[to])

        return p

    def createProducerPrimitive(self, from_, to, via):
        p = Primitive()
        p.typename = "producer_cp"
        p.from_ = self.processors[from_]
        p.to = self.processors[to]
        p.via = self.memories[via]

        route = self.getRoute(from_, to)
        hops = len(route)

        p.consumePrepare = CostModel("242")
        p.consumeRequest = CostModel("7.7*hops", bw=8.0, hops=hops)
        p.consumeTransport = CostModel("7.7*hops+x/bw", bw=8.0, hops=hops)

        p.consumeRequest.resources.append(self.nis_out[to])
        p.consumeRequest.resources.append(self.nis_in[from_])
        p.consumeTransport.resources.append(self.nis_out[from_])
        p.consumeTransport.resources.extend(route)
        p.consumeTransport.resources.append(self.nis_in[to])

        return p

    def __init__(self, env):
        super(Platform, self).__init__()
        self.env = env

        self.nis_in = []
        self.nis_out = []

        self.links={}

        for i in range(0, 16):
            processor = Processor("PE" + str(i), 'RISC', 200000000)
            self.processors.append(processor)
            memory = Memory("pe" + str(i) + "_mem", 32768)
            self.memories.append(memory)

            ni = Resource(env, capacity=1)
            no = Resource(env, capacity=1)
            self.nis_in.append(ni)
            self.nis_out.append(no)

        for x in range(0,4):
            for y in range(0,4):
                if x < 4:
                    name = "%d%d_to_%d%d" % (x, y, x+1, y)
                    self.links[name] = Resource(env)
                if y < 4:
                    name = "%d%d_to_%d%d" % (x, y, x, y+1)
                    print(name)
                    self.links[name] = Resource(env)
                if x > 0:
                    name = "%d%d_to_%d%d" % (x, y, x-1, y)
                    self.links[name] = Resource(env)
                if y > 0:
                    name = "%d%d_to_%d%d" % (x, y, x, y-1)
                    self.links[name] = Resource(env)

        for i in range(0, 16):
            for j in range(0, 16):
                p = self.createConsumerPrimitive(i, j, j)
                self.primitives.append(p)
                p = self.createProducerPrimitive(i, j, i)
                self.primitives.append(p)

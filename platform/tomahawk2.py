# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pytrm import Platform
from pytrm import Link
from pytrm import XYRouter
from pytrm import Processor
from pytrm import Memory
from pytrm import Endpoint
from pytrm import Primitive


class Tomahawk2Platform(Platform):

    def create_links_and_connect(self, bandwidth, _from, _to):
        link_fw = Link(bandwidth)
        link_bw = Link(bandwidth)
        link_fw.connect(_from, _to)
        link_bw.connect(_to, _from)
        self.links.append(link_fw)
        self.links.append(link_bw)

    def __init__(self):
        super(Platform, self).__init__()

        router00 = XYRouter(0, 0)
        router01 = XYRouter(0, 1)
        router10 = XYRouter(1, 0)
        router11 = XYRouter(1, 1)

        self.routers = [router00, router01, router10, router11]

        self.create_links_and_connect(10, router00, router01)
        self.create_links_and_connect(10, router00, router10)
        self.create_links_and_connect(10, router11, router01)
        self.create_links_and_connect(10, router11, router10)

        for i in range(0, 8):
            processor = Processor("PE" + str(i), 'RISC', 2000000)
            self.processors.append(processor)
            memory = Memory("sp" + str(i), 32768)
            self.memories.append(memory)
            self.endpoints.append(Endpoint(processor, memory))

        for i in range(0, 4):
            self.create_links_and_connect(8, self.endpoints[i], router10)
        for i in range(4, 8):
            self.create_links_and_connect(8, self.endpoints[i], router01)

        for i in range(0, 8):
            for j in range(0, 8):
                if i != j:
                    self.primitives.append(Primitive(
                        self, "noc_cp", self.processors[i],
                        self.processors[j], self.memories[j],
                        "200+x", "0", "100"))  # TODO cost functions

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from pytrm import Memory
from pytrm import NocPrimitive
from pytrm import Platform
from pytrm import Primitive
from pytrm import Processor


class Tomahawk2Platform(Platform):

    def __init__(self):
        super(Platform, self).__init__()

        for i in range(0, 8):
            processor = Processor("PE" + str(i), 'RISC', 200000)
            self.processors.append(processor)
            memory = Memory("sp" + str(i), 32768)
            self.memories.append(memory)

        for i in range(0, 8):
            for j in range(0, 8):
                self.primitives.append(Primitive(
                    "global_ram_cp", self.processors[i], self.processors[j],
                    self.memories[i], "299+0.128*x", "0", "209.5 + 0.3179*x"))

        for i in range(0, 4):
            for j in range(0, 4):
                self.primitives.append(NocPrimitive(
                    "consumer_cp", self.processors[i], self.processors[j],
                    self.memories[i], "299.2+x/bw", "0", "164",
                    1, 8.0, None, None, None, None))
                self.primitives.append(NocPrimitive(
                    "producer_cp", self.processors[i], self.processors[j],
                    self.memories[i], "205", "0", "242.2+15.4*hops+x/bw",
                    None, None, None, None, 1, 8.0))

        for i in range(4, 8):
            for j in range(4, 8):
                self.primitives.append(NocPrimitive(
                    "consumer_cp", self.processors[i], self.processors[j],
                    self.memories[i], "299.2+x/bw", "0", "164",
                    1, 8.0, None, None, None, None))
                self.primitives.append(NocPrimitive(
                    "producer_cp", self.processors[i], self.processors[j],
                    self.memories[i], "205", "0", "242.2+15.4*hops+x/bw",
                    None, None, None, None, 1, 8.0))

        for i in range(0, 4):
            for j in range(4, 8):
                self.primitives.append(NocPrimitive(
                    "consumer_cp", self.processors[i], self.processors[j],
                    self.memories[i], "299.2+x/bw", "0", "164",
                    3, 8.0, None, None, None, None))
                self.primitives.append(NocPrimitive(
                    "producer_cp", self.processors[i], self.processors[j],
                    self.memories[i], "205", "0", "242.2+15.4*hops+x/bw",
                    None, None, None, None, 3, 8.0))
                self.primitives.append(NocPrimitive(
                    "consumer_cp", self.processors[j], self.processors[i],
                    self.memories[j], "299.2+x/bw", "0", "164",
                    3, 8.0, None, None, None, None))
                self.primitives.append(NocPrimitive(
                    "producer_cp", self.processors[j], self.processors[i],
                    self.memories[j], "205", "0", "242.2+15.4*hops+x/bw",
                    None, None, None, None, 3, 8.0))

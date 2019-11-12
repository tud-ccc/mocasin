# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.simulate.system import RuntimeSystem
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.common.platform import Platform
from platforms.platformDesigner import PlatformDesigner
from pykpn.mapper.random import RandomMapping
from tgff.tgffGenerators import TgffTraceGenerator

class TgffRuntimeSystem(RuntimeSystem):
    def __init__(self, tgff_processor, tgff_graphs, env):
        platform = TgffRuntimePlatform(tgff_processor)
        applications = []
        trace_generator = TgffTraceGenerator({tgff_processor.name : tgff_processor}, tgff_graphs)
        for tgff_graph in tgff_graphs.values():
            name = tgff_graph.identifier
            kpn_graph = tgff_graph.to_kpn_graph()
            mapping = RandomMapping(kpn_graph, platform)
            applications.append(RuntimeKpnApplication(name, kpn_graph, mapping, trace_generator, env))
        
        super(TgffRuntimeSystem, self).__init__(platform, applications, env)

class TgffRuntimePlatform(Platform):
    """Initializes an example 2x2 architecture with the 
    given processor as processing element connected via
    a shared memory.
    """
    def __init__(self, tgff_processor, name="example_platform"):
        super(TgffRuntimePlatform, self).__init__(name)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")
        designer.addPeClusterTMP("cluster_0", tgff_processor.to_pykpn_processor(), 4)
        #just some random guessed numbers from here on
        designer.addCommunicationResource("shared_memory", ["cluster_0"], 100, 100, 1000, 1000, frequencyDomain=2000)
        designer.finishElement()
        
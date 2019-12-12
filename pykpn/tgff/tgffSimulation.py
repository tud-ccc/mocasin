# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Platform
from pykpn.mapper.random import RandomMapping
from pykpn.simulate.system import RuntimeSystem
from pykpn.platforms.topologies import meshTopology
from pykpn.tgff.tgffGenerators import TgffTraceGenerator
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.platforms.platformDesigner import PlatformDesigner
from pykpn.tgff.tgffParser.parser import Parser
from pykpn.platforms.utils import simpleDijkstra as sd


class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""
    pass


class RuntimeParser(Parser):
    __instance = None
    file_path = None
    components = None
    def __new__(self):
        if not RuntimeParser.__instance:
            RuntimeParser.__instance = object.__new__(RuntimeParser)
            RuntimeParser.__instance.__init__()
        return RuntimeParser.__instance
    
    def __init__(self):
        super(RuntimeParser, self).__init__()
    
    def parse_file(self, file_path):
        if not file_path == RuntimeParser.file_path:
            RuntimeParser.file_path = file_path
            RuntimeParser.components = super(RuntimeParser, self).parse_file(file_path)
            return RuntimeParser.components
        else:
            return RuntimeParser.components
    

class TgffRuntimeSystem(RuntimeSystem):
    """Specification of the RuntimeSystem class for tgff simulation
    """
    def __init__(self, tgff_processor, tgff_graphs, env, topology="bus"):
        """Create a new RuntimeSystem for simulation purposes. As simulation
        platform a mesh or bus architecture will be created, using the given
        tgff processor. 
        :param tgff_processor: The processing element for the platform.
        :type tgff_processor: TgffProcessor
        :param tgff_graphs: A set of tgff application graphs, which should be 
                            executed on the platform.
        :type tgff_graphs: dict {String : TgffGraph}
        :param env: The related simpy environment
        :type env: Environment
        """
        platform = None
        if topology == 'bus':
            platform = TgffRuntimePlatformBus(tgff_processor)
        elif topology == 'mesh':
            platform = TgffRuntimePlatformMesh(tgff_processor)
            #TODO: implement a mesh example architecture
            #specify the amount of pe's? how?
            pass
        else:
            raise RuntimeError("Please provide a valid topology for the runtime platform!")
        applications = []
        trace_generator = TgffTraceGenerator({tgff_processor.name : tgff_processor}, tgff_graphs)
        for tgff_graph in tgff_graphs.values():
            name = tgff_graph.identifier
            kpn_graph = tgff_graph.to_kpn_graph()
            mapping = RandomMapping(kpn_graph, platform)
            applications.append(RuntimeKpnApplication(name, kpn_graph, mapping, trace_generator, env))
        
        super(TgffRuntimeSystem, self).__init__(platform, applications, env)


class KpnGraphFromTgff():
    """New, since we want to return a common.kpn instance instead of am TgffToKpnGraph instance
    """
    #TODO: Add doc string
    def __new__(self, file_path, task_graph):
        parser = RuntimeParser()
        tgff_graphs = parser.parse_file(file_path)[0]
        
        if not task_graph in tgff_graphs:
            raise TgffReferenceError()
        
        return tgff_graphs[task_graph].to_kpn_graph()


class TraceGeneratorWrapper():
    def __new__(self, file_path):
        parser = RuntimeParser()
        tgff_components = parser.parse_file(file_path)
        trace_generator = TgffTraceGenerator(tgff_components[1], tgff_components[0])
        return trace_generator
    

class PlatformFromTgff():
    def __new__(self, platform_type, processor, file_path, amount):
        parser = RuntimeParser()
        tgff_processors = parser.parse_file(file_path)[1]
        if processor < 0 or processor >= len(tgff_processors):
            raise TgffReferenceError()
        if platform_type == 'bus':
            return TgffRuntimePlatformBus(tgff_processors[processor])
        elif platform_type == 'mesh':
            return TgffRuntimePlatformMesh(tgff_processors[processor])
        else:
            raise RuntimeError('You have to implement this type first!')


class TgffRuntimePlatformBus(Platform):
    def __init__(self, tgff_processor, name="simulation_platform"):
        """Initializes an example platform with four processing
        elements connected via an shared memory.
        :param tgff_processor: the processing element for the platform
        :type tgff_processor: TgffProcessor
        :param name: The name for the returned platform
        :type name: String
        """
        super(TgffRuntimePlatformBus, self).__init__(name)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")
        designer.addPeClusterForProcessor("cluster_0", tgff_processor.to_pykpn_processor(), 4)
        designer.addCommunicationResource("shared_memory", ["cluster_0"], 100, 100, 1000, 1000, frequencyDomain=2000)
        designer.finishElement()
        

class TgffRuntimePlatformMesh(Platform):
    def __init__(self, tgff_processor, name="simulation_platform"):
        super(TgffRuntimePlatformMesh, self).__init__(name)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")
        designer.addPeClusterForProcessor("cluster_0", tgff_processor.to_pykpn_processor(), 4)
        topology = meshTopology(['processor_0', 'processor_1','processor_2', 'processor_3'])
        designer.createNetworkForCluster("cluster_0", 'testNet', topology, sd, 2000, 100, 100, 100, 100)
        designer.finishElement()
    
        
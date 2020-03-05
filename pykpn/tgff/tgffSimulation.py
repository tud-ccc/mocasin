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

_parsed_tgff_files = {}

class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""
    pass


class KpnGraphFromTgff():
    """New, since we want to return a common.kpn instance instead of am TgffToKpnGraph instance
    """
    #TODO: Add doc string
    def __new__(self, file_path, task_graph):
        if not file_path in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_graphs = _parsed_tgff_files[file_path][0]
        
        if not task_graph in tgff_graphs:
            raise TgffReferenceError()
        
        return tgff_graphs[task_graph].to_kpn_graph()


class TraceGeneratorWrapper():
    def __new__(self, file_path):
        if not file_path in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_components = _parsed_tgff_files[file_path]
        trace_generator = TgffTraceGenerator(tgff_components[1], tgff_components[0])
        
        return trace_generator
    

class PlatformFromTgff():
    def __new__(self, platform_type, processor, file_path, amount):
        
        if not file_path in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_processors = _parsed_tgff_files[file_path][1]
        
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
    
        
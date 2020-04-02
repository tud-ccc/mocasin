# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Platform
from pykpn.platforms.topologies import meshTopology
from pykpn.platforms.platformDesigner import PlatformDesigner
from pykpn.platforms.utils import simpleDijkstra as sd
from pykpn.tgff.trace import TgffTraceGenerator
from pykpn.tgff.tgffParser.parser import Parser

_parsed_tgff_files = {}

class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""
    pass


class KpnGraphFromTgff():
    """New, since we want to return a common.kpn instance instead of am TgffToKpnGraph instance
    """
    #TODO: Add doc string
    def __new__(self, file_path, task_graph):
        if file_path not in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_graphs = _parsed_tgff_files[file_path][0]
        
        if task_graph not in tgff_graphs:
            raise TgffReferenceError()
        
        return tgff_graphs[task_graph].to_kpn_graph()


class TraceGeneratorWrapper():
    def __new__(self, file_path):
        if not file_path in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_components = _parsed_tgff_files[file_path]
        processor_dict = {}
        for processor in tgff_components[1]:
            processor_dict.update({processor.type : processor})
        trace_generator = TgffTraceGenerator(processor_dict, tgff_components[0])
        
        return trace_generator
    

class PlatformFromTgff():
    def __new__(self, platform_type, processor, file_path, amount):
        print(processor)
        if not file_path in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_processors = _parsed_tgff_files[file_path][1]


        if int(processor.split('_')[1]) >= len(tgff_processors):
            raise TgffReferenceError()

        processor_dict = {}
        for proc in tgff_processors:
            processor_dict.update({proc.type : proc})


        if platform_type == 'bus':
            return TgffRuntimePlatformBus(processor_dict[processor])
        elif platform_type == 'mesh':
            return TgffRuntimePlatformMesh(processor_dict[processor])
        elif platform_type == 'clustered':
            return TgffRuntimePlatformMultiCluster(processor_dict[processor], processor_dict[processor])
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
        designer.addPeClusterForProcessor("cluster_0", tgff_processor.to_pykpn_processor(), 16)
        topology = meshTopology(['processor_0', 'processor_1', 'processor_2', 'processor_3', 'processor_4',
                                 'processor_5', 'processor_6', 'processor_7', 'processor_8', 'processor_9',
                                 'processor_10', 'processor_11', 'processor_12', 'processor_13', 'processor_14',
                                 'processor_15'])
        designer.createNetworkForCluster("cluster_0", 'testNet', topology, sd, 2000, 100, 100, 100, 100)
        designer.finishElement()
        
class TgffRuntimePlatformMultiCluster(Platform):
    def __init__(self, processor_cl0, processor_cl1, name="simulation_platform"):
        super(TgffRuntimePlatformMultiCluster, self).__init__(name)
        designer = PlatformDesigner(self)
        
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")
        
        #cluster 0
        designer.addPeClusterForProcessor("cluster_0",
                                          processor_cl0.to_pykpn_processor(),
                                          4)
        designer.addCommunicationResource("lvl2_cl0",
                                          ["cluster_0"],
                                          25,
                                          30,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=600000000.0)
        
        #cluster 1
        designer.addPeClusterForProcessor("cluster_1",
                                          processor_cl1.to_pykpn_processor(),
                                          2)
        designer.addCommunicationResource("lvl2_cl1",
                                          ["cluster_1"],
                                          25,
                                          30,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=667000000.0)
        
        #shared memory
        designer.addCommunicationResource("RAM",
                                          ["cluster_0", "cluster_1"],
                                          55,
                                          60,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=670000000.0)
        designer.finishElement()
        
        
        
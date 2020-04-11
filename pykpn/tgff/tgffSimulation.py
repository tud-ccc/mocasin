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
        if file_path not in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_components = _parsed_tgff_files[file_path]
        processor_dict = {}
        for processor in tgff_components[1]:
            processor_dict.update({processor.type : processor})
        trace_generator = TgffTraceGenerator(processor_dict, tgff_components[0])
        
        return trace_generator
    

class PlatformFromTgff():
    def __new__(self, platform_type, processor_1, processor_2, processor_3, processor_4, file_path):
        if file_path not in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_processors = _parsed_tgff_files[file_path][1]

        processor_dict = {}
        for proc in tgff_processors:
            processor_dict.update({proc.type : proc})


        if platform_type == 'bus':
            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()
            return TgffRuntimePlatformBus(processor_dict[processor_1])

        elif platform_type == 'parallella':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformMesh(processor_dict[processor_1], processor_dict[processor_2])

        elif platform_type == 'exynos990':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_3.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_4.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformMultiCluster(processor_dict[processor_1],
                                                   processor_dict[processor_2],
                                                   processor_dict[processor_3],
                                                   processor_dict[processor_4])
        elif platform_type == 'coolidge':
            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformCoolidge(processor_dict[processor_1])

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
        
#prallella inspired
class TgffRuntimePlatformMesh(Platform):
    def __init__(self, tgff_processor, processor_2, name="simulation_platform"):
        super(TgffRuntimePlatformMesh, self).__init__(name)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")

        designer.addPeClusterForProcessor("cluster_0", tgff_processor.to_pykpn_processor(), 16)
        topology = meshTopology(['processor_0', 'processor_1', 'processor_2', 'processor_3', 'processor_4',
                                 'processor_5', 'processor_6', 'processor_7', 'processor_8', 'processor_9',
                                 'processor_10', 'processor_11', 'processor_12', 'processor_13', 'processor_14',
                                 'processor_15'])
        designer.createNetworkForCluster("cluster_0", 'testNet', topology, sd, 6000000.0, 100, 150, 100, 60)

        designer.addPeClusterForProcessor("cluster_1", processor_2.to_pykpn_processor(), 2)
        designer.addCommunicationResource("lvl2_cl1",
                                          ["cluster_1"],
                                          500,
                                          1000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=600000000.0)


        designer.addCommunicationResource("RAM",
                                          ["cluster_0", "cluster_1"],
                                          1000,
                                          3000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=6000000.0)
        designer.finishElement()

#exynos inspired
class TgffRuntimePlatformMultiCluster(Platform):
    def __init__(self, processor_1, processor_2, processor_3, processor_4, name="simulation_platform"):
        super(TgffRuntimePlatformMultiCluster, self).__init__(name)
        designer = PlatformDesigner(self)
        
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")
        
        #cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_0",
                                          processor_1.to_pykpn_processor(),
                                          2)
        #Add L1/L2 caches
        designer.addCacheForPEs("cluster_0", 5,7, float('inf'), float('inf'), frequencyDomain=6000000.0 ,name='L1')
        designer.addCommunicationResource("lvl2_cl0",
                                          ["cluster_0"],
                                          225,
                                          300,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=600000000.0)
        
        #cluster 1, with l2 cache
        designer.addPeClusterForProcessor("cluster_1",
                                          processor_2.to_pykpn_processor(),
                                          2)
        #Add L1/L2 caches
        designer.addCacheForPEs("cluster_1", 5,7, float('inf'), float('inf'), frequencyDomain=6670000.0 ,name='L1')
        designer.addCommunicationResource("lvl2_cl1",
                                          ["cluster_1"],
                                          225,
                                          300,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=667000000.0)

        #cluster 2, with l2 cache
        designer.addPeClusterForProcessor("cluster_2",
                                          processor_3.to_pykpn_processor(),
                                          4)
        #Add L1/L2 caches
        designer.addCacheForPEs("cluster_2", 5,7, float('inf'), float('inf'), frequencyDomain=6670000.0 ,name='L1')
        designer.addCommunicationResource("lvl2_cl2",
                                          ["cluster_2"],
                                          225,
                                          300,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=667000000.0)

        #RAM connecting all clusters
        designer.addCommunicationResource("RAM",
                                          ["cluster_0", "cluster_1", "cluster_2"],
                                          800,
                                          2000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=6000000.0)

        #single GPU
        designer.addPeClusterForProcessor("GPU",
                                          processor_4.to_pykpn_processor(),
                                          1)
        designer.addCacheForPEs("GPU", 5,7, float('inf'), float('inf'), frequencyDomain=6670000.0 ,name='GPU_MEM')

        #another memory, simulating BUS
        designer.addCommunicationResource("BUS",
                                          ["cluster_0", "cluster_1", "cluster_2", "GPU"],
                                          2000,
                                          6000,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=4000000.0)

        designer.finishElement()

class TgffRuntimePlatformCoolidge(Platform):
    #The topology and latency numbers (!) of this should come from the MPPA3 Coolidge
    #sheet published by Kalray
    def __init__(self, processor_1, processor_2, name="coolidge-inspired"):
        super(TgffRuntimePlatformCoolidge, self).__init__(name)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('coolidge')

        for i in range(0, 5):
            designer.newElement('cluster_{0}'.format(i))

            for j in range(0, 4):
                designer.addPeClusterForProcessor('cluster_{0}_{1}'.format(i, j),
                                                  processor.to_pykpn_processor(),
                                                  4)

                topology = fullyConnectedTopology(['processor_{0}'.format(i * 16 + j * 4),
                                         'processor_{0}'.format(i * 16 + j * 4 + 1),
                                         'processor_{0}'.format(i * 16 + j * 4 + 2),
                                         'processor_{0}'.format(i * 16 + j * 4 + 3)])

                designer.createNetworkForCluster('cluster_{0}_{1}'.format(i, j),
                                                 'noc_{0}_{1}'.format(i, j),
                                                 topology,
                                                 sd,
                                                 2000, 100, 500, 100, 20)

            designer.addCommunicationResource('L2_{0}'.format(i),
                                              ['cluster_{0}_0'.format(i),
                                               'cluster_{0}_1'.format(i),
                                               'cluster_{0}_2'.format(i),
                                               'cluster_{0}_3'.format(i)],
                                              100, 100, 1000, 1000, frequencyDomain=2000)

            designer.finishElement()

        designer.addCommunicationResource("RAM", ['chip_0', 'chip_1', 'chip_2', 'chip_3', 'chip_4'],
                                          1000, 1000, 1000, 1000, frequencyDomain=10000)

        designer.finishElement()


# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.common.platform import Platform
from pykpn.platforms.topologies import meshTopology, fullyConnectedTopology
from pykpn.platforms.platformDesigner import PlatformDesigner
from pykpn.platforms.utils import simpleDijkstra as sd
from pykpn.tgff.trace import TgffTraceGenerator
from pykpn.tgff.tgffParser.parser import Parser

_parsed_tgff_files = {}

class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""
    pass


class KpnGraphFromTgff:
    """New, since we want to return a common.kpn instance instead of am TgffToKpnGraph instance
    """
    def __new__(cls, file_path, task_graph):
        if file_path not in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_graphs = _parsed_tgff_files[file_path][0]
        
        if task_graph not in tgff_graphs:
            raise TgffReferenceError()
        
        return tgff_graphs[task_graph].to_kpn_graph()


class TraceGeneratorWrapper:
    def __new__(cls, file_path, task_graph, repetition=1):
        if file_path not in _parsed_tgff_files:
            _parsed_tgff_files.update( {file_path : Parser().parse_file(file_path)} )
        
        tgff_components = _parsed_tgff_files[file_path]
        processor_dict = {}

        for processor in tgff_components[1]:
            processor_dict.update({processor.type : processor})

        trace_generator = TgffTraceGenerator(processor_dict, tgff_components[0][task_graph], repetition)
        
        return trace_generator
    

class PlatformFromTgff:
    def __new__(cls, platform_type, processor_1, processor_2, processor_3, processor_4, file_path):
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

        elif platform_type == 'odroid':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformOdroid(processor_dict[processor_1],
                                                processor_dict[processor_2])

        elif platform_type == 'exynos990':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_3.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_4.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformExynos990(processor_dict[processor_1],
                                                   processor_dict[processor_2],
                                                   processor_dict[processor_3],
                                                   processor_dict[processor_4])
        elif platform_type == 'coolidge':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformCoolidge(processor_dict[processor_1], processor_dict[processor_2])

        elif platform_type == 'multi_cluster':
            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return TgffRuntimePlatformMultiCluster(processor_dict[processor_1], processor_dict[processor_2])


        else:
            raise RuntimeError('You have to implement this type first!')


class TgffRuntimePlatformBus(Platform):
    def __init__(self, tgff_processor, name="bus"):
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
    def __init__(self, tgff_processor, processor_2, name="parallella-styled"):
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


class TgffRuntimePlatformOdroid(Platform):
    def __init__(self, processor_1, processor_2, name="odroid"):
        super(TgffRuntimePlatformOdroid, self).__init__(name)
        designer = PlatformDesigner(self)

        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("exynos5422")

        # cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_a7",
                                          processor_1.to_pykpn_processor(),
                                          4)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_a7", 1, 0, 8.0, float('inf'), frequencyDomain=1400000000.0, name='L1_A7')
        designer.addCommunicationResource("L2_A7",
                                          ["cluster_a7"],
                                          250,
                                          250,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=1400000000.0)

        # cluster 1, with l2 cache
        designer.addPeClusterForProcessor("cluster_a15",
                                          processor_2.to_pykpn_processor(),
                                          4)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_a15", 1, 4, 8.0, 8.0, frequencyDomain=2000000000.0, name='L1_A15')
        designer.addCommunicationResource("L2_A15",
                                          ["cluster_a15"],
                                          250,
                                          250,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=2000000000.0)

        # RAM connecting all clusters
        designer.addCommunicationResource("DRAM",
                                          ["cluster_a7", "cluster_a15"],
                                          120,
                                          120,
                                          8.0,
                                          8.0,
                                          frequencyDomain=933000000.0)
        designer.finishElement()


class TgffRuntimePlatformExynos990(Platform):
    def __init__(self, processor_1, processor_2, processor_3, processor_4, name="exynos-990"):
        super(TgffRuntimePlatformExynos990, self).__init__(name)
        designer = PlatformDesigner(self)
        
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("test_chip")
        
        #cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_0",
                                          processor_1.to_pykpn_processor(),
                                          2)
        #Add L1/L2 caches
        designer.addCacheForPEs("cluster_0", 5, 7, float('inf'), float('inf'), frequencyDomain=6000000.0, name='L1')
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
        designer.addCacheForPEs("cluster_1", 5, 7, float('inf'), float('inf'), frequencyDomain=6670000.0, name='L1')
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
        designer.addCacheForPEs("cluster_2", 5, 7, float('inf'), float('inf'), frequencyDomain=6670000.0, name='L1')
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
        designer.addCacheForPEs("GPU", 5, 7, float('inf'), float('inf'), frequencyDomain=6670000.0, name='GPU_MEM')

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
    def __init__(self, processor_1, processor_2, name="coolidge"):
        super(TgffRuntimePlatformCoolidge, self).__init__(name)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('coolidge')

        #create five chips with 16 cores, NoC, +Security Core
        for i in range(0, 5):
            designer.newElement('cluster_{0}'.format(i))

            designer.addPeClusterForProcessor(f'cluster_{i}_0', processor_1.to_pykpn_processor(), 16)

            topology = fullyConnectedTopology(['processor_{0}'.format(i * 17), 'processor_{0}'.format(i * 17 + 1),
                                               'processor_{0}'.format(i * 17 + 2), 'processor_{0}'.format(i * 17 + 3),
                                               'processor_{0}'.format(i * 17 + 4), 'processor_{0}'.format(i * 17 + 5),
                                               'processor_{0}'.format(i * 17 + 6), 'processor_{0}'.format(i * 17 + 7),
                                               'processor_{0}'.format(i * 17 + 8), 'processor_{0}'.format(i * 17 + 9),
                                               'processor_{0}'.format(i * 17 + 10), 'processor_{0}'.format(i * 17 + 11),
                                               'processor_{0}'.format(i * 17 + 12), 'processor_{0}'.format(i * 17 + 13),
                                               'processor_{0}'.format(i * 17 + 14), 'processor_{0}'.format(i * 17 + 15)
                                               ])

            designer.createNetworkForCluster(f'cluster_{i}_0', f'noc_{i}', topology, sd, 40000.0, 100, 150, 100, 60)

            designer.addPeClusterForProcessor(f'cluster_{i}_1', processor_2.to_pykpn_processor(), 1)

            designer.addCommunicationResource(f'L2_{i}', [f'cluster_{i}_0', f'cluster_{i}_1'], 500, 1500,
                                              float('inf'), float('inf'), frequencyDomain=600000.0)

            designer.finishElement()

        designer.addCommunicationResource("RAM", ['chip_0', 'chip_1', 'chip_2', 'chip_3', 'chip_4'],
                                          1000, 3000, float('inf'), float('inf'), frequencyDomain=10000)

        designer.finishElement()

class TgffRuntimePlatformMultiCluster(Platform):
    def __init__(self, processor_1, processor_2, name='multi_cluster'):
        super(TgffRuntimePlatformMultiCluster, self).__init__(name)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement('multi_cluster')

        #add first cluster with L2 cache
        designer.addPeClusterForProcessor('cluster_0', processor_1.to_pykpn_processor(), 2)
        designer.addCommunicationResource('cl0_l2', ['cluster_0'], 100, 100, float('inf'), float('inf'),
                                          frequencyDomain=10000)

        #add second cluster with L2 cache
        designer.addPeClusterForProcessor('cluster_1', processor_2.to_pykpn_processor(), 2)
        designer.addCommunicationResource('cl1_l2', ['cluster_1'], 100, 100, float('inf'), float('inf'),
                                          frequencyDomain=10000)

        #connect both clusters via RAM
        designer.addCommunicationResource('RAM', ['cluster_0', 'cluster_1'], 1000, 1000, float('inf'), float('inf'),
                                          frequencyDomain=1000)

        designer.finishElement()

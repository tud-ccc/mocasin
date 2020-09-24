# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.common.platform import Platform, FrequencyDomain
from pykpn.platforms.topologies import meshTopology, fullyConnectedTopology
from pykpn.platforms.platformDesigner import PlatformDesigner
from pykpn.platforms.utils import simpleDijkstra as sd
from pykpn.tgff.trace import TgffTraceGenerator
from pykpn.tgff.tgffParser.parser import Parser

import logging
log = logging.getLogger(__name__)

_parsed_tgff_files = {}

class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""
    pass


class KpnGraphFromTgff:
    """New, since we want to return a common.kpn instance instead of am TgffToKpnGraph instance
    """
    def __new__(cls, tgff_file, name):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update( {tgff_file : Parser().parse_file(tgff_file)} )
        
        tgff_graphs = _parsed_tgff_files[tgff_file][0]
        
        if name not in tgff_graphs:
            raise TgffReferenceError()
        
        return tgff_graphs[name].to_kpn_graph()


class TraceGeneratorWrapper:
    def __new__(cls, tgff_file, graph_name, repetition=1):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update( {tgff_file : Parser().parse_file(tgff_file)} )
        
        tgff_components = _parsed_tgff_files[tgff_file]
        processor_dict = {}

        for processor in tgff_components[1]:
            processor_dict.update({processor.type : processor})

        trace_generator = TgffTraceGenerator(processor_dict, tgff_components[0][graph_name], repetition)
        
        return trace_generator
    

class PlatformFromTgff:
    def __new__(cls, platform_type, processor_1, processor_2, processor_3, processor_4, tgff_file):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update( {tgff_file : Parser().parse_file(tgff_file)} )
        
        tgff_processors = _parsed_tgff_files[tgff_file][1]

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
        processor1 = processor_1.to_pykpn_processor()
        if processor1.frequency_domain.frequency != 1400000000.0:
            log.warning(f"Rescaling processor {processor_1.name} to fit Odroid frequency")
            fd_a7 = FrequencyDomain('fd_a7', 1400000000.0)
            processor1.frequency_domain = fd_a7

        processor2 = processor_2.to_pykpn_processor()
        designer = PlatformDesigner(self)
        if processor2.frequency_domain.frequency != 2000000000.0:
            log.warning(f"Rescaling processor {processor_2.name} to fit Odroid frequency")
            fd_a15 = FrequencyDomain('fd_a15', 2000000000.0)
            processor2.frequency_domain = fd_a15

        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("exynos5422")

        # cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_a7",
                                          processor1,
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
                                          processor2,
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

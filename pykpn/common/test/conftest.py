# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
from pykpn.tgff.tgffSimulation import KpnGraphFromTgff, TraceGeneratorWrapper, PlatformFromTgff
from pykpn.mapper.gbm_fullmapper import DerivedPrimitive

tgff_file = 'pykpn/tgff/graphs/auto-indust-cords.tgff'
tgff_graph = 'TASK_GRAPH_1'
processor0 = 'processor_0'
processor1 = 'processor_1'
processor2 = 'processor_2'
processor3 = 'processor_3'
kpn_graph = KpnGraphFromTgff(tgff_file, tgff_graph)
platform_object = PlatformFromTgff('multi_cluster', processor0, processor1, processor2, processor3, tgff_file)

@pytest.fixture
def kpn():
    return kpn_graph

@pytest.fixture
def trace_generator():
    return TraceGeneratorWrapper(tgff_file)

@pytest.fixture
def process_mapping():
    process_mapping = {}

    for process in kpn_graph.processes():
        process_mapping.update({process.name : ['processor_0', 'processor_1']})

    return process_mapping


@pytest.fixture
def channel_mapping():
    chan_mapping = {}

    for channel in kpn_graph.channels():
        chan_mapping.update({channel.name : [1000, 2000]})

    return chan_mapping

@pytest.fixture
def processor_groups():
    return {'processor_0' : list(filter(lambda x : x.type == 'processor_0', list(platform_object.processors()))),
            'processor_1' : list(filter(lambda x : x.type == 'processor_1', list(platform_object.processors())))}

@pytest.fixture
def primitive_groups():
    """ It is not easily possible to get the primitive groups how they are constructed in gbm without instantiating
    the mapper. Therefore we use made up ones.
    """
    l2 = platform_object.find_primitive('prim_multi_cluster_cl0_l2_1')
    ram = platform_object.find_primitive('prim_multi_cluster_RAM_1')

    processor_0 = platform_object.find_processor('processor_0')
    processor_1 = platform_object.find_processor('processor_1')
    processor_2 = platform_object.find_processor('processor_2')

    prim_groups = { 1000 : [DerivedPrimitive(processor_0, processor_1, l2)],
                    2000 : [DerivedPrimitive(processor_0, processor_2, ram)]}
    return prim_groups

@pytest.fixture
def platform():
    return platform_object

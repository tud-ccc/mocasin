# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.platform import SlxPlatform
from pykpn.common.trace import TraceGraph
from pykpn.mapper.utils import DerivedPrimitive
from pykpn.tgff.tgffSimulation import KpnGraphFromTgff
from pykpn.platforms.multi_cluster import DesignerPlatformMultiCluster
from pykpn.platforms.platformDesigner import genericProcessor

import networkx as nx

#========================================
#setup tgff test data

tgff_file = 'examples/tgff/e3s-0.9/auto-indust-cords.tgff'
tgff_graph = 'TASK_GRAPH_1'
processor0 = genericProcessor('proc_type_0')
processor1 = genericProcessor('proc_type_1')

kpn_tgff = KpnGraphFromTgff(tgff_file, tgff_graph)
platform_tgff = DesignerPlatformMultiCluster( processor0, processor1)

process_mapping_tgff = {}
for process in kpn_tgff.processes():
    process_mapping_tgff.update({process.name : ['proc_type_0', 'proc_type_1']})

channel_mapping_tgff = {}
for channel in kpn_tgff.channels():
    channel_mapping_tgff.update({channel.name : [1000, 2000]})

processor_groups_tgff = {'proc_type_0' : list(filter(
                            lambda x : x.type == 'proc_type_0', list(platform_tgff.processors()))),
                         'proc_type_1' : list(filter(
                            lambda x : x.type == 'proc_type_1', list(platform_tgff.processors())))}

l2 = platform_tgff.find_primitive('prim_multi_cluster_cl0_l2_1')
ram = platform_tgff.find_primitive('prim_multi_cluster_RAM_1')

processor_0 = platform_tgff.find_processor('processor_0')
processor_1 = platform_tgff.find_processor('processor_1')
processor_2 = platform_tgff.find_processor('processor_2')

prim_groups_tgff = { 1000 : [DerivedPrimitive(processor_0, processor_1, l2)],
                     2000 : [DerivedPrimitive(processor_0, processor_2, ram)]}

#========================================

def test_trace_graph_tgff(trace_generator_tgff):
    trace_graph = TraceGraph(kpn_tgff,
                             trace_generator_tgff,
                             process_mapping_tgff,
                             channel_mapping_tgff,
                             processor_groups_tgff,
                             prim_groups_tgff)

    elements, _, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['idct', 'a1_2']
    assert nodes == ['V_s', 'idct_1', 'idct_2', 'idct_3', 'r_a1_2_0']

    try:
        nx.find_cycle(trace_graph, 'V_s')
    except nx.exception.NetworkXNoCycle:
        assert True
        return

    assert False

def test_change_process_mapping_tgff(trace_generator_tgff):
    trace_graph = TraceGraph(kpn_tgff,
                             trace_generator_tgff,
                             process_mapping_tgff,
                             channel_mapping_tgff,
                             processor_groups_tgff,
                             prim_groups_tgff)

    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('src', {'src' : ['proc_type_0']}, processor_groups_tgff, definitive=True)
    elements, time, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['idct', 'a1_2']
    assert time == 1000004550000
    assert nodes == ['V_s', 'idct_1', 'idct_2', 'idct_3', 'r_a1_2_0']

def test_change_channel_mapping_tgff_1(trace_generator_tgff):
    trace_graph = TraceGraph(kpn_tgff,
                             trace_generator_tgff,
                             process_mapping_tgff,
                             channel_mapping_tgff,
                             processor_groups_tgff,
                             prim_groups_tgff)

    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('a1_0', {'a1_0' : [1000]}, prim_groups_tgff, definitive=True)

    elements, time, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['idct', 'a1_2']
    assert time == 1000004550000
    assert nodes == ['V_s', 'idct_1', 'idct_2', 'idct_3', 'r_a1_2_0']

def test_change_channel_mapping_tgff_2(trace_generator_tgff):
    trace_graph = TraceGraph(kpn_tgff,
                             trace_generator_tgff,
                             process_mapping_tgff,
                             channel_mapping_tgff,
                             processor_groups_tgff,
                             prim_groups_tgff)

    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('a1_0', {'a1_0' : [1000]}, prim_groups_tgff, definitive=True)
    trace_graph.change_element_mapping('a1_2', {'a1_2' : [1000]}, prim_groups_tgff, definitive=True)

    elements, time, nodes = trace_graph.determine_critical_path_elements()

    assert elements == ['iir', 'a1_1']
    assert time == 1000000400000
    assert nodes == ['V_s', 'iir_1', 'iir_2', 'iir_3', 'r_a1_1_0']

#========================================
#setup test data for slx
kpn_slx = SlxKpnGraph('audio_filter', '../../../examples/slx/app/audio_filter/audio_filter.cpn.xml')
platform_slx = SlxPlatform('exynos', '../../../examples/slx/platforms/exynos.platform')

process_mapping_slx = {}
for process in kpn_slx.processes():
    process_mapping_slx.update({process.name : ['ARM_CORTEX_A7', 'ARM_CORTEX_A15']})

channel_mapping_slx = {}
for channel in kpn_slx.channels():
    channel_mapping_slx.update({channel.name : [1500, 20000]})

processor_groups_slx = {'ARM_CORTEX_A7' : list(filter(
                            lambda x : x.type == 'ARM_CORTEX_A7', list(platform_slx.processors()))),
                        'ARM_CORTEX_A15' : list(filter(
                            lambda x : x.type == 'ARM_CORTEX_A15', list(platform_slx.processors())))}

dram = platform_slx.find_primitive('comm_DRAM')
l2_a7 = platform_slx.find_primitive('comm_L2_A7')

arm_0 = platform_slx.find_processor('ARM00')
arm_1 = platform_slx.find_processor('ARM01')
arm_7 = platform_slx.find_processor('ARM07')

prim_groups_slx = {}
prim_groups_slx = { 1500 : [DerivedPrimitive(arm_0, arm_1, l2_a7)],
                    20000 : [DerivedPrimitive(arm_0, arm_7, dram)]}

#========================================

def test_trace_graph_slx(trace_generator_slx):
    trace_graph = TraceGraph(kpn_slx,
                             trace_generator_slx,
                             process_mapping_slx,
                             channel_mapping_slx,
                             processor_groups_slx,
                             prim_groups_slx)

    elements, _, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['fft_r', 'src_right', 'src', 'src_left']
    assert nodes == ['V_s', 'fft_r_1', 'fft_r_2', 'fft_r_3', 'fft_r_4', 'fft_r_5', 'fft_r_6', 'fft_r_7', 'fft_r_8',
                     'fft_r_9', 'fft_r_10', 'fft_r_11', 'fft_r_12', 'fft_r_13', 'fft_r_14', 'fft_r_15', 'fft_r_16',
                     'fft_r_17', 'fft_r_18', 'fft_r_19', 'fft_r_20', 'fft_r_21', 'fft_r_22', 'r_src_right_10', 'src_24',
                     'r_src_left_10', 'src_25']

    try:
        nx.find_cycle(trace_graph, 'V_s')
    except nx.exception.NetworkXNoCycle:
        assert True
        return

    assert False

def test_change_process_mapping_slx(trace_generator_slx):
    trace_graph = TraceGraph(kpn_slx,
                             trace_generator_slx,
                             process_mapping_slx,
                             channel_mapping_slx,
                             processor_groups_slx,
                             prim_groups_slx)

    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('fft_r', {'fft_r' : ['ARM_CORTEX_A15']}, processor_groups_slx, definitive=True)
    elements, time, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['fft_l', 'src_left', 'src']
    assert time == 31960989283
    assert nodes == ['V_s', 'fft_l_1', 'fft_l_2', 'fft_l_3', 'fft_l_4', 'fft_l_5', 'fft_l_6', 'fft_l_7', 'fft_l_8',
                     'fft_l_9', 'fft_l_10', 'fft_l_11', 'fft_l_12', 'fft_l_13', 'fft_l_14', 'fft_l_15', 'fft_l_16',
                     'fft_l_17', 'fft_l_18', 'fft_l_19', 'fft_l_20', 'fft_l_21', 'fft_l_22', 'r_src_left_10', 'src_25']

def test_change_channel_mapping_slx_1(trace_generator_slx):
    trace_graph = TraceGraph(kpn_slx,
                             trace_generator_slx,
                             process_mapping_slx,
                             channel_mapping_slx,
                             processor_groups_slx,
                             prim_groups_slx)

    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('src_left', {'src_left' : [1500]}, prim_groups_slx, definitive=True)

    elements, time, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['fft_r', 'src_right', 'src', 'src_left']
    assert time == 31961346425
    assert nodes == ['V_s', 'fft_r_1', 'fft_r_2', 'fft_r_3', 'fft_r_4', 'fft_r_5', 'fft_r_6', 'fft_r_7', 'fft_r_8',
                     'fft_r_9', 'fft_r_10', 'fft_r_11', 'fft_r_12', 'fft_r_13', 'fft_r_14', 'fft_r_15', 'fft_r_16',
                     'fft_r_17', 'fft_r_18', 'fft_r_19', 'fft_r_20', 'fft_r_21', 'fft_r_22', 'r_src_right_10', 'src_24',
                     'r_src_left_10', 'src_25']

def test_change_channel_mapping_slx_2(trace_generator_slx):
    trace_graph = TraceGraph(kpn_slx,
                             trace_generator_slx,
                             process_mapping_slx,
                             channel_mapping_slx,
                             processor_groups_slx,
                             prim_groups_slx)

    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('src_left', {'src_left' : [1500]}, prim_groups_slx, definitive=True)
    trace_graph.change_element_mapping('src_right', {'src_right' : [1500]}, prim_groups_slx, definitive=True)

    elements, time, nodes = trace_graph.determine_critical_path_elements()

    assert elements == ['fft_r', 'src_right', 'src', 'src_left']
    assert time == 31961096424
    assert nodes == ['V_s', 'fft_r_1', 'fft_r_2', 'fft_r_3', 'fft_r_4', 'fft_r_5', 'fft_r_6', 'fft_r_7', 'fft_r_8',
                     'fft_r_9', 'fft_r_10', 'fft_r_11', 'fft_r_12', 'fft_r_13', 'fft_r_14', 'fft_r_15', 'fft_r_16',
                     'fft_r_17', 'fft_r_18', 'fft_r_19', 'fft_r_20', 'fft_r_21', 'fft_r_22', 'r_src_right_10', 'src_24',
                     'r_src_left_10', 'src_25']

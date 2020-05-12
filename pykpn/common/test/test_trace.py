# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.trace import TraceGraph
import networkx as nx

def test_trace_graph(kpn, trace_generator, process_mapping, channel_mapping, processor_groups, primitive_groups):
    trace_graph = TraceGraph(kpn,
                             trace_generator,
                             process_mapping,
                             channel_mapping,
                             processor_groups,
                             primitive_groups)

    elements, _, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['src', 'a1_0']
    assert nodes == ['V_s', 'src_1', 'src_2', 'r_a1_0_0']

    try:
        nx.find_cycle(trace_graph, 'V_s')
    except nx.exception.NetworkXNoCycle:
        assert True
        return

    assert False

def test_change_process_mapping_1(kpn, trace_generator, process_mapping, channel_mapping, processor_groups,
                                  primitive_groups):
    trace_graph = TraceGraph(kpn,
                             trace_generator,
                             process_mapping,
                             channel_mapping,
                             processor_groups,
                             primitive_groups)
    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('src', {'src' : ['processor_0']}, processor_groups, definitive=True)
    elements, time, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['src', 'a1_0']
    assert time == 1000000100000
    assert nodes == ['V_s', 'src_1', 'src_2', 'r_a1_0_0']

def test_change_channel_mapping_1(kpn, trace_generator, process_mapping, channel_mapping, processor_groups,
                                  primitive_groups):
    trace_graph = TraceGraph(kpn,
                             trace_generator,
                             process_mapping,
                             channel_mapping,
                             processor_groups,
                             primitive_groups)
    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('a1_0', {'a1_0' : [1000]}, primitive_groups, definitive=True)

    elements, time, nodes = trace_graph.determine_critical_path_elements()
    assert elements == ['sink', 'a1_2']
    assert time == 1000000000000
    assert nodes == ['V_s', 'sink_1', 'r_a1_2_0']

def test_change_channel_mapping_2(kpn, trace_generator, process_mapping, channel_mapping, processor_groups,
                                  primitive_groups):
    trace_graph = TraceGraph(kpn,
                             trace_generator,
                             process_mapping,
                             channel_mapping,
                             processor_groups,
                             primitive_groups)
    trace_graph.determine_critical_path_elements()

    trace_graph.change_element_mapping('a1_0', {'a1_0' : [1000]}, primitive_groups, definitive=True)
    trace_graph.change_element_mapping('a1_2', {'a1_2' : [1000]}, primitive_groups, definitive=True)

    elements, time, nodes = trace_graph.determine_critical_path_elements()

    assert elements == ['sink', 'a1_2']
    assert time == 1000000000000
    assert nodes == ['V_s', 'sink_1', 'r_a1_2_0']

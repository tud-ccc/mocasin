# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.kpn import KpnGraph
from pykpn.common.platform import Processor, CommunicationResource
from pykpn.tgff.tgffParser.dataStructures import TgffProcessor, TgffGraph, TgffLink

def test_graph_dict(graph_dict):
    assert(len(graph_dict) == 4)
    
    """Test common methods for all graphs
    """
    for tgff_graph in graph_dict.values():
        assert(isinstance(tgff_graph, TgffGraph))
        kpn_graph = tgff_graph.to_kpn_graph()
        assert(isinstance(kpn_graph, KpnGraph))
        
    """Test some specific properties for some selected graphs
    """
    tgff_graph = graph_dict['TASK_GRAPH_0']
    assert(len(tgff_graph.tasks) == 6)
    assert(len(tgff_graph.channels) == 5)
    execution_order = tgff_graph.get_execution_order('src')
    assert(len(execution_order) == 2)
    #Todo: get the right execution time
    assert(execution_order == [('e', 45), ('w', 'TASK_GRAPH_0.a0_0')])
    
    tgff_graph = graph_dict['TASK_GRAPH_3']
    assert(len(tgff_graph.tasks) == 5)
    assert(len(tgff_graph.channels) == 4)
    execution_order = tgff_graph.get_execution_order('cache')
    assert(len(execution_order) == 3)
    #Todo: get the right execution time
    assert(execution_order == [('r', 'TASK_GRAPH_3.a3_1'),('e', 3), ('w', 'TASK_GRAPH_3.a3_2')])
    
def test_processor_dict(processor_list):
    assert(len(processor_list) == 34)
    
    """Test common methods for all processors
    """
    for tgff_processor in processor_list:
        assert(isinstance(tgff_processor, TgffProcessor))
        pykpn_processor = tgff_processor.to_pykpn_processor()
        assert(isinstance(pykpn_processor, Processor))
        assert(len(tgff_processor.operations) == 46)
        
    """Test some specific properties for selected processors
    """
    tgff_processor = processor_list[0]
    assert(tgff_processor.name == 'CLIENT_PE_0')
    assert(tgff_processor.type == 'processor_0')
    #Todo: Get right cycle time
    assert(tgff_processor.cycle_time == float('1e-06'))
    #Todo: Get correct execution cycles
    assert(tgff_processor.operations[0] == 45)
    
    tgff_processor = processor_list[32]
    assert(tgff_processor.name == 'SERVER_PE_15')
    assert(tgff_processor.type == 'processor_32')
    #Todo: Get right cycle time
    assert(tgff_processor.cycle_time == float('1e-07'))
    #Todo: Get correct execution cycles
    assert(tgff_processor.operations[0] == 0)

def test_link_dict(link_dict):
    assert(len(link_dict) == 6)
    
    for link in link_dict.values():
        assert(isinstance(link, TgffLink))
        comm_resource = link.to_pykpn_communication_resource()
        assert(isinstance(comm_resource, CommunicationResource))

def test_communication_quantitites(communication_quantities):
    assert(len(communication_quantities) == 1)
    assert(communication_quantities[0][0] == float('2E6'))
    assert(communication_quantities[0][1] == float('6E6'))
    assert(communication_quantities[0][2] == float('1E6'))


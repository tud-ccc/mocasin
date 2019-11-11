# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from tgffParser.parser import Parser
from tgffGenerators import TgffTraceGenerator

'''A simple example script to demonstrate the use of the 
tgff parser and the corresponding generators.
'''
def main():
    '''Instantiate a parser object
    '''
    tgff_parser = Parser()
    
    '''Parse a specified file. Result is a list containing following items in specified order:
    [0] tgff graph dict
    [1] tgff communication quantities
    [2] processor dict
    [3] link dict
    '''
    tgff_components = tgff_parser.parse_file('graphs/auto-indust-cords.tgff')
    
    '''Transfer tgff graphs into kpn graphs
    '''
    kpnGraphes = []
    for tgffGraph in tgff_components[0].values():
        kpnGraphes.append(tgffGraph.to_kpn_graph())
    
    '''Transfer tgff processors into kpn processors
    '''
    kpnProcessors = []
    for processor in tgff_components[2].values():
        kpnProcessors.append(processor.to_pykpn_processor())
        
    '''Create a traceGenerator based on the tgff components
    '''
    generators =[]
    for tgff_graph in tgff_components[0].values():
        generators.append(TgffTraceGenerator(tgff_components[2], tgff_graph, repetition=2))
    
    segments = []
    for i in range(0,30):
        segment = generators[0].next_segment('src','PROC_0')
        segments.append(segment)
        
    '''Transfer tgff links into pykpn communication ressources
    WARNING: communication ressources are not complete due to a lack of information in
    the tgff representation
    '''
    comm_resources = []
    for link in tgff_components[3].values():
        comm_resources.append(link.to_pykpn_communication_resource())
        
    print('Finished sample')
        
    

if __name__ == '__main__':
    main()
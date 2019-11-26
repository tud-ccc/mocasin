# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import simpy
from pykpn.tgff.tgffParser.parser import Parser
from pykpn.tgff.tgffSimulation import TgffRuntimeSystem
from pykpn.tgff.tgffGenerators import TgffTraceGenerator

'''A simple example script to demonstrate the use of the 
tgff parser and the corresponding generators.
'''
def main():
    '''Instantiate a parser object
    '''
    tgff_parser = Parser()
    
    '''Parse a specified file. Result is a list containing following items in specified order:
    [0] tgff graph dict
    [1] processor dict
    [2] link dict
    [3] tgff communication quantities
    '''
    tgff_components = tgff_parser.parse_file('pykpn/tgff/graphs/auto-indust-cords.tgff')
    
    '''Transfer tgff graphs into kpn graphs
    '''
    kpnGraphes = []
    for tgffGraph in tgff_components[0].values():
        kpnGraphes.append(tgffGraph.to_kpn_graph())
    
    '''Transfer tgff processors into kpn processors
    '''
    pykpnProcessors = []
    for processor in tgff_components[1].values():
        pykpnProcessors.append(processor.to_pykpn_processor())
        
    '''Create a traceGenerator based on the tgff components
    '''
    generator = TgffTraceGenerator(tgff_components[1], tgff_components[0], repetition=2)
     
    '''Transfer tgff links into pykpn communication ressources
    WARNING: communication ressources are not complete due to a lack of information in
    the tgff representation
    '''
    comm_resources = []
    for link in tgff_components[2].values():
        comm_resources.append(link.to_pykpn_communication_resource())
    
    '''Simulating the execution of the parsed tgff graphs on the specified processor,
    PROC_0 in the example
    '''
    env = simpy.Environment()
    system = TgffRuntimeSystem(tgff_components[1]['PROC_0'], tgff_components[0], env, topology='mesh')
    system.simulate()
    print('Finished sample')
        
    

if __name__ == '__main__':
    main()
    
    
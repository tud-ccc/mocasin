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
    tgffParser = Parser()
    
    '''Parse a specified file. Result is a list containing following items in specified order:
    [0] tgff graph dict
    [1] tgff communication quantities
    [2] processor dict
    '''
    tgffComponents = tgffParser.parseFile('graphs/auto-indust-cords.tgff')
    
    '''Transfer tgff graphs into kpn graphs
    '''
    kpnGraphes = []
    for tgffGraph in tgffComponents[0].values():
        kpnGraphes.append(tgffGraph.toPykpnGraph())
    
    '''Transfer tgff processors into kpn processors
    '''
    kpnProcessors = []
    for processor in tgffComponents[2].values():
        kpnProcessors.append(processor.toPykpnProcessor())
        
    '''Create a traceGenerator based on the tgff components
    '''
    generators =[]
    for tgffGraph in tgffComponents[0].values():
        generators.append(TgffTraceGenerator(tgffComponents[2], tgffGraph, repetition=2))
    
    segments = []
    for i in range(0,30):
        segment = generators[0].next_segment('src','PROC_0')
        segments.append(segment)
    
    print('Stop')

if __name__ == '__main__':
    main()
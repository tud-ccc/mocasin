# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from tgffParser.parser import Parser

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
    tgffComponents = tgffParser.parseFile('graphs/auto-indust-cowls.tgff')
    for tgffGraph in tgffComponents[0].values():
        tgffGraph.getExecutionOrder()
    
    
    '''Transfer tgff graphs into kpn graphs
    '''
    kpnGraphes = []
    for tgffGraph in tgffComponents[0].values():
        kpnGraphes.append(tgffGraph.toPykpnGraph())
    
    '''Obtain pykpn processor objects from the intermediate representation of tgff processors
    '''
    kpnProcessors = []
    for processor in tgffComponents[2].values():
        kpnProcessors.append(processor.toPykpnProcessor())
        
    print('Stop')

if __name__ == '__main__':
    main()
# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import re
from pyxb.utils.six import file

class Parser():
    def __init__(self):
        self.quantityDict = {}
        self.linkDict = {}
        
        self.regexDict = { 'comment' : re.compile(r'#.*'),
                       'task' : re.compile(r'TASK (?P<name>([ab-z]|[0-9])+) TYPE (?P<type>\d+)\n'),
                       'channel' : re.compile(r'ARC (?P<name>([AB-Z]|[ab-z]|[0-9]|\_)+) FROM (?P<source>([ab-z]|[0-9])+) TO (?P<destination>([ab-z]|[0-9])+) TYPE (?P<type>\d+)'),
                       'task_graph' : re.compile(r'@TASK_GRAPH (?P<identifier>\d+) {'),
                       'scope_limiter' : re.compile(r'}'),
                       'commun_quant' : re.compile(r'@COMMUN_QUANT (?P<identifier>\d+) {'),
                       'commun_value' : re.compile(r'(?P<identifier>\d+) (?P<value>\d+)E(?P<exponent>\d+)'),
                       'link' : re.compile(r'@LINK (?P<identifier>\d+) {'),
                       'link_type' : re.compile(r'  (?P<identifier>\d+)    (\d+)    (?P<size>\d+).*')}
        
    
    def parseFile(self, filePath):
        with open(filePath, 'r') as file:
            currentLine  = file.readline()
            
            while currentLine:
                key, match = self._parseLine(currentLine)
                
                if key == 'comment':
                    print('Ignored comment')
                elif key == 'task_graph':
                    pass
                elif key == 'communication_quant':
                    pass
                elif key == 'link':
                    pass      
                else:
                    print('Parse error on position: ' + str(file.tell()))
                
                currentLine = file.readline()
    
    def _parseTaskGraph(self, file):
        pass
    
    def _parseCommunQuant(self, file):
        pass
    
    def _parseLink(self, file):
        pass
    
    def _parseLine(self, line):
        for key, rx in self.regexDict.items():
            match = rx.search(line)
            if match:
                return key, match
        
        return None, None
    
def main():
    mParser = Parser()
    mParser.parseFile('test.txt')

if __name__ == "__main__":
    main()
    
    
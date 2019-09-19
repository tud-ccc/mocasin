# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import regEx as expr

class Parser():
    def __init__(self, debug=False):
        self._debug = debug
        
        self.quantityDict = {}
        self.linkDict = {}
        self.taskGraphDict = {}
        
        self.regexDict = { 'comment' : expr.comment(),
                          'task_graph' : expr.task_graph(),
                          'task' : expr.task(),
                          'channel' : expr.channel(),
                          'commun_quant' : expr.commun_quant(),
                          'commun_value' : expr.commun_value(),
                          'link' : expr.link(),
                          'link_type' : expr.link_type(),
                          'scope_limiter' : expr.scope_limiter(),
                          'new_line' : expr.new_line()}
        
    
    def parseFile(self, filePath):
        with open(filePath, 'r') as file:
            currentLine  = file.readline()
            while currentLine:
                key, match = self._parseLine(currentLine)
                
                if key == 'comment':
                    if self._debug:
                        print('Ignored comment')
                elif key == 'task_graph':
                    if self._debug:
                        print('Parsing task graph')
                    self._parseTaskGraph(file, match)
                elif key == 'commun_quant':
                    if self._debug:
                        print('Parsing communication quant')
                    self._parseCommunQuant(file, match)
                elif key == 'link':
                    if self._debug:
                        print('Parsing link')
                    self._parseLink(file, match)
                elif key == 'new_line' or key == 'comment':
                    if self._debug:
                        print('Skip empty or comment line')
                else:
                    if self._debug:
                        print('No valid regex for position: ' + str(file.tell()))
                    else:
                        print('Parse error on position: ' + str(file.tell()))
                
                currentLine = file.readline()
    
    def _parseTaskGraph(self, file, match):
        identifier = int(match.group('identifier'))
        tasks = {}
        channels = {}
        taskIndexExtension = 0
        channelIndexExtension = 0
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine)
            
            if key == 'task':
                if self._debug:
                    print('Added task: ' + match.group('name') + ' ' + match.group('type'))
                if not match.group('name') in tasks:
                    tasks.update( {match.group('name') : match.group('type')} )
                else:
                    tasks.update( {match.group('name') + '_' + str(taskIndexExtension) : match.group('type')} )
                    taskIndexExtension += 1
            elif key == 'channel':
                if self._debug:
                    print('Added channel: ' + match.group('name') + ' ' + match.group('type'))
                if not match.group('name') in channels:
                    channels.update( {match.group('name') : [match.group('source'), match.group('destination'), match.group('type')]} ) 
                else:
                    channels.update( {match.group('name') + '_' + str(channelIndexExtension): [match.group('source'), match.group('destination'), match.group('type')]} )
                    channelIndexExtension += 1
            elif key == 'scope_limiter':
                if self._debug:
                    print('Reached end of task graph')
                break
            elif key == 'new_line' or key == 'comment':
                if self._debug:
                    print('Skip empty or comment line')
            else:
                if self._debug:
                    print('No valid regex for position: ' + str(file.tell()))
                else:
                    print ('Parse error on position: ' + str(file.tell()))
            
            currentLine = file.readline()
        
        if self._debug:
            print('Added to graph dict: ' + str(identifier))
        self.taskGraphDict.update( {identifier : [tasks, channels]} )
    
    def _parseCommunQuant(self, file, match):
        identifier = match.group('identifier')
        communValues = {}
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine)
            
            if key == 'commun_value':
                if self._debug:
                    print('Added commun_value ' + match.group('identifier') + ' ' + match.group('value'))
                #TODO: resolve somehow this exponential expression
                communValues.update( {match.group('identifier') : [match.group('value'), match.group('exponent')]} )
            elif key == 'scope_limiter':
                if self._debug:
                    print('Reached end of commun_quant')
                break
            elif key == 'new_line' or key == 'comment':
                if self._debug:
                    print('Skip empty or comment line')
            else:
                if self._debug:
                    print('No valid regex for position: ' + str(file.tell()))
                else:
                    print('Parse error on position: ' + str(file.tell()))
            
            currentLine = file.readline()
        if self._debug:
            print('Added to commun_quant dict: ' + identifier)
        self.quantityDict.update( {identifier : communValues} )
        
    def _parseLink(self, file, match):
        identifier = match.group('identifier')
        linkTypes = {}
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine)
            
            if key == 'link_type':
                if self._debug:
                    print('Added link type: ' + match.group('identifier') + ' ' + match.group('size'))
                linkTypes.update( {match.group('identifier') : match.group('size')} )
            elif key == 'scope_limiter':
                if self._debug:
                    print('Reached end of link')
                break
            elif key == 'new_line' or key == 'comment':
                if self._debug:
                    print('Skip empty or comment line')
            else:
                if self._debug:
                    print('No valid regex for position: ' + str(file.tell()))
                else:
                    print('Parse error on position: ' + str(file.tell()))
            
            currentLine = file.readline()
        
        if self._debug:
            print('Added to link dict: ' + str(identifier))
        self.linkDict.update( {identifier : linkTypes} )
    
    def _parseLine(self, line):
        for key, rx in self.regexDict.items():
            match = rx.fullmatch(line)
            if match:
                return key, match
        
        return None, None
    
def main():
    mParser = Parser(debug=True)
    mParser.parseFile('reduced.tgff')
    print('Finished parsing')

if __name__ == "__main__":
    main()
    
    
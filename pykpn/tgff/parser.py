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
        self.processorDict= {}
        
        self.regexDict = { 'comment' : expr.comment(),
                          'task_graph' : expr.task_graph(),
                          'period' : expr.period(),
                          'task' : expr.task(),
                          'channel' : expr.channel(),
                          'hard_deadline' : expr.hard_deadline(),
                          'soft_deadline' : expr.soft_deadline(),
                          'commun_quant' : expr.commun_quant(),
                          'commun_value' : expr.commun_value(),
                          'link' : expr.link(),
                          'link_type' : expr.link_type(),
                          'scope_limiter' : expr.scope_limiter(),
                          'new_line' : expr.new_line(),
                          'processor' : expr.processor(),
                          'properties' : expr.properties(),
                          'hyperperiod' : expr.hyperperiod(),
                          'memory' : expr.memory(),
                          'operation' : expr.operation()}
        
    
    def parseFile(self, filePath):
        with open(filePath, 'r') as file:
            currentLine  = file.readline()
            while currentLine:
                key, match = self._parseLine(currentLine)
                
                if key == 'task_graph':
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
                elif key == 'processor':
                    if self._debug:
                        print('Parse processor')
                    self._parseProcessor(file, match)
                else:
                    self._keyMissmatch(key, file.tell())
                
                currentLine = file.readline()
        
        print(ioColors.SUCCESS + 'Finished parsing' + ioColors.ENDC)
    
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
            else:
                self._keyMissmatch(key, file.tell())
            
            currentLine = file.readline()
        
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
            else:
                self._keyMissmatch(key, file.tell())
            
            currentLine = file.readline()
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
                    print('Added link type: ' + match.group('use_price') + ' ' + match.group('packet_size'))
                linkTypes.update( {match.group('use_price') : match.group('packet_size')} )
            elif key == 'scope_limiter':
                if self._debug:
                    print('Reached end of link')
                break
            else:
                self._keyMissmatch(key, file.tell())
            
            currentLine = file.readline()
        
        print('Added to link dict: ' + str(identifier))
        self.linkDict.update( {identifier : linkTypes} )
        
    def _parseProcessor(self, file, match):
        identifier = match.group('name') + '_' + match.group('identifier')
        properties = []
        operations = {}
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine)
            
            if key == 'properties':
                if self._debug:
                    print('Parsed processor properties')
                properties.append(match.group('price'))
                properties.append(match.group('buffered'))
                properties.append(match.group('preempt_power'))
                properties.append(match.group('commun_energ_bit'))
                properties.append(match.group('io_energ_bit'))
                properties.append(match.group('idle_power'))
            elif key == 'operation':
                if self._debug:
                    print('Parsed processor operation')
                tmpList = list()
                tmpList.append(match.group('version'))
                tmpList.append(match.group('valid'))
                tmpList.append(match.group('task_time'))
                tmpList.append(match.group('preempt_time'))
                tmpList.append(match.group('code_bits'))
                tmpList.append(match.group('task_power'))
                operations.update( { int(match.group('type')) : tmpList} )
            elif key == 'scope_limiter':
                if self._debug:
                    print('Reached end of processor')
                break
            else:
                self._keyMissmatch(key, file.tell())
                
            currentLine = file.readline()
            
        print('Added to processor dict: ' + str(identifier))
        self.processorDict.update( {identifier : (properties, operations)} )
    
    def _parseLine(self, line):
        for key, rx in self.regexDict.items():
            match = rx.fullmatch(line)
            if match:
                return key, match
        
        return None, None
    
    def _keyMissmatch(self, key, position):
        if key == 'new_line' or key == 'comment':
            if self._debug:
                print('Skip empty or comment line')
        elif not key == None:
            print(ioColors.WARNING + 'Parsed unhandled group: <' + key + '> at position: ' + str(position) + ioColors.ENDC)
        else:
            if self._debug:
                print(ioColors.WARNING + 'No valid regex for position: ' + str(position) + ioColors.ENDC)
            else:
                print(ioColors.FAIL + 'Parse error on position: ' + str(position) + ioColors.ENDC)
    
class ioColors():
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    SUCCESS = '\033[92m'
    ENDC = '\033[0m'
    
def main():
    mParser = Parser(debug=False)
    mParser.parseFile('graphs/auto-indust-cowls.tgff')

if __name__ == "__main__":
    main()
    
    
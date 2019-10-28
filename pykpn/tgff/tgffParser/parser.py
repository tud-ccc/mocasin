# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from tgffParser import regEx as expr
import argparse

from tgffParser.logger import Logger
from tgffParser.dataStructures import TgffProcessor, TgffGraph
from pykpn.common.kpn import KpnProcess, KpnGraph, KpnChannel

class Parser():
    def __init__(self, debug=False, silent=False):
        self._debug = debug
        self.logger = Logger(debug, silent)
        
        self.quantityDict = {}
        self.stdLinkDict = {}
        self.primLinkDict = {}
        self.taskGraphDict = {}
        self.processorDict= {}
        
        self.commonComponents = { 
            'comment' : expr.comment(),
            'new_line' : expr.new_line(),
            'scope_limiter' : expr.scope_limiter(),
            }
        
        self.dataComponents = {
            'task_graph' : expr.task_graph(),
            'commun_quant' : expr.commun_quant(),
            'hw_component' : expr.hw_component(),
            'hyperperiod' : expr.hyperperiod(),
            }
        
        self.taskGraphComponents = {
            'period' : expr.period(),
            'task' : expr.task(),
            'channel' : expr.channel(),
            'hard_deadline' : expr.hard_deadline(),
            'soft_deadline' : expr.soft_deadline(),
            }
        
        self.hwComponents = {
            'properties' : expr.properties(),
            'operation' : expr.operation(),
            'std_link_value' : expr.std_link_value(),
            'prim_link_value': expr.prim_link_value()
            }
        
        self.communQuantComponents = {
            'commun_value' : expr.commun_value(),
            }
        
        self.unusedComponents = {
            'unused_statement' : expr.unused_statement(),
            'unused_scope' : expr.unused_scope(),
            }

    
    def parseFile(self, filePath):
        with open(filePath, 'r') as file:
            currentLine  = file.readline()
            
            while currentLine:
                key, match = self._parseLine(currentLine, self.dataComponents)
                if key == 'task_graph':
                    self.logger.logDebug('Parsing task graph')
                    self._parseTaskGraph(file, match)
                elif key == 'commun_quant':
                    self.logger.logDebug('Parsing communication quant')
                    self._parseCommunQuant(file, match)
                elif key == 'hw_component':
                    self.logger.logDebug('Parse HW component')
                    self._parseHardwareComponent(file, match)
                elif key == 'unused_scope':
                    self.logger.logDebug('Parse unused group')
                    self._parse_unused_scope(file)
                else:
                    self._keyMissmatch(key, file.tell())
                currentLine = file.readline()
        
        self.logger.logSuccess('Finished parsing')
        return [self.taskGraphDict, self.quantityDict, self.processorDict]
    
    def _parseTaskGraph(self, file, match):
        identifier = int(match.group('identifier'))
        tasks = {}
        channels = {}
        taskIndexExtension = 0
        channelIndexExtension = 0
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine, self.taskGraphComponents)
            if key == 'task':
                self.logger.logDebug('Added task: ' + match.group('name') + ' ' + match.group('type'))
                if not match.group('name') in tasks:
                    tasks.update( {match.group('name') : match.group('type')} )
                else:
                    tasks.update( {match.group('name') + '_' + str(taskIndexExtension) : match.group('type')} )
                    taskIndexExtension += 1
            elif key == 'channel':
                self.logger.log('Added channel: ' + match.group('name') + ' ' + match.group('type'))
                if not match.group('name') in channels:
                    channels.update( {match.group('name') : [match.group('source'), match.group('destination'), match.group('type')]} ) 
                else:
                    channels.update( {match.group('name') + '_' + str(channelIndexExtension): [match.group('source'), match.group('destination'), match.group('type')]} )
                    channelIndexExtension += 1
            elif key == 'scope_limiter':
                self.logger.logDebug('Reached end of task graph')
                break
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
        
        self.logger.log('Added to graph dict: ' + str(identifier))
        self.taskGraphDict.update( {identifier : TgffGraph(identifier, tasks, channels, self.quantityDict)} )
    
    def _parseCommunQuant(self, file, match):
        identifier = match.group('identifier')
        communValues = {}
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine, self.communQuantComponents)
            if key == 'commun_value':
                self.logger.logDebug('Added commun_value ' + match.group('identifier') + ' ' + match.group('value'))
                communValues.update( {int(match.group('identifier')) : float(match.group('value'))} )
            elif key == 'scope_limiter':
                self.logger.logDebug('Reached end of commun_quant')
                break
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
        
        self.logger.log('Added to commun_quant dict: ' + identifier)
        self.quantityDict.update( {int(identifier) : communValues} )
    
    def _parseHardwareComponent(self, file, match):
        identifier = match.group('name') + '_' + match.group('identifier')
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine, self.hwComponents)
            if key == 'std_link_value':
                self._parseStdLink(identifier, file, match)
                return
            elif key == 'prim_link_value':
                self._parsePrimLink(identifier, file, match)
                return
            elif key == 'properties' or key == 'operation':
                self._parseProcessor(identifier, file, key, match)
                return
            elif key == 'scope_limiter':
                self.logger.logError('Reached end of scope. Unable to recognize HW component!')
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
        
    def _parseStdLink(self, identifier, file, match):
        self.logger.logDebug('Recognized component as standard link!')
        stdLinkValues = []
        self._addStdLinkValue(stdLinkValues, match)
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine, self.hwComponents)
            if key == 'std_link_value':
                self._addStdLinkValue(stdLinkValues, match)
            elif key == 'scope_limiter':
                self.logger.logDebug('Reached end of stdLink')
                break
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
            
        self.logger.log('Added to link dict: ' + str(identifier))
        self.stdLinkDict.update( {identifier : stdLinkValues } )
        
    def _addStdLinkValue(self, dataStruct, match):
        dataStruct.append(match.group('use_price'))
        dataStruct.append(match.group('contact_price'))
        dataStruct.append(match.group('packet_size'))
        dataStruct.append(match.group('bit_time'))
        dataStruct.append(match.group('power'))
        dataStruct.append(match.group('contacts'))
    
    def _parsePrimLink(self, identifier, file, match):
        self.logger.log("Recognized component as primitive link!")
        primLinkValues = []
        self._addPrimLinkValue(primLinkValues, match)
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine, self.hwComponents)
            if key == 'prim_link_value':
                self._addPrimLinkValue(primLinkValues, match)
            elif key == 'scope_limiter':
                self.logger.logDebug("Reached end of primLink")
                break
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
            
        self.logger.log('Added to link dict: ' + str(identifier))
        self.primLinkDict.update( {identifier : primLinkValues } )
    
    def _addPrimLinkValue(self, dataStruct, match):
        dataStruct.append(match.group('c_use_prc'))
        dataStruct.append(match.group('c_cont_prc'))
        dataStruct.append(match.group('s_use_prc'))
        dataStruct.append(match.group('s_cont_prc'))
        dataStruct.append(match.group('packet_size'))
        dataStruct.append(match.group('bit_time'))
        dataStruct.append(match.group('power'))
        
    def _parseProcessor(self, identifier, file, key, match):
        self.logger.logDebug("Recognized component as processing element")
        properties = []
        operations = {}
        
        if key == 'properties':
            self._addProperties(properties, match)
        elif key == 'operation':
            self._addOperation(operations, match)
        
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine, self.hwComponents)
            if key == 'properties':
                self._addProperties(properties, match)
            elif key == 'operation':
                self._addOperation(operations, match)
            elif key == 'scope_limiter':
                self.logger.logDebug('Reached end of processor')
                break
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
            
        self.logger.log('Added to processor dict: ' + str(identifier))
        self.processorDict.update( {identifier : TgffProcessor(identifier, operations)} )
    
    def _addProperties(self, properties, match):
        self.logger.logDebug('Parsed processor properties')
        properties.append(match.group('price'))
        properties.append(match.group('buffered'))
        properties.append(match.group('preempt_power'))
        properties.append(match.group('commun_energ_bit'))
        properties.append(match.group('io_energ_bit'))
        properties.append(match.group('idle_power'))
    
    def _addOperation(self, operations, match):
        self.logger.logDebug('Parsed processor operation')
        tmpList = list()
        tmpList.append(match.group('version'))
        tmpList.append(match.group('valid'))
        tmpList.append(float(match.group('task_time')))
        tmpList.append(float(match.group('preempt_time')))
        tmpList.append(match.group('code_bits'))
        tmpList.append(match.group('task_power'))
        operations.update( { int(match.group('type')) : tmpList} )
        
    def _parse_unused_scope(self, file):
        currentLine = file.readline()
        
        while currentLine:
            key, match = self._parseLine(currentLine)
            if key == 'unused_statement':
                self.logger.log("Ignored statement")
            elif key == 'scope_limiter':
                self.logger.log("Parsed block which will be ignored")
                break
            else:
                self._keyMissmatch(key, file.tell())
            currentLine = file.readline()
    
    def _parseLine(self, line, additionalComponents=None):
        for key, rx in self.commonComponents.items():
            match = rx.fullmatch(line)
            if match:
                return key, match
        
        if not additionalComponents == None:
            for key, rx in additionalComponents.items():
                match = rx.fullmatch(line)
                if match:
                    return key, match
            
        for key, rx in self.unusedComponents.items():
            match = rx.fullmatch(line)
            if match:
                return key, match
        
        return None, None
    
    def _keyMissmatch(self, key, position):
        if key == 'new_line' or key == 'comment':
            if self._debug:
                print('Skip empty or comment line')
        elif not key == None:
            self.logger.logWarning('Parsed unhandled group: <' + key + '> at position: ' + str(position))
        else:
            self.logger.logError('Parse error on position: ' + str(position))
                
def main():
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument('path',metavar='P', type=str)
    argumentParser.add_argument('--debug', metavar='D', const=True, nargs='?')
    args = argumentParser.parse_args()

    mParser = Parser(debug=args.debug)
    mParser.parseFile(args.path)
    
    
if __name__ == "__main__":
    main()
    
    
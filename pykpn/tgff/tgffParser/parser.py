# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import argparse
import os
from pykpn.util import logging
from pykpn.tgff.tgffParser import regEx as expr
from pykpn.tgff.tgffParser.dataStructures import TgffProcessor, TgffGraph, TgffLink

class Parser:
    """A parser for .tgff files. The information parsed from a file are 
    transfered into intermediate representations which can be found in 
    dataStructures.py
    
    The parser recognizes the patterns inside a .tgff file via regular 
    expressions. These can be found in regEx.py
    """
    def __init__(self, debug=False):
        self._debug = debug
        self.logger = logging.getLogger('tgff_parser')
        
        self.quantity_dict = {}
        self.std_link_dict = {}
        self.prim_link_dict = {}
        self.task_graph_dict = {}
        self.processor_list= []
        
        self.common_components = { 
            'comment' : expr.comment(),
            'new_line' : expr.new_line(),
            'scope_limiter' : expr.scope_limiter(),
            }
        
        self.data_components = {
            'task_graph' : expr.task_graph(),
            'commun_quant' : expr.commun_quant(),
            'hw_component' : expr.hw_component(),
            'hyperperiod' : expr.hyperperiod(),
            }
        
        self.task_graph_components = {
            'period' : expr.period(),
            'task' : expr.task(),
            'channel' : expr.channel(),
            'hard_deadline' : expr.hard_deadline(),
            'soft_deadline' : expr.soft_deadline(),
            }
        
        self.hw_components = {
            'properties' : expr.properties(),
            'operation' : expr.operation(),
            'std_link_value' : expr.std_link_value(),
            'prim_link_value': expr.prim_link_value()
            }
        
        self.commun_quant_components = {
            'commun_value' : expr.commun_value(),
            }
        
        self.unused_components = {
            'unused_statement' : expr.unused_statement(),
            'unused_scope' : expr.unused_scope(),
            }

    """Parses the specified file. Creates and returns the corresponding 
    intermediate tgff representations.
    
    :param file_path: the path to the file relative to the script location.
    :type file_path: string
    :returns: A list containing all types of intermediate representations in
    following order:
    [0]:    dictionary of all TgffGraphs
    [1]:    dictionary of identifiers mapped to possible channel sizes
    [2]:    dictionary of all TgffProcessors
    [3]:    dictionary of all Links
    
    :rtype: tuple(  dict{string : TgffGraph},
                    list[TgffProcessor],
                    dict{string : TgffLink},
                    dict{int : dict{int : float}})
    """
    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            last_mismatch = None
            current_line  = file.readline()
            
            while current_line:
                key, match = self._parse_line(current_line, self.data_components)
                if key == 'task_graph':
                    self.logger.debug('Parsing task graph')
                    self._parse_task_graph(file, match)
                elif key == 'commun_quant':
                    self.logger.debug('Parsing communication quant')
                    self._parse_commun_quant(file, match)
                elif key == 'hw_component':
                    self.logger.debug('Parse HW component')
                    self._parse_hw_component(file, match, last_mismatch)
                elif key == 'unused_scope':
                    self.logger.debug('Parse unused group')
                    self._parse_unused_scope(file)
                else:
                    self._key_mismatch(key, file.tell())
                    if not key is None:
                        last_mismatch = (key, match)
                    
                current_line = file.readline()
        
        self.logger.info('Finished parsing')
        return (self.task_graph_dict, self.processor_list, self.std_link_dict, self.quantity_dict)
    
    def _parse_task_graph(self, file, match):
        identifier = 'TASK_GRAPH_' + (match.group('identifier'))
        tasks = {}
        channels = {}
        task_index_extension = 0
        channel_index_extension = 0
        
        current_line = file.readline()
        
        while current_line:
            key, match = self._parse_line(current_line, self.task_graph_components)
            if key == 'task':
                self.logger.debug('Added task: ' + match.group('name') + ' ' + match.group('type'))
                if not match.group('name') in tasks:
                    tasks.update( {match.group('name') : int(match.group('type'))} )
                else:
                    tasks.update( {match.group('name') + '_' + str(task_index_extension) : match.group('type')} )
                    task_index_extension += 1
            elif key == 'channel':
                self.logger.info('Added channel: ' + match.group('name') + ' ' + match.group('type'))
                if not match.group('name') in channels:
                    channels.update( {match.group('name') : [match.group('source'), match.group('destination'), match.group('type')]} ) 
                else:
                    channels.update( {match.group('name') + '_' + str(channel_index_extension): [match.group('source'), match.group('destination'), match.group('type')]} )
                    channel_index_extension += 1
            elif key == 'scope_limiter':
                self.logger.debug('Reached end of task graph')
                break
            else:
                self._key_mismatch(key, file.tell())
            current_line = file.readline()
        
        self.task_graph_dict.update( {identifier : TgffGraph(identifier, tasks, channels, self.quantity_dict)} )
        
    def _parse_commun_quant(self, file, match):
        identifier = match.group('identifier')
        commun_values = {}
        current_line = file.readline()
        
        while current_line:
            key, match = self._parse_line(current_line, self.commun_quant_components)
            if key == 'commun_value':
                self.logger.debug('Added commun_value ' + match.group('identifier') + ' ' + match.group('value'))
                commun_values.update( {int(match.group('identifier')) : float(match.group('value'))} )
            elif key == 'scope_limiter':
                self.logger.debug('Reached end of commun_quant')
                break
            else:
                self._key_mismatch(key, file.tell())
            current_line = file.readline()
        
        self.logger.info('Added to commun_quant dict: ' + identifier)
        self.quantity_dict.update( {int(identifier) : commun_values} )
    
    def _parse_hw_component(self, file, match, last_missmatch):
        identifier = match.group('name') + '_' + match.group('identifier')
        current_line = file.readline()
        lower_last_missmatch = None
        upper_last_missmatch = last_missmatch
        
        
        while current_line:
            key, match = self._parse_line(current_line, self.hw_components)
            if key == 'std_link_value':
                self._parse_std_link(identifier, file, match, lower_last_missmatch)
                return
            elif key == 'prim_link_value':
                self._parse_prim_link(identifier, file, match)
                return
            elif key == 'properties' or key == 'operation':
                self._parse_processor(identifier, file, key, match, upper_last_missmatch)
                return
            elif key == 'scope_limiter':
                self.logger.error('Reached end of scope. Unable to recognize HW component!')
            else:
                self._key_mismatch(key, file.tell())
                lower_last_missmatch = (key, match)
            current_line = file.readline()
        
    def _parse_std_link(self, identifier, file, match, last_missmatch):
        self.logger.debug('Recognized component as standard link!')
        
        name = identifier
        if last_missmatch[0] == 'comment':
            name = last_missmatch[1].group('comment').split()[0]
        throughput = 1 / float(match.group('bit_time'))
        link = TgffLink(name, throughput)
        
        self.logger.info('Added to link dict: ' + str(identifier))
        self.std_link_dict.update( {identifier : link } )
        
        current_line = file.readline()
        
        while(current_line):
            key, match = self._parse_line(current_line, None)
            if key == 'scope_limiter':
                return
            else:
                self._key_mismatch(key, file.tell())
        
    
    def _parse_prim_link(self, identifier, file, match):
        self.logger.info("Recognized component as primitive link!")
        prim_link_values = []
        self._add_prim_link_value(prim_link_values, match)
        
        current_line = file.readline()
        
        while current_line:
            key, match = self._parse_line(current_line, self.hw_components)
            if key == 'prim_link_value':
                self._add_prim_link_value(prim_link_values, match)
            elif key == 'scope_limiter':
                self.logger.debug("Reached end of primLink")
                break
            else:
                self._key_mismatch(key, file.tell())
            current_line = file.readline()
            
        self.logger.info('Added to link dict: ' + str(identifier))
        self.prim_link_dict.update( {identifier : prim_link_values } )
    
    def _add_prim_link_value(self, data_struct, match):
        data_struct.append(match.group('c_use_prc'))
        data_struct.append(match.group('c_cont_prc'))
        data_struct.append(match.group('s_use_prc'))
        data_struct.append(match.group('s_cont_prc'))
        data_struct.append(match.group('packet_size'))
        data_struct.append(match.group('bit_time'))
        data_struct.append(match.group('power'))
        
    def _parse_processor(self, identifier, file, key, match, last_missmatch):
        self.logger.debug("Recognized component as processing element")
        properties = []
        operations = {}
        
        if key == 'properties':
            self._add_properties(properties, match)
        elif key == 'operation':
            self._add_operation(operations, match)
        
        current_line = file.readline()
        
        while current_line:
            key, match = self._parse_line(current_line, self.hw_components)
            if key == 'properties':
                self._add_properties(properties, match)
            elif key == 'operation':
                self._add_operation(operations, match)
            elif key == 'scope_limiter':
                self.logger.debug('Reached end of processor')
                break
            else:
                self._key_mismatch(key, file.tell())
            current_line = file.readline()
            
        self.logger.info('Added to processor dict: ' + str(identifier))
        
        self.processor_list.append(TgffProcessor(identifier,
                                                 operations,
                                                 processor_type=("processor_" + str(len(self.processor_list)))))
    
    def _add_properties(self, properties, match):
        self.logger.debug('Parsed processor properties')
        properties.append(match.group('price'))
        properties.append(match.group('buffered'))
        properties.append(match.group('preempt_power'))
        properties.append(match.group('commun_energ_bit'))
        properties.append(match.group('io_energ_bit'))
        properties.append(match.group('idle_power'))
    
    def _add_operation(self, operations, match):
        self.logger.debug('Parsed processor operation')
        tmpList = list()
        tmpList.append(match.group('version'))
        tmpList.append(match.group('valid'))
        tmpList.append(float(match.group('task_time')))
        tmpList.append(float(match.group('preempt_time')))
        tmpList.append(match.group('code_bits'))
        tmpList.append(match.group('task_power'))
        operations.update( { int(match.group('type')) : tmpList} )
        
    def _parse_unused_scope(self, file):
        current_line = file.readline()
        
        while current_line:
            key, match = self._parse_line(current_line)
            if key == 'unused_statement':
                self.logger.info("Ignored statement")
            elif key == 'scope_limiter':
                self.logger.info("Parsed block which will be ignored")
                break
            else:
                self._key_mismatch(key, file.tell())
            current_line = file.readline()
    
    def _parse_line(self, line, additional_components=None):
        """Try to match the line to the patterns with the 
        most occurrence.
        """
        for key, rx in self.common_components.items():
            match = rx.fullmatch(line)
            if match:
                return key, match
        
        """Try to match the line to the patterns that can
        occur in the current context.
        """
        if additional_components is not None:
            for key, rx in additional_components.items():
                match = rx.fullmatch(line)
                if match:
                    return key, match
            
        """Try to match the line to patterns for information
        that will not be extracted by the parser.
        """
        for key, rx in self.unused_components.items():
            match = rx.fullmatch(line)
            if match:
                return key, match
        
        return None, None
    
    def _key_mismatch(self, key, position):
        if key == 'new_line' or key == 'comment':
            if self._debug:
                print('Skip empty or comment line')
        elif key is not None:
            self.logger.warning('Parsed unhandled group: <' + key + '> at position: ' + str(position))
        else:
            self.logger.error('Parse error on position: ' + str(position))


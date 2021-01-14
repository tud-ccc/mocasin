# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import math
from mocasin.common.kpn import KpnProcess, KpnChannel, KpnGraph
from mocasin.common.platform import Processor, FrequencyDomain, CommunicationResource

class TgffProcessor():
    """Represents the relevant information about a processor, included in a .tgff file.
    The processor can be transfered into the mocasin representation.
    """
    def __init__(self, name, operations, processor_type):
        self.name = name
        self.type = processor_type
        self.operations = {}
        self.cycle_time = self._get_cycle_time(operations)
        self._transform_operations(operations)
            
    def get_operation(self, idx):
        return self.operations[idx]
    
    """Returns a mocasin Processor object, equivalent to the TgffProcessor object.
    :returns: equivalent processor object
    :rtype: Processor
    """
    def to_mocasin_processor(self):
        frequency_domain = FrequencyDomain('fd{0}'.format(self.name), math.ceil(1/self.cycle_time))
        return Processor(self.name, self.type, frequency_domain)
    
    """Calculates the time needed for a single processor cycle, in a way that the 
    execution time og all operations are an integer multiple of the cycle time.
    
    :param operations: maps the indentifier of an operation to its execution time
    :type operations: dict{int : int}
    :returns: largest possible time step for a single cylce
    :rtype: float
    """
    def _get_cycle_time(self, operations):
        task_time = 1
        
        for properties in operations.values():
            if properties[2] < task_time and not properties[2] == 0:
                task_time = properties[2]
        
        tmp_string =list("{0:1.12f}".format(task_time))
        i = len(tmp_string) - 1
        
        while i > 1:
            if not tmp_string[i]  == '0':
                return 1 * (10 ** -(i-1))
            else:
                i -= 1
        return i
    
    """Transforms the mapping of operation identifier to execution time 
    to a mapping of operation identifier to execution cycles.
    
    :param operations: mapping of identifier to execution time
    :type operations: dict {int : int}
    """
    def _transform_operations(self, operations):
        for key, properties in operations.items():
            cycles = int(properties[2] / self.cycle_time)
            self.operations.update({key : cycles})
            
class TgffGraph():
    """Represents the relevant information about a task graph, parsed from
    a .tgff file. The tgff graph can be transfered into a kpn graph.
    """
    def __init__(self, identifier, task_set, channel_set, quantities):
        self.identifier = identifier
        self.tasks = task_set
        self.channels = channel_set
        self._quantities = quantities
        
    def get_task_type(self, identifier):
        return self.tasks[identifier]
    
    """Returns the order of actions for a single task (node) of the task
    graph
    
    :param task_name: the name of the specific task
    :type task_name: String
    :returns the order and type of actions the task performs when executed
    :rtype list[tuple(char, string)] a list of actions (read, write execute)
    and their target operation/channel
    """
    def get_execution_order(self, task_name):
        execution_order = []
        read_from = []
        write_to = []
        
        for name, properties in self.channels.items():
            #source
            if task_name == properties[0]:
                write_to.append(name)
            #sink
            if task_name == properties[1]:
                read_from.append(name)
                
        for channel_name in read_from:
            execution_order.append(('r', channel_name))
        
        execution_order.append(('e', self.tasks[task_name]))
        
        for channel_name in write_to:
            execution_order.append(('w', channel_name))
            
        return execution_order
    
    """Transfers the the tgff graph into a kpn graph
    :returns: the equivalent kpn graph representation
    :rtype: KpnGraph
    """                   
    def to_kpn_graph(self):
        kpn_graph = KpnGraph(self.identifier)
        tasks = []
        channels = []
            
        '''Create process for each node in 
        tgff graph
        '''
        for task in self.tasks:
            task = KpnProcess(task)
            tasks.append(task)
                
        '''Create channel for each edge in
        tgff graph.
        '''
        for key, properties in self.channels.items():
            name = key
            token_size = int(self._quantities[0][int(properties[2])])
            channel = KpnChannel(name, token_size)
                
            for task in tasks:
                if task.name == properties[0]:
                    task.connect_to_outgoing_channel(channel)
                if task.name == properties[1]:
                    task.connect_to_incomming_channel(channel)
                
            channels.append(channel)
            
            '''Add channels and processes to empty
            kpnGraph
            '''
        for task in tasks:
            kpn_graph.add_process(task)
            
        for channel in channels:
            kpn_graph.add_channel(channel)
        
        return kpn_graph
    
class TgffLink():
    """Represents the information about a hardware link included in a .tgff file.
    """
    def __init__(self, name, throughput):
        self.name = name
        self.throughput = throughput
    
    """Transfers the tgff hardware representation into mocasin representation. 
    ATTENTION: tgff does not include all necessary information. Mocasin link object 
    will be incomplete!
    :returns: An equivalent mocasin communication resource object
    :rtype: CommunicationRessource
    """
    def to_mocasin_communication_resource(self):
        #raise RuntimeWarning("The transformation into mocasin is not sufficient due to a lack of necessary properties!")
        return CommunicationResource(self.name, None, None, None, self.throughput, self.throughput, False, False)
    
     
    

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Processor, FrequencyDomain, CommunicationResource
from pykpn.common.kpn import KpnProcess, KpnChannel, KpnGraph

class TgffProcessor():
    def __init__(self, identifier, operations, processor_type=None):
        self.identifier = identifier
        self.type = processor_type
        self.operations = {}
        self.cycle_time = self._get_cycle_time(operations)
        self._transform_operations(operations)
            
    def get_operation(self, idx):
        return self.operations[idx]
    
    def to_pykpn_processor(self):
        frequency_domain = FrequencyDomain('fd{0}'.format(self.identifier), 1/self.cycle_time)
        pykpn_processor = None
        
        if not self.type is None:
            pykpn_processor = Processor(self.identifier, self.type, frequency_domain)
        else:
            pykpn_processor = Processor(self.identifier, self.identifier, frequency_domain)
        
        return pykpn_processor
    
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
    
    def _transform_operations(self, operations):
        for key, properties in operations.items():
            cycles = int(properties[2] / self.cycle_time)
            self.operations.update({key : cycles})
            
class TgffGraph():
    def __init__(self, identifier, task_set, channel_set, quantities):
        self.identifier = identifier
        self.tasks = task_set
        self.channels = channel_set
        self._quantities = quantities
        
    def get_task_type(self, identifier):
        return self.tasks[identifier]
    
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
            execution_order.append(('r',channel_name))
        
        execution_order.append(('e', self.tasks[task_name]))
        
        for channel_name in write_to:
            execution_order.append(('w', channel_name))
            
        return execution_order
                    
    def to_pykpn_graph(self):
        kpn_graph = KpnGraph()
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
    def __init__(self, name, throughput):
        self.name = name
        self.throughput = throughput
    
    def to_pykpn_communication_resource(self):
        raise RuntimeWarning("The transformation into pykpn is not sufficient due to a lack of necessary properties!")
        return CommunicationResource(self.name, None, None, None, self.throughput, self.throughput, False, False)
    
     
    
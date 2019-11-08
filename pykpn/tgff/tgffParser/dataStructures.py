# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.common.platform import Processor, FrequencyDomain
from pykpn.common.kpn import KpnProcess, KpnChannel, KpnGraph

class TgffProcessor():
    def __init__(self, identifier, operations, processorType=None):
        self.identifier = identifier
        self.type = processorType
        self.operations = {}
        self.cycleTime = self._getCycleTime(operations)
        self._transformOperations(operations)
            
    def getOperation(self, idx):
        return self.operations[idx]
    
    def toPykpnProcessor(self):
        frequencyDomain = FrequencyDomain('fd{0}'.format(self.identifier), 1/self.cycleTime)
        pykpnProcessor = None
        
        if not self.type is None:
            pykpnProcessor = Processor(self.identifier, self.type, frequencyDomain)
        else:
            pykpnProcessor = Processor(self.identifier, self.identifier, frequencyDomain)
        
        return pykpnProcessor
    
    def _getCycleTime(self, operations):
        taskTime = 1
        
        for properties in operations.values():
            if properties[2] < taskTime and not properties[2] == 0:
                taskTime = properties[2]
        
        tmpString =list("{0:1.12f}".format(taskTime))
        i = len(tmpString) - 1
        
        while i > 1:
            if not tmpString[i]  == '0':
                return 1 * (10 ** -(i-1))
            else:
                i -= 1
        return i
    
    def _transformOperations(self, operations):
        for key, properties in operations.items():
            cycles = int(properties[2] / self.cycleTime)
            self.operations.update({key : cycles})
            
class TgffGraph():
    def __init__(self, identifier, taskSet, channelSet, quantities):
        self.identifier = identifier
        self.tasks = taskSet
        self.channels = channelSet
        self._quantities = quantities
        
    def getTaskType(self, identifier):
        return self.tasks[identifier]
    
    def getExecutionOrder(self, task_name):
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
                    
    def toPykpnGraph(self):
        kpnGraph = KpnGraph()
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
            tokenSize = int(self._quantities[0][int(properties[2])])
            channel = KpnChannel(name, tokenSize)
                
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
            kpnGraph.add_process(task)
            
        for channel in channels:
            kpnGraph.add_channel(channel)
        
        return kpnGraph    
    
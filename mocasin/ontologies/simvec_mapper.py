#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from mocasin.common.mapping import Mapping
from mocasin.mapper.partial import ComPartialMapper, ProcPartialMapper
from mocasin.mapper.random import RandomPartialMapper
from builtins import StopIteration

class SimpleVectorMapper():
    def __init__(self, kpn, platform, mappingConstraints, sharedCoreConstraints, processingConstraints, vec, debug=False):
        self.__fullMapper = MappingCompletionWrapper(kpn, platform)
        self.__processors = len(platform.processors())
        self.__processes = len(kpn.processes())
        self.__debug = debug
        
        self.__stateVector = []
        self.__unmappedProcesses = []
        self.__frameMapping = []
        self.__sharedCoreDict = {}
        self.__processingConstraints = []
        
        for constraint in processingConstraints:
            if constraint.isNegated():
                self.__processingConstraints.append(constraint)
        
        """Initialize a vector where mapping constraints are set, unmapped processed encoded
        with -1
        """
        for i in range(0, self.__processes):
            self.__frameMapping.append(-1)
        for constraint in mappingConstraints:
            constraint.setEntry(self.__frameMapping)
        
        """Initialize a dictionary encoding the shared core constraints, the key is an index,
        the value is a list of indexes, the processor mapped to the key process, have to be mapped
        to each value process
        """
        for constraint in sharedCoreConstraints:
            vector = list(constraint.getIdVector())
            if vector == []:
                raise RuntimeError("Invalid vector")
            idx = 0
            for value in vector:
                if not self.__frameMapping[value] == -1:
                    idx = vector.index(value)
                    break
            key = vector.pop(idx)
            self.__sharedCoreDict.update({key : vector})
        
        #check which process in the frame mapping is unmapped
        #they're the degrees of freedom for the generation mapping generation
        for i in range(0, self.__processes):
            if self.__frameMapping[i] == -1:
                skip = False
                for key in self.__sharedCoreDict:
                    if i in self.__sharedCoreDict[key]:
                        skip = True
                if skip:
                    continue
                self.__unmappedProcesses.append(i)
                self.__stateVector.append(0)
                
        if vec and len(vec) == len(self.__stateVector):
            self.__stateVector = vec
        
    def __iter__(self):
        return self
    
    def __next__(self):
        nextMapping = self.nextMapping()
        return nextMapping
                
    def nextMapping(self):        
        if not self.__reachedLastIteration():
            for idx in range(0, len(self.__stateVector)):
                self.__frameMapping[self.__unmappedProcesses[idx]] = self.__stateVector[idx]
                idx += 1
            
            for key in self.__sharedCoreDict:
                for idx in self.__sharedCoreDict[key]:
                    self.__frameMapping[idx] = self.__frameMapping[key]
                    
            for constraint in self.__processingConstraints:
                for k in range(0, len(self.__frameMapping)):
                    if self.__frameMapping[k] == constraint.getProcessorId() and self.__frameMapping[k] < self.__processors-1:
                        self.__frameMapping[k] += 1
            
            for component in self.__frameMapping:
                if component == -1:
                    print("stop")
            
            mapping = self.__fullMapper.completeMappingBestEffort(self.__frameMapping)
            self.__stateIncrement(0)
            return mapping

        else:
            raise StopIteration()
    
    def __stateIncrement(self, currentIndex):
        #Check if the possible mapping space is fully explored
        if self.__debug:
            print(self.__stateVector)
        if self.__reachedLastIteration():
            return
        
        self.__stateVector[currentIndex] += 1
        if self.__stateVector[currentIndex] == self.__processors:
            self.__stateVector[currentIndex] = 0
            self.__stateIncrement(currentIndex + 1)
    
    def __reachedLastIteration(self):
        if self.__stateVector.count(self.__processors - 1) == len(self.__stateVector):
            if self.__debug:
                print("Iteration stopped!")
            return True            
    
    def getStateVector(self):
        return self.__stateVector
    
    def setStateVector(self, stateVector):
        self.__stateVector = stateVector
        
            
class MappingCompletionWrapper():
    """A wrapper class for different partial and full mappers in order
    to create a complete mapping out of a process mapping vector.
    """
    def __init__(self, kpn, platform):
        self.__kpn = kpn
        self.__platform = platform
        
        self.__fullMapper = RandomPartialMapper(kpn, platform, None)
        self.__communicationMapper = ComPartialMapper(kpn, platform, self)
        self.__processMapper = ProcPartialMapper(kpn, platform, self)
            
    def completeMappingAtRandom(self, processMappingVector):
        #create empty mapping, complete it with generated process mapping
        #and random channel mapping
        mapping = Mapping(self.__kpn, self.__platform)
        mapping.from_list(processMappingVector)
        
        assert(mapping.get_unmapped_channels() == [])
        assert(mapping.get_unmapped_processes() == [])
        
        return mapping
    
    def completeMappingBestEffort(self, processMappingVector):
        mapping = self.__processMapper.generate_mapping(processMappingVector)
        mapping = self.__fullMapper.generate_mapping(part_mapping=mapping)
        #self.__processMapper.reset() #not sure what this is supposed to do
        return mapping
        
    def generate_mapping(self, mapping):
        return mapping
        

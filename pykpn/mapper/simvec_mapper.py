#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.common.mapping import Mapping
from pykpn.mapper.com_partialmapper import ComPartialMapper
from pykpn.mapper.rand_partialmapper import RandomPartialMapper
from pykpn.mapper.proc_partialmapper import ProcPartialMapper

class SimpleVectorMapper():
    def __init__(self, kpn, platform, mappingConstraints, processingConstraints):
        self.__kpn = kpn
        self.__platform = platform
        self.__frameMapper = FrameMapper(kpn)
        self.__fullMapper = FullMapper(kpn, platform)
        
        self.__frameMapping = self.__frameMapper.generateFrameMapping(mappingConstraints)
        self.__processingConstraints = processingConstraints
        
        self.__processors = len(platform.processors())
        self.__unmappedProcesses = []
        self.__innerState = []
        i = 0 
        for process in self.__frameMapping:
            if process == -1:
                self.__unmappedProcesses.append(i)
                self.__innerState.append(0)
            i += 1
        
        self.__oldMapping = []
        self.__iterate = True
                
    def nextMapping(self):        
        while self.__iterate:
            self.__oldMapping = list(self.__frameMapping)
            idx = 0
            for idx in range(0, len(self.__innerState)):
                self.__frameMapping[self.__unmappedProcesses[idx]] = self.__innerState[idx]
                idx += 1
            
            if not self.__oldMapping == self.__frameMapping:
                mapping = self.__fullMapper.completeMappingBestEffort(self.__frameMapping)
                valid = True
                for constraint in self.__processingConstraints:
                    if not constraint.isFulFilled(mapping):
                        valid = False
                if valid:
                    self.__increaseInnerState(0)
                    yield mapping
                else:
                    self.__increaseInnerState(0)
                    self.nextMapping()
            else:
                self.__increaseInnerState(0)
                self.nextMapping()
    
    def __increaseInnerState(self, currentIndex):
        #Check if the possible mapping space is fully explored
        if self.__reachedLastIteration():
            return
        
        self.__innerState[currentIndex] += 1
        
        if self.__innerState[currentIndex] == self.__processors:
            self.__innerState[currentIndex] = 0
            self.__increaseInnerState(currentIndex + 1)
    
    def __reachedLastIteration(self):
        if self.__innerState.count(self.__processors - 1) == len(self.__innerState):
            self.__iterate = False
            return True            
    
    def getMapperState(self):
        return self.__innerState
    
    def setMapperState(self, stateVector):
        self.__innerState = stateVector
        
    def setKpn(self, kpn):
        pass
    
    def setPlatform(self, platform):
        pass
        
    
class FrameMapper():
    """Takes a set of constraints which must be fulfilled for a specific query. Returns a Vector
    which can be interpreted as simple vector representation of a partial mapping. -1 corresponds
    with an unmapped task.
    """
    def __init__(self, kpn):
        self.__frameLength = len(kpn.processes())
            
    def generateFrameMapping(self, mappingConstraints):
        frameMapping = []
        for i in range(0, self.__frameLength):
            frameMapping.append(-1)
        
        for constraint in mappingConstraints:
            constraint.setEntry(frameMapping)
            
        return frameMapping
            
class FullMapper():
    def __init__(self, kpn, platform):
        self.__kpn = kpn
        self.__platform = platform
        
        self.__fullMapper = RandomPartialMapper(kpn, platform, None)
        self.__communicationMapper = ComPartialMapper(kpn, platform, self)
        self.__processMapper = ProcPartialMapper(kpn, platform, self)
            
    def completeMappingAtRandom(self, processMappingVector):
        #Create empty mapping
        mapping = Mapping(self.__kpn, self.__platform)
        mapping.from_list(processMappingVector)
        
        if not mapping.get_unmapped_processes() == []:
            print("Unmapped processes: " + mapping.get_unmapped_processes())
            
        if not mapping.get_unmapped_channels() == []:
            print("Unmapped channels: " + mapping.get_unmapped_channels())
        
        return mapping
    
    def completeMappingBestEffort(self, processMappingVector):
        mapping = self.__processMapper.generate_mapping(processMappingVector)
        mapping = self.__fullMapper.generate_mapping(seed=None, part_mapping=mapping)
        self.__processMapper.reset()
        return mapping
        
    def generate_mapping(self, mapping):
        return mapping
    
    def setKpn(self, kpn):
        self.__kpn = kpn
        self.__fullMapper = RandomPartialMapper(kpn, self.__platform)
        self.__comMapper = ComPartialMapper(kpn, self.__platform, self.__fullMapper)
        self.__processMapper = ProcPartialMapper(kpn, self.__platform, self.__comMapper)
        
    def setPlatform(self, platform):
        self.__platform = platform
        self.__fullMapper = RandomPartialMapper(self.__kpn, platform)
        self.__comMapper = ComPartialMapper(self.__kpn, platform, self.__fullMapper)
        self.__processMapper = ProcPartialMapper(self.__kpn, platform, self.__comMapper)
        

#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.common.mapping import Mapping

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
                
        self.__processingConstraintsMapping = []
        self.__processingConstraintsState = []
        i = 0
        for constraint in self.__processingConstraints:
            self.__processingConstraintsMapping.append(self.__unmappedProcesses[i])
            self.__processingConstraintsState.append(i)
            i += 1
        self.__oldMapping = []
        self.__iterate = True
                
    def nextMapping(self):        
        while self.__iterate:
            self.__oldMapping = list(self.__frameMapping)
            for processMapping in self.__processingConstraintsMapping:
                idx = self.__processingConstraintsMapping.index(processMapping)
                self.__frameMapping[processMapping] = self.__processingConstraints[idx].getProcessorId()
            idx = 0
            for processMapping in self.__innerState:
                if not self.__unmappedProcesses[idx] in self.__processingConstraintsMapping:
                    self.__frameMapping[self.__unmappedProcesses[idx]] = self.__innerState[idx]
                idx += 1
            
            if not self.__oldMapping == self.__frameMapping:
                self.__increaseInnerState(0)
                yield self.__fullMapper.completeMappingAtRandom(self.__frameMapping)
            else:
                self.__increaseInnerState(0)
                self.nextMapping()
    
    def __increaseInnerState(self, currentIndex):
        #Check if the possible mapping space is fully explored
        if self.reachedLastIteration():
            return
        
        self.__innerState[currentIndex] += 1
        
        if currentIndex == len(self.__innerState) - 1 and self.__innerState[currentIndex] == self.__processors:
            self.__innerState[currentIndex] = 0
            self.__increaseConstraintState(len(self.__processingConstraintsState) - 1)
        elif self.__innerState[currentIndex] == self.__processors:
            self.__innerState[currentIndex] = 0
            self.__increaseInnerState(currentIndex + 1)
            
    def __increaseConstraintState(self, currentIndex, update=True):
        self.__processingConstraintsState[currentIndex] += 1
        if currentIndex >= 1 and self.__processingConstraintsState[currentIndex] == self.__processingConstraintsState[currentIndex - 1]:
            self.__processingConstraintsState[currentIndex] += 1
        elif currentIndex >= 1 and self.__processingConstraintsState[currentIndex] == len(self.__unmappedProcesses):
            self.__processingConstraintsState[currentIndex] = 0
            self.__increaseConstraintState(currentIndex - 1, update=False)
        
        if update:
            i = 0
            for idx in self.__processingConstraintsState:
                self.__processingConstraintsMapping[i] = self.__unmappedProcesses[idx]
                i += 1 
    
    def reachedLastIteration(self):
        if self.__processingConstraintsState == []:
            if self.__innerState[0] >= self.__processors - 1 and self.__innerState[-1] >= self.__processors - 1:
                self.__iterate = False
                return True
        '''
        else:
            if self.__processingConstraintsState[0] >=  and self.__processingConstraintsState[-1] == 0:
                self.__iterate = False
                return True
        return False
        '''
            #TODO: Redo increment of the constraint state and get this one to a working state
    
    def getMapperState(self):
        return (self.__innerState, self.__processingConstraintsState)
    
    def setMapperState(self, stateVector):
        self.__innerState = stateVector
        
    def setConstraintsState(self, stateVector):
        self.__processingConstraintsState = stateVector
    
    def getProcessMapping(self):
        return self.__frameMapping
    
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
            
    def completeMappingAtRandom(self, processMappingVector):
        #Create empty mapping
        mapping = Mapping(self.__kpn, self.__platform)
        mapping.from_list(processMappingVector)
        
        if not mapping.get_unmapped_processes() == []:
            print("Unmapped processes: " + mapping.get_unmapped_processes())
            
        if not mapping.get_unmapped_channels() == []:
            print("Unmapped channels: " + mapping.get_unmapped_channels())
        
        return mapping



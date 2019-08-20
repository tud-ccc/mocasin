#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

class SimpleVectorMapper():
    def __init__(self, kpn, platform, mappingConstraints, processingConstraints, remainingConstraints):
        self.__kpn = kpn
        self.__platform = platform
        
        self.__frameMapping = FrameMapper(mappingConstraints)
    
class FrameMapper():
    """Take a set of constraints which must be fulfilled for a specific query. Returns a Vector
    which can be interpreted as simple vector representation of a mapping.
    :param list[MappingConstraint] mappingConstraints: The constraints that are non optional for the specific query.
    :param int amount: The amount of processes in the kpn graph.
    :returns: A list similar to the vector abstraction of a mapping
    :rtype: list[int] 
    """
    def __init__(self, mappingConstraints, amount):
        frameMapping = []
        for i in range(0, amount):
            frameMapping.append(-1)
            
        for constraint in mappingConstraints:
            constraint.setEntry(frameMapping)
            
        return frameMapping
            
class FullMapper():
    def __init__(self):
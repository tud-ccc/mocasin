#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.mapper.simvec_mapper import SimpleVectorMapper
from logicLanguage import MappingConstraint, ProcessingConstraint
from pykpn.common.mapping import Mapping

class Solver():
    def __init__(self, kpnGraph, platform):
        self.__kpn = kpnGraph
        self.__platform = platform
    
          
    def getMappingGenerator(self, query):
        """Method decides, which kind of Generator suits the best for a given constraint set
        """
        for constraintSet in query:
            mappingConstraints = []
            processingConstraints = []
            remaining = []
            for constraint in constraintSet:
                if isinstance(constraint, MappingConstraint):
                    mappingConstraints.append(constraint)
                
                elif isinstance(constraint, ProcessingConstraint):
                    processingConstraints.append(constraint)
                
                else:
                    remaining.append(constraint)
            
            return SimpleVectorMapper(self.__kpn, self.__platform, mappingConstraints, processingConstraints, remaining)
            #TODO: start thread for each possible frame_mapping?
                
    def simpleVectorGenerator(self, constraintSet):
        """Method creates a Generator for SimpleVector constraints
        """
        solution = Mapping(self.__kpn, self.__platform)
        
        for constraint in constraintSet:
            if isinstance(constraint, MappingConstraint):
                constraint.applyToMapping(solution, self.__kpn, self.__platform)
        
        
            
            
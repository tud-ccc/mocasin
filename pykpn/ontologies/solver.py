#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.mapper.simvec_mapper import SimpleVectorMapper
from pykpn.common.mapping import Mapping
from arpeggio import ParserPython, visit_parse_tree
from logicLanguage import Grammar, SemanticAnalysis, MappingConstraint, ProcessingConstraint
from threading import Thread

import queue


class Solver():
    def __init__(self, kpnGraph, platform, mappingDict={},  debug=False):
        self.__kpn = kpnGraph
        self.__platform = platform
        self.__mappingDict = mappingDict
        self.__debug = debug
        self.__parser = ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=debug)
    
    def setKpnGraph(self, kpnGraph):
        self.__kpn = kpnGraph
        
    def setPlatform(self, platform):
        self.__platform = platform
        
    def request(self, queryString, vec=None):
        parse_tree = self.__parser.parse(queryString)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(self.__kpn, self.__platform, self.__mappingDict, debug=self.__debug))
        
        resultQueue = queue.Queue()
        
        #start a different thread for each constraint set, so each thread can work
        #with an individual generator
        threadCounter = 0
        for constraintSet in constraints:
            threadCounter += 1
            thread = Thread(target=self.searchMapping, args=(constraintSet, resultQueue, vec, threadCounter))
            thread.daemon = True
            thread.start()
        
        while threadCounter > 0:
            threadResult = resultQueue.get()
            threadCounter -= 1
            
            if isinstance(threadResult[1], Mapping):
                print(threadResult[0])
                return threadResult[1]
        
        #In case neither of the threads returned a valid mapping
        return False
        
    def searchMapping(self, constraintSet, resultQueue, vec, id):
        mappingConstraints = []
        processingConstraints =[]
        remaining = []
        
        for constraint in constraintSet:
            #Sort Constraints
            if isinstance(constraint, MappingConstraint):
                mappingConstraints.append(constraint)
            elif isinstance(constraint, ProcessingConstraint):
                processingConstraints.append(constraint)
            else:
                remaining.append(constraint)
        
        #TODO: Decide which mapper is the most efficient to use, not using SimpleVec by default
        mapper = SimpleVectorMapper(self.__kpn, self.__platform, mappingConstraints, processingConstraints)
        
        if vec:
            mapper.setMapperState(vec)
       
        for mapping in mapper.nextMapping():
            if self.__debug:
                print(mapper.getMapperState())
            mappingValid = True
            for constraint in remaining:
                if not constraint.isFulFilled(mapping):
                    mappingValid = False
            
            if mappingValid:
                resultQueue.put((id, mapping))
                return
            
        resultQueue.put((id, False))
        

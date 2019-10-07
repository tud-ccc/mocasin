#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.mapper.mapgen import MappingGeneratorOrbit, MappingGeneratorSimvec
from pykpn.common.mapping import Mapping
from pykpn.representations.representations import RepresentationType
from pykpn.ontologies.logicLanguage import Grammar, SemanticAnalysis, MappingConstraint, EqualsConstraint, SharedCoreUsageConstraint
from arpeggio import ParserPython, visit_parse_tree
from threading import Thread

import queue

class Solver():
    def __init__(self, kpnGraph, platform, mappingDict={}, debug=False):
        self.__kpn = kpnGraph
        self.__platform = platform
        self.__mappingDict = mappingDict
        self.__parser = ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=debug)
        self.__debug = debug
        
    def request(self, queryString, vec=None):
        parse_tree = self.__parser.parse(queryString)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(self.__kpn, self.__platform, self.__mappingDict, debug=self.__debug))
        threadQueue = queue.Queue()
        
        #start a different thread for each constraint set, so each thread can work
        #with an individual generator
        threadCounter = 0
        for constraintSet in constraints:
            threadCounter += 1
            thread = Thread(target=self.exploreMappingSpace, args=(constraintSet, threadQueue, vec, threadCounter))
            thread.daemon = True
            thread.start()
        
        while threadCounter > 0:
            threadResult = threadQueue.get()
            threadCounter -= 1
            
            if isinstance(threadResult[1], Mapping):
                print(threadResult[0])
                return threadResult[1]
        
        #In case neither of the threads returned a valid mapping
        return False
    
    def parseString(self, queryString):
        parse_tree = self.__parser.parse(queryString)
        return visit_parse_tree(parse_tree, SemanticAnalysis(self.__kpn, self.__platform, self.__mappingDict, debug=self.__debug))
        
    def exploreMappingSpace(self, constraintSet, returnBuffer, vec, threadIdentifier):
        mappingConstraints = []
        equalsConstraints = []
        sharedCoreConstraints = []
        remaining = []
        
        for constraint in constraintSet:
            #Sort Constraints
            if constraint.isNegated():
                remaining.append(constraint)
            else:
                if isinstance(constraint, MappingConstraint):
                    mappingConstraints.append(constraint)
                elif isinstance(constraint, EqualsConstraint):
                    equalsConstraints.append(constraint)
                elif isinstance(constraint, SharedCoreUsageConstraint):
                    sharedCoreConstraints.append(constraint)
                else:
                    remaining.append(constraint)
        
        generator = None
        
        #if there is at least one equalsConstraint, this generator is chosen
        if not equalsConstraints == []:
            genMapping = equalsConstraints[0].getMapping()
            
            #check if all given mappings in the constrains are equal
            if len(equalsConstraints) > 1:
                for i in range(1, len(equalsConstraints)):
                    if not equalsConstraints[i].isFulfilled(genMapping):
                        returnBuffer.put((threadIdentifier, False))
            
            #if so, generate a generator for later use
            remaining = remaining + mappingConstraints + sharedCoreConstraints
            symmetryLense = RepresentationType['Symmetries'].getClassType()(self.__kpn, self.__platform)
            generator = MappingGeneratorOrbit(symmetryLense, genMapping)
        
        #otherwise the simpleVectorMapper is used a generator
        else:
            generator = MappingGeneratorSimvec(self.__kpn, self.__platform, mappingConstraints, sharedCoreConstraints, vec)
        
        if generator:
            for mapping in generator:
                mappingValid = True
                for constraint in remaining:
                    if not constraint.isFulfilled(mapping):
                        mappingValid = False
                        break
            
                if mappingValid:
                    returnBuffer.put((threadIdentifier, mapping))
                    return
            
        returnBuffer.put((threadIdentifier, False))
        

#Copyright (C) 2019-2020 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit, Andrés Goens


from threading import Thread
from pykpn.common.mapping import Mapping
from arpeggio import ParserPython, visit_parse_tree
from pykpn.representations.__init__ import RepresentationType
from pykpn.mapper.mapgen import MappingGeneratorOrbit, MappingGeneratorSimvec
from pykpn.ontologies.logicLanguage import Grammar, SemanticAnalysis, MappingConstraint, EqualsConstraint,\
                                            SharedCoreUsageConstraint, ProcessingConstraint

import sys
import queue
import traceback

from pykpn.util import logging
log = logging.getLogger(__name__)

#GLOBAL DEFINITION
RUN_THREADS = True

class Solver():
    def __init__(self, kpnGraph, platform, cfg, mappingDict={}, debug=False):
        self.__kpn = kpnGraph
        self.__platform = platform
        self.__mappingDict = mappingDict
        self.__parser = ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=debug)
        self.__debug = debug
        self.__cfg = cfg
        
    def request(self, queryString, vec=None):
        parse_tree = self.__parser.parse(queryString)
        sema = SemanticAnalysis(self.__kpn, self.__platform, self.__cfg, self.__mappingDict, debug=self.__debug)
        constraints = visit_parse_tree(parse_tree, sema)
        threadQueue = queue.Queue()
        
        """Creation of individual threads for each constraint set
        """
        threadCounter = 0
        threadPool = []
        global RUN_THREADS
        RUN_THREADS = True
        for constraintSet in constraints:
            threadCounter += 1
            thread = Thread(target=self.exploreMappingSpace, args=(constraintSet, threadQueue, vec, threadCounter))
            thread.daemon = True
            threadPool.append(thread)
            thread.start()
        
        """Waiting for results in the thread queue
        """
        result = False
        while threadCounter > 0:
            threadResult = threadQueue.get()
            threadCounter -= 1
            if isinstance(threadResult[1], Mapping):
                print(threadResult[0])
                result = threadResult[1]
                RUN_THREADS = False
                break
        for thread in threadPool:
            thread.join(1)
        log.info("All threads terminated")
        
        return result
    
    def parseString(self, queryString):
        parse_tree = self.__parser.parse(queryString)
        sema = SemanticAnalysis(self.__kpn, self.__platform, self.__cfg, self.__mappingDict, debug=self.__debug)
        return visit_parse_tree(parse_tree, sema)
        
    def exploreMappingSpace(self, constraintSet, returnBuffer, vec, threadIdentifier):
        mappingConstraints = []
        equalsConstraints = []
        sharedCoreConstraints = []
        processingConstraints = []
        remaining = []
        
        """Sorting of constraints in given set
        """
        for constraint in constraintSet:
            if isinstance(constraint, ProcessingConstraint):
                processingConstraints.append(constraint)
            elif constraint.isNegated():
                remaining.append(constraint)
            else:
                if isinstance(constraint, MappingConstraint):
                    mappingConstraints.append(constraint)
                elif isinstance(constraint, EqualsConstraint):
                    equalsConstraints.append(constraint)
                elif isinstance(constraint, SharedCoreUsageConstraint):
                    sharedCoreConstraints.append(constraint)
                    remaining.append(constraint)
                else:
                    remaining.append(constraint)
                    
        """Checking for contradictions in constraints
        """
        for i in range(0, len(mappingConstraints) - 1):
            firstConstraint = mappingConstraints[i].getProperties()
            for j in range(i+1,len(mappingConstraints)):
                secondConstraint = mappingConstraints[j].getProperties()
                if firstConstraint[0] == secondConstraint[0] and not firstConstraint[1] == secondConstraint[1]:
                    returnBuffer.put((threadIdentifier, False))
                    return
        
        #checking for contradictions in mapping constraints
        for firstConstraint in mappingConstraints:
            for secondConstraint in equalsConstraints:
                if firstConstraint != secondConstraint:
                    if firstConstraint.processId == secondConstraint.processId and firstConstraint.processorId != secondConstraint.processId:
                        returnBuffer.put((threadIdentifier, False))
                        return
        
        for sharedConst in sharedCoreConstraints:
            vector = sharedConst.getIdVector()
            pePool = []
            for mapConst in mappingConstraints:
                properties = mapConst.getProperties()
                if properties[0] in vector:
                    if not properties[1] in pePool:
                        pePool.append(properties[1])
            if len(pePool) > 1:
                returnBuffer.put((threadIdentifier, False))
                return
        
        for i in range(0, len(processingConstraints)-1):
            identifier = processingConstraints[i].getProcessorId()
            negated = processingConstraints[i].isNegated()
            for j in range( i+1, len(processingConstraints)):
                if processingConstraints[j].getProcessorId() == identifier and ((processingConstraints[j].isNegated() and not negated) or (not processingConstraints[j].isNegated() and negated)):
                    returnBuffer.put((threadIdentifier, False))
                    return
                
        for constraint in processingConstraints:
            if constraint.isNegated():
                for mappConst in mappingConstraints:
                    if mappConst.getProperties()[1] == constraint.getProcessorId() and not mappConst.isNegated():
                        returnBuffer.put((threadIdentifier, False))
                        return
                
        remaining += processingConstraints
       
        """Decision which generator to choose and creation of generator
        """
        generator = None
        try:
            if not equalsConstraints == []:
                genMapping = equalsConstraints[0].getMapping()
            
                """Check for contradictions in IsEqualConstraints
                """
                if len(equalsConstraints) > 1:
                    for i in range(1, len(equalsConstraints)):
                        if not equalsConstraints[i].isFulfilled(genMapping):
                            returnBuffer.put((threadIdentifier, False))
                            return
            
                remaining = remaining + mappingConstraints + sharedCoreConstraints
                symmetryLens = RepresentationType['Symmetries'].getClassType()(self.__kpn, self.__platform,self.__cfg)
                generator = MappingGeneratorOrbit(symmetryLens, genMapping)
            else:
                generator = MappingGeneratorSimvec(self.__kpn, self.__platform, mappingConstraints, sharedCoreConstraints, processingConstraints, vec)
        
            """Iteration over the mapping space, checking if remaining constraints are fulfilled
            """
            if generator:
                for mapping in generator:
                    global RUN_THREADS
                    if not RUN_THREADS:
                        return
                    mappingValid = True
                    for constraint in remaining:
                        if not constraint.isFulfilled(mapping):
                            mappingValid = False
                            break
            
                    if mappingValid:
                        returnBuffer.put((threadIdentifier, mapping))
                        return
        except:
            print("Exception occurred: ", sys.exc_info()[0])
            traceback.print_exc()
            returnBuffer.put((threadIdentifier, False))

            
        returnBuffer.put((threadIdentifier, False))


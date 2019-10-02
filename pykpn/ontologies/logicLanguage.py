#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.common.mapping import Mapping
from pykpn.representations.representations import RepresentationType
from arpeggio import OrderedChoice, EOF, PTNodeVisitor, OneOrMore, Optional
from arpeggio import RegExMatch as _
from abc import ABC, abstractmethod
from arpeggio.peg import OPTIONAL
from builtins import staticmethod

class Grammar():
    @staticmethod
    def __mappingIdentifier(): return _(r'([ab-z]|[AB-Z])(([ab-z]|[AB-z]|[0-9]|\_)*)')
    
    @staticmethod
    def __peIdentifier(): return _(r'([ab-z]|[AB-Z])(([ab-z]|[AB-z]|[0-9]|\_)*)')
    
    @staticmethod
    def __taskIdentifier(): return _(r'([ab-z]|[AB-Z])(([ab-z]|[AB-z]|[0-9]|\_)*)')
    
    @staticmethod
    def __taskIdentifierSeparated(): return ((Grammar.__taskIdentifier), (','))
    
    @staticmethod
    def __isEqualOp(): return (Optional("NOT"), ("EQUALS"), Grammar.__mappingIdentifier)
    
    @staticmethod
    def __sharedCoreOp(): return (Optional("NOT"), ("RUNNING TOGETHER ["), OneOrMore(Grammar.__taskIdentifierSeparated), Grammar.__taskIdentifier, ("]"))
    
    @staticmethod
    def __processingOp(): return (Optional("NOT"), Grammar.__peIdentifier, ("PROCESSING"))
    
    @staticmethod
    def __mappingOp(): return (Optional("NOT"), Grammar.__taskIdentifier, ("MAPPED"), Grammar.__peIdentifier)
    
    @staticmethod
    def __operation(): return OrderedChoice([
                                    (Grammar.__mappingOp),
                                    (Grammar.__processingOp),
                                    (Grammar.__sharedCoreOp),
                                    (Grammar.__isEqualOp)
                                    ])
    
    @staticmethod
    def __relation(): return OrderedChoice([
                                    ("AND"),
                                    ("OR")
                                    ])
    
    @staticmethod
    def __andExpression(): return OrderedChoice([
                                    (Grammar.__operation, OneOrMore(("AND"), Grammar.__operation))
                                    ])
    
    @staticmethod
    def __orExpression(): return OrderedChoice([
                                    (Grammar.__operation, OneOrMore(("OR"), Grammar.__operation))
                                    ])
    
    @staticmethod
    def __expression(): return OrderedChoice([
                                    (("("), Grammar.__expression, (")"), Grammar.__relation, ("("), Grammar.__expression, (")")),
                                    Grammar.__andExpression,
                                    Grammar.__orExpression,
                                    Grammar.__operation
                                    ])
    
    @staticmethod
    def logicLanguage(): return ("EXISTS "), Grammar.__expression, EOF
    
class SemanticAnalysis(PTNodeVisitor): 
    def __init__(self, kpnGraph, platform, mappingDict={}, defaults=True, **kwargs):
        '''Map processors and processes to integer values
        '''
        self.__processors = {}
        for i, pe in enumerate(platform.processors()):
            self.__processors[pe.name] = i
        self.__processes = {}
        for i, process in enumerate(kpnGraph.processes()):
            self.__processes[process.name] = i
        
        self.__mappingDict = mappingDict
        self.__kpn = kpnGraph
        self.__platform = platform
        super(SemanticAnalysis, self).__init__(defaults, **kwargs)
        
    def visit_logicLanguage(self, node, children):
        '''Check for single constraints, that may not be packed in a list
        '''
        result = []
        if isinstance(children[0], list):
            for element in children[0]:
                if isinstance(element, list):
                    result.append(element)
                else:
                    result.append([element])
            return result
        else:
            '''In case there is just a single constraint it must be double packed
            '''
            return [[children[0]]]
    
    def visit___expression(self, node, children):
        result = []

        if len(children) == 1:
            result = children
        else:
            if children[1] == "AND":
                for leftHandSet in children[0]:
                    for rightHandSet in children[2]:
                        tmpSet = list(leftHandSet)
                        for constraint in rightHandSet:
                            tmpSet.append(constraint)
                        result.append(tmpSet)

            elif children[1] == "OR":
                for constraintSet in children[0]:
                    result.append(constraintSet)
                for constraintSet in children[2]:
                    result.append(constraintSet)
            else:
                raise RuntimeError("Unexpected relation operator!")
        
        return result
    
    def visit___andExpression(self, node, children):
        result = [[]]
        for child in children:
            if isinstance(child, list):
                result[0].append(child[0][0])
        return result
    
    def visit___orExpression(self, node, children):
        result = []
        for child in children:
            if isinstance(child, list):
                result.append(child[0])
        return result
    
    def visit___relation(self, node, children):
        return str(node)
    
    def visit___operation(self, node, children):
        return children[0]
    
    def visit___mappingOp(self, node, children):
        if len(children) == 2:
            negate = False
            processName = children[0]
            processorName = children[1]
        else:
            negate = True
            processName = children[1]
            processorName = children[2]
        processId = self.__processes[processName]
        processorId = self.__processors[processorName]
        return [[MappingConstraint(negate, processName, processId, processorName, processorId)]]
    
    def visit___processingOp(self, node, children):
        if len(children) == 1:
            negate = False
            processorName = children[0]
        else:
            negate = True
            processorName = children[1]
        processorId = self.__processors[processorName]
        return [[ProcessingConstraint(negate, processorName, processorId)]]
    
    def visit___sharedCoreOp(self, node, children):
        idVec = []
        offset = 0
        negate = False
        if children[0] == "NOT":
            offset = 1
            negate = True
        for i in range(offset, len(children)):
            taskName = children[i]
            idVec.append(self.__processes[taskName])
        return [[SharedCoreUsageConstraint(negate, idVec)]]
    
    def visit___isEqualOp(self, node, children):
        if len(children) == 1:
            negate = False
            mappingName = children[0]
        else:
            negate = True
            mappingName = children[1]
        return [[EqualsConstraint(negate, self.__mappingDict[mappingName], self.__kpn, self.__platform)]]
    
    def visit___mappingIdentifier(self, node, children):
        name = str(node)
        if not name in self.__mappingDict:
            raise RuntimeError(name + " is no valid mapping identifier!")
        return name
    
    def visit___taskIdentifier(self, node, children):
        name = str(node)
        if not name in self.__processes:
            raise RuntimeError(name + " is no valid process identifier!")
        return name
    
    def visit___taskIdentifierSeparated(self, node, children):
        return children[0]
    
    def visit___peIdentifier(self, node, children):
        name = str(node)
        if not name in self.__processors:
            raise RuntimeError(name + " is no valid processor identifier!")
        return name
    
class Constraint(ABC):
    @abstractmethod
    def isFulfilled(self, mapping):
        pass
    
class MappingConstraint(Constraint):
    def __init__(self, negate, processName, processId, processorName, processorId):
        self.__negate = negate
        self.__processName = processName
        self.__processId = processId
        self.__processorName = processorName
        self.__processorId = processorId
    
    def isFulfilled(self, mapping):
        if isinstance(mapping, Mapping):
            procVec = mapping.to_list()
            if procVec[self.__processId] == self.__processorId:
                if self.__negate:
                    return False
                return True
            else:
                if self.__negate:
                    return True
                return False
        else:
            return False
    
    def setEntry(self, partialMapping):
        partialMapping[self.__processId] = self.__processorId
        
    def isNegated(self):
        return self.__negate
        
class ProcessingConstraint(Constraint):
    def __init__(self, negate, processorName, processorId):
        self.__negate = negate
        self.__processorName = processorName
        self.__processorId = processorId
    
    def isFulfilled(self, mapping):
        #TODO:
        #-> Check if mapping is in simple vector representation
        #-> Check if core is processing using this mapping
        if not isinstance(mapping, Mapping):
            raise RuntimeWarning("Mapping object is needed to evaluate constraint!")
        else:
            processList = mapping.to_list()
            if self.__processorId in processList:
                if self.__negate:
                    return False
                return True
            else:
                if self.__negate:
                    return True
                return False
    
    def getProcessorId(self):
        return self.__processorId
    
class SharedCoreUsageConstraint(Constraint):
    def __init__(self, negate, idVec):
        self.__negate = negate
        self.__idVector = idVec
        
    def isFulfilled(self, mapping):
        if isinstance(mapping, Mapping):
            simVec = mapping.to_list()
            if self.__negate:
                taskPool = []
                for key in self.__idVector:
                    if simVec[key] in taskPool:
                        return False
                    else:
                        taskPool.append(simVec[key])
                return True
            else:
                executingPe = simVec[self.__idVector[0]]
                for key in self.__idVector:
                    if not simVec[key] == executingPe:
                        return False
                return True            
        else:
            return False
        
class EqualsConstraint(Constraint):
    def __init__(self, negate, mappingObject, kpn, platform):
        self.__negate = negate
        self.__mapping = mappingObject
        self.__lense = RepresentationType['Symmetries'].getClassType()(kpn, platform)
        
    def isFulfilled(self, mapping):
        if isinstance(mapping, Mapping):
            allEquivalent = self.__lense.allEquivalentGen(mapping)
            for equivalent in allEquivalent:
                if equivalent.to_list() == mapping.to_list():
                    if self.__negate:
                        return False
                    return True
            if self.__negate:
                return True
            return False
        else:
            return False
        
    def getMapping(self):
        return self.__mapping
    
    def isNegated(self):
        return self.__negate





    
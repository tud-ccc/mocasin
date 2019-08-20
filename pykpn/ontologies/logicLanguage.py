#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from builtins import staticmethod
from arpeggio import OrderedChoice, EOF, PTNodeVisitor
from arpeggio import RegExMatch as _
from abc import ABC, abstractmethod
from pykpn.common.mapping import ProcessMappingInfo

class Grammar():
    @staticmethod
    def __peIdentifier(): return _(r'([ab-z]|[AB-Z])(([ab-z]|[AB-z]|[0-9]|\_)*)')
    
    @staticmethod
    def __taskIdentifier(): return _(r'([ab-z]|[AB-Z])(([ab-z]|[AB-z]|[0-9]|\_)*)')
    
    @staticmethod
    def __processingOp(): return (Grammar.__peIdentifier, ("PROCESSING"))
    
    @staticmethod
    def __mappingOp(): return (Grammar.__taskIdentifier, ("MAPPED"), Grammar.__peIdentifier)
    
    @staticmethod
    def __operation(): return OrderedChoice([
                                    (Grammar.__mappingOp),
                                    (Grammar.__processingOp)
                                    ])
    
    @staticmethod
    def __relation(): return OrderedChoice([
                                    ("AND"),
                                    ("OR")
                                    ])
    
    @staticmethod
    def __expression(): return OrderedChoice([
                                        (("("), Grammar.__expression, (")"), Grammar.__relation, ("("), Grammar.__expression, (")")),
                                        (Grammar.__operation, Grammar.__relation, ("("), Grammar.__expression, (")")),
                                        (("("), Grammar.__expression, (")"), Grammar.__relation, Grammar.__operation),
                                        (Grammar.__operation, Grammar.__relation, Grammar.__expression),
                                        (Grammar.__operation)
                                        ])
    
    @staticmethod
    def logicLanguage(): return ("EXISTS "), Grammar.__expression, EOF
    
class SemanticAnalysis(PTNodeVisitor): 
    def __init__(self, kpnGraph, platform, defaults=True, **kwargs):
        '''Map processors and processes to integer values
        '''
        self.__processors = {}
        for i, pe in enumerate(platform.processors()):
            self.__processors[pe.name] = i
        self.__processes = {}
        for i, process in enumerate(kpnGraph.processes()):
            self.__processes[process.name] = i
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

        if children[1] == 'AND':
            if isinstance(children[0], list):
                for constraintSetL in children[0]:
                    if isinstance(children[2], list):
                        for constraintSetR in children[2]:
                            tmpSet = list(constraintSetL)
                            if isinstance(constraintSetR, list):
                                for constraint in constraintSetR:
                                    tmpSet.append(constraint)
                                result.append(tmpSet)
                            else:
                                tmpSet.append(constraintSetR)
                                result.append(tmpSet)
                    else:
                        constraintSetL.append(children[2])
                        result.append(constraintSetL)
            else:
                if isinstance(children[2], list):
                    for constraintSetR in children[2]:
                        if isinstance(constraintSetR, list):
                            constraintSetR.append(children[0])
                            result.append(constraintSetR)
                        else:
                            result.append([children[0], constraintSetR])
                else:
                    result.append([children[0], children[2]])
        elif children[1] == 'OR':
            if isinstance(children[0], list):
                for element in children[0]:
                    result.append(element)
            else:
                result.append([children[0]])
            if isinstance(children[2], list):
                for element in children[2]:
                    result.append(element)
            else:
                result.append([children[2]])
        else:
            if self.debug:
                print("Unexpected keyword for an expression of length 3!")
            else:
                raise RuntimeError("Unexpected keyword in an expression!")
        return result
    
    def visit___relation(self, node, children):
        return str(node)
    
    def visit___operation(self, node, children):
        return children[0]
    
    def visit___mappingOp(self, node, children):
        processName = children[0]
        if not processName in self.__processes:
            raise RuntimeError(processName + " is no valid process identifier!")
        processId = self.__processes[processName]
        
        processorName = children[1]
        if not processorName in self.__processors:
            raise RuntimeError(processorName + " is no valid processor identifier!")
        processorId = self.__processors[processorName]
        
        return MappingConstraint(processName, processId, processorName, processorId)
    
    def visit___processingOp(self, node, children):
        processorName = children[0]
        if not processorName in self.__processors:
            raise RuntimeError(processorName + " is no valid processor identifier!")
        processorId = self.__processors[processorName]
        
        return ProcessingConstraint(processorName, processorId)
    
    def visit___taskIdentifier(self, node, children):
        name = str(node)
        return name
    
    def visit___peIdentifier(self, node, children):
        name = str(node)
        return name
    
class Constraint(ABC):
    @abstractmethod
    def isFulFilled(self, mapping):
        pass
    
class MappingConstraint(Constraint):
    def __init__(self, processName, processId, processorName, processorId):
        self.__processName = processName
        self.__processId = processId
        self.__processorName = processorName
        self.__processorId = processorId
    
    def isFulFilled(self, mapping):
        if not isinstance(mapping, list):
            raise RuntimeWarning("SimpleVector representation is needed to evaluate constraint!")
        else:
            if mapping[self.__processId] == self.__processorId:
                return True
        return False
    
    def setEntry(self, partialMapping):
        partialMapping[self.__processId] = self.__processorId
        
class ProcessingConstraint(Constraint):
    def __init__(self, processorName, processorId):
        self.__processorName = processorName
        self.__processorId = processorId
    
    def isFulFilled(self, mapping):
        #TODO:
        #-> Check if mapping is in simple vector representation
        #-> Check if core is processing using this mapping
        if not isinstance(mapping, list):
            raise RuntimeWarning("SimpleVector representation is needed to evaluate constraint!")
        else:
            if self.__processorId in mapping:
                return True
        return False
    
            






    
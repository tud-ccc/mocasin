#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from builtins import staticmethod
from arpeggio import OrderedChoice, EOF, PTNodeVisitor
from arpeggio import RegExMatch as _
from abc import ABC, abstractmethod

class Grammar():
    @staticmethod
    def __identifier(): return  _(r'([ab-z]|[AB-Z])(([ab-z]|[AB-z]|[0-9]|\_)*)')
    
    @staticmethod
    def __processingOp(): return (Grammar.__identifier, ("PROCESSING"))
    
    @staticmethod
    def __mappingOp(): return (Grammar.__identifier, ("MAPPED"), Grammar.__identifier)
    
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
    def visit_logicLanguage(self, node, children):
        return children[0]
    
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
                result.append([children[0]])
                if isinstance(children[2], list):
                    for constraintSetR in children[2]:
                        if isinstance(constraintSetR, list):
                            for constraint in constraintSetR:
                                result[0].append(constraint)
                        else:
                            result[0].append(constraintSetR)
                else:
                    result[0].append(children[2])
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
        return MappingContstraint(children[0], children[1])
    
    def visit___processingOp(self, node, children):
        return ProcessingConstraint(children[0])
    
    def visit___identifier(self, node, children):
        return str(node)
    
class Constraint(ABC):
    @abstractmethod
    def isFulFilled(self, mapping):
        pass
    
class MappingContstraint(Constraint):
    def __init__(self, processName, peName):
        self.__processName = processName
        self.__peName = peName
    
    def isFulFilled(self, mapping):
        #TODO:
        # -> Check if Mapping is in simple vector representation
        # -> Check if process is mapped on core
        pass
    
class ProcessingConstraint(Constraint):
    def __init__(self, peName):
        self.__peName = peName
    
    def isFulFilled(self, mapping):
        #TODO:
        #-> Check if mapping is in simple vector representation
        #-> Check if core is processing using this mapping
        pass
    
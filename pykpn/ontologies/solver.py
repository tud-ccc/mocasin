#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from pykpn.mapper.random import RandomMapping

class RandomSolver():
    def __init__(self, kpnGraph, platform):
        self.__kpn = kpnGraph
        self.__platform = platform
        self.__mapping = RandomMapping(self.__kpn, self.__platform).to_list()
    
    def generateNewMapping(self):
        self.__mapping = RandomMapping(self.__kpn, self.__platform).to_list()
      
    def solveQuery(self, query):
        for constraintSet in query:
            setFulfilled = True
            for constraint in constraintSet:
                if not constraint.isFulFilled(self.__mapping):
                    setFulfilled = False
            if setFulfilled:
                return True
        return False
        
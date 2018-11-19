"""Containing classes that are just needed for testing issues.
"""
import sys
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.mapper.random import RandomMapping
from random import Random

class dataProvider():
    def __init__(self, platform):
        self.__mPlatform = platform
        
        gettrace = getattr(sys, 'gettrace', None)
        self.__path = None
        if gettrace is None:
            self.__path = sys.path[1] + "/apps/audio_filter.cpn.xml"
        elif gettrace():
            """In case of an attached debugger the sys.path list will change
            """
            self.__path = sys.path[2] + "/apps"
        else:
            self.__path = sys.path[1] + "/apps"
        
        self.__mKpnInstance = self.__kpnInstance = SlxKpnGraph('SlxKpnGraph',self.__path + '/audio_filter.cpn.xml','2017.04')
        self.__mGenerator = Random()
    
    def generateRandomMapping(self):
        return RandomMapping(self.__mKpnInstance, self.__mPlatform)
    
    def generatePossibleMapping(self, usedCores):
        mapping = RandomMapping(self.__kpnInstance, self.__mPlatform)
        coreDict = mapping.to_coreDict()
        possibleCores = []
        for key  in coreDict:
            if not key in usedCores:
                possibleCores.append(key)
        for key in coreDict:
            if key in usedCores and coreDict[key] != []:
                for process in coreDict[key]:
                    rndInt = self.__mGenerator.randint(0, len(possibleCores) - 1)
                    mapping.change_affinity(process, possibleCores[rndInt])
        return mapping
        
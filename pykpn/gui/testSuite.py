"""Containing classes that are just needed for testing issues.
"""
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.mapper.random import RandomMapping
from random import Random

class dataProvider():
    def __init__(self, platform):
        self.__mPlatform = platform
        
        self.__mKpnInstance = self.__kpnInstance = SlxKpnGraph('SlxKpnGraph','/net/home/teweleit/eclipse-workspace/pykpn/pykpn/apps/audio_filter/audio_filter.cpn.xml','2017.04')
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
        
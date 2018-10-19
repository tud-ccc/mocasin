#author Felix Teweleit
from pykpn.gui.utils import platformOperations

class mappingInformation():
    def __init__(self, mappingObject, identifier, color):
        self.__mMappingObject = mappingObject
        self.__mappingDescription = mappingObject.to_coreDict()
        self.__mappingId = identifier
        self.__color = color
        self.__circleHandles = []
        self.__nameHandles = {}
        
    def addCircleHandle(self, handle):
        self.__circleHandles.append(handle)
        return
    
    def getCircleHandles(self):
        return self.__circleHandles
    
    def addNameHandle(self, handle, name):
        self.__nameHandles.update({handle : name})
        return
    
    def getNameHandles(self):
        return self.__nameHandles
    
    def clearHandles(self):
        self.__circleHandles.clear()
        self.__nameHandles.clear()
    
    def getColor(self):
        return self.__color
    
    def getMappingDescription(self):
        return self.__mappingDescription
    
    def getMappingId(self):
        return self.__mappingId

    def changeAffinity(self, circleHandle, peName):
        processName = self.__nameHandles[circleHandle + 1]
        self.__mMappingObject.change_affinity(processName, peName)
        self.__mappingDescription = self.__mMappingObject.to_coreDict()
        return

class platformInformation():
    def __init__(self, platformObject):
        self.__mPlatformObject = platformObject
        self.__createPlatformDescription(platformObject)
        self.__coreDictionary = {}
        self.__coreClasses = []
                
    def __createPlatformDescription(self, platformObject):
        description = platformOperations.getPlatformDescription(platformOperations, platformObject.processors(), platformObject.primitives())    
        
        #check if this platform contains a network on chip
        networkOnChip = False
        self.__mEqualList = platformOperations.findEqualPrimitives(platformOperations, platformObject)
        description = platformOperations.mergeEqualPrimitives(platformOperations, description, self.__mEqualList) 
        for equalSheet in self.__mEqualList:
            if len(equalSheet) > 2:
                    networkOnChip = True
        if networkOnChip:         
            description = platformOperations.createNocMatrix(platformOperations, description, platformObject)
            
        self.__mPlatformDescription = description
        
    def getPlatformDescription(self):
        return self.__mPlatformDescription
    
    def addCoreClass(self,length):
        i = 0
        isInserted = False
        if self.__coreClasses == []:
                self.__coreClasses.append(length)
                return
        for entry in self.__coreClasses:
            if entry == length:
                return
            elif entry < length:
                i += 1
            else:
                self.__coreClasses.insert(i, length)
                isInserted = True
        if not isInserted:
            self.__coreClasses.insert(i, length)
        return

    def getCoreClasses(self):
        return self.__coreClasses
       
    def updateCoreDict(self, key, value):
        self.__coreDictionary.update({key : value})
        
    def getCoreDict(self):
        return self.__coreDictionary
        
        
        
        
        
        
# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.gui.utils import platformOperations, listOperations

class mappingInformation():
    """Data object that holds the necessary information to draw a mapping.
    :ivar Mapping __mMappingObject: The actual pykpn Mapping object.
    :ivar {str, list[str]} __mappingDescription: A dictionary with core names as key and a list of applied process names as value.
    :ivar int __mappingId: The id given to the mapping by the user.
    :ivar string __color: The Tkinter color value in which the mapping dots should be drawn.
    :ivar list[int] __circleHandles: A list of handles of the drawn mapping dots given by a Tkinter Canvas.
    :ivar dict{int, str} __nameHandles: A dictionary with handles of displayed process names as key and the name of the process as value.
    """
    def __init__(self, mappingObject, identifier, color):
        """Initializes a mappingInformation object.
        :param Mapping mappingObject: The pykpn Mapping object which should be visualized.
        :param int identifier: The id of the mapping given by the user.
        :param str color: The color in which the mapping should be drawn. Can be set by user or uses a color of the default color vector.
        """
        self.__mMappingObject = mappingObject
        self.__mappingDescription = mappingObject.to_coreDict()
        self.__mappingId = identifier
        self.__color = color
        self.__circleHandles = []
        self.__nameHandles = {}
        
    def addCircleHandle(self, handle):
        """Adds a ne handle to the list of circle handles.
        :param int handle: The handle that should be added.
        """
        self.__circleHandles.append(handle)
        return
    
    def getCircleHandles(self):
        """Returns the list of circle handles.
        :returns: The list of circle handles.
        :rtype list[int]:
        """
        return self.__circleHandles
    
    def addNameHandle(self, handle, name):
        """Adds an entry to the __nameHandles dict.
        :param int handle: The handle that should be added as key.
        :param str name: The process name that should be added as value.
        """
        self.__nameHandles.update({handle : name})
        return
    
    def getNameHandles(self):
        """Returns the __nameHandle dict.
        :returns: The __nameHandle dictionary.
        :rtype {int, str}:
        """
        return self.__nameHandles
    
    def clearHandles(self):
        """Resets the __circleHandles list and the __nameHandles dictionary.
        """
        self.__circleHandles.clear()
        self.__nameHandles.clear()
    
    def getColor(self):
        """Returns the color value of the mappingInformation object.
        :returns: The Tkinter color value __color.
        :rtype str:
        """
        return self.__color
    
    def getMappingDescription(self):
        """Returns the mapping description dictionary of the mappingInformation object.
        :returns: The __mappingDescription dictionary.
        :rtype dict{int, str}: 
        """
        return self.__mappingDescription
    
    def getMappingId(self):
        """Returns the ID of the mappingInformation object.
        :returns: The __mappingId value.
        :rtype int:
        """
        return self.__mappingId

    def changeAffinity(self, circleHandle, peName):
        """Wrapper method to the changeAffinity method of the pykpn Mapping object.
        :param int circleHandle: The handle of the mapping dot for which  the affinity should be changed.
        :param str peName: The name of the processing element for which the new affinity should be set.
        """
        processName = self.__nameHandles[circleHandle + 1]
        self.__mMappingObject.change_affinity(processName, peName)
        self.__mappingDescription = self.__mMappingObject.to_coreDict()
        return


class TRMVplatformInformation():
    """Data object that holds all necessary information to draw a platform.
    :ivar Platform platformObject: The platform object which should be drawn.
    :ivar list[(str, list[str])] __platformDescription: The description of the platform that can be interpreted by the drawManager class.
    :ivar dict{str, list[int]} __coreDictionary: A dictionary with the name o    f the core as key and the start x and y value and the end x and y value and 
                                                 the handle given by the Canvas as values.
    :ivar list[int] __coreClasses: A list that has an entry for every core size that appears in the platform structure.
    """
    def __init__(self, platformObject):
        """Initializes a platformInformation object.
        :param Platform platformObject: The pykpn Platform object that should be drawn.
        """
        self.__mPlatformObject = platformObject
        self.__createPlatformDescription(platformObject)
        self.__coreDictionary = {}
        self.__coreClasses = []
                
    def __createPlatformDescription(self, platformObject):
        """Creates the hierarchic platform description that can be interpreted by the drawManager.
        :param Platform platformObject: The pykpn Platform object for which the description should be created.
        """
        description = platformOperations.getPlatformDescription(platformObject.processors(), platformObject.primitives())    
        
        self.__mEqualList = platformOperations.findEqualPrimitives(platformObject)
        description = platformOperations.mergeEqualPrimitives(description, self.__mEqualList) 
        
        networkOnChip = False
        for equalSheet in self.__mEqualList:
            if len(equalSheet) > 2:
                    networkOnChip = True
        if networkOnChip:         
            description = platformOperations.createNocMatrix(description, platformObject)
            
        self.__platformDescription = description
        
    def getPlatformDescription(self):
        """Returns the platformDescription.
        :returns: The __platformDescription value.
        :rtype list[(str, [list])]:
        """
        return self.__platformDescription
    
    def addCoreClass(self,length):
        """Adds a size of processing elements to the list of existing sizes of processing elements.
        :param int length: The size of the processing element that should be appended.
        """
        if not length in self.__coreClasses:
            self.__coreClasses.append(length)

    def getCoreClasses(self):
        """Returns the list of existing sizes of processing elements.
        :returns: The __coreClasses value.
        :rtype list[int]:
        """
        return self.__coreClasses
       
    def updateCoreDict(self, key, value):
        """Adds an entry to the coreDictionary.
        :param str key: The name of the processing element.
        :param list[int] value: A list of integers containing start x and y value, end x and y value, the handle and the color of the processing element in this order.
        """
        self.__coreDictionary.update({key : value})
        
    def getCoreDict(self):
        """Returns the dictionary of existing processing elements.
        :returns: The __coreDictionary value.
        :rtype dict{str, list[int]}
        """
        return self.__coreDictionary
    
    def clearHandles(self):
        """Clears the dictionary containing all information about the drawn cores in case the platform has to be redrawn
        """
        self.__coreDictionary.clear() 
     
     
class PlatformInformation():
    def __init__(self, platform):
        self.__platformObject = platform
        self.__clusterDict = {}
        self.__primitiveDict = {}
        self.__coreDict = {}
        
        self.__nextClusterId = 0
        self.__L1Prims = []
        
        self.__coreClasses = []
        
        self.__extractPlatformInformation(platform)
        
    def getPlatformObject(self):
        return self.__platformObject
    
    def getClusterDict(self):
        return self.__clusterDict
    
    def getPrimitiveDict(self):
        return self.__primitiveDict
    
    def updateCoreDict(self, key, value):
        self.__coreDict.update({key : value})
    
    def getCoreDict(self):
        return self.__coreDict
    
    def addCoreClass(self,length):
        """Adds a size of processing elements to the list of existing sizes of processing elements.
        :param int length: The size of the processing element that should be appended.
        """
        if not length in self.__coreClasses:
            self.__coreClasses.append(length)
    
    def getCoreClasses(self):
        return self.__coreClasses
    
    def __extractPlatformInformation(self, platform):
        primitives = list(platform.primitives())
        self.__findClusters(primitives)
        
        for prim in self.__L1Prims:
            pe = prim.producers[0].name
            for key in self.__clusterDict:
                if pe in self.__clusterDict[key][0]:
                    self.__clusterDict[key][3] = True
                    
        for key in self.__clusterDict: 
            if len(self.__clusterDict[key][1]) == len(self.__clusterDict[key][0]):
                self.__clusterDict[key][2] = True
                self.__clusterDict[key][1] = ['network_on_chip']
            
            elif len(self.__clusterDict[key][1]) < len(self.__clusterDict[key][0]):
                self.__clusterDict[key][4] = True
                self.__clusterDict[key][1] = ['L2_Cache']
            
            elif len(self.__clusterDict[key][1]) > len(self.__clusterDict[key][0]):
                self.__clusterDict[key][2] = True
                self.__clusterDict[key][4] = True
                self.__clusterDict[key][1] = ['network_on_chip']
        
        toRemove  = []
        for key in self.__primitiveDict:
            if key in toRemove:
                continue
            clusterList = self.__primitiveDict[key]
            for innerKey in self.__primitiveDict:
                if not key == innerKey and clusterList == self.__primitiveDict[innerKey]:
                    toRemove.append(innerKey)
        for key in toRemove:
            self.__primitiveDict.pop(key)
        
    def __findClusters(self, primitives):
        smallestPrim = None
        
        for prim in primitives:
            if smallestPrim == None:
                smallestPrim = prim
                continue
            else:
                if len(prim.producers) < len(smallestPrim.producers):
                    smallestPrim = prim
        
        
        if len(smallestPrim.producers) > 1: 
        
            toAdd = True
            belongingClusters = []
        
            for key in self.__clusterDict:
                peList = self.__clusterDict[key][0]
                for processor in smallestPrim.producers:
                    if processor.name in peList and not key in belongingClusters:
                        toAdd = False
                        belongingClusters.append(key)
                    
            if toAdd:
                peNames = []
                for processor in smallestPrim.producers:
                    peNames.append(processor.name)
                self.__clusterDict.update({ self.__nextClusterId : [peNames, [smallestPrim.name], False, False, False] })
                self.__nextClusterId += 1
        
            else:
                if len(belongingClusters) == 1:
                    self.__clusterDict[belongingClusters[0]][1].append(smallestPrim.name)
                else:
                    self.__primitiveDict.update({ smallestPrim.name : belongingClusters})
                
                
        else:
            self.__L1Prims.append(smallestPrim)
        
        primitives.remove(smallestPrim)
        if len(primitives) > 0:
            self.__findClusters(primitives)
            
    
class platformLayout:
    
    def __init__(self, dimension, slotSizeX, slotSizeY):
        """Inner layout: [Free, startX, EndX, startY, endY, clusterID]
        """
        self.__dimension = dimension
        self.__slotSizeX = slotSizeX
        self.__slotSizeY = slotSizeY
        self.__layout = []
        self.__primList = []
        self.__blankLayout()
        self.__primDict = {}

        self.__nameStack = []
        self.__currentName = None
        
        #Bad design, change later
        self.nextId = 0

    def __blankLayout(self):
        """Initialize blank layout
        """
        for i in range(0, self.__dimension):
            self.__layout.append([])
            for j in range(0, self.__dimension):
                self.__layout[i].append([True, None,
                                         j * self.__slotSizeX,
                                         i * self.__slotSizeY,
                                         (j + 1) * self.__slotSizeX,
                                         (i + 1 ) * self.__slotSizeY])
    
    def addPrimitives(self, primDescription):
        """Add new Informations to the adjacency List
        """
        tmpPrimDescription = dict(primDescription)
        
        while not tmpPrimDescription == {}:
            longestKey = None
            for key in tmpPrimDescription:
                if longestKey == None:
                    longestKey = key
                else:
                    if len(tmpPrimDescription[key]) > len(tmpPrimDescription[longestKey]):
                        longestKey = key
            
            if self.__primList == []:
                self.__primList = tmpPrimDescription[longestKey]
                
            else:
                self.__primList = self.sortIn(tmpPrimDescription[longestKey], self.__primList)
            tmpPrimDescription.pop(longestKey, None)
            self.__nameStack.append(longestKey)
        
        self.assignSlots(self.__primList)
           
    def sortIn(self, smallerList, biggerList):
        innerList = None
        atThisLevel = False
        toRemove = []
        for item in biggerList:
            if isinstance(item, list):
                if listOperations.containsItem(item, smallerList[0]):
                    innerList = item
            else:
                if item in smallerList:
                    toRemove.append(item)
                    atThisLevel = True
        if atThisLevel:
            for item in toRemove:
                biggerList.remove(item)
            biggerList.append(smallerList)
        if not innerList == None:
            biggerList.remove(innerList)
            biggerList.append(self.sortIn(smallerList, innerList))
        return biggerList
    
    def assignSlots(self, clusterList):
        toAssign = []
        lowerPrimitives = []
        for element in clusterList:
            if isinstance(element, list):
                for idx in self.assignSlots(element):
                    lowerPrimitives.append(idx)
            else:
                toAssign.append(element)
        
        
        if len(toAssign) == 0:
            if not lowerPrimitives == []:
                self.__primDict.update({ self.nextId : []})
                for idx in lowerPrimitives:
                    for value in self.__primDict[idx]:
                        self.__primDict[self.nextId].append(value)
                self.nextId += 1
                return [self.nextId - 1]
        else:
            for i in range(0, self.__dimension):
                if i % 2 == 0:
                    for j in range(0, self.__dimension):
                        if self.__layout[i][j][0]:
                            remaining = len(toAssign) - 1
                            path = [(i,j)]
                            posX = j
                            posY = i
                            while(remaining > 0):
                                if posX < self.__dimension - 1 and self.__layout[posY][posX+1][0]:
                                    posX += 1
                                    path.append((posY, posX))
                                    remaining -= 1
                                elif posY < self.__dimension - 1 and self.__layout[posY+1][posX][0]:
                                    posY += 1
                                    path.append((posY, posX))
                                    remaining -= 1
                                else:
                                    break
                            if remaining == 0:
                                if not self.nextId in self.__primDict:
                                    self.__primDict.update( {self.nextId : [ ]} )
                            
                                for idx in lowerPrimitives:
                                    for entry in self.__primDict[idx]:
                                        self.__primDict[self.nextId].append(entry)
                            
                                if len(toAssign) != len(path):
                                    raise RuntimeError("Something went wrong!")
                                else:
                                    for idx in range(0, len(toAssign)):
                                        self.__layout[path[idx][0]][path[idx][1]][0] = False
                                        self.__layout[path[idx][0]][path[idx][1]][1] = toAssign[idx]
                                    
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][2])
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][3])
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][4])
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][5])
                            
                                lowerPrimitives.append(self.nextId)
                                self.nextId += 1
                                return lowerPrimitives
                else:
                    for j in range(self.__dimension-1, -1, -1):
                        if self.__layout[i][j][0]:
                            remaining = len(toAssign) - 1
                            path = [(i,j)]
                            posX = j
                            posY = i
                            while(remaining > 0):
                                if posX > 0 and self.__layout[posY][posX-1][0]:
                                    posX -= 1
                                    path.append((posY, posX))
                                    remaining -= 1
                                elif posY < self.__dimension - 1 and self.__layout[posY+1][posX][0]:
                                    posY += 1
                                    path.append((posY, posX))
                                    remaining -= 1
                                else:
                                    break
                            if remaining == 0:
                                if not self.nextId in self.__primDict:
                                    self.__primDict.update( {self.nextId : [ ]} )
                            
                                for idx in lowerPrimitives:
                                    for entry in self.__primDict[idx]:
                                        self.__primDict[self.nextId].append(entry)
                            
                                if len(toAssign) != len(path):
                                    raise RuntimeError("Something went wrong!")
                                else:
                                    for idx in range(0, len(toAssign)):
                                        self.__layout[path[idx][0]][path[idx][1]][0] = False
                                        self.__layout[path[idx][0]][path[idx][1]][1] = toAssign[idx]
                                        
                                        """Insert x and y values in swapped order and revert the whole list 
                                        in the end. So it can be read from left to right later on.
                                        """
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][5])
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][4])
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][3])
                                        self.__primDict[self.nextId].append(self.__layout[path[idx][0]][path[idx][1]][2])
                                
                                self.__primDict[self.nextId].reverse()
                                lowerPrimitives.append(self.nextId)
                                self.nextId += 1
                                return lowerPrimitives
                    
        return lowerPrimitives
    
    def getLayout(self):
        for i in range(0, self.__dimension):
            for j in range(0, self.__dimension):
                try:
                    yield self.__layout[i][j]
                except:
                    print("Failure!")
                    
    def getPrimitives(self):
        #just an unrealistic large number, so dict entries are smaller
        n = 0
        usedKeys = []
        while( n < len(self.__primDict)):
            actualKey = None
            for key in self.__primDict:
                if actualKey == None and not key in usedKeys:
                    actualKey = key
                else:
                    if actualKey == None:
                        continue
                    if len(self.__primDict[key]) > len(self.__primDict[actualKey]) and not key in usedKeys:
                        actualKey = key
            n += 1
            usedKeys.append(actualKey)
            yield (actualKey, self.__primDict[actualKey])
                    
        
        
        
    
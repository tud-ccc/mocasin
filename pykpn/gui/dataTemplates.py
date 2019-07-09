# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.gui.utils import platformOperations

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

class platformInformation():
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
        
        
        
        
        
        
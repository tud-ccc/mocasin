#author Felix Teweleit
from pykpn.gui.dataTemplates import mappingInformation
from pykpn.gui.dataTemplates import platformInformation
from pykpn.gui.managers import drawManager

class drawAPI():
    """"Main interface for the user to visualize platforms and mapped processes.
    
    :ivar platformInformation __mPlatform: The platform that should be visualized.
    :ivar bool __drawOnlyPEs: States if the whole
    :ivar dict {int, mappingInformation} __mMappings: Dict of processes mapped on the platform.
    :ivar list [str] __usedCores: List of cores which are already in use by other processes. 
    :ivar drawManager __mDrawManager: Does the actual visualization.
    """
    def __init__(self, canvas, border, scaling, width, height, **kwargs):
        """"Initialize the api.
        :param Canvas canvas: A Tkinter canvas from the GUI of the user. Everything will be drawn in this canvas.
        :param int border: Defines the space between components of the platform and the canvas edge and between components themselves.
        :param int scaling: Should be less than one. Defines which percentage of remaining Space components will use.
        :param int width: The width of the canvas.
        :param int height: The height of the canvas.
        :param kwargs: Is valid for parameters:
                        :int textSpace: The space on the bottom of processing elements that is reserved for their names.
                        :int fontSize: The size of the font all names are displayed in.
        """
        self.__mPlatform = None
        self.__drawOnlyPEs = None
        self.__mMappings = {}
        self.__usedCores = []
        self.__mDrawManager = drawManager(self, canvas, border, scaling, width, height, **kwargs)
        
     
     
    """
    Methods that can be called by the user.
    """
       
    def setPlatform(self, platform, drawOnlyPEs = False):
        """Analysis and draws the given platform.
        :param SlxPlatform platform: The pykpn platform object.
        :param bool drawOnlyPEs: Defines if the drawManager should only draw the PEs of the platform
        """ 
        if self.__mPlatform == None:
            self.__mPlatform = platformInformation(platform)
        else:
            self.__mMappings.clear()
            self.__mPlatform = platformInformation(platform)
        
        self.__mDrawManager.drawPlatform(drawOnlyPEs)
        self.__drawOnlyPEs = drawOnlyPEs
        return

    def addMapping(self, mapping, mappingID, color = 'default'):
        """Applies the mapping for a given application to the platform.
        :param Mapping mapping: The pykpn mapping object that should be applied.
        :param int mappingID: The ID for the mapping so the api can identify it.
        :param str color: A Tkinter color value. The dots of the mapping will be drawn in this color.
                        If not given, a default color will be applied.
        """
        if self.__mPlatform == None:
            raise RuntimeWarning('Can not add a mapping if no platform is specified')
            return
        
        if not mappingID in self.__mMappings and isinstance(mappingID, int):
            key = mappingID
            if not color == 'default':
                mappingColor = color
            else:
                mappingColor = self.__mDrawManager.getColorForMapping()
            if mappingColor != None:
                value = mappingInformation(mapping, mappingID, mappingColor)
                self.__mMappings.update({key : value})
                self.__mDrawManager.drawMappings()
            else:
                raise RuntimeWarning('Could not add mapping  because no color was available!')
        else:
            raise RuntimeWarning('Mapping ID already exists or is not valid!')
        
        return
    
    def removeMapping(self, mappingID):
        """Removes the mapping with the given ID.
        :param int mappingID: The ID of the mapping that should be removed.
        """
        if not mappingID in self.__mMappings:
            raise RuntimeWarning('This ID is currently not in use!')
        else:
            self.__mDrawManager.clearMappings()
            color = self.__mMappings[mappingID].getColor()
            self.__mDrawManager.addingAvailableColor(color)
            del self.__mMappings[mappingID]
            self.__mDrawManager.drawMappings()
        return
    
    def setUsedCores(self, coreList):
        """Set the list of processing elements that are already used by a process.
        :param list[str]: The names of processing elements which should be added. 
        """
        self.__usedCores = coreList
        self.__mDrawManager.clearMappings()
        self.__mDrawManager.drawMappings()
        return
    
    def getUsedCores(self):
        """Returns the list of processing elements already used by a process.
        :returns: A list containing the names of the processing elements.
        :rtype list[str]:
        """
        return self.__usedCores
    
    def setColorVectors(self, platformVector = ['default'], mappingVector = ['default'], peVector = ['default']):
        """Set custom default colors for platform components, mappings and processing elements.
        :param list[str] platformVector: A list of Tkinter color values. Is used for default platform colors.
        :param list[str] mappingVector: A list of Tkinter color values. Is used for default mapping colors.
        :param list[str] peVector: A list of Tkinter color values. Is used for default processing element colors.
        """
        self.__mDrawManager.setColorVectors(platformVector, mappingVector, peVector)
    
    def toggleTaskNames(self):
        """Hides or shows the names of the tasks of a applied mapping.
        """
        self.__mDrawManager.toggleTaskNames()
    
    def togglePENames(self):
        """Hides or shows the names of the processing elements. Redraws everything on the canvas after call.
        """
        self.__mDrawManager.togglePENames()
        
        if self.__mPlatform != None:
            self.__mPlatform.clearHandles()
        
        if self.__drawOnlyPEs != None:
            self.__mDrawManager.drawPlatform(self.__drawOnlyPEs)
            self.__mDrawManager.drawMappings()
        
    
    def toggleDragAndDrop(self):
        """Enables or disables the editing of mappings via drag and drop.
        """
        self.__mDrawManager.toggleDragAndDrop()
    
    def getPlatform(self):
        """
        :returns: The platformInformation object hold by the api.
        :rtype platformInformation:
        """
        return self.__mPlatform     
        
    def getMappings(self):
        """
        :returns: The dictionary of applied mappings and their IDs.
        :rtype dict[int, mappingInformation]:
        """
        return self.__mMappings
    
    
    
    
    
    
    
    
    
    
    
    
    
       
        
        
        
from pykpn.gui import drawAPI
from pykpn.gui.utils import listOperations
import tkinter as tk


class tetrisEngine():
    """Main interface for an engine which makes the tetris algorithm playable as a game
    :ivar list[list[optionPanel]] __mPanelMatrix: A matrix of panels where the different possible mappings are shown.
    :ivar tetrisPanel __mTetrisPanel: The main panel which draws the whole platform and all applied mappings.
    :ivar int __optionAmount: Saves the given amount of possible options.
    """
    def __init__(self, tkFrame, width, height, optionAmount):
        """Initializes the engine.
        :param tkinter.Frame tkFrame: The frame of the Tkinter Window in which the game will be played.
        :param int width: The width of the frame.
        :param int height: The height of the frame.
        :param int optionAmount: The amount of different mappings that will be available at  one time.
        """
        dimension = self.__createOptionPanel(optionAmount, tkFrame, height, width)
        tkFrame.focus_set()
        tkFrame.bind("<Key>", self.__keyPressed)
        self.__mTetrisPanel = tetrisPanel(tkFrame, width, height, dimension)
        self.__optionAmount = optionAmount
    
    def setPlatform(self, platform, mapping = None):
        """Sets the platform for all initialized panels.
        :param SlxPlatform platform: The platform that should be set for all panels. 
        :param Mapping mapping: An optional initial mapping for the platform, defining already used cores.
        """
        self.__mTetrisPanel.setPlatform(platform)
        if mapping != None:
            self.__mTetrisPanel.applyInitialMapping(mapping)
        for row in self.__panelMatrix:
            for panel in row:
                panel.setPlatform(platform)
        return
    
    def __keyPressed(self, event):
        print('Pressed key!')
    
    def setMappingOption(self, mappingList):
        """Applies mappings on all optionPanels initialized
        :param list[Mapping] mappingList: The list of mappings that should be applied on different panels.
        """
        if len(mappingList) > self.__optionAmount:
            raise RuntimeError('To many options given for the amount of option panels!')
        else:
            i = 0
            for row in self.__panelMatrix:
                for panel in row:
                    panel.setMappingOption(mappingList[i])
                    i += 1
        return
    
    def __createOptionPanel(self, optionAmount, tkFrame, height, width):
        """Creates the matrix of optionPanels out of the given amount.
        :param int optionAmount: The total amount of available optionPanels.
        :param tkinter.Frame tkFrame: The frame of the Tkinter Window in which the game will be played.
        :param int height: The height of the frame.
        :param int width: The width of the frame.
        :returns: The maximal dimension of the created matrix.
        :rtype int:
        """
        i = 0
        panels = []
        while i < optionAmount:
            i += 1
            panels.append(optionPanel(tkFrame, i))
        self.__panelMatrix = listOperations.convertToMatrix(listOperations, panels)
        
        dimension = listOperations.getDimension(listOperations, self.__panelMatrix)
        
        panelWidth = width / (2 * dimension)
        panelHeight = height / dimension
        i = 0
        j = 1
        for row in self.__panelMatrix:
            for entry in row:
                entry.setParameters(panelWidth, panelHeight, i, j)
                j += 1
            j = 1
            i += 1
        return dimension

class tetrisPanel():
    """The panel of the engine where the whole platform and all applied mappings will be drawn.
    :ivar tkinter.Frame __mMainFrame: The frame of the Tkinter Window in which the game will be played.
    :ivar tkinter.Canvas __mCanvas: The canvas in which an instance of the drawAPI will work.
    :ivar drawAPI __mApiInstance: The instance of the drawAPI needed for visualization.
    :ivar list[str] __usedCores: A list containing all names of cores which are already used by a process.
    :ivar Mapping __appliedMapping: The mapping currently applied by the user.
    """
    def __init__(self, tkFrame, width, height, dimension):
        """Initializes the tetrisPanel.
        :param tkinter.Frame tkFrame: The frame of the Tkinter Window in which the game will be played.
        :param int width: The width of the frame.
        :param int height: The height of the frame.
        :param int dimension: The maximal dimension of the optionPanel matrix. Needed to define the rowspan.
        """
        drawWidth = width / 2
        drawHeight = height
        self.__mMainFrame = tkFrame
        self.__mCanvas = tk.Canvas(self.__mMainFrame, width = drawWidth, height = drawHeight)
        self.__mCanvas.grid(row = 0, column = 0, rowspan = dimension)
        self.__mApiInstance = drawAPI.drawAPI(self.__mCanvas, 5, 15, drawWidth, drawHeight)
        
        self.__usedCores = []
        self.__appliedMapping = None
        
    def applyInitialMapping(self, mapping):
        """Converts a mapping in a list of cores used by this mapping.
        :param Mapping mapping: The mapping that should be converted.
        """
        if mapping != None:
            coreDict = mapping.to_coreDict()
            for key in coreDict:
                if coreDict[key] != []:
                    self.__usedCores.append(key)
        self.__mApiInstance.setUsedCores(self.__usedCores)
        return
    
    def setPlatform(self, platform):
        """Applies a platform to the drawAPI instance of the tetrisPanel.
        :param SlxPlatform platform: The platform that should be applied.
        """
        self.__mApiInstance.setPlatform(platform)
        return
    
    def applyMapping(self, mapping):
        """Removes the currently applied mapping if there is one and applies a new one.
        :param Mapping mapping: The new mapping that should be applied.
        """
        if self.__appliedMapping == None:
            self.__mApiInstance.addMapping(mapping, 0)
        else:
            self.__mApiInstance.removeMapping(0)
            self.__mApiInstance.addMapping(mapping, 0)
            self.__appliedMapping = mapping
        return
    
    def finalizeMapping(self):
        """Removes the currently applied mapping and adds every core used by this mapping to the list of used cores.
        """
        for key in self.__appliedMapping.to_coreDict():
            if not key in self.__usedCores:
                self.__usedCores.append(key)
        self.__mApiInstance.removeMapping(0)
        self.__appliedMapping = None
        self.__mApiInstance.setUsedCores(self.__usedCores)
        return
    
class optionPanel():
    """A panel where the PE's of a platform will be drawn in order to show optional mappings on them.
    :ivar tkinter.Frame __mMainFrame: The frame of the Tkinter Window in which the game will be played.
    :ivar int __id: The id of the panel to distinguish different optionPanels.
    :ivar Mapping __mActualMapping: The mapping currently shown as possible option.
    :ivar tkinter.Canvas __mCanvas: The canvas the drawAPI will use for the visualization.
    :ivar drawAPI __mApiInstance: The instance of the drawAPI needed for visualization.
    """
    def __init__(self, tkFrame, panelId):
        """Initializes a optionPanel.
        :param tkinter.Frame: The frame of the Tkinter Window in which the game will be played.
        :param int panelId: The id for the panel.
        """
        self.__mMainFrame = tkFrame
        self.__id = panelId
        self.__mActualMapping = None
    
    def setParameters(self, pWidth, pHeight, assignedRow, assignedColumn):
        """Sets the necessary parameters for an optionPanel to finish its initialization.
        :param int pWidth: The width available for the panel.
        :param int pHeight: The height available for the panel.
        :param int assignedRow: The row in the grid of the frame which the panel will take.
        :param int assignedColumn: The column of the grid of the frame which the panel will take.
        """
        self.__mCanvas = tk.Canvas(self.__mMainFrame, width = pWidth, height = pHeight, bg = 'white')
        self.__mCanvas.grid(row = assignedRow, column = assignedColumn)
        self.__mCanvas.create_rectangle(0, 0, pWidth/15, pHeight/15, width=3)
        self.__mCanvas.create_text(pWidth/30, pHeight/30, text=self.__id)
        self.__mApiInstance = drawAPI.drawAPI(self.__mCanvas, 5, 10, pWidth, pHeight)
        return
    
    def setPlatform(self, platform):
        """Sets the platform of the drawAPI instance, but only draws the processing elements of the platform.
        :param SlxPlatform platform: The platform that will be set.
        """
        self.__mApiInstance.setPlatform(platform, True)
        return
    
    def setMappingOption(self, mapping):
        """Applies an mapping on the processing elements as possible option.
        :param Mapping mapping: The mapping that will be applied.
        """
        self.clearMappingOption()
        self.__mActualMapping = mapping
        self.__mApiInstance.addMapping(mapping, 0)
    
    def getMappingOption(self):
        """Returns the actual, as option, applied mapping.
        :returns: The mapping object.
        :rtype Mapping:
        """
        return self.__mActualMapping
    
    def clearMappingOption(self):
        """Removes the currently applied mapping option.
        """
        if self.__mActualMapping != None:
            self.__mActualMapping = None
            self.__mApiInstance.removeMapping(0)
        
        
        
        
        
        
from pykpn.gui import drawAPI
from pykpn.gui.utils import listOperations
from pykpn.gui.testSuite import dataProvider
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
        self.__panelMatrix = None
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
        self.__mDataProvider = dataProvider(platform)
        if mapping != None:
            self.__mTetrisPanel.applyInitialMapping(mapping)
        for row in self.__panelMatrix:
            for panel in row:
                panel.setPlatform(platform)
        return
    
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
    
    def toggleTaskNames(self, target = 'default'):
        """Toggle if the names of the different tasks of the mappings should be shown or not.
        :param str target: Defines if the call targets:
                            default -> the main panel and all option panels.
                            mainPanel -> only the main panel.
                            optionPanel -> all option panels.
        """
        if target == 'default':
            self.__mTetrisPanel.toggleTaskNames()
            for row in self.__panelMatrix:
                for panel in row:
                    panel.toggleTaskNames()
        elif target == 'mainPanel':
            self.__mTetrisPanel.toggleTaskNames()
        elif target == 'optionPanel':
            for row in self.__panelMatrix:
                for panel in row:
                    panel.toggleTaskNames()
        return
    
    def toggleDragAndDrop(self, target = 'default'):
        """Toggle if the drag and drop feature for mapping dots is enabled or not.
        :param str target: Defines if the call targets:
                            default -> the main panel and all option panels.
                            mainPanel -> only the main panel.
                            optionPanel -> all option panels.
        """
        if target == 'default':
            self.__mTetrisPanel.toggleDragAndDrop()
            for row in self.__panelMatrix:
                for panel in row:
                    panel.toggleDragAndDrop()
        elif target == 'mainPanel':
            self.__mTetrisPanel.toggleDragAndDrop()
        elif target == 'optionPanel':
            for row in self.__panelMatrix:
                for panel in row:
                    panel.toggleDragAndDrop()
        return
    
    def togglePENames(self, target = 'default'):
        """Toggles if the names of the processing elements should be shown or not.
        :param str target: Defines if the call targets:
                            default -> the main panel and all option panels.
                            mainPanel -> only the main panel.
                            optionPanel -> all option panels.
        """
        if target == 'default':
            self.__mTetrisPanel.togglePENames()
            for row in self.__panelMatrix:
                for panel in row:
                    panel.togglePENames()
        elif target == 'mainPanel':
            self.__mTetrisPanel.togglePENames()
        elif target == 'optionPanel':
            for row in self.__panelMatrix:
                for panel in row:
                    panel.togglePENames()
        return
    
    def getUsedCores(self):
        """Returns a list of all cores used by different finalized mappings.
        :returns A list with all core names:
        :rtype list[str]:
        """
        return self.__mTetrisPanel.getUsedCores()
    
    
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
    
    def __keyPressed(self, event):
        """Callback function if a key is pressed
        :param event event: The actual fired event when a key is pressed.
        """
        if self.__panelMatrix == None:
            return
        else:
            searchedMapping = None
            for row in self.__panelMatrix:
                for panel in row:
                    if event.char == str(panel.getId()):
                        searchedMapping = panel.getMappingOption()
                        break
            if searchedMapping != None:
                self.__mTetrisPanel.applyMapping(searchedMapping)
            else:
                if event.keysym == 'Return':
                    if self.__mTetrisPanel.finalizeMapping():
                        for row in self.__panelMatrix:
                            for panel in row:
                                panel.clearMappingOption()
    
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
            self.__appliedMapping = mapping
        else:
            self.__mApiInstance.removeMapping(0)
            self.__mApiInstance.addMapping(mapping, 0)
            self.__appliedMapping = mapping
        return
    
    def finalizeMapping(self):
        """Removes the currently applied mapping and adds every core used by this mapping to the list of used cores.
        """
        if self.__appliedMapping == None:
            return False
        coreDict = self.__appliedMapping.to_coreDict()
        for key in coreDict:
            if not key in self.__usedCores and coreDict[key] != []:
                self.__usedCores.append(key)
        self.__mApiInstance.removeMapping(0)
        self.__appliedMapping = None
        self.__mApiInstance.setUsedCores(self.__usedCores)
        return True
    
    def getUsedCores(self):
        """Returns a list of all cores used by different finalized mappings.
        :returns A list with all core names:
        :rtype list[str]:
        """
        return self.__mApiInstance.getUsedCores()
    
    def toggleTaskNames(self):
        """Toggle if the names of the different tasks of the mappings should be shown or not.
        """
        self.__mApiInstance.toggleTaskNames()
    
    def togglePENames(self):
        """Toggles if the names of the processing elements should be shown or not.
        """
        self.__mApiInstance.togglePENames()
    
    def toggleDragAndDrop(self):
        """Toggle if the drag and drop feature for mapping dots is enabled or not.
        """
        self.__mApiInstance.toggleDragAndDrop()
    
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
        
        self.__height = pHeight
        self.__width = pWidth
        self.__mCanvas.create_rectangle(0, 0, self.__width/15, self.__height/15, width=3)
        self.__mCanvas.create_text(pWidth/30, pHeight/30, text=self.__id)
        self.__mApiInstance = drawAPI.drawAPI(self.__mCanvas, 5, 10, self.__width, self.__height)
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
    
    def getId(self):
        """Returns the panel id
        :returns The panel id:
        :rtype int:
        """
        return self.__id
    
    def clearMappingOption(self):
        """Removes the currently applied mapping option.
        """
        if self.__mActualMapping != None:
            self.__mActualMapping = None
            self.__mApiInstance.removeMapping(0)
            
    def toggleTaskNames(self):
        """Toggle if the names of the different tasks of the mappings should be shown or not.
        """
        self.__mApiInstance.toggleTaskNames()
    
    def togglePENames(self):
        """Toggles if the names of the processing elements should be shown or not.
        """
        self.__mApiInstance.togglePENames()
        self.__mCanvas.create_rectangle(0, 0, self.__width/15, self.__height/15, width=3)
        self.__mCanvas.create_text(self.__width/30, self.__height/30, text=self.__id)
    
    def toggleDragAndDrop(self):
        """Toggle if the drag and drop feature for mapping dots is enabled or not.
        """
        self.__mApiInstance.toggleDragAndDrop()
        
        
        
           
        
        
        
        
# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from mocasin.gui.utils import listOperations, platformOperations
from mocasin.gui.dataTemplates import platformLayout
import tkinter as tk

class drawManager():
    """Handle the user requests send via the drawAPI.
    :ivar drawAPI __mApiInstance: holds the instance of the api that initialized the manager.
    :ivar Canvas __mCanvas: A Tkinter canvas from the GUI of the user. Everything will be drawn in this canvas.
    :ivar dragAndDropManger __mDragAndDropManager: This manager provides the methods for DaD behavior.
    :ivar int __border: Defines the space between components of the platform and the canvas edge and between components themselves.
    :ivar int __scaling: Should be less than one. Defines which percentage of remaining Space components will use.
    :ivar int __width: The width of the canvas.
    :ivar int __height: The height of the canvas.
    :ivar int __textSpace: The space on the bottom of processing elements that is reserved for their names.
    :ivar int __fontSize: The size of the font all names are displayed in.
    :ivar int __minimalPeSize: The minimal of the height or width of all processing elements.
    :ivar bool __displayTaskNames: States if whether names of task should be displayed or not. Is true by default.
    :ivar bool __displayPENames: States if whether the names of the processing elements should be displayed or not. Is true by default.
    :ivar bool __enableDragAndDrop: State if whether drag and drop feature is enabled or not. Is false by default.
    :ivar list [int] __drawnCrosses: Holds the handles of each cross drawn for an already used core. 
    """
    def __init__(self, apiInstance, canvas, border, scaling, width, height, **kwargs):
        """Initizalizes a drawManager.
        :param drawAPI apiInstance: Holds the instance of the api that initialized the manager.
        :param Canvas canvas: A Tkinter canvas from the GUI of the user. Everything will be drawn in this canvas.
        :param int border: Defines the space between components of the platform and the canvas edge and between components themselves.
        :param int scaling: Should be less than one. Defines which percentage of remaining Space components will use.
        :param int width: The width of the canvas.
        :param int height: The height of the canvas.
        :param kwargs: Is valid for parameters:
                        :int textSpace: The space on the bottom of processing elements that is reserved for their names.
                        :int fontSize: The size of the font all names are displayed in.
        """
        self.__mApiInstance = apiInstance
        self.__mCanvas = canvas
        self.__mDragAndDropManager = dragAndDropManager(self)
        
        self.__border = border
        self.__scaling = scaling
        self.__drawWidth  = width
        self.__drawHeight = height
        self.__minimalPeSize = height
        
        self.__displayTaskNames = True
        self.__displayPENames = True
        self.__enableDragAndDrop = False
        
        self.__drawnCrosses = []
        
        self.__textSpace = 5
        self.__fontSize = 'default'
        self.__layout = None
        
        for key in kwargs:
            if key == 'fontSize':
                self.__fontSize = kwargs[key]
            if key == 'textSpace':
                self.__textSpace = kwargs[key]
        
        self.setColorVectors()
        
        
        self.__cornerRadius = 20
        self.__currentPaddingLevel = 1
        self.__clusterPadding = 20
        self.__pePadding = 10
        self.__lastPrimitiveSize = 0
    
    def setColorVectors(self, platformColors = ['default'], mappingColors = ['default'], peColors = ['default']):
        """Applies custom color values.
        :param list[str] platformVector: A list of Tkinter color values. Is used for default platform colors.
        :param list[str] mappingVector: A list of Tkinter color values. Is used for default mapping colors.
        :param list[str] peVector: A list of Tkinter color values. Is used for default processing element colors.
        """
        self.__initializePlatformColors(platformColors)
        self.__initializeMappingColors(mappingColors)
        self.__initializePEColors(peColors)
        return
    
    def getColorForMapping(self):
        """Returns a available default color for mapping dots.
        :returns: The Tkinter color value.
        :rtype str or None:
        """
        if len(self.__mappingColors) > 0:
            return self.__mappingColors.pop()
        else:
            return None
    
    def addingAvailableColor(self, color):
        """Returns an unused color to the pool of available colors.
        :param str color: The new color to add.
        """
        self.__mappingColors.append(color)
        return
    
    def TRMVdrawPlatform(self, drawOnlyPEs):
        """Draws the platform given to the api with the given canvas.
        :param bool drawOnlyPEs: Defines if the hole platform or just the PEs should be drawn
        """
        for handle in self.__mCanvas.find_all():
            self.__mCanvas.delete(handle)
            
        toDraw = self.__mApiInstance.getPlatform().getPlatformDescription()
        drawWidth = self.__drawWidth / len(toDraw)
        drawHeight = self.__drawHeight
        
        if not drawOnlyPEs:
            i = 0
            for item in toDraw:
                self.__drawInnerRessource(item, drawWidth, drawHeight, i, 0, 0)
                i += 1
        else:
            i = 0
            for item in toDraw:
                self.__skipInnerRessource(item, drawWidth, drawHeight, i, 0, 0)
                i += 1
        return
    
    def drawMappings(self):
        """Draw every applied mapping and marks used cores in the processing elements of the platform.
        """
        self.clearMappings()
        coreUsage = self.__createCoreUsage()
        coreDict = self.__mApiInstance.getPlatform().getCoreDict()
        usedCores = self.__mApiInstance.getUsedCores()
        
        for coreName in usedCores:
            startPointX = self.__mApiInstance.getPlatform().getCoreDict()[coreName][0]
            startPointY = self.__mApiInstance.getPlatform().getCoreDict()[coreName][2]
            endPointX = self.__mApiInstance.getPlatform().getCoreDict()[coreName][1]
            endPointY = self.__mApiInstance.getPlatform().getCoreDict()[coreName][3]
            
            self.__drawnCrosses.append(self.__mCanvas.create_line(startPointX, startPointY, endPointX, endPointY, width = 4, fill = 'red'))
            self.__drawnCrosses.append(self.__mCanvas.create_line(startPointX, endPointY, endPointX, startPointY, width = 4, fill = 'red'))
        
        keyWithMostProcs = None
        mostProcs = 0
        for key in coreUsage:
            amount = 0
            for innerKey in coreUsage[key]:
                amount += len(coreUsage[key][innerKey])
            if amount > mostProcs:
                mostProcs = amount
                keyWithMostProcs = key 
        
        if mostProcs == 0:
            self.__givenMappingColors = 0
            return
        
        tmpList = []
        for key in coreUsage[keyWithMostProcs]:
                for element in coreUsage[keyWithMostProcs][key]:
                    tmpList.append(element)
        matrix = listOperations.convertToMatrix(tmpList)
        maxLength = listOperations.getDimension(matrix)
        radius = self.__minimalPeSize / (2 * maxLength)
        self.__mDragAndDropManager.setRadius(radius)
        
        for key in coreUsage:
            if bool(coreUsage[key]):
                if key in usedCores:
                    self.__mCanvas.itemconfig(coreDict[key][4], fill = 'red')
                startPointX = coreDict[key][0]
                endPointX = coreDict[key][1]
                startPointY = coreDict[key][2]
                currentX = startPointX + radius
                currentY = startPointY + radius
                for innerKey in coreUsage[key]:
                    color = self.__mApiInstance.getMappings()[innerKey].getColor()
                    for entry in coreUsage[key][innerKey]:
                        if (currentX + radius) > endPointX:
                            currentY += 2 * radius
                            currentX = startPointX + radius
                        circleHandle = self.__mCanvas.create_oval(currentX - radius, currentY - radius, currentX + radius, currentY + radius, fill = color)
                        self.__mApiInstance.getMappings()[innerKey].addCircleHandle(circleHandle)
                        
                        nameHandle = None
                        if self.__displayTaskNames:
                            if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
                                nameHandle = self.__mCanvas.create_text(currentX, currentY, font = ('Helvetica', self.__fontSize), text = entry)
                            else:
                                nameHandle = self.__mCanvas.create_text(currentX, currentY, text = entry)
                            self.__mApiInstance.getMappings()[innerKey].addNameHandle(nameHandle, entry)
                        else:
                            if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
                                nameHandle = self.__mCanvas.create_text(currentX, currentY, font = ('Helvetica', self.__fontSize), text = entry, state = tk.HIDDEN)
                            else:
                                nameHandle = self.__mCanvas.create_text(currentX, currentY, text = entry, state = tk.HIDDEN)
                            self.__mApiInstance.getMappings()[innerKey].addNameHandle(nameHandle, entry)
                            
                        if self.__enableDragAndDrop and nameHandle != None:
                            self.__mCanvas.tag_bind(circleHandle, "<ButtonPress-1>", self.__mDragAndDropManager.onPressDot)
                            self.__mCanvas.tag_bind(nameHandle, "<ButtonPress-1>", self.__mDragAndDropManager.onPressName)
                        currentX += (2 * radius)
            
            else:
                continue
        
        return    
    
    def clearMappings(self):
        """Deletes all mappings and core marks drawn.
        """
        for handle in self.__drawnCrosses:
            self.__mCanvas.delete(handle)
        try:
            coreDict = self.__mApiInstance.getPlatform().getCoreDict()
            if not coreDict == None:
                for key in coreDict:
                    self.__mCanvas.itemconfig(coreDict[key][4], fill = coreDict[key][5])
        except:
            pass
        mappingDict = self.__mApiInstance.getMappings()
        for key in mappingDict:
            for handle in mappingDict[key].getCircleHandles():
                self.__mCanvas.delete(handle)
            for handle in mappingDict[key].getNameHandles():
                self.__mCanvas.delete(handle)
            mappingDict[key].clearHandles()
        return
    
    def toggleTaskNames(self):
        """Hides or shows the names of the tasks of a applied mapping.
        """
        if self.__displayTaskNames:
            self.__displayTaskNames = False
            mappingDict = self.__mApiInstance.getMappings()
            for key in mappingDict:
                for handle in mappingDict[key].getNameHandles():
                    self.__mCanvas.itemconfigure(handle, state = tk.HIDDEN)
        else:
            self.__displayTaskNames = True
            self.drawMappings()
        return
    
    def togglePENames(self):
        """Hides or shows the names of the processing elements. Clears the complete canvas because the platform has
            to been redrawn after the call of this method.
        """
        if self.__displayPENames:
            self.__displayPENames = False
            self.clearMappings()
        else:
            self.__displayPENames = True
            self.clearMappings()
        self.__mCanvas.delete('all')
    
    def toggleDragAndDrop(self):
        """Enables or disables the editing of mappings via drag and drop.
        """
        mappingDict = self.__mApiInstance.getMappings()
        if self.__enableDragAndDrop:
            self.__enableDragAndDrop = False
            for key in mappingDict:
                for handle in mappingDict[key].getCircleHandles():
                    self.__mCanvas.tag_unbind(handle, '<ButtonPress-1>')
                    
                for innerKey in mappingDict[key].getNameHandles():
                    self.__mCanvas.tag_unbind(innerKey, '<ButtonPress-1>')
        else:
            self.__enableDragAndDrop = True
            for key in mappingDict:
                for handle in mappingDict[key].getCircleHandles():
                    self.__mCanvas.tag_bind(handle, '<ButtonPress-1>', self.__mDragAndDropManager.onPressDot)
                
                for innerKey in mappingDict[key].getNameHandles():
                    self.__mCanvas.tag_bind(innerKey, '<ButtonPress-1>', self.__mDragAndDropManager.onPressName)
        return
    
    def getApiInstance(self):
        """
        :returns: The instance of the api instance that initialized this manager.
        :rtype drawAPI:
        """
        return self.__mApiInstance
    
    def getTaskNameStatus(self):
        """
        :returns: The status if wheter names of task should be shown or not.
        :rtype bool:
        """
        return self.__displayTaskNames
    
    def getCanvas(self):
        """
        :returns: The Tkinter canvas of the user GUI that uses this api.
        :rtype Canvas:
        """
        return self.__mCanvas
    
    def __createCoreUsage(self):
        """Calculate every mapped process for each processing element of the platform.
        :returns: A dict with a key for each processing element and dicts as values with a mappingID as key and each applied process as value.
        :rtype dict[str, list[dict[int, str]]]
        """
        coreUsage = {}
        
        for key in self.__mApiInstance.getMappings():
            mapping = self.__mApiInstance.getMappings()[key]
            mappingDescription = mapping.getMappingDescription()
            if coreUsage == {}:
                for innerKey in mappingDescription:
                    coreUsage.update({innerKey : {}})
            
            for innerKey in mappingDescription:
                if len(mappingDescription[innerKey]) == 0:
                    continue
                else:
                    coreUsage[innerKey].update({mapping.getMappingId() : mappingDescription[innerKey]})
        
        return coreUsage
    
    def __resolvePlatformColor(self, colorValue):
        """Returns a available default color for platform components.
        :param int colorValue: Integer of the depth of the component in the platform hierarchy.
        :returns: An available Tkiner color value.
        :rtype str:
        """
        if isinstance(colorValue, int) and colorValue >= 0 and colorValue <= len(self.__platformColors):
            return self.__platformColors[colorValue]
        else:
            return self.__resolvePlatformColor(colorValue % len(self.__platformColors))
        
    def __resolvePEColor(self, coreSize):
        """Returns a available color for a processing element.
        :param int coreSize: The index of the processing element in the core classes list of the platformInformation object.
        :returns: A Tkinter color value.
        :rtype str:
        """
        coreClasses = self.__mApiInstance.getPlatform().getCoreClasses()
        multiplicator = len(self.__peColors) / len(coreClasses)
        return self.__peColors[int(multiplicator) * coreClasses.index(coreSize)]
        
    def __initializePlatformColors(self, colorList):
        """Initializes a dictionary which represents the pool of available colors for platform components.
        :param list[str] colorList: The list of used Tkinter color values.
        """
        self.__platformColors = {}
        if colorList[0] == 'default':
            self.__platformColors = { 0: 'lightsteelblue1',
                                    1: 'mediumturquoise',
                                    2: 'darkseagreen',
                                    3: 'greenyellow',
                                    4: 'palegreen',
                                    5: 'darkkhaki',
                                    6: 'khaki',
                                    7: 'indianred',
                                    8: 'tomato',
                                    9: 'pink',
                                    10: 'maroon',
                                    }
        else:
            i = 1
            for entry in colorList:
                self.platformColors.update({i : entry})
                i += 1
        return
    
    def __initializeMappingColors(self, colorList):
        """Initializes a list which represents the pool of available colors for mappings.
        :param list[str] colorList: The list of used Tkinter color values.
        """
        if colorList[0] == 'default':
            self.__mappingColors = ['red2','orangered3','tomato2', 'coral2', 'salmon2','darkorange2','orange3', 'cornflower blue','pale goldenrod',
                                    'deep pink', 'RoyalBlue1','PaleTurquoise2', 'sienna3', 'magenta4', 'IndianRed3', 'aquamarine2']
        else:
            self.__mappingColors = colorList
        return
       
    def __initializePEColors(self, colorList):
        """Initializes a dictionary which represents the pool of available colors for processing elements.
        :param list[str] colorList: The list of used Tkinter color values.
        """
        self.__peColors = {}
        if colorList[0] == 'default':
            self.__peColors = { 0:'snow', 
                               1:'burlywood',
                               2: 'whitesmoke',
                               3: 'linen',
                               4: 'antique white',
                               5: 'lemonchiffon',
                               6: 'navajowhite'
                               }
        else:
            i = 0
            for entry in colorList:
                self.__peColors.update({i : entry})
                i += 1
        return 

#TODO: REMOVE FOLLOWING CODE!
    def __drawInnerRessource(self, toDraw, drawWidth, drawHeight, relativeXValue, xIndent, colorValue):      
        """Draws components, mostly primitives, of the platform. Calls itself recursively as long as there are primitives left.
        :param list[(str, [str])] toDraw: List that contains tuples with first the name of the primitive an second a list of primitives and or processing
                                          elements that communicate via this primitive.
        :param int drawWidth: The width of the canvas left to draw this primitive.
        :param int drawHeight: The height of the canvas left to draw this primitive.
        :param int relativeXValue: The amount of components on the same hierarchy level and the same parent primitive that are allready drawn.
        :param int XIndent: The space taken by components on the same hierarchy level but different parent primitives that are allready drawn.
        :param int colorValue: An integer used to resolve the color for the primitive. Each level of hierarchy resolves in the same color.
        """
        border = self.__border
        length = drawWidth - border
        
        startPointX = border + relativeXValue * (length + border) + xIndent
        startPointY = drawHeight - border - drawHeight / self.__scaling
        
        endPointX = startPointX + length
        endPointY = drawHeight  - border
        
        textPointX = endPointX - (endPointX - startPointX) / 2
        textPointY = endPointY - (endPointY  - startPointY) / 2
        
        color = self.__resolvePlatformColor(colorValue)
        
        self.__mCanvas.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
        
        if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
            self.__mCanvas.create_text(textPointX, textPointY, font=('Helevetica',self.__fontSize), text = toDraw[0], width = length)
        else:
            self.__mCanvas.create_text(textPointX, textPointY, text = toDraw[0], width = length)
        
        restSizeX = drawWidth / len(toDraw[1])
        restSizeY = drawHeight - drawHeight / self.__scaling - border
        
        
        drawPEs = True
        for item in toDraw[1]:
            if isinstance(item, tuple):
                drawPEs = False
                
        drawPEsWithPrimitive = True
        for item in toDraw[1]:
            if not isinstance(item, tuple) or len(item[1]) > 1:
                drawPEsWithPrimitive = False
        
        nextColor = colorValue + 1 
        
        if drawPEs or drawPEsWithPrimitive:
            if drawWidth < restSizeY:
                yIndent = restSizeY - drawWidth
                restSizeY = drawWidth
            else:
                yIndent = 0
            if drawPEs and (toDraw[0] == 'network_on_chip'):
                self.__drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, xIndent + relativeXValue * (length + border), yIndent, True)
            elif drawPEs:
                self.__drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, xIndent + relativeXValue * (length + border), yIndent, False)
            elif drawPEsWithPrimitive:
                self.__drawPEsWithPrimitive(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + border), yIndent, toDraw[0].split('_')[len(toDraw[0].split('_'))-1])
            else:
                raise(RuntimeWarning('There is no known primitive Structure to draw'))
        
        elif not drawPEs and not drawPEsWithPrimitive:
            i = 0
            for item in toDraw[1]:
                self.__drawInnerRessource(item, restSizeX, restSizeY, i, relativeXValue * drawWidth, nextColor)
                i += 1
        return
    
    def __skipInnerRessource(self, toDraw, drawWidth, drawHeight, relativeXValue, xIndent, colorValue):
        """ 
        :param list[(str, [str])] toDraw: List that contains tuples with first the name of the primitive an second a list of primitives and or processing
                                          elements that communicate via this primitive.
        :param int drawWidth: The width of the canvas left to draw this primitive.
        :param int drawHeight: The height of the canvas left to draw this primitive.
        :param int relativeXValue: The amount of components on the same hierarchy level and the same parent primitive that are allready drawn.
        :param int XIndent: The space taken by components on the same hierarchy level but different parent primitives that are allready drawn.
        :param int colorValue: An integer used to resolve the color for the primtive if there is a primitive on the PE level. Each level of hierarchy resolves 
                                in the same color.
        """
        border = self.__border
        restSizeX = drawWidth / len(toDraw[1])
        restSizeY = drawHeight
        length = drawWidth - border
        
        drawPEs = True
        for item in toDraw[1]:
            if isinstance(item, tuple):
                drawPEs = False
                
        drawPEsWithPrimitive = True
        for item in toDraw[1]:
            if not isinstance(item, tuple) or len(item[1]) > 1:
                drawPEsWithPrimitive = False
        
        nextColor = colorValue + 1
        
        if drawPEs or drawPEsWithPrimitive:
            if drawWidth < drawHeight:
                yIndent = drawHeight - drawWidth
                restSizeY = drawWidth
            else:
                yIndent = 0
            if drawPEs and (toDraw[0] == 'network_on_chip'):
                self.__drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, xIndent + relativeXValue * (length + border), yIndent, True)
            elif drawPEs:
                self.__drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, xIndent + relativeXValue * (length + border), yIndent, False)
            elif drawPEsWithPrimitive:
                self.__drawPEsWithPrimitive(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + border), yIndent, toDraw[0].split('_')[2])
            else:
                raise(RuntimeWarning('There is no known primitive Structure to draw'))
        
        elif not drawPEs and not drawPEsWithPrimitive:
            i = 0
            for item in toDraw[1]:
                self.__skipInnerRessource(item, restSizeX, drawHeight, i, relativeXValue * drawWidth, nextColor)
                i += 1
        return
 
    def __drawPEsWithPrimitive(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY, coreName):
        """Draws the level of the hierarchy on which the processing elements are placed. This method is called of every processing element has its own primitive.
        :param list[(str, [str])] toDraw: A list of tuples which contains first, the name of the primitive and second a list that contains only the name of the
                                          processing element.
        :param int drawWidth: The width of the canvas left to draw this primitive.
        :param int drawHeight: The height of the canvas left to draw this primitive.
        :param int relativeXValue: The amount of components on the same hierarchy level and the same parent primitive that are allready drawn.
        :param int indentX: The space taken by components on the same hierarchy level but different parent primitives that are allready drawn.
        :param int indentY: Indent to the top border of the canvas, so the processing element structure is drawn on top of the last primitive.
        :param str coreName: The name of the processing elements. Needed to resolve cores with higher power consumption in differen colors.
        """
        platform = self.__mApiInstance.getPlatform()
        
        matrix = listOperations.convertToMatrix(toDraw)
        dimension = listOperations.getDimension(matrix)
        
        sizeX = (restSizeX - dimension * self.__border) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.__border ) / dimension

        platform.addCoreClass(sizeX)
        
        sizePEY = sizeY * 0.8
        sizePrimitiveY = sizeY * 0.2
        
        if (sizePEY - self.__textSpace) < sizeX and (sizePEY - self.__textSpace) < self.__minimalPeSize:
            self.__minimalPeSize = sizePEY - self.__textSpace
        elif sizeX <= sizePEY and sizeX < self.__minimalPeSize:
            self.__minimalPeSize = sizeX
        
        colorPrimitive = self.__resolvePlatformColor(colorValue + 1)
        
        i = 0
        for row in matrix:
            startPointPEY = restSizeY - (dimension - i) * self.__border - ((dimension - i) * sizeY) + indentY
            startPointPrimitiveY = startPointPEY + sizePEY
            
            endPointPEY = startPointPEY + sizePEY 
            endPointPrimitiveY = startPointPrimitiveY + sizePrimitiveY
            
            textPointPEY = endPointPEY - (self.__textSpace / 2)
            textPointPrimitiveY = endPointPrimitiveY - (endPointPrimitiveY - startPointPrimitiveY) / 2
            
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.__border) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                color = None
                if coreName == 'A15':
                    color = 'snow'
                else:
                    color = 'antique white'
                peHandle = self.__mCanvas.create_rectangle(startPointX, startPointPEY, endPointX, endPointPEY, fill = color)
                if self.__fontSize != 'default' and isinstance(self.__fontSize, int) and self.__displayPENames:
                    self.__mCanvas.create_text(textPointX, textPointPEY, font=('Helvetica', self.__fontSize), text = item[1][0], width = sizeX)
                elif self.__displayPENames:
                    self.__mCanvas.create_text(textPointX, textPointPEY, text = item[1][0], width = sizeX)
                platform.updateCoreDict(item[1][0], [startPointX, endPointX, startPointPEY, endPointPEY, peHandle, color])
                
                self.__mCanvas.create_rectangle(startPointX, startPointPrimitiveY, endPointX, endPointPrimitiveY, fill = colorPrimitive)
                if self.__fontSize != 'default' and isinstance(self.__fontSize, int) and self.__displayPENames:
                    self.__mCanvas.create_text(textPointX, textPointPrimitiveY, font=('Helvetica', self.__fontSize), text = item[0], width = sizeX)
                elif self.__displayPENames:
                    self.__mCanvas.create_text(textPointX, textPointPrimitiveY, text = item[0], width = sizeX)
                j += 1
            i += 1
        
        return
    
    def __drawPEs(self, toDraw, restSizeX, restSizeY, relativeXValue, indentX, indentY, networkOnChip):
        """Draws the level of the hierarchy on which the processing elements are placed. This method is called if there are nor further primitives on 
           in the structure of processing elements.
        :param list[(str, [str])] toDraw: A list of tuples which contains first, the name of the primitive and second a list that contains only the name of the
                                          processing element.
        :param int drawWidth: The width of the canvas left to draw this primitive.
        :param int drawHeight: The height of the canvas left to draw this primitive.
        :param int relativeXValue: The amount of components on the same hierarchy level and the same parent primitive that are allready drawn.
        :param int indentX: The space taken by components on the same hierarchy level but different parent primitives that are allready drawn.
        :param int indentY: Indent to the top border of the canvas, so the processing element structure is drawn on top of the last primitive.
        :param bool networkOnChip: Marks if the processing elements communicate through a network on chip to each other.
        """
        platform = self.__mApiInstance.getPlatform()
        if not networkOnChip:
            try:
                toDraw = platformOperations.getSortedProcessorScheme(toDraw)
            except:
                pass
        matrix = listOperations.convertToMatrix(toDraw)
        dimension = listOperations.getDimension(matrix)
    
        sizeX = (restSizeX - dimension * self.__border) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.__border ) / dimension
        
        platform.addCoreClass(sizeX)
        
        if (sizeY - self.__textSpace) < sizeX and (sizeY - self.__textSpace) < self.__minimalPeSize:
            self.__minimalPeSize = sizeY - self.__textSpace
        elif sizeX <= sizeY and sizeX < self.__minimalPeSize:
            self.__minimalPeSize = sizeX - self.__textSpace
    
        color = self.__resolvePEColor(sizeX)
    
        i = 0
        for row in matrix:
            startPointY = restSizeY - (dimension - i) * self.__border - ((dimension - i) * sizeY) + indentY
            endPointY = startPointY + sizeY 
            textPointY = endPointY - (self.__textSpace / 2)
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.__border) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                peHandle = self.__mCanvas.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
                
                if self.__fontSize != 'default' and isinstance(self.__fontSize, int) and self.__displayPENames:
                    self.__mCanvas.create_text(textPointX, textPointY, font=('Helvetica', self.__fontSize), text = item, width = sizeX)
                elif self.__displayPENames:
                    self.__mCanvas.create_text(textPointX, textPointY, text = item, width = sizeX)
                platform.updateCoreDict(item, [startPointX, endPointX, startPointY, endPointY, peHandle, color])
                
                if networkOnChip:
                    linkRightStartX = endPointX
                    linkRightStartY = endPointY - (endPointY - startPointY)/2
                    linkRightEndX = endPointX + self.__border
                    linkRightEndY = linkRightStartY
                    
                    linkDownStartX = endPointX - (endPointX - startPointX)/2
                    linkDownStartY = endPointY
                    linkDownEndX = linkDownStartX
                    linkDownEndY = endPointY + self.__border
                    
                    if i < dimension - 1:
                        self.__mCanvas.create_line(linkDownStartX, linkDownStartY, linkDownEndX, linkDownEndY, width = 2)
                    if j < dimension - 1:
                        self.__mCanvas.create_line(linkRightStartX, linkRightStartY, linkRightEndX, linkRightEndY, width = 2)
            
                j += 1
            i += 1
        return
    
    
#END OF TO REMOVE CODE 
    def drawPlatform(self):
        #clear the canvas
        for handle in self.__mCanvas.find_all():
            self.__mCanvas.delete(handle)
            
        toDraw = self.__mApiInstance.getPlatform()
        clusters = toDraw.getClusterDict()
        
        matrix = []
        for clusterId in clusters:
            matrix.append(clusters[clusterId])
            
        matrix = listOperations.convertToMatrix(matrix)
        
        dimension = len(matrix[0])
        slotSizeX = self.__drawWidth / dimension
        slotSizeY = self.__drawHeight / dimension
        
        self.__layout = platformLayout(dimension, slotSizeX, slotSizeY)
        self.__layout.addPrimitives(toDraw.getPrimitiveDict())
        
        for prim in self.__layout.getPrimitives():
            self.drawPrimitive(prim)
        
        self.__currentPaddingLevel += 1
        for slot in self.__layout.getLayout():
            if not slot[0]:
                """In case a cluster is assigned to this slot
                """
                self.drawProcessingElements(slot[2] + self.__currentPaddingLevel * self.__clusterPadding,
                                             slot[3] + self.__currentPaddingLevel * self.__clusterPadding, 
                                             slot[4] - self.__currentPaddingLevel * self.__clusterPadding, 
                                             slot[5] - self.__currentPaddingLevel * self.__clusterPadding, 
                                             clusters[slot[1]])
         
    def drawProcessingElements(self, startX, startY, endX, endY, clusterObject):
        matrix = listOperations.convertToMatrix(clusterObject[0])
        dimension = len(matrix[0])
        slotSizeX = (endX - startX) / dimension
        slotSizeY = (endY - startY) / dimension
        
        platform = self.__mApiInstance.getPlatform()
        platform.addCoreClass(slotSizeX)
        color = self.__resolvePEColor(slotSizeX)
        
        if clusterObject[4]:
            """In case cluster has a L2 cache
            """
            self.draw_rectangle(startX, 
                                startY, 
                                endX, 
                                endY,
                                fill=self.__resolvePlatformColor(1))
        
        for i in range(0, dimension):
            leftCornerY = startY + i * slotSizeY + self.__pePadding
            rightCornerY = startY + (i + 1) * slotSizeY - self.__pePadding
            peSizeY = rightCornerY - leftCornerY
                
            if clusterObject[3]:
                    """In case PE's in cluster have a level 1 cache
                    """
                    platformColor = self.__resolvePlatformColor(0)
                    rightCornerYPrim = rightCornerY
                    rightCornerY = rightCornerY - 0.3 * peSizeY
                    leftCornerYPrim = rightCornerY
                    primSizeY = rightCornerYPrim - leftCornerYPrim
            
            for j in range(0, dimension):
                try:
                    """Test if there is a actually a core
                    """
                    matrix[i][j]
                except:
                    continue
                
                leftCornerX = startX + j * slotSizeX + self.__pePadding
                rightCornerX = startX + (j + 1) * slotSizeX - self.__pePadding
                
                peSizeX = rightCornerX - leftCornerX
                
                peHandle = self.__mCanvas.create_rectangle(leftCornerX, leftCornerY, rightCornerX, rightCornerY, fill=color)
                if self.__displayPENames:
                    self.__mCanvas.create_text(leftCornerX + 0.5 * peSizeX, rightCornerY - self.__textSpace, text=matrix[i][j])
                
                if peSizeY < peSizeX and peSizeY < self.__minimalPeSize:
                    self.__minimalPeSize = peSizeY
                elif peSizeX <= peSizeY and peSizeX < self.__minimalPeSize:
                    self.__minimalPeSize = peSizeY
                
                self.__mApiInstance.getPlatform().updateCoreDict(matrix[i][j], [leftCornerX,
                                                                                rightCornerX,
                                                                                leftCornerY,
                                                                                rightCornerY,
                                                                                peHandle,
                                                                                color])
                if clusterObject[3]:
                    """Draw belonging level 1 cache
                    """
                    self.__mCanvas.create_rectangle(leftCornerX, leftCornerYPrim, rightCornerX, rightCornerYPrim, fill=platformColor)
                    self.__mCanvas.create_text(leftCornerX + 0.5 * peSizeX, leftCornerYPrim + 0.5 * primSizeY, text="L1 Cache")
                
                
                if clusterObject[2]:
                    """In case PE's in cluster are connected via network on chip
                    """
                    if i < dimension - 1:
                        lineStartY = rightCornerY
                        if clusterObject[3]:
                            lineStartY = rightCornerYPrim
                        lineEndY = lineStartY + 2 * self.__pePadding
                        lineX = leftCornerX + 0.5 * peSizeX
                        self.__mCanvas.create_line(lineX, lineStartY, lineX, lineEndY)
                    
                    if j < dimension - 1:
                        lineY = leftCornerY + 0.5 * peSizeY
                        lineStartX = rightCornerX
                        lineEndX = lineStartX + 2 * self.__pePadding
                        self.__mCanvas.create_line(lineStartX, lineY, lineEndX, lineY)
                        

        return
    
    def drawPrimitive(self, primitive):
        clusterAmount = int(len(primitive[1]) / 4)
        color = self.__resolvePlatformColor(clusterAmount)
        
        if self.__lastPrimitiveSize == 0:
            self.__lastPrimitiveSize = clusterAmount
        elif clusterAmount < self.__lastPrimitiveSize:
            self.__currentPaddingLevel += 1
            self.__lastPrimitiveSize = clusterAmount
        
        for i in range(0, clusterAmount):
            startPointX = primitive[1][i * 4]
            startPointY = primitive[1][i * 4 + 1]
            
            endPointX = primitive[1][i * 4 + 2]
            endPointY = primitive[1][i * 4 + 3]
            
            for j in range(i + 1, clusterAmount):
                if primitive[1][j * 4 + 1] == primitive[1][i * 4 + 1]:
                    """In case next cluster in X direction belongs to the same primitive
                    """
                    if primitive[1][i * 4] >= primitive[1][j * 4]:
                        startPointX = primitive[1][j * 4]
                    else:
                        endPointX = primitive[1][j * 4 + 2] 
                if primitive[1][j * 4] == primitive[1][i * 4]:
                    """In case next cluster in Y direction belongs to the same primitive
                    """
                    if primitive[1][i * 4 + 1] >= primitive[1][j * 4 + 1]:
                        startPointY = primitive[1][j * 4 + 1]
                    else:
                        endPointY = primitive[1][j * 4 + 3]
            
            self.draw_rectangle(startPointX + self.__currentPaddingLevel * self.__clusterPadding, 
                                startPointY + self.__currentPaddingLevel * self.__clusterPadding, 
                                endPointX - self.__currentPaddingLevel * self.__clusterPadding, 
                                endPointY - self.__currentPaddingLevel * self.__clusterPadding, 
                                fill=color)
            print(self.__currentPaddingLevel)

    def draw_rectangle(self, x1, y1, x2, y2, fill='red', outline=False):
        radius = self.__cornerRadius
        
        points = [x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1,]
        if outline:
            self.__mCanvas.create_polygon(points, fill=fill,smooth=True, outline='black')
        else:
            self.__mCanvas.create_polygon(points, fill=fill,smooth=True)
    
class dragAndDropManager():
    """This manager provides the necessary method for dragging and dropping elements of a canvas.
    :ivar drawManager __mDrawManager: The drawManager object that created the instance of the dragAndDropManager.
    :ivar Canvas __mCanvas: The canvas which elements should be dragged and dropped.
    :ivar drawAPI __mApiInstance: The drawAPI object that created the instance of the drawManager object.
    :ivar int __startX: If a element is moved this holds the x value of the original position.
    :ivar int __startY: If a element is moved this holds the y value of the original position.
    :ivar int __mouseX: Holds the x value of the mouse if an event is handled.
    :ivar int __mouseY: Holds the y value if the mouse if an event is handled.
    :ivar int __radius: Holds the radius of the drawn mapping dots.
    :ivar int __draggedItemId: Holds the handle of the dragged item given by its controlling canvas.
    """
    def __init__(self, drawManager):
        """Initializes a dragAndDropManager.
        :param drawManager drawManager: The drawManager object that initialized the dragAndDropManager.
        """
        self.__mDrawManager = drawManager
        self.__mCanvas = drawManager.getCanvas()
        self.__mApiInstance = drawManager.getApiInstance()
        self.__startX = None
        self.__startY = None
        self.__mouseX = None
        self.__mouseY = None
        self.__radius = None
        self.__draggedItemId = None
    
    def setRadius(self, radius):
        """Sets the ivar __radius.
        :param int radius: The radius of the drawn mapping dots.
        """
        self.__radius = radius
        return
    
    def onPressDot(self, event):
        """The method that handles the fired event if a mapping dot is pressed with the left mouse button.
        :param Event event: The event that is fired.
        """
        if self.__radius == None:
            return
        
        mappingDict = self.__mApiInstance.getMappings()
        
        self.__mouseX = event.x
        self.__mouseY = event.y
        
        for key in mappingDict:
            for handle in mappingDict[key].getCircleHandles():
                found = False
                coordinates = self.__mCanvas.coords(handle)
            
                midX = coordinates[0] + (coordinates[2] - coordinates[0]) / 2
                midY = coordinates[1] + (coordinates[3] - coordinates[1]) / 2
            
                if (self.__mouseX - midX) ** 2 + (self.__mouseY - midY) ** 2 <= self.__radius ** 2:
                    self.__draggedItemId = handle
                    self.__startX = midX
                    self.__startY = midY
                    found = True
                    break
            if found:
                break
        
        if not self.__draggedItemId == None:
            self.__mCanvas.tag_bind(self.__draggedItemId, "<Motion>", self.__onMove)
            self.__mCanvas.tag_bind(self.__draggedItemId, "<ButtonRelease-1>", self.__onRelease, '+')
    
    def onPressName(self, event):
        self.onPressDot(event)
        self.__mCanvas.tag_bind(self.__draggedItemId + 1, "<Motion>", self.__onMove)
        self.__mCanvas.tag_bind(self.__draggedItemId + 1, "<ButtonRelease-1>", self.__onRelease, '+')
  
    def __onMove(self, event):
        """The method that handles the fired event if a mapping dot is dragged and the mouse moves.
        :param Event event: The event that is fired.
        """
        x = event.x
        y = event.y
        differenceX = x - self.__mouseX
        differenceY = y - self.__mouseY
        
        if differenceX >= 1 or differenceX <= -1:
            self.__mCanvas.move(self.__draggedItemId, differenceX, 0)
            if self.__mDrawManager.getTaskNameStatus():
                self.__mCanvas.move(self.__draggedItemId + 1, differenceX, 0)
            self.__mouseX = x
        if differenceY >= 1 or differenceY <= -1:
            self.__mCanvas.move(self.__draggedItemId, 0, differenceY)
            if self.__mDrawManager.getTaskNameStatus():
                self.__mCanvas.move(self.__draggedItemId + 1, 0, differenceY)
            self.__mouseY = y  
            
    def __onRelease(self, event):
        """The method that handles the fired event if a mapping dot is dragged and the left mouse button is released.
        :param Event event: The event that is fired.
        """
        mappingHandle = self.__draggedItemId
        
        self.__mCanvas.tag_unbind(self.__draggedItemId, "<Motion>")
        self.__mCanvas.tag_unbind(self.__draggedItemId, "<ButtonRelease-1>")
        self.__mCanvas.tag_unbind(self.__draggedItemId + 1, "<Motion>")
        self.__mCanvas.tag_unbind(self.__draggedItemId + 1, "<ButtonRelease-1>")
        self.__mCanvas.tag_bind(self.__draggedItemId, "<ButtonPress-1>", self.onPressDot)
        self.__mCanvas.tag_bind(self.__draggedItemId + 1, "<ButtonPress-1>", self.onPressName)
        self.__draggedItemId = None
        self.__draggedSomething = False
        
        coordinates = self.__mCanvas.coords(mappingHandle)
            
        midX = coordinates[0] + (coordinates[2] - coordinates[0]) / 2
        midY = coordinates[1] + (coordinates[3] - coordinates[1]) / 2
        
        peName = None
        coreDict = self.__mApiInstance.getPlatform().getCoreDict()
        for key in coreDict:
            handle = coreDict[key][4]
            coordinates = self.__mCanvas.coords(handle)
            
            if midX >= coordinates[0] and midX <= coordinates[2] and midY >= coordinates[1] and midY <= coordinates[3]:
                peName = key
            else:
                pass
        
        if not peName == None and not peName in self.__mApiInstance.getUsedCores() :
            mappingToChange = None
            mappings = self.__mApiInstance.getMappings()
            for key in mappings:
                if mappingHandle in mappings[key].getCircleHandles():
                    mappingToChange = mappings[key]
                    break
            
            if mappingToChange != None:
                mappingToChange.changeAffinity(mappingHandle, peName)
                self.__mDrawManager.drawMappings()
            else:
                raise RuntimeWarning('Something went wrong during dropping the item!')
        else:
            diffX = self.__startX - midX
            diffY = self.__startY - midY
            self.__mCanvas.move(mappingHandle, diffX, diffY)
            if self.__mDrawManager.getTaskNameStatus():
                self.__mCanvas.move(mappingHandle + 1, diffX, diffY)
                
                
                

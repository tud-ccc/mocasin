'''
created by Felix Teweleit
26.08.2018
'''

from pykpn.gui.listOperations import listOperations
from pykpn.gui.platformOperations import platformOperations
from tkinter.constants import HIDDEN, NORMAL
import tkinter as tk

class drawAPI():
    '''
    drawManager must be a canvas object which should draw the elements, height and width of canvas will be draw height and width, border
    is the space in pixel between the drawn elements and scaling is the factor how high the elements will be drawn, e.g. a scaling of 15 
    means each element will take 1/15 of the remaining height, width and height should match width and height of the canvas, platform-
    and mappingColor are optional parameters which represent a list of color names or codes in python
    '''
    def __init__(self, drawDevice, border, scaling, width, height,textSpace = 10, fontSize = 'default'):
        self.__drawDevice = drawDevice
        self.__innerBorder = border
        self.__outerBorder = border
        self.__scaling = scaling
        self.__drawHeight = height
        self.__drawWidth  = width
        self.__fontSize = fontSize
        
        self.__platformColors = {}                    #holds the available colors for platform elements
        self.__mappingColors = {}                     #holds the available colors for mapping elements
        self.__peColors = {}                          #holds the available colors for mapping elements
        
        self.__platformDescription = []               #holds the description of the platform which should be drawn
        self.__mappingDescription = {}                #holds the description of the currently applied mappings
        self.__equalList = []                         #a list of lists of primitives which connect the same processing elements
        self.__coreDict = {}                          #dictionary, which will hold PE name, start and end points, will be updated during draw Process
        self.__coreClasses = []                       #list which has one entry for every core size
        
        self.__platformDrawn = False
        self.__mappingDrawn = False
        self.__displayTaskNames = True
        
        self.__PESize = height                        #the minimum of PE length or height after drawing, do not mess with
        self.__textSpace = textSpace                  #the space for PE names, so tasks will not overlay them
        
        self.__mappingIDs = []
        self.__mappingHandles = []                    #list contains handles of all drawn mapping elements in purpose to easily remove them
        self.__mappingNameHandles = []
        
        self.setColorVectors()
          
    '''
    first method that should be called, requires an object of the platform class and sets platform description and equalList
    attributes of drawAPI instance
    '''
    def setPlatform(self, platform):
        description = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())    
        
        #check if this platform contains a network on chip
        noc = False
        equalList = platformOperations.findEqualPrimitives(platformOperations, platform)
        description = platformOperations.mergeEqualPrimitives(platformOperations, description, equalList) 
        for equalSheet in equalList:
            if len(equalSheet) > 2:
                    noc = True
        if noc:         
            description = platformOperations.createNocMatrix(platformOperations, description, platform)
            
        self.__platformDescription = description
    
    '''
    gives the possibility to set custom color vectors for platform, mapping and cores. Arguments should be lists of color names
    '''
    def setColorVectors(self, platformColors = ['default'], mappingColors = ['default'], peColors = ['default']):
        self.__initializePlatformColors(platformColors)
        self.__initializeMappingColors(mappingColors)
        self.__initializePEColors(peColors)
        
        return
    
    '''
    requires an object of the mapping class and sets the mapping description of the drawAPI instance, should be called before
    attempting to draw the mapping
    '''
    def addMapping(self, mapping, mappingID):
        if listOperations.containsItem(listOperations, self.__mappingIDs, mappingID) or not isinstance(mappingID, int):
            raise(RuntimeError('This mapping id is already in use or not an integer!'))
        else:
            self.__mappingIDs.append(mappingID)
            
        tmpMappingDescription = mapping.to_coreList()
        
        if self.__mappingDescription == {}:
            for key in tmpMappingDescription:
                self.__mappingDescription.update({key : {}})
        
        for key in tmpMappingDescription:
            if len(tmpMappingDescription[key]) == 0:
                continue
            else:
                self.__mappingDescription[key].update({mappingID : tmpMappingDescription[key]})
        if self.__mappingDrawn:
            self.clearMappings()
            self.drawMapping()
        
        return
    
    '''
    removes the mapping belonging to the given mapping ID and redraw the mappings
    '''
    def removeMapping(self, mappingID):
        if not listOperations.containsItem(listOperations, self.__mappingIDs, mappingID):
            raise(RuntimeError('This ID is currently not in use!'))
        else:
            for key in self.__mappingDescription:
                if mappingID in self.__mappingDescription[key]:
                    del self.__mappingDescription[key][mappingID]
            self.__mappingIDs.remove(mappingID)
            if self.__mappingDrawn:
                self.clearMappings()
        return    
    
    '''
    deletes all drawn mapping elements
    '''
    def clearMappings(self):  
        for handle in self.__mappingHandles:
            self.__drawDevice.delete(handle)
        for handle in self.__mappingNameHandles:
            self.__drawDevice.delete(handle)
        self.__mappingHandles = []
        self.drawMapping()
    
    '''
    after initialization of the drawAPI class via constructor and setPlatform method, draw can be called which introduces
    the given canvas to draw the platform
    '''    
    def drawPlatform(self):
        self.__platformDrawn = True
        toDraw = self.__platformDescription
        drawWidth = self.__drawWidth / len(toDraw)
        drawHeight = self.__drawHeight
        
        i = 0
        for item in toDraw:
            self.__drawInnerRessource(item, drawWidth, drawHeight, i, 0, 0, len(toDraw))
            i += 1

        return
    
    '''
    checks if a platform has been drawn and a mapping description is set, if so it draws the mapping description in top
    of the platform description
    '''
    def drawMapping(self):
        self.__mappingDrawn = True
        if self.__mappingDescription == {}:
            raise(RuntimeError('Please set a mapping description before attempt to draw a mapping'))
        if not self.__platformDrawn:
            raise(RuntimeError('Please draw a platform before attempt to draw a mapping'))
        
        keyWithMostProcs = None
        mostProcs = 0
        for key in self.__mappingDescription:
            amount = 0
            for innerKey in self.__mappingDescription[key]:
                amount += len(self.__mappingDescription[key][innerKey])
            if amount > mostProcs:
                mostProcs = amount
                keyWithMostProcs = key
        
        #creating a tempList containing all mapping elements of the PE with most mapping elements on it, its not really needed
        #and just for the purpose of calculating the draw size of the mapping dots
        tmpList = []
        for key in self.__mappingDescription[keyWithMostProcs]:
                for element in self.__mappingDescription[keyWithMostProcs][key]:
                    tmpList.append(element)
        matrix = listOperations.convertToMatrix(listOperations, tmpList)
        maxLength = listOperations.getDimension(listOperations, matrix)
        radius = self.__PESize / (2 * maxLength)
        
        for key in self.__mappingDescription:
            if bool(self.__mappingDescription[key]):
                startPointX = self.__coreDict[key][0]
                endPointX = self.__coreDict[key][1]
                startPointY = self.__coreDict[key][2]
                currentX = startPointX + radius
                currentY = startPointY + radius
                for innerKey in self.__mappingDescription[key]:
                    color = self.__resolveMappingColor(innerKey)
                    for entry in self.__mappingDescription[key][innerKey]:
                        if (currentX + radius) > endPointX:
                            currentY += 2 * radius
                            currentX = startPointX + radius
                        self.__mappingHandles.append(self.__drawDevice.create_oval(currentX - radius, currentY - radius, currentX + radius, currentY + radius, fill = color))
                        if self.__displayTaskNames:
                            if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
                                i = self.__drawDevice.create_text(currentX, currentY, font = ('Helvetica', self.__fontSize), text = entry)
                            else:
                                i = self.__drawDevice.create_text(currentX, currentY, text = entry)
                            self.__mappingNameHandles.append(i)
                        currentX += (2 * radius)
            
            else:
                continue
        
        
        return
    
    '''
    toggles if task names should be displayed or not
    '''
    def toggleTaskNames(self):
        if self.__displayTaskNames:
            self.__displayTaskNames = False
            for handle in self.__mappingNameHandles:
                self.__drawDevice.itemconfigure(handle, state = HIDDEN)
        else:
            self.__displayTaskNames = True
            for handle in self.__mappingNameHandles:
                self.__drawDevice.itemconfigure(handle, state = NORMAL)
        return
    
    '''
    method is used internally to determine the colors for the drawn elements, should not be called manually
    '''    
    def __resolvePlatformColor(self, colorValue):
        if isinstance(colorValue, int) and colorValue >= 0 and colorValue <= 6:
            return self.__platformColors[colorValue]
        else:
            raise ValueError('Wrong color value to resolve given!')
        
    '''
    method is used internally to determine the colors for the drawn elements, should not be called manually
    '''    
    def __resolveMappingColor(self, colorValue):
        if isinstance(colorValue, int) and colorValue >= 0 and colorValue <= 6:
            return self.__mappingColors[colorValue]
        else:
            raise ValueError('Wrong color value to resolve given!')
    
    '''
    method is used internally to determine the colors for the drawn elements, should not be called manually
    '''
    def __resolvePEColor(self, coreSize):
        multiplicator = len(self.__peColors) / len(self.__coreClasses)
        return self.__peColors[int(multiplicator) * self.__coreClasses.index(coreSize)]
        pass
       
    '''
    method draws primitives, should not be called manually
    '''
    def __drawInnerRessource(self, toDraw, drawWidth, drawHeight, relativeXValue, xIndent, colorValue, amount):      
        innerBorder = self.__innerBorder
        outerBorder = self.__outerBorder
        length = drawWidth - innerBorder
        
        startPointX = outerBorder + relativeXValue * (length + innerBorder) + xIndent
        startPointY = drawHeight - outerBorder - drawHeight / self.__scaling
        
        endPointX = startPointX + length
        endPointY = drawHeight  - outerBorder
        
        textPointX = endPointX - (endPointX - startPointX) / 2
        textPointY = endPointY - (endPointY  - startPointY) / 2
        
        color = self.__resolvePlatformColor(colorValue)
        
        self.__drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
        
        if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
            self.__drawDevice.create_text(textPointX, textPointY, font=('Helevetica',self.__fontSize), text = toDraw[0], width = length)
        else:
            self.__drawDevice.create_text(textPointX, textPointY, text = toDraw[0], width = length)
        
        restSizeX = drawWidth / len(toDraw[1])
        restSizeY = drawHeight - drawHeight / self.__scaling - innerBorder
        
        
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
                self.__drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + innerBorder), yIndent, True)
            elif drawPEs:
                self.__drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + innerBorder), yIndent, False)
            elif drawPEsWithPrimitive:
                self.__drawPEsWithPrimitive(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + innerBorder), yIndent, toDraw[0].split('_')[2])
            else:
                raise(RuntimeError('There is no known primitive Structure to draw'))
        
        elif not drawPEs and not drawPEsWithPrimitive:
            i = 0
            for item in toDraw[1]:
                self.__drawInnerRessource(item, restSizeX, restSizeY, i, relativeXValue * drawWidth, nextColor, len(toDraw[1]))
                i += 1
        return
    
    '''
    method draws processing elements, should not be called manually
    '''
    def __drawPEsWithPrimitive(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY, coreSize):
        
        matrix = listOperations.convertToMatrix(listOperations, toDraw)
        dimension = listOperations.getDimension(listOperations, matrix)
        
        sizeX = (restSizeX - dimension * self.__innerBorder) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.__innerBorder ) / dimension
        
        self.__addCoreClass(sizeX)
        
        sizePEY = sizeY * 0.8
        sizePrimitiveY = sizeY * 0.2
        
        if (sizePEY - self.__textSpace) < sizeX and (sizePEY - self.__textSpace) < self.__PESize:
            self.__PESize = sizePEY - self.__textSpace
        elif sizeX <= sizePEY and sizeX < self.__PESize:
            self.__PESize = sizeX
        
        colorPE = self.__resolvePEColor(sizeX)
        colorPrimitive = self.__resolvePlatformColor(colorValue + 1)
        
        i = 0
        for row in matrix:
            startPointPEY = restSizeY - (dimension - i) * self.__innerBorder - ((dimension - i) * sizeY) + indentY
            startPointPrimitiveY = startPointPEY + sizePEY
            
            endPointPEY = startPointPEY + sizePEY 
            endPointPrimitiveY = startPointPrimitiveY + sizePrimitiveY
            
            textPointPEY = endPointPEY - (self.__textSpace / 2)
            textPointPrimitiveY = endPointPrimitiveY - (endPointPrimitiveY - startPointPrimitiveY) / 2
            
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.__innerBorder) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                if coreSize == 'A15':
                    self.__drawDevice.create_rectangle(startPointX, startPointPEY, endPointX, endPointPEY, fill = 'snow')
                else:
                    self.__drawDevice.create_rectangle(startPointX, startPointPEY, endPointX, endPointPEY, fill = 'antique white')
                                  
                if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
                    self.__drawDevice.create_text(textPointX, textPointPEY, font=('Helvetica', self.__fontSize), text = item[1][0], width = sizeX)
                else:
                    self.__drawDevice.create_text(textPointX, textPointPEY, text = item[1][0], width = sizeX)
                self.__coreDict.update({item[1][0] : [startPointX, endPointX, startPointPEY, endPointPEY]})
                
                self.__drawDevice.create_rectangle(startPointX, startPointPrimitiveY, endPointX, endPointPrimitiveY, fill = colorPrimitive)
                if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
                    self.__drawDevice.create_text(textPointX, textPointPrimitiveY, font=('Helvetica', self.__fontSize), text = item[0], width = sizeX)
                else:
                    self.__drawDevice.create_text(textPointX, textPointPrimitiveY, text = item[0], width = sizeX)
                j += 1
            i += 1
        
        return
        
    '''
    method draws processing elements, should not be called manually
    '''    
    def __drawPEs(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY, noc):
        
        if not noc:
            try:
                toDraw = platformOperations.getSortedProcessorScheme(platformOperations, toDraw)
            except:
                pass
        matrix = listOperations.convertToMatrix(listOperations, toDraw)
        dimension = listOperations.getDimension(listOperations, matrix)
    
        sizeX = (restSizeX - dimension * self.__innerBorder) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.__innerBorder ) / dimension
        
        self.__addCoreClass(sizeX)
        
        if (sizeY - self.__textSpace) < sizeX and (sizeY - self.__textSpace) < self.__PESize:
            self.__PESize = sizeY - self.__textSpace
        elif sizeX <= sizeY and sizeX < self.__PESize:
            self.__PESize = sizeX - self.__textSpace
    
        color = self.__resolvePEColor(sizeX)
    
        i = 0
        for row in matrix:
            startPointY = restSizeY - (dimension - i) * self.__innerBorder - ((dimension - i) * sizeY) + indentY
            endPointY = startPointY + sizeY 
            textPointY = endPointY - (self.__textSpace / 2)
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.__innerBorder) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                self.__drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
                
                if self.__fontSize != 'default' and isinstance(self.__fontSize, int):
                    self.__drawDevice.create_text(textPointX, textPointY, font=('Helvetica', self.__fontSize), text = item, width = sizeX)
                else:
                    self.__drawDevice.create_text(textPointX, textPointY, text = item, width = sizeX)
                self.__coreDict.update({item : [startPointX, endPointX, startPointY, endPointY]})
                
                if noc:
                    linkRightStartX = endPointX
                    linkRightStartY = endPointY - (endPointY - startPointY)/2
                    linkRightEndX = endPointX + self.__innerBorder
                    linkRightEndY = linkRightStartY
                    
                    linkDownStartX = endPointX - (endPointX - startPointX)/2
                    linkDownStartY = endPointY
                    linkDownEndX = linkDownStartX
                    linkDownEndY = endPointY + self.__innerBorder
                    
                    if i < dimension - 1:
                        self.__drawDevice.create_line(linkDownStartX, linkDownStartY, linkDownEndX, linkDownEndY, width = 2)
                    if j < dimension - 1:
                        self.__drawDevice.create_line(linkRightStartX, linkRightStartY, linkRightEndX, linkRightEndY, width = 2)
            
                j += 1
            i += 1
        return    
    
    '''
    adds a new PE class to the class dict
    '''
    def __addCoreClass(self, length):
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
    
    '''
    method initialize the color dictionary for platform elements, should not be called manually
    '''
    def __initializePlatformColors(self, colorList):
        if colorList[0] == 'default':
            self.__platformColors = { 0: 'royalblue1',
                                    1: 'steelblue1',
                                    2: 'skyblue1',
                                    3: 'lightskyblue1',
                                    4: 'slategray1',
                                    5: 'lightsteelblue1',
                                    6: 'lightblue1'
                                    }
        else:
            i = 1
            for entry in colorList:
                self.platformColors.update({i : entry})
                i += 1
        return
    
    '''
    method initialize the color dictionary for platform elements, should not be called manually
    '''
    def __initializeMappingColors(self, colorList):
        if colorList[0] == 'default':
            self.__mappingColors = { 0:'red2', 
                                   1:'orangered3', 
                                   2:'tomato2', 
                                   3:'coral2', 
                                   4:'salmon2', 
                                   5:'darkorange2', 
                                   6:'orange3' 
                                   }
        else:
            i = 1
            for entry in colorList:
                self.__mappingColors.update({i : entry})
                i += 1
        return
    
    '''
    method initialize the color dictionary for processing elements, should not be called manually
    '''    
    def __initializePEColors(self, colorList):
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
        
        
        
        
        
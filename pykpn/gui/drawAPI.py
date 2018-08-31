'''
created by Felix Teweleit
26.08.2018
'''

from pykpn.gui.listOperations import listOperations
from pykpn.gui.platformOperations import platformOperations
from textwrap import fill

class drawAPI():
    '''
    drawManager must be a canvas object which should draw the elements, height and width of canvas will be draw height and width, border
    is the space in pxl between the drawn elements and scaling is the factor how high the elements will be drawn, eg. a scaling of 15 
    means each element will take 1/15 of the remaining height, width and height should match width and height of the canvas
    '''
    def __init__(self, drawDevice, border, scaling, width, height):
        self.drawDevice = drawDevice
        self.innerBorder = border
        self.outerBorder = border
        self.scaling = scaling
        self.drawHeight = height
        self.drawWidth  = width
        self.colorDict = {1:'aliceblue', 
                          2:'aqua', 
                          3:'azure1', 
                          4:'yellow', 
                          5:'bisque1', 
                          6:'blue', 
                          7:'blueviolet', 
                          8:'brown1', 
                          9:'burlywood',
                          10: 'cadetblue',
                          11: 'orange',
                          12: 'chartreuse1',
                          13: 'chocolate',
                          14: 'cornsilk2',
                          15: 'coral',
                          16: 'cornflowerblue',
                          17: 'cyan2',
                          18: 'darkgoldenrod1',
                          19: 'darkorange',
                          20: 'darkorchid'}
        self.platformDescription = []               #holds the description of the platform which should be drawn
        self.mappingDescription = {}                #not implemented yet
        self.equalList = []                         #a list of lists of primitives which connect the same processing elements
        self.coreDict = {}                          #dict, which will hold PE name, start and end points, will be updated during draw Process
        self.platformDrawn = False
        self.PESize = height                        #the minimum of PE length or height after drawing, is set to height because no PE can be drawn with initial height value
                                                    #so it must reduce 
    
    '''
    method is used internally to determine the colors for the drawn elements
    '''    
    def resolveColor(self, colorValue):
        if isinstance(colorValue, int) and colorValue <= 20 and colorValue > 0:
            return self.colorDict[colorValue]
        else:
            raise ValueError('Wrong color value to resolve given!')
        
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
            
        self.platformDescription = description    
  
    '''
    requires an object of the mapping class and sets the mapping description of the drawAPI instance, should be called before
    attempting to draw the mapping
    '''
    def addMapping(self, mapping):
        self.mappingDescription = mapping.to_coreList()
        return
    
    '''
    after initialization of the drawAPI class via constructor and setPlatform method, draw can be called which introduces
    the given canvas to draw the platform
    '''    
    def drawPlatform(self):
        self.platformDrawn = True
        toDraw = self.platformDescription
        drawWidth = self.drawWidth / len(toDraw)
        drawHeight = self.drawHeight
        
        i = 0
        for item in toDraw:
            self.drawInnerRessource(item, drawWidth, drawHeight, i, 0, 20, len(toDraw))
            i += 1

        return
    
    '''
    NOT COMPLETLY IMPLEMENTED YET
    checks if a platform has been drawn and a mapping description is set, if so it draws the mapping description in top
    of the platform description
    '''
    def drawMapping(self):
        if self.mappingDescription == {}:
            raise(RuntimeError('Please set a mapping description before attempt to draw a mapping'))
        if not self.platformDrawn:
            raise(RuntimeError('Please draw a platform before attempt to draw a mapping'))
        
        keyWithMostProcs = None
        mostProcs = 0
        for key in self.mappingDescription:
            if len(self.mappingDescription[key]) > mostProcs:
                mostProcs = len(self.mappingDescription[key])
                keyWithMostProcs = key
                
        matrix = listOperations.convertToMatrix(listOperations, self.mappingDescription[keyWithMostProcs])
        maxLength = listOperations.getDimension(listOperations, matrix)
        radius = self.PESize / (2 * maxLength)
        
        for key in self.mappingDescription:
            if len(self.mappingDescription[key]) > 0:
                startPointX = self.coreDict[key][0]
                endPointX = self.coreDict[key][1]
                startPointY = self.coreDict[key][2]
                currentX = startPointX + radius
                currentY = startPointY + radius
                
                for entry in self.mappingDescription[key]:
                    if (currentX + radius) > endPointX:
                        currentY += 2 * radius
                        currentX = startPointX + radius
                    self.drawDevice.create_oval(currentX - radius, currentY - radius, currentX + radius, currentY + radius, fill = self.resolveColor(1))
                    self.drawDevice.create_text(currentX, currentY, text = entry)
                    currentX += (2 * radius)
            
            else:
                continue
        
        
        return
        
    '''
    method draws primitives, should not be called manually
    '''
    def drawInnerRessource(self, toDraw, drawWidth, drawHeight, relativeXValue, xIndent, colorValue, amount):      
        innerBorder = self.innerBorder
        outerBorder = self.outerBorder
        length = drawWidth - innerBorder
        
        startPointX = outerBorder + relativeXValue * (length + innerBorder) + xIndent
        startPointY = drawHeight - outerBorder - drawHeight / self.scaling
        
        endPointX = startPointX + length
        endPointY = drawHeight  - outerBorder
        
        textPointX = endPointX - (endPointX - startPointX) / 2
        textPointY = endPointY - (endPointY  - startPointY) / 2
        
        color = self.resolveColor(colorValue)
        
        self.drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
        self.drawDevice.create_text(textPointX, textPointY, text = toDraw[0])
        
        
        restSizeX = drawWidth / len(toDraw[1])
        restSizeY = drawHeight - drawHeight / self.scaling - innerBorder
        
        
        drawPEs = True
        for item in toDraw[1]:
            if isinstance(item, tuple):
                drawPEs = False
                
        drawPEsWithPrimitive = True
        for item in toDraw[1]:
            if not isinstance(item, tuple) or len(item[1]) > 1:
                drawPEsWithPrimitive = False
        
        nextColor = colorValue - 1 
        
        if drawPEs or drawPEsWithPrimitive:
            if drawWidth < restSizeY:
                yIndent = restSizeY - drawWidth
                restSizeY = drawWidth
            else:
                yIndent = 0
            if drawPEs and (toDraw[0] == 'network_on_chip'):
                self.drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + innerBorder), yIndent, True)
            elif drawPEs:
                self.drawPEs(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + innerBorder), yIndent, False)
            elif drawPEsWithPrimitive:
                self.drawPEsWithPrimitive(toDraw[1], drawWidth, restSizeY, relativeXValue, nextColor, xIndent + relativeXValue * (length + innerBorder), yIndent)
            else:
                raise(RuntimeError("There is no known primitive Structure to draw"))
        
        elif not drawPEs and not drawPEsWithPrimitive:
            i = 0
            for item in toDraw[1]:
                self.drawInnerRessource(item, restSizeX, restSizeY, i, relativeXValue * drawWidth, nextColor, len(toDraw[1]))
                i += 1
        return
    
    '''
    method draws processing elements, should not be called manually
    '''
    def drawPEsWithPrimitive(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY):
        
        matrix = listOperations.convertToMatrix(listOperations, toDraw)
        dimension = listOperations.getDimension(listOperations, matrix)
        
        sizeX = (restSizeX - dimension * self.innerBorder) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.innerBorder ) / dimension
        
        sizePEY = sizeY * 0.8
        sizePrimitiveY = sizeY * 0.2
        
        if sizePEY < sizeX and sizePEY < self.PESize:
            self.PESize = sizePEY
        elif sizeX <= sizePEY and sizeX < self.PESize:
            self.PESize = sizeX
        
        colorPE = self.resolveColor(colorValue)
        colorPrimitive = self.resolveColor(colorValue - 1)
        
        i = 0
        for row in matrix:
            startPointPEY = restSizeY - (dimension - i) * self.innerBorder - ((dimension - i) * sizeY) + indentY
            startPointPrimitiveY = startPointPEY + sizePEY
            
            endPointPEY = startPointPEY + sizePEY 
            endPointPrimitiveY = startPointPrimitiveY + sizePrimitiveY
            
            textPointPEY = endPointPEY - (endPointPEY - startPointPEY)/2
            textPointPrimitiveY = endPointPrimitiveY - (endPointPrimitiveY - startPointPrimitiveY) / 2
            
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.innerBorder) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                self.drawDevice.create_rectangle(startPointX, startPointPEY, endPointX, endPointPEY, fill = colorPE)
                self.drawDevice.create_text(textPointX, textPointPEY, text = item[1][0])
                self.coreDict.update({item[1][0] : [startPointX, endPointX, startPointPEY, endPointPEY]})
                
                self.drawDevice.create_rectangle(startPointX, startPointPrimitiveY, endPointX, endPointPrimitiveY, fill = colorPrimitive)
                self.drawDevice.create_text(textPointX, textPointPrimitiveY, text = item[0])
                j += 1
            i += 1
        
        return
        
    '''
    method draws processing elements, should not be called manually
    '''    
    def drawPEs(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY, noc):
        
        if not noc:
            try:
                toDraw = platformOperations.getSortedProcessorScheme(platformOperations, toDraw)
            except:
                pass
        matrix = listOperations.convertToMatrix(listOperations, toDraw)
        dimension = listOperations.getDimension(listOperations, matrix)
    
        sizeX = (restSizeX - dimension * self.innerBorder) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.innerBorder ) / dimension
        
        if sizeY < sizeX and sizeY < self.PESize:
            self.PESize = sizeY
        elif sizeX <= sizeY and sizeX < self.PESize:
            self.PESize = sizeX
    
        color = self.resolveColor(colorValue)
    
        i = 0
        for row in matrix:
            startPointY = restSizeY - (dimension - i) * self.innerBorder - ((dimension - i) * sizeY) + indentY
            endPointY = startPointY + sizeY 
            textPointY = endPointY - (endPointY - startPointY)/2
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.innerBorder) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                self.drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
                self.drawDevice.create_text(textPointX, textPointY, text = item)
                self.coreDict.update({item : [startPointX, endPointX, startPointY, endPointY]})
                
                if noc:
                    linkRightStartX = endPointX
                    linkRightStartY = endPointY - (endPointY - startPointY)/2
                    linkRightEndX = endPointX + self.innerBorder
                    linkRightEndY = linkRightStartY
                    
                    linkDownStartX = endPointX - (endPointX - startPointX)/2
                    linkDownStartY = endPointY
                    linkDownEndX = linkDownStartX
                    linkDownEndY = endPointY + self.innerBorder
                    
                    if i < dimension - 1:
                        self.drawDevice.create_line(linkDownStartX, linkDownStartY, linkDownEndX, linkDownEndY, width = 2)
                    if j < dimension - 1:
                        self.drawDevice.create_line(linkRightStartX, linkRightStartY, linkRightEndX, linkRightEndY, width = 2)
            
                j += 1
            i += 1
        return    
        
        
        
        
        
        
        
        
        
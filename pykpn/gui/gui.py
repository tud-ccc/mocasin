#crated 14.06.18
#author Felix Teweleit

from Tkinter import *
from tkMessageBox import showinfo
from pykpn.platforms.exynos_2chips import Exynos2Chips
from platformOperations import platformOperations
from listOperations import listOperations
from numpy import integer

'''
an instance of this class holds the variables that should be accessable global in the hole script.
'''
class guiVariables(object):
    def __init__(self, innerBorder, outerBorder, width, height):
        self.platformDescription = []
        self.mappingDescription = []
        self.innerBorder = innerBorder
        self.outerBorder = outerBorder
        self.drawWidth = width
        self.drawHeight = height
        self.colorDict = {1:'deep sky blue', 
                          2:'pale green', 
                          3:'yellow', 
                          4:'violet', 
                          5:'orange', 
                          6:'purple1', 
                          7:'SkyBlue4', 
                          8:'lemon chiffon', 
                          9:'mint cream'}
    def getPlatformDescription(self):
        return self.platformDescription
    def getMappingDescription(self):
        return self.mappingDescription
    def getInnerBorder(self):
        return self.innerBorder
    def getOuterBorder(self):
        return self.outerBorder
    def getDrawWidth(self):
        return self.drawWidth
    def getDrawHeight(self):
        return self.drawHeight
    def resolveColor(self, colorValue):
        if isinstance(colorValue, int):
            return self.colorDict[colorValue]
        else:
            raise ValueError('Wrong color value to resolve given!')
        


#Function Area
'''
still in work. if finished this method should open a dialog where you can select a platform file to 
load an draw 
'''
def load():
    showinfo('Load Dialog','Not realy implemented, for test issues the exynos2 description will be loaded!')
    try:
        platform = Exynos2Chips()
        variables.platformDescription = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
        drawButton['state'] = NORMAL
    except:
        showinfo('Exception thrown', 'Unexpected error during loading, please try something other!')

'''
still in work. if finished this method should open a settings dialog where you can configure the probertys of the
guiVariables class instance
'''
def openSettings():
    showinfo('Settings dialog', 'Not implemented yet!')
'''
wrapper method to easily hand arguments to the actualDrawing method
'''
def drawPlatform():
    if variables.getPlatformDescription() == []:
        showinfo('Error', 'Something went wrong. No platform device currently loaded!')
    else:
        toDraw = variables.getPlatformDescription()
        i = 0
        sizeX = variables.getDrawWidth() / len(toDraw)
        sizeY = variables.getDrawHeight() - variables.getInnerBorder()
        for item in toDraw:
            actualDrawing(item, sizeX, sizeY, (i * sizeX))

'''
function is called recursive, so for every Level of given primitive Layers the primitive an maybe contained pe's can be drawn independent
'''
def actualDrawing(toDraw, restSizeX, restSizeY, relativeXValue):
    listDepth = listOperations.getListDepth(listOperations, toDraw)    
    sizeY = restSizeY / 5
    sizeX = restSizeX - 2 * variables.getInnerBorder()
        
    startPointX = relativeXValue + variables.getInnerBorder()
    startPointY = restSizeY - sizeY
        
    endPointX = startPointX + sizeX
    endPointY = startPointY + sizeY
        
    color = variables.resolveColor(listDepth)
    drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill=color)
    textPointX = endPointX - (endPointX - startPointX)/2
    textPointY = endPointY - (endPointY - startPointY)/2
    drawDevice.create_text(textPointX,textPointY, text = toDraw[0])
        
    if listDepth > 2:
        i = 0
        newRestSizeX = restSizeX / len(toDraw[1])
        newRestsizeY = restSizeY - sizeY - variables.getInnerBorder()
        for item in toDraw[1]:
            actualDrawing(item, newRestSizeX, newRestsizeY, relativeXValue + (i * newRestSizeX))
            i += 1
    elif listDepth == 2:
        peList = []
        for item in toDraw[1]:
            for pe in item[1]:
                peList.append(pe)
        newRestsizeY = restSizeY - sizeY - variables.getInnerBorder()
        if newRestsizeY > restSizeX:
            indent = newRestsizeY - restSizeX
            drawPEs(peList, restSizeX, restSizeX, relativeXValue, 1, indent)
        else:
            drawPEs(peList, restSizeX, newRestsizeY, relativeXValue, 1, 0)
    else:
        raise RuntimeError('The list can not be drawn any further. Please check if if your platform description is correct!')

'''
function is called by actualDrawing after all primitives were drawn, it now draws the remaining processing elements on the last layer
'''
def drawPEs(toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indent):
    toDraw = platformOperations.getSortedProcessorScheme(platformOperations, toDraw)
    matrix = listOperations.convertToMatrix(listOperations, toDraw)
    dimension = listOperations.getDimension(listOperations, matrix)
    
    sizeX = (restSizeX - dimension * variables.getInnerBorder()) / dimension
    sizeY = (restSizeY - (dimension - 1) * variables.getInnerBorder() ) / dimension
    
    color = variables.resolveColor(colorValue)
    
    i = 0
    for row in matrix:
        startPointY = restSizeY - (dimension - i) * variables.getInnerBorder() - ((dimension - i) * sizeY) + indent
        endPointY = startPointY + sizeY 
        textPointY = endPointY - (endPointY - startPointY)/2
        j = 0
        for item in row:
            startPointX = relativeXValue + ((j+1) * variables.getInnerBorder()) + (j * sizeX)
            endPointX = startPointX + sizeX
            textPointX = endPointX - (endPointX - startPointX)/2
            
            drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
            drawDevice.create_text(textPointX, textPointY, text = item)
            
            j += 1
        i += 1

#GUI description area
rootWindow = Tk()

variables = guiVariables(2, 5, 1000, 600) #initiated with 5px as value for inner and outer border

controlPanel = Frame(rootWindow)
controlPanel.pack(side=LEFT)


loadButton = Button(controlPanel, text='Load', command=load)
loadButton.pack()

drawButton = Button(controlPanel,text='Draw platform', command=drawPlatform, state=DISABLED)
drawButton.pack()

settingsButton = Button(controlPanel, text ='Settings', command=openSettings)

exitButton = Button(controlPanel, text='Exit', command=controlPanel.quit)
exitButton.pack()

drawPanel = Frame(rootWindow)
drawPanel.pack()

drawDevice = Canvas(drawPanel, width=variables.getDrawWidth(), height=variables.getDrawHeight())
drawDevice.create_rectangle(0,0, variables.getDrawWidth(), variables.getDrawHeight(), fill='#fffafa')
drawDevice.pack(side=LEFT)

mainloop()

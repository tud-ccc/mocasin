#crated 14.06.18
#author Felix Teweleit

from Tkinter import *
from tkMessageBox import showinfo
from pykpn.platforms.exynos_2chips import Exynos2Chips
from platformOperations import platformOperations
from pykpn.gui.listOperations import listOperations

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

#Function Area
def load():
    showinfo('Load Dialog','Not realy implemented, for test issues the exynos2 description will be loaded!')
    try:
        platform = Exynos2Chips()
        variables.platformDescription = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
        drawButton['state'] = NORMAL
    except:
        showinfo('Exception thrown', 'Unexpected error during loading, please try something other!')

def drawPlatform():
    if variables.getPlatformDescription() == []:
        showinfo('Error', 'Something went wrong. No platform device currently loaded!')
    else:
        toDraw = variables.getPlatformDescription
        actualDrawing(toDraw, variables.getDrawWidth(), variables.getDrawHeight())

'''
function is called recursive, so for every Level of given primitive Layers the primitive an maybe contained pe's can be drawn independent
'''
def actualDrawing(toDraw, restSizeX, restSizeY):
    objectsOnLayer = len(toDraw)
    listDepth = listOperations.getListDepth(listOperations, toDraw)
    objectWidth = (restSizeX - 2 * variables.getOuterBorder() - (objectsOnLayer - 1) * variables.getInnerBorder()) / objectsOnLayer
    
    if listDepth == 1:
        return  #this is the last layer, so all space can be used for drawing of the processing elements
    else:
        objectHeight = (restSizeY) / 5
        restSizeY = restSizeY - objectHeight - variables.getInnerBorder()
        
        return #draw the layer and continue with the next call of the actualDraw function
    
    
#Window element and global variables area
rootWindow = Tk()

variables = guiVariables(5, 5, 800, 600) #initiated with 5px as value for inner and outer border

controlPanel = Frame(rootWindow)
controlPanel.pack(side=LEFT)


loadButton = Button(controlPanel, text='Load', command=load)
loadButton.pack()

drawButton = Button(controlPanel,text='Draw platform', command=drawPlatform, state=DISABLED)
drawButton.pack()

exitButton = Button(controlPanel, text='Exit', command=controlPanel.quit)
exitButton.pack()

drawPanel = Frame(rootWindow)
drawPanel.pack()

drawDevice = Canvas(drawPanel, width=variables.getDrawWidth(), height=variables.getDrawHeight())
drawDevice.create_rectangle(0,0, variables.getDrawWidth(), variables.getDrawHeight(), fill='#fffafa')
drawDevice.pack(side=LEFT)

mainloop()

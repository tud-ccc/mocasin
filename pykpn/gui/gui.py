#created 14.06.18
#author Felix Teweleit

import os
import sys
sys.path.append('../..')

import tkinter as tk
from tkinter import filedialog

from pykpn.gui.platformOperations import platformOperations
from pykpn.gui.listOperations import listOperations
from pykpn.slx.platform import SlxPlatform
from tkinter import messagebox


'''
an instance of this class holds the variables that should be accessible global in the whole script.
'''
class guiVariables(object):
    def __init__(self, innerBorder, outerBorder, width, height):
        self.platformDescription = []
        self.mappingDescription = []
        self.innerBorder = innerBorder
        self.outerBorder = outerBorder
        self.drawWidth = width
        self.drawHeight = height
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
    
    def setInnerBorder(self, innerBorder):
        self.innerBorder = innerBorder
        return
    def setOuterBorder(self, outerBorder):
        self.outerBorder = outerBorder
        return
    def setDrawWidht(self, drawWidth):
        self.drawWidth = drawWidth
        return
    def setDrawHeight(self, drawHeight):
        self.drawHeight = drawHeight
        return
    
    def resolveColor(self, colorValue):
        if isinstance(colorValue, int):
            return self.colorDict[colorValue]
        else:
            raise ValueError('Wrong color value to resolve given!')
        
def redraw():
    for item in drawDevice.find_all():
        drawDevice.delete(item)
    drawDevice.update()
    drawDevice.create_rectangle(0,0, variables.getDrawWidth(), variables.getDrawHeight(), fill='#fffafa')

#Function Area
'''
still in work. if finished this method should open a dialog where you can select a platform file to 
load an draw 
'''
def load():
    
    
    #open file dialog, ready to work
    '''
    filename =  filedialog.askopenfilename(initialdir = os.getcwd(),title = 'Select file',filetypes = (('platform files','*.platform'),('all files','*.*')))
    platform = SlxPlatform('SlxPlatform', filename, '2017.04') 
    drawButton['state'] = tk.NORMAL
    variables.platformDescription = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
    '''
    #for test issues:
    platform = SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/parallella/parallella.platform', '2017.04') 
    drawButton['state'] = tk.NORMAL
    variables.platformDescription = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
'''
wrapper method to easily hand arguments to the openSettings method
'''
def openSettingsWrapper():
    openSettings(rootWindow)
    return

'''
still in work. if finished this method should open a settings dialog where you can configure the properties of the
guiVariables class instance
'''
def openSettings(mainWindow):
    
    def applySettings():
        everythingCorrect = True
        if heightBox.get().isdigit():
            variables.setDrawHeight(int(heightBox.get()))
        else:
            heightBox.delete(0, tk.END)
            heightBox.insert(0, variables.getDrawHeight())
            everythingCorrect = False
        
        if widthBox.get().isdigit():
            variables.setDrawWidht(int(widthBox.get()))
        else:
            widthBox.delete(0, tk.END)
            widthBox.insert(0, variables.getDrawWidth())
            everythingCorrect = False
        
        if innerBorderBox.get().isdigit():
            variables.setInnerBorder(int(innerBorderBox.get()))
        else:
            innerBorderBox.delete(0, tk.END)
            innerBorderBox.insert(0, variables.getInnerBorder())
            everythingCorrect = False
        
        if outerBorderBox.get().isdigit():
            variables.setOuterBorder(outerBorderBox.get())
        else:
            outerBorderBox.delete(0, tk.END)
            outerBorderBox.insert(0, variables.getOuterBorder())
            everythingCorrect = False
            
        if everythingCorrect:
            settingWindow.destroy()
            redraw()
    
    settingWindow = tk.Toplevel(mainWindow)
    settingWindow.wm_title('Settings')
    settingWindow.grab_set()
    
    heightPanel = tk.Frame(settingWindow)
    
    heightLabel = tk.Label(heightPanel, text='Draw panel height: ')
    heightLabel.pack(side = tk.LEFT)
    
    heightBox = tk.Entry(heightPanel)
    heightBox.insert(0, str(variables.getDrawHeight()))
    heightBox.pack(side = tk.RIGHT)
    
    heightPanel.pack()
    
    widthPanel = tk.Frame(settingWindow)
    
    widthLabel = tk.Label(widthPanel, text='Draw panel width: ')
    widthLabel.pack(side = tk.LEFT)
    
    widthBox = tk.Entry(widthPanel)
    widthBox.insert(0, str(variables.getDrawWidth()))
    widthBox.pack(side = tk.RIGHT)
    
    widthPanel.pack()
    
    innerBorderPanel = tk.Frame(settingWindow)
    
    innerBorderLabel = tk.Label(innerBorderPanel, text='Inner border: ')
    innerBorderLabel.pack(side = tk.LEFT)
    
    innerBorderBox = tk.Entry(innerBorderPanel)
    innerBorderBox.insert(0, str(variables.getInnerBorder()))
    innerBorderBox.pack(side = tk.RIGHT)
    
    innerBorderPanel.pack()
    
    outerBorderPanel = tk.Frame(settingWindow)
    
    outerBorderLabel = tk.Label(outerBorderPanel, text='Outer border: ')
    outerBorderLabel.pack(side = tk.LEFT)
    
    outerBorderBox = tk.Entry(outerBorderPanel)
    outerBorderBox.insert(0, str(variables.getOuterBorder()))
    outerBorderBox.pack(side = tk.RIGHT)
    
    outerBorderPanel.pack()
    
    buttonPanel = tk.Frame(settingWindow)
    
    submitButton = tk.Button(buttonPanel, text='Submit', command=applySettings)
    submitButton.pack(side=tk.LEFT)
    cancelButton = tk.Button(buttonPanel, text='Cancel', command=settingWindow.destroy)
    cancelButton.pack(side=tk.LEFT)
    
    buttonPanel.pack()
    


'''
wrapper method to easily hand arguments to the actualDrawing method
'''
def drawPlatformWrapper():
    if variables.getPlatformDescription() == []:
        messagebox.showinfo('Error', 'Something went wrong. No platform device currently loaded!')
    else:
        toDraw = variables.getPlatformDescription()
        i = 0
        sizeX = variables.getDrawWidth() / len(toDraw)
        sizeY = variables.getDrawHeight() - variables.getInnerBorder()
        for item in toDraw:
            drawPlatform(item, sizeX, sizeY, (i * sizeX))
            i += 1
    return

'''
function is called recursive, so for every Level of given primitive Layers the primitive and maybe contained pe's can be drawn independent
'''
def drawPlatform(toDraw, restSizeX, restSizeY, relativeXValue):
    listDepth = listOperations.getListDepth(listOperations, toDraw)    
    sizeY = restSizeY / 15
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
            drawPlatform(item, newRestSizeX, newRestsizeY, relativeXValue + (i * newRestSizeX))
            i += 1
    elif listDepth == 2 or listDepth == 1:
        peList = []
        for item in toDraw[1]:
            if listDepth == 2:      #every pe has its own primitive
                for pe in item[1]:
                    peList.append(pe)
            elif listDepth == 1:    #there is one primitive for a lot of pe's
                peList.append(item)
        newRestsizeY = restSizeY - sizeY - variables.getInnerBorder()
        if newRestsizeY > restSizeX:
            indent = newRestsizeY - restSizeX
            drawPEs(peList, restSizeX, restSizeX, relativeXValue, 1, indent)
        else:
            drawPEs(peList, restSizeX, newRestsizeY, relativeXValue, 1, 0)
    else:
        raise RuntimeError('The list can not be drawn any further. Please check if if your platform description is correct!')
    return

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
    return

#GUI description area

'''
looks if there are arguments given by the terminal when the script is started, if so 
'''
def fetchSystemArguments():
    for argument in sys.argv:
        if colorVector(argument):
            pass 
        if platformFile(argument):
            try:
                platform = SlxPlatform('SlxPlatform', argument, '2017.04')
                drawButton['state'] = tk.NORMAL
                variables.platformDescription = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
                drawPlatformWrapper()
            except:
                pass
        if argument == os.path.basename(__file__):
            pass
        else:
            print('Invalid argument: ' + argument)
    return

'''
not implemented yet, please move along
'''
def colorVector(argument):
    return False

'''
checks if given argument is the path to a platform file
'''
def platformFile(argument):
    try:
        tmpString = argument.split('/')
        toCheck = tmpString[len(tmpString)-1].split('.')
        if toCheck[1] == 'platform':
            return True
        return False
    except:
        return False

rootWindow = tk.Tk()

variables = guiVariables(10, 5, 1000, 1000) #initiated with 5px as value for inner and outer border

controlPanel = tk.Frame(rootWindow)
controlPanel.pack(side=tk.LEFT)


loadButton = tk.Button(controlPanel, text='Load', command=load)
loadButton.pack()

drawButton = tk.Button(controlPanel,text='Draw platform', command=drawPlatformWrapper, state=tk.DISABLED)
drawButton.pack()

settingsButton = tk.Button(controlPanel, text ='Settings', command=openSettingsWrapper)
settingsButton.pack()

exitButton = tk.Button(controlPanel, text='Exit', command=controlPanel.quit)
exitButton.pack()

drawPanel = tk.Frame(rootWindow)
drawPanel.pack()

drawDevice = tk.Canvas(drawPanel, width=variables.getDrawWidth(), height=variables.getDrawHeight())
drawDevice.create_rectangle(0,0, variables.getDrawWidth(), variables.getDrawHeight(), fill='#fffafa')
drawDevice.pack(side=tk.LEFT)

fetchSystemArguments()

rootWindow.mainloop()


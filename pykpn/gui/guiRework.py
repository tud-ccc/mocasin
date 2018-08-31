#author Felix Teweleit

import sys
sys.path.append('../..')
import os
import tkinter as tk
from pykpn.gui.listOperations import listOperations
from pykpn.gui.platformOperations import platformOperations
from tkinter import filedialog
from tkinter import messagebox
from pykpn.slx.platform import SlxPlatform

class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        loadButton = tk.Button(text='Load', command=self.load)
        loadButton.grid(row = 0)
        drawButton = tk.Button(text='Draw', command=self.draw)
        drawButton.grid(row = 1)
        clearButton = tk.Button(text='Clear', command=self.parent.drawPanel.clear)
        clearButton.grid(row = 2)
        settingButton = tk.Button(text='Settings', command=self.parent.settingDialog.showDialog)
        settingButton.grid(row = 3)
        exitButton = tk.Button(text='Exit', command=parent.quit)
        exitButton.grid(row = 4)
                  
    def load(self, filename = 'default'):
        '''
        loading the platform xml from the file system
        '''
        
        '''
        if filename == 'default':
            filename =  filedialog.askopenfilename(initialdir = os.getcwd(),title = 'Select file',filetypes = (('platform files','*.platform'),('all files','*.*')))
            platform = SlxPlatform('SlxPlatform', filename, '2017.04')
        else:
            platform = SlxPlatform('SlxPlatform', filename, '2017.04')
        '''
        platform = SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/exynos/exynos.platform', '2017.04')
        
        description = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
            
        '''
        check if this platform contains a network on chip
        '''
        noc = False
        
        equalList = platformOperations.findEqualPrimitives(platformOperations, platform)
        description = platformOperations.mergeEqualPrimitives(platformOperations, description, equalList) 
        for equalSheet in equalList:
            if len(equalSheet) > 2:
                    noc = True
        
        if noc:         
            description = platformOperations.createNocMatrix(platformOperations, description, platform)
            
        self.parent.variables.platformDescription = description
        if self.parent.variables.getCurrentlyDrawn():
            self.parent.drawPanel.clear()

    def draw(self):
        if(self.parent.variables.getPlatformDescription()== []):
            messagebox.showwarning('Warning', 'There is no platform description available!')
        else: 
            self.parent.variables.setCurrentlyDrawn(True)
            toDraw = self.parent.variables.getPlatformDescription()
            self.parent.drawPanel.drawPlatform(toDraw)
        
class drawPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.drawDevice = tk.Canvas(width = parent.variables.getDrawWidth(), height = parent.variables.getDrawHeight())
        self.drawDevice.create_rectangle(0,0, self.parent.variables.getDrawWidth(), self.parent.variables.getDrawHeight(), fill='#fffafa')
        self.drawDevice.grid(row = 0, column = 1, rowspan = 5)
        
    def redraw(self):
        for item in self.drawDevice.find_all():
            self.drawDevice.delete(item)
        self.drawDevice.config(width = self.parent.variables.getDrawWidth(), height = self.parent.variables.getDrawHeight())
        self.drawDevice.create_rectangle(0,0, self.parent.variables.getDrawWidth(), self.parent.variables.getDrawHeight(), fill='#fffafa')
        if self.parent.variables.getCurrentlyDrawn():
            toDraw = self.parent.variables.getPlatformDescription()
            self.drawPlatform(toDraw)
        return
    
    def drawPlatform(self, toDraw):
        
        drawWidth = self.parent.variables.getDrawWidth() / len(toDraw)
        drawHeight = self.parent.variables.getDrawHeight()
        
        i = 0
        for item in toDraw:
            self.drawInnerRessource(item, drawWidth, drawHeight, i, 0, 20, len(toDraw))
            i += 1

        return
    
    def drawInnerRessource(self, toDraw, drawWidth, drawHeight, relativeXValue, xIndent, colorValue, amount):
        
        innerBorder = self.parent.variables.getInnerBorder()
        outerBorder = self.parent.variables.getOuterBorder()
        length = drawWidth - innerBorder
        
        startPointX = outerBorder + relativeXValue * (length + innerBorder) + xIndent
        startPointY = drawHeight - outerBorder - drawHeight / self.parent.variables.getHeightScaling()
        
        endPointX = startPointX + length
        endPointY = drawHeight  - outerBorder
        
        textPointX = endPointX - (endPointX - startPointX) / 2
        textPointY = endPointY - (endPointY  - startPointY) / 2
        
        color = self.parent.variables.resolveColor(colorValue)
        
        self.drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
        self.drawDevice.create_text(textPointX, textPointY, text = toDraw[0])
        
        
        restSizeX = drawWidth / len(toDraw[1])
        restSizeY = drawHeight - drawHeight / self.parent.variables.getHeightScaling() - innerBorder
        
        
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
    
    def drawPEs(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY, noc):
        
        if not noc:
            try:
                toDraw = platformOperations.getSortedProcessorScheme(platformOperations, toDraw)
            except:
                pass
        matrix = listOperations.convertToMatrix(listOperations, toDraw)
        dimension = listOperations.getDimension(listOperations, matrix)
    
        sizeX = (restSizeX - dimension * self.parent.variables.getInnerBorder()) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.parent.variables.getInnerBorder() ) / dimension
    
        color = self.parent.variables.resolveColor(colorValue)
    
        i = 0
        for row in matrix:
            startPointY = restSizeY - (dimension - i) * self.parent.variables.getInnerBorder() - ((dimension - i) * sizeY) + indentY
            endPointY = startPointY + sizeY 
            textPointY = endPointY - (endPointY - startPointY)/2
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.parent.variables.getInnerBorder()) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                self.drawDevice.create_rectangle(startPointX, startPointY, endPointX, endPointY, fill = color)
                self.drawDevice.create_text(textPointX, textPointY, text = item)
                
                if noc:
                    linkRightStartX = endPointX
                    linkRightStartY = endPointY - (endPointY - startPointY)/2
                    linkRightEndX = endPointX + self.parent.variables.getInnerBorder()
                    linkRightEndY = linkRightStartY
                    
                    linkDownStartX = endPointX - (endPointX - startPointX)/2
                    linkDownStartY = endPointY
                    linkDownEndX = linkDownStartX
                    linkDownEndY = endPointY + self.parent.variables.getInnerBorder()
                    
                    if i < dimension - 1:
                        self.drawDevice.create_line(linkDownStartX, linkDownStartY, linkDownEndX, linkDownEndY, width = 2)
                    if j < dimension - 1:
                        self.drawDevice.create_line(linkRightStartX, linkRightStartY, linkRightEndX, linkRightEndY, width = 2)
            
                j += 1
            i += 1
        return
 
    def drawPEsWithPrimitive(self, toDraw, restSizeX, restSizeY, relativeXValue, colorValue, indentX, indentY):
        
        matrix = listOperations.convertToMatrix(listOperations, toDraw)
        dimension = listOperations.getDimension(listOperations, matrix)
        
        sizeX = (restSizeX - dimension * self.parent.variables.getInnerBorder()) / dimension
        sizeY = (restSizeY - (dimension - 1) * self.parent.variables.getInnerBorder() ) / dimension
        
        sizePEY = sizeY * 0.8
        sizePrimitiveY = sizeY * 0.2
        
        colorPE = self.parent.variables.resolveColor(colorValue)
        colorPrimitive = self.parent.variables.resolveColor(colorValue - 1)
        
        i = 0
        for row in matrix:
            startPointPEY = restSizeY - (dimension - i) * self.parent.variables.getInnerBorder() - ((dimension - i) * sizeY) + indentY
            startPointPrimitiveY = startPointPEY + sizePEY
            
            endPointPEY = startPointPEY + sizePEY 
            endPointPrimitiveY = startPointPrimitiveY + sizePrimitiveY
            
            textPointPEY = endPointPEY - (endPointPEY - startPointPEY)/2
            textPointPrimitiveY = endPointPrimitiveY - (endPointPrimitiveY - startPointPrimitiveY) / 2
            
            j = 0
            for item in row:
                startPointX = relativeXValue + ((j+1) * self.parent.variables.getInnerBorder()) + (j * sizeX) + indentX
                endPointX = startPointX + sizeX
                textPointX = endPointX - (endPointX - startPointX)/2
                
                self.drawDevice.create_rectangle(startPointX, startPointPEY, endPointX, endPointPEY, fill = colorPE)
                self.drawDevice.create_text(textPointX, textPointPEY, text = item[1][0])
                
                self.drawDevice.create_rectangle(startPointX, startPointPrimitiveY, endPointX, endPointPrimitiveY, fill = colorPrimitive)
                self.drawDevice.create_text(textPointX, textPointPrimitiveY, text = item[0])
                j += 1
            i += 1
        
        return
        
    def clear(self):
        for item in self.drawDevice.find_all():
            self.drawDevice.delete(item)
        self.drawDevice.create_rectangle(0,0, self.parent.variables.getDrawWidth(), self.parent.variables.getDrawHeight(), fill='#fffafa')
        self.parent.variables.setCurrentlyDrawn(False)
        
class guiVariables(object):
    def __init__(self, innerBorder, outerBorder, width, height):
        self.currentlyDrawn = False
        self.platformDescription = []
        self.mappingDescription = []
        self.innerBorder = innerBorder
        self.outerBorder = outerBorder
        self.drawWidth = width
        self.drawHeight = height
        self.heightScaling = 15
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
    def getCurrentlyDrawn(self):
        return self.currentlyDrawn
    def getHeightScaling(self):
        return self.heightScaling
    
    def setCurrentlyDrawn(self, currentlyDrawn):
        self.currentlyDrawn = currentlyDrawn
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

class settingDialog(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
    
    def showDialog(self):
        self.settingWindow = tk.Toplevel(self.parent)
        self.settingWindow.wm_title('Settings')
        self.settingWindow.grab_set()
    
        self.heightPanel = tk.Frame(self.settingWindow)
    
        self.heightLabel = tk.Label(self.heightPanel, text='Draw panel height: ')
        self.heightLabel.pack(side = tk.LEFT)
    
        self.heightBox = tk.Entry(self.heightPanel)
        self.heightBox.insert(0, str(self.parent.variables.getDrawHeight()))
        self.heightBox.pack(side = tk.RIGHT)
    
        self.heightPanel.pack()
    
        self.widthPanel = tk.Frame(self.settingWindow)
    
        self.widthLabel = tk.Label(self.widthPanel, text='Draw panel width: ')
        self.widthLabel.pack(side = tk.LEFT)
    
        self.widthBox = tk.Entry(self.widthPanel)
        self.widthBox.insert(0, str(self.parent.variables.getDrawWidth()))
        self.widthBox.pack(side = tk.RIGHT)
    
        self.widthPanel.pack()
    
        self.innerBorderPanel = tk.Frame(self.settingWindow)
    
        self.innerBorderLabel = tk.Label(self.innerBorderPanel, text='Inner border: ')
        self.innerBorderLabel.pack(side = tk.LEFT)
    
        self.innerBorderBox = tk.Entry(self.innerBorderPanel)
        self.innerBorderBox.insert(0, str(self.parent.variables.getInnerBorder()))
        self.innerBorderBox.pack(side = tk.RIGHT)
    
        self.innerBorderPanel.pack()
    
        self.outerBorderPanel = tk.Frame(self.settingWindow)
    
        self.outerBorderLabel = tk.Label(self.outerBorderPanel, text='Outer border: ')
        self.outerBorderLabel.pack(side = tk.LEFT)
    
        self.outerBorderBox = tk.Entry(self.outerBorderPanel)
        self.outerBorderBox.insert(0, str(self.parent.variables.getOuterBorder()))
        self.outerBorderBox.pack(side = tk.RIGHT)
    
        self.outerBorderPanel.pack()
    
        self.buttonPanel = tk.Frame(self.settingWindow)
    
        self.submitButton = tk.Button(self.buttonPanel, text='Submit', command=self.applySettings)
        self.submitButton.pack(side=tk.LEFT)
        self.cancelButton = tk.Button(self.buttonPanel, text='Cancel', command=self.settingWindow.destroy)
        self.cancelButton.pack(side=tk.LEFT)
    
        self.buttonPanel.pack()
     
    def applySettings(self):
        everythingCorrect = True
        if self.heightBox.get().isdigit():
            self.parent.variables.setDrawHeight(int(self.heightBox.get()))
        else:
            self.heightBox.delete(0, tk.END)
            self.heightBox.insert(0, self.parent.variables.getDrawHeight())
            everythingCorrect = False
        
        if self.widthBox.get().isdigit():
            self.parent.variables.setDrawWidht(int(self.widthBox.get()))
        else:
            self.widthBox.delete(0, tk.END)
            self.widthBox.insert(0, self.parent.variables.getDrawWidth())
            everythingCorrect = False
        
        if self.innerBorderBox.get().isdigit():
            self.parent.variables.setInnerBorder(int(self.innerBorderBox.get()))
        else:
            self.innerBorderBox.delete(0, tk.END)
            self.innerBorderBox.insert(0, self.parent.variables.getInnerBorder())
            everythingCorrect = False
        
        if self.outerBorderBox.get().isdigit():
            self.parent.variables.setOuterBorder(self.outerBorderBox.get())
        else:
            self.outerBorderBox.delete(0, tk.END)
            self.outerBorderBox.insert(0, self.parent.variables.getOuterBorder())
            everythingCorrect = False
            
        if everythingCorrect:
            self.parent.drawPanel.redraw()
            self.settingWindow.destroy()
       
class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.settingDialog = settingDialog(self)
        self.variables = guiVariables(5,5,800,800)
        self.drawPanel = drawPanel(self)
        self.controlPanel = controlPanel(self)
        for argument in sys.argv:
            if argument == os.path.basename(__file__):
                pass
            if self.platformFile(argument):
                try:
                    self.controlPanel.load(argument)
                    print('File successfully loaded')
                except:
                    print('Error during load of platform description')
                
    def platformFile(self, argument):
        try:
            tmpString = argument.split('/')
            toCheck = tmpString[len(tmpString)-1].split('.')
            if toCheck[1] == 'platform':
                return True
            return False
        except:
            return False

if __name__ == '__main__':
    root = tk.Tk()
    mainWindow(root)
    root.mainloop()
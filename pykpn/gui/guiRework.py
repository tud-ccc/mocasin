#author Felix Teweleit

import tkinter as tk
import sys
import os
from tkinter import filedialog

sys.path.append('../..')
from pykpn.slx.platform import SlxPlatform
from pykpn.gui.platformOperations import platformOperations

class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        loadButton = tk.Button(text='Load', command=self.load)
        loadButton.pack()
        drawButton = tk.Button(text='Draw')
        drawButton.pack()
        settingButton = tk.Button(text='Settings', command=self.parent.settingDialog.showDialog)
        settingButton.pack()
        exitButton = tk.Button(text='Exit', command=parent.quit)
        exitButton.pack()
        
        
           
    def load(self):
        filename =  filedialog.askopenfilename(initialdir = os.getcwd(),title = 'Select file',filetypes = (('platform files','*.platform'),('all files','*.*')))
        platform = SlxPlatform('SlxPlatform', filename, '2017.04') 
        self.parent.variables.platformDescription = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
    def openSettings(self):
        return

class drawPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
    
    def redraw(self):
        return
    def drawPlatform(self):
        return
    def drawPEs(self):
        return
    
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
        self.cancelButton = tk.Button(self.buttonPanel, text='Cancel', command=self.quit)
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
            self.quit()
       
class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.settingDialog = settingDialog(self)
        self.variables = guiVariables(0,0,0,0)
        self.controlPanel = controlPanel(self)
        self.controlPanel.pack(side='left', fill='x')
        self.drawPanel = drawPanel(self)


if __name__ == '__main__':
    root = tk.Tk()
    mainWindow(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
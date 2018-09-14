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
from pykpn.gui import drawAPI

class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        loadButton = tk.Button(text='Load')
        loadButton.grid(row = 0)
        drawButton = tk.Button(text='Draw')
        drawButton.grid(row = 1)
        clearButton = tk.Button(text='Clear')
        clearButton.grid(row = 2)
        settingButton = tk.Button(text='Settings')
        settingButton.grid(row = 3)
        exitButton = tk.Button(text='Exit')
        exitButton.grid(row = 4)
                  
        
class drawPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.__canvas = tk.Canvas(width = 800, height = 600)
        self.__canvas.grid(row = 0, column = 1, rowspan = 5)
        self.drawDevice = drawAPI(self.__canvas, 5, 15, 800, 600)

       
class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.drawPanel = drawPanel(self)
        self.controlPanel = controlPanel(self)

if __name__ == '__main__':
    root = tk.Tk()
    mainWindow(root)
    root.mainloop()
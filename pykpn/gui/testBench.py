#author Felix Teweleit

'''
this file is just for purposes of debugging and will be removed later
'''
import sys
sys.path.append('../..')
import tkinter as tk

from pykpn.gui.drawAPI import drawAPI
from pykpn.slx.platform import SlxPlatform


root = tk.Tk()

drawThing = tk.Canvas(width = 800, height = 800)
drawThing.pack()

classInstance = drawAPI(drawThing, 5, 15, 800, 800)
platform =  SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/exynos/exynos.platform', '2017.04')
classInstance.setPlatform(platform)
classInstance.draw()

root.mainloop()

'''
class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.drawThing = tk.Canvas(width = 800, height = 800)
        self.drawThing.pack()
        self.classInstance = drawAPI(self.drawThing, 5, 15)
        self.platform =  SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/parallella/parallella.platform', '2017.04')
        self.classInstance.setPlatform(self.platform)                            


if __name__ == '__main__':
    root = tk.Tk()
    mainWindow(root)
    root.mainloop()
'''

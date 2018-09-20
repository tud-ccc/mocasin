#author Felix Teweleit

'''
this file is just for purposes of debugging and will be removed later
'''
import sys
sys.path.append('../..')
import tkinter as tk

from pykpn.gui.drawAPI import drawAPI

#parses the platform
from pykpn.slx.platform import SlxPlatform

#parses the mapping file
from pykpn.slx.mapping import SlxMapping

#parses the Kpn Graph
from pykpn.slx.kpn import SlxKpnGraph

#generates random mapping
from pykpn.mapper.random import RandomMapping


root = tk.Tk()

drawThing = tk.Canvas(width = 800, height = 800)
drawThing.pack()

#class instances
classInstance = drawAPI(drawThing, 5, 15, 800, 800)
platform =  SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/exynos/exynos.platform', '2017.04')
kpnInstance = SlxKpnGraph('SlxKpnGraph','/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter.cpn.xml','2017.04')
mapping1 = RandomMapping(kpnInstance, platform)
mapping2 = RandomMapping(kpnInstance, platform)
mapping3 = RandomMapping(kpnInstance, platform)


classInstance.setPlatform(platform)
classInstance.addMapping(mapping1, 0)
classInstance.removeMapping(0)
classInstance.addMapping(mapping2, 1)
classInstance.drawPlatform()
classInstance.drawMapping()
classInstance.removeMapping(1)
classInstance.addMapping(mapping2, 0)
print('just a break point')
root.mainloop()



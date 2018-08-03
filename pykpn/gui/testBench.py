#author Felix Teweleit

'''
this file is just for purposes of debugging and will be removed later
'''
import os
import sys
sys.path.append('../..')
import os

from pykpn.gui.listOperations import listOperations
from pykpn.gui.platformOperations import platformOperations
from pykpn.slx.platform import SlxPlatform



platform = SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/exynos/exynos.platform', '2017.04')
print(platform.processors())
listToPrint = platformOperations.findEqualPrimitives(platformOperations, platform)
for item in listToPrint:
    print(item)

'''
for entry in platform.to_adjacency_dict():
    minimalCost = 1000000000000000
    peWithMinimalCost = []
    for tupel in platform.to_adjacency_dict()[entry]:
        if tupel[1] < minimalCost and tupel[1] > 0:
            minimalCost = tupel[1]
            peWithMinimalCost = []
        if tupel[1] == minimalCost:
            peWithMinimalCost.append(tupel[0])
    print(entry)
    print(minimalCost)
    print(peWithMinimalCost)
'''
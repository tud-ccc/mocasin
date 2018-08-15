#author Felix Teweleit

'''
this file is just for purposes of debugging and will be removed later
'''
import sys
sys.path.append('../..')

from pykpn.gui.platformOperations import platformOperations
from pykpn.slx.platform import SlxPlatform


platform = SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/parallella/parallella.platform', '2017.04')

description = platformOperations.getPlatformDescription(platformOperations, platform.processors(), platform.primitives())
equalList = platformOperations.findEqualPrimitives(platformOperations, platform)
description = platformOperations.mergeEqualPrimitives(platformOperations, description, equalList) 
description = platformOperations.createNocMatrix(platformOperations, description, platform)
print('stop')
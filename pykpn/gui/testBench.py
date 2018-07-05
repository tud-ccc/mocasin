#author Felix Teweleit

'''
this file is just for purposes of debugging and will be removed later
'''

from platformOperations import *
from listOperations import *
from pykpn.platforms.exynos_2chips import Exynos2Chips


i = Exynos2Chips()

primitives = platformOperations.getPlatformDescription(platformOperations, i.processors(), i.primitives())
list = [(1,[2]), (4,[5]), (6,[(4,[5]),(7, [8])])]

number = listOperations.getListDepth(listOperations, list)
print number
print primitives

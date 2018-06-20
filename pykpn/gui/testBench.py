#author Felix Teweleit

'''
this file is just for purposes of debugging and will be removed later
'''

from platformOperations import *
from listOperations import *
from pykpn.platforms.exynos_2chips import Exynos2Chips

i = Exynos2Chips()
dict = platformOperations.getSortedProcessorScheme(platformOperations ,i.processors())
print 'stop'
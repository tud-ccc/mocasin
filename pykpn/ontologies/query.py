#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Andrès Goens, Felix Teweleit

from __future__ import unicode_literals, print_function 
try:
    text=unicode
except:
    text=str

from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.common.mapping import Mapping
from pykpn.mapper.random import RandomMapping

from solver import Solver

def main():
    kpn = SlxKpnGraph('SlxKpnGraph',  "apps/audio_filter/audio_filter.cpn.xml",'2017.04')
    platform = SlxPlatform('SlxPlatform', 'apps/audio_filter/exynos/exynos.platform', '2017.04')
    mappingDict = {"mapping_one" : RandomMapping(kpn, platform), "otherMapping" : RandomMapping(kpn, platform)}
    mSolver = Solver(kpn, platform, mappingDict, debug=False)
    
    #inputString = "EXISTS ARM00 PROCESSING AND ARM01 PROCESSING AND ARM02 PROCESSING AND src MAPPED ARM07 AND RUNNING TOGETHER [sink, src ]"
    inputString = "EXISTS EQUALS mapping_one OR EQUALS otherMapping"
    
    answer = mSolver.request(inputString)
    
    
    if isinstance(answer, Mapping):
        print(answer.to_list(channels=False))
    else:
        print("No valid mapping found!")
    
if __name__ == "__main__":
    main()
    
    
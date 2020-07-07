#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

import pytest
from arpeggio import ParserPython
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.ontologies.solver import Solver
from pykpn.slx.platform import SlxPlatform
from pykpn.ontologies.logicLanguage import Grammar
from pykpn.mapper.simvec_mapper import MappingCompletionWrapper

@pytest.fixture
def parser():
    return ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=False)

@pytest.fixture
def kpnGraph():
    return SlxKpnGraph('SlxKpnGraph',  'examples/slx/app/audio_filter/audio_filter.cpn.xml')

@pytest.fixture
def platform():
    return SlxPlatform('SlxPlatform', 'examples/slx/platforms/exynos.platform')

@pytest.fixture
def solver():
    kpn = SlxKpnGraph('SlxKpnGraph',  'examples/slx/app/audio_filter/audio_filter.cpn.xml')
    platform = SlxPlatform('SlxPlatform', 'examples/slx/platforms/exynos.platform')
    cfg = {}
    return Solver(kpn, platform, cfg)

@pytest.fixture
def mapDictSolver():
    kpn = SlxKpnGraph('SlxKpnGraph',  'examples/slx/app/audio_filter/audio_filter.cpn.xml')
    platform = SlxPlatform('SlxPlatform', 'examples/slx/platforms/exynos.platform')
    fullMapper = MappingCompletionWrapper(kpn, platform)
    
    processMappingVec = [7, 6, 5, 4, 3, 2, 1, 0]
    firstMapping = fullMapper.completeMappingBestEffort(processMappingVec)
    
    processMappingVec = [1, 1, 1, 1, 1, 1, 1, 1]
    secondMapping = fullMapper.completeMappingBestEffort(processMappingVec)
    cfg = {}
    
    mapDict = {'map_one' : firstMapping, 'map_two' : secondMapping}
    return Solver(kpn, platform, cfg, mappingDict=mapDict)

@pytest.fixture
def cfg():
    return {}

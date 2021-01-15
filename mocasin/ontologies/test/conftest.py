# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
from arpeggio import ParserPython
from mocasin.maps.kpn import MapsKpnGraph
from mocasin.maps.platform import MapsPlatform
from mocasin.ontologies.solver import Solver
from mocasin.ontologies.logicLanguage import Grammar
from mocasin.ontologies.simvec_mapper import MappingCompletionWrapper


@pytest.fixture
def parser():
    return ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=False)


@pytest.fixture
def kpnGraph():
    return MapsKpnGraph(
        "MapsKpnGraph", "examples/maps/app/audio_filter/audio_filter.cpn.xml"
    )


@pytest.fixture
def platform():
    return MapsPlatform(
        "MapsPlatform", "examples/maps/platforms/exynos.platform"
    )


@pytest.fixture
def solver():
    kpn = MapsKpnGraph(
        "MapsKpnGraph", "examples/maps/app/audio_filter/audio_filter.cpn.xml"
    )
    platform = MapsPlatform(
        "MapsPlatform", "examples/maps/platforms/exynos.platform"
    )
    cfg = {}
    return Solver(kpn, platform, cfg)


@pytest.fixture
def map_dict_solver():
    kpn = MapsKpnGraph(
        "MapsKpnGraph", "examples/maps/app/audio_filter/audio_filter.cpn.xml"
    )
    platform = MapsPlatform(
        "MapsPlatform", "examples/maps/platforms/exynos.platform"
    )
    fullMapper = MappingCompletionWrapper(kpn, platform)

    processMappingVec = [7, 6, 5, 4, 3, 2, 1, 0]
    firstMapping = fullMapper.completeMappingBestEffort(processMappingVec)

    processMappingVec = [1, 1, 1, 1, 1, 1, 1, 1]
    secondMapping = fullMapper.completeMappingBestEffort(processMappingVec)
    cfg = {}

    mapDict = {"map_one": firstMapping, "map_two": secondMapping}
    return Solver(kpn, platform, cfg, mappingDict=mapDict)


@pytest.fixture
def cfg():
    return {}

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

import pytest
from arpeggio import ParserPython
from mocasin.maps.graph import MapsDataflowGraph
from mocasin.maps.platform import MapsPlatform
from mocasin.ontologies.solver import Solver
from mocasin.ontologies.logicLanguage import Grammar
from mocasin.ontologies.simvec_mapper import MappingCompletionWrapper


@pytest.fixture
def parser():
    return ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=False)


@pytest.fixture
def graph():
    return MapsDataflowGraph(
        "MapsDataflowGraph",
        "examples/maps/app/audio_filter/audio_filter.cpn.xml",
    )


@pytest.fixture
def platform():
    return MapsPlatform(
        "MapsPlatform", "examples/maps/platforms/exynos.platform"
    )


@pytest.fixture
def solver():
    graph = MapsDataflowGraph(
        "MapsDataflowGraph",
        "examples/maps/app/audio_filter/audio_filter.cpn.xml",
    )
    platform = MapsPlatform(
        "MapsPlatform", "examples/maps/platforms/exynos.platform"
    )
    cfg = {}
    return Solver(graph, platform, cfg)


@pytest.fixture
def map_dict_solver():
    graph = MapsDataflowGraph(
        "MapsDataflowGraph",
        "examples/maps/app/audio_filter/audio_filter.cpn.xml",
    )
    platform = MapsPlatform(
        "MapsPlatform", "examples/maps/platforms/exynos.platform"
    )
    fullMapper = MappingCompletionWrapper(graph, platform)

    processMappingVec = [7, 6, 5, 4, 3, 2, 1, 0]
    firstMapping = fullMapper.completeMappingBestEffort(processMappingVec)

    processMappingVec = [1, 1, 1, 1, 1, 1, 1, 1]
    secondMapping = fullMapper.completeMappingBestEffort(processMappingVec)
    cfg = {}

    mapDict = {"map_one": firstMapping, "map_two": secondMapping}
    return Solver(graph, platform, cfg, mappingDict=mapDict)


@pytest.fixture
def cfg():
    return {}

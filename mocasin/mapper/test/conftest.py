# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import pytest

from mocasin.common.graph import DataflowProcess, DataflowGraph
from mocasin.common.platform import Platform, Processor, Scheduler

from mocasin.representations import SimpleVectorRepresentation
from mocasin.common.trace import EmptyTraceGenerator
from mocasin.maps.platform import MapsPlatform
from mocasin.maps.graph import MapsDataflowGraph
from mocasin.maps.trace import MapsTraceReader


@pytest.fixture
def num_procs():
    return 7


@pytest.fixture
def graph():
    k = DataflowGraph("a")
    k.add_process(DataflowProcess("a"))
    k.add_process(DataflowProcess("b"))
    return k


@pytest.fixture
def platform(num_procs, mocker):
    p = Platform("platform")
    procs = []
    for i in range(num_procs):
        proc = Processor(("processor" + str(i)), "proctype", mocker.Mock())
        procs.append(proc)
        p.add_processor(proc)
    policies = [mocker.Mock()]
    sched = Scheduler("name", procs, policies)
    p.add_scheduler(sched)
    return p


@pytest.fixture
def representation(graph, platform):
    return SimpleVectorRepresentation(graph, platform)


@pytest.fixture
def representation_pbc(graph, platform):
    return SimpleVectorRepresentation(
        graph, platform, periodic_boundary_conditions=True
    )


@pytest.fixture
def trace():
    return EmptyTraceGenerator()


@pytest.fixture
def maps_speaker_recognition_setup():
    graph_file = (
        "examples/maps/app/speaker_recognition/speaker_recognition.cpn.xml"
    )
    platform_file = "examples/maps/platforms/exynos.platform"
    trace_dir = "examples/maps/app/speaker_recognition/exynos/traces"

    graph = MapsDataflowGraph("MapsDataflowGraph", graph_file)
    platform = MapsPlatform("MapsPlatform", platform_file)
    trace_generator = MapsTraceReader(trace_dir)

    return [graph, platform, trace_generator]


@pytest.fixture
def maps_hog_setup():
    graph_file = "examples/maps/app/hog/hog.cpn.xml"
    platform_file = "examples/maps/platforms/exynos.platform"
    trace_dir = "examples/maps/app/hog/exynos/traces"

    graph = MapsDataflowGraph("MapsDataflowGraph", graph_file)
    platform = MapsPlatform("MapsPlatform", platform_file)
    trace_generator = MapsTraceReader(trace_dir)

    return [graph, platform, trace_generator]


@pytest.fixture
def maps_parallella_setup():
    graph_file = "examples/maps/app/audio_filter/audio_filter.cpn.xml"
    platform_file = "examples/maps/platforms/parallella.platform"
    trace_dir = "examples/maps/app/audio_filter/parallella/traces"

    graph = MapsDataflowGraph("MapsDataflowGraph", graph_file)
    platform = MapsPlatform("MapsPlatform", platform_file)
    trace_generator = MapsTraceReader(trace_dir)

    return [graph, platform, trace_generator]


@pytest.fixture
def maps_multidsp_setup():
    graph_file = "examples/maps/app/audio_filter/audio_filter.cpn.xml"
    platform_file = "examples/maps/platforms/multidsp.platform"
    trace_dir = "examples/maps/app/audio_filter/multidsp/traces"

    graph = MapsDataflowGraph("MapsDataflowGraph", graph_file)
    platform = MapsPlatform("MapsPlatform", platform_file)
    trace_generator = MapsTraceReader(trace_dir)

    return [graph, platform, trace_generator]

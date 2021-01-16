import pytest

from mocasin.common.graph import DataflowProcess, DataflowGraph
from mocasin.common.platform import Platform, Processor, Scheduler

from mocasin.tgff.tgffSimulation import (
    DataflowGraphFromTgff,
    TraceGeneratorWrapper,
)
from mocasin.platforms.platformDesigner import genericProcessor
from mocasin.platforms.generic_mesh import DesignerPlatformMesh
from mocasin.platforms.exynos990 import DesignerPlatformExynos990
from mocasin.platforms.mppa_coolidge import DesignerPlatformCoolidge
from mocasin.platforms.multi_cluster import DesignerPlatformMultiCluster
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
def tgff_parallella_setup():
    file = "examples/tgff/e3s-0.9/auto-indust-cords.tgff"

    tgff_graph = "TASK_GRAPH_0"

    processor0 = genericProcessor("proc_type_0")
    processor1 = genericProcessor("proc_type_1")

    graph = DataflowGraphFromTgff(file, tgff_graph)
    platform = DesignerPlatformMesh(processor0, processor1)
    trace_generator = TraceGeneratorWrapper(file, tgff_graph)

    return [graph, platform, trace_generator]


@pytest.fixture
def tgff_exynos_setup():
    file = "examples/tgff/e3s-0.9/auto-indust-cowls.tgff"

    tgff_graph = "TASK_GRAPH_3"

    processor0 = genericProcessor("proc_type_13")
    processor1 = genericProcessor("proc_type_14")
    processor2 = genericProcessor("proc_type_15")
    processor3 = genericProcessor("proc_type_16")

    graph = DataflowGraphFromTgff(file, tgff_graph)
    platform = DesignerPlatformExynos990(
        processor0, processor1, processor2, processor3
    )
    trace_generator = TraceGeneratorWrapper(file, tgff_graph)

    return [graph, platform, trace_generator]


@pytest.fixture
def tgff_coolidge_setup():
    file = "examples/tgff/e3s-0.9/office-automation-mocsyn.tgff"

    tgff_graph = "TASK_GRAPH_0"

    processor0 = genericProcessor("proc_type_20")
    processor1 = genericProcessor("proc_type_21")

    graph = DataflowGraphFromTgff(file, tgff_graph)
    platform = DesignerPlatformCoolidge(processor0, processor1)
    trace_generator = TraceGeneratorWrapper(file, tgff_graph)

    return [graph, platform, trace_generator]


@pytest.fixture
def tgff_multi_cluster_setup():
    file = "examples/tgff/e3s-0.9/auto-indust-cords.tgff"

    tgff_graph = "TASK_GRAPH_1"

    processor0 = genericProcessor("proc_type_0")
    processor1 = genericProcessor("proc_type_1")

    graph = DataflowGraphFromTgff(file, tgff_graph)
    platform = DesignerPlatformMultiCluster(processor0, processor1)
    trace_generator = TraceGeneratorWrapper(file, tgff_graph)

    return [graph, platform, trace_generator]


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

from unittest.mock import Mock
import pytest

from pykpn.common.kpn import KpnProcess, KpnGraph
from pykpn.common.platform import Platform, Processor, Scheduler

from pykpn.tgff.tgffSimulation import KpnGraphFromTgff, TraceGeneratorWrapper
from pykpn.platforms.platformDesigner import genericProcessor
from pykpn.platforms.generic_mesh import DesignerPlatformMesh
from pykpn.platforms.exynos990 import DesignerPlatformExynos990
from pykpn.platforms.mppa_coolidge import DesignerPlatformCoolidge
from pykpn.platforms.multi_cluster import DesignerPlatformMultiCluster
from pykpn.representations import SimpleVectorRepresentation
from pykpn.common.trace import EmptyTraceGenerator
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.trace import SlxTraceReader

@pytest.fixture
def num_procs():
    return 7

@pytest.fixture
def kpn():
    k = KpnGraph('a')
    k.add_process(KpnProcess('a'))
    k.add_process(KpnProcess('b'))
    return k


@pytest.fixture
def platform(num_procs):
    p = Platform('platform')
    procs = []
    for i in range(num_procs):
        proc = Processor(('processor' + str(i)), 'proctype', Mock())
        procs.append(proc)
        p.add_processor(proc)
    policies = [Mock()]
    sched = Scheduler('name', procs, policies)
    p.add_scheduler(sched)
    return p

@pytest.fixture
def representation(kpn,platform):
    return SimpleVectorRepresentation(kpn,platform)

@pytest.fixture
def representation_pbc(kpn,platform):
    return SimpleVectorRepresentation(kpn,platform,periodic_boundary_conditions=True)

@pytest.fixture
def trace():
    return EmptyTraceGenerator()


@pytest.fixture
def tgff_parallella_setup():
    file = 'examples/tgff/e3s-0.9/auto-indust-cords.tgff'

    graph = 'TASK_GRAPH_0'

    processor0 = genericProcessor('proc_type_0')
    processor1 = genericProcessor('proc_type_1')

    kpn = KpnGraphFromTgff(file, graph)
    platform = DesignerPlatformMesh(processor0, processor1)
    trace_generator = TraceGeneratorWrapper(file, graph)

    return [kpn, platform, trace_generator]

@pytest.fixture
def tgff_exynos_setup():
    file = 'examples/tgff/e3s-0.9/auto-indust-cowls.tgff'

    graph = 'TASK_GRAPH_3'

    processor0 = genericProcessor('proc_type_13')
    processor1 = genericProcessor('proc_type_14')
    processor2 = genericProcessor('proc_type_15')
    processor3 = genericProcessor('proc_type_16')

    kpn = KpnGraphFromTgff(file, graph)
    platform = DesignerPlatformExynos990(processor0, processor1, processor2, processor3)
    trace_generator = TraceGeneratorWrapper(file, graph)

    return [kpn, platform, trace_generator]

@pytest.fixture
def tgff_coolidge_setup():
    file = 'examples/tgff/e3s-0.9/office-automation-mocsyn.tgff'

    graph = 'TASK_GRAPH_0'

    processor0 = genericProcessor('proc_type_20')
    processor1 = genericProcessor('proc_type_21')

    kpn = KpnGraphFromTgff(file, graph)
    platform = DesignerPlatformCoolidge(processor0, processor1)
    trace_generator = TraceGeneratorWrapper(file, graph)

    return [kpn, platform, trace_generator]

@pytest.fixture
def tgff_multi_cluster_setup():
    file = 'examples/tgff/e3s-0.9/auto-indust-cords.tgff'

    graph = 'TASK_GRAPH_1'

    processor0 = genericProcessor('proc_type_0')
    processor1 = genericProcessor('proc_type_1')

    kpn = KpnGraphFromTgff(file, graph)
    platform = DesignerPlatformMultiCluster(processor0, processor1)
    trace_generator = TraceGeneratorWrapper(file, graph)

    return [kpn, platform, trace_generator]

@pytest.fixture
def slx_speaker_recognition_setup():
    kpn_file = 'examples/slx/app/speaker_recognition/speaker_recognition.cpn.xml'
    platform_file = 'examples/slx/platforms/exynos.platform'
    trace_dir = 'examples/slx/app/speaker_recognition/exynos/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file)
    platform = SlxPlatform('SlxPlatform', platform_file)
    trace_generator = SlxTraceReader(trace_dir)

    return [kpn, platform, trace_generator]

@pytest.fixture
def slx_hog_setup():
    kpn_file = 'examples/slx/app/hog/hog.cpn.xml'
    platform_file = 'examples/slx/platforms/exynos.platform'
    trace_dir = 'examples/slx/app/hog/exynos/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file)
    platform = SlxPlatform('SlxPlatform', platform_file)
    trace_generator = SlxTraceReader(trace_dir)

    return [kpn, platform, trace_generator]

@pytest.fixture
def slx_parallella_setup():
    kpn_file = 'examples/slx/app/audio_filter/audio_filter.cpn.xml'
    platform_file = 'examples/slx/platforms/parallella.platform'
    trace_dir = 'examples/slx/app/audio_filter/parallella/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file)
    platform = SlxPlatform('SlxPlatform', platform_file)
    trace_generator = SlxTraceReader(trace_dir)

    return [kpn, platform, trace_generator]

@pytest.fixture
def slx_multidsp_setup():
    kpn_file = 'examples/slx/app/audio_filter/audio_filter.cpn.xml'
    platform_file = 'examples/slx/platforms/multidsp.platform'
    trace_dir = 'examples/slx/app/audio_filter/multidsp/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file)
    platform = SlxPlatform('SlxPlatform', platform_file)
    trace_generator = SlxTraceReader(trace_dir)

    return [kpn, platform, trace_generator]

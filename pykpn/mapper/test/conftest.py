from unittest.mock import Mock
import pytest

from pykpn.common.kpn import KpnProcess, KpnGraph
from pykpn.common.platform import Platform, Processor, Scheduler

from pykpn.tgff.tgffSimulation import PlatformFromTgff, KpnGraphFromTgff, TraceGeneratorWrapper
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
def tgff_parallella_setup():
    file = 'pykpn/tgff/graphs/auto-indust-cords.tgff'

    graph = 'TASK_GRAPH_0'

    platform_type = 'parallella'
    processor0 = 'processor_0'
    processor1 = 'processor_1'
    processor2 = 'processor_2'
    processor3 = 'processor_3'

    kpn = KpnGraphFromTgff(file, graph)
    platform = PlatformFromTgff(platform_type, processor0, processor1, processor2, processor3, file)
    trace_generator = TraceGeneratorWrapper(file)

    return [kpn, platform, trace_generator]

@pytest.fixture
def tgff_exynos_setup():
    file = 'pykpn/tgff/graphs/auto-indust-cowls.tgff'

    graph = 'TASK_GRAPH_3'

    platform_type = 'exynos990'
    processor0 = 'processor_13'
    processor1 = 'processor_14'
    processor2 = 'processor_15'
    processor3 = 'processor_16'

    kpn = KpnGraphFromTgff(file, graph)
    platform = PlatformFromTgff(platform_type, processor0, processor1, processor2, processor3, file)
    trace_generator = TraceGeneratorWrapper(file)

    return [kpn, platform, trace_generator]

@pytest.fixture
def tgff_coolidge_setup():
    file = 'pykpn/tgff/graphs/office-automation-mocsyn.tgff'

    graph = 'TASK_GRAPH_0'

    platform_type = 'coolidge'
    processor0 = 'processor_20'
    processor1 = 'processor_21'
    processor2 = 'processor_22'
    processor3 = 'processor_23'

    kpn = KpnGraphFromTgff(file, graph)
    platform = PlatformFromTgff(platform_type, processor0, processor1, processor2, processor3, file)
    trace_generator = TraceGeneratorWrapper(file)

    return [kpn, platform, trace_generator]

@pytest.fixture
def slx_speaker_recognition_setup():
    slx_version = '2017.10'
    kpn_file = 'examples/slx/app/speaker_recognition/speaker_recognition.cpn.xml'
    platform_file = 'examples/slx/platforms/exynos.platform'
    trace_dir = 'examples/slx/app/speaker_recognition/exynos/traces'
    
    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file, slx_version)
    platform = SlxPlatform('SlxPlatform', platform_file, '2017.04')
    trace_generator = SlxTraceReader(trace_dir, slx_version, 'SlxKpnGraph.')

    return [kpn, platform, trace_generator, trace_generator]

@pytest.fixture
def slx_hog_setup():
    slx_version = '2017.10'
    kpn_file = 'examples/slx/app/hog/hog.cpn.xml'
    platform_file = 'examples/slx/platforms/exynos.platform'
    trace_dir = 'examples/slx/app/hog/exynos/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file, slx_version)
    platform = SlxPlatform('SlxPlatform', platform_file, '2017.04')
    trace_generator = SlxTraceReader(trace_dir, slx_version, 'SlxKpnGraph.')

    return [kpn, platform, trace_generator, trace_generator]

@pytest.fixture
def slx_parallella_setup():
    slx_version = '2017.10'
    kpn_file = 'examples/slx/app/audio_filter/audio_filter.cpn.xml'
    platform_file = 'examples/slx/platforms/parallella.platform'
    trace_dir = 'examples/slx/app/audio_filter/parallella/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file, slx_version)
    platform = SlxPlatform('SlxPlatform', platform_file, '2017.04')
    trace_generator = SlxTraceReader(trace_dir, slx_version, 'SlxKpnGraph.')

    return [kpn, platform, trace_generator, trace_generator]

@pytest.fixture
def slx_multidsp_setup():
    slx_version = '2017.10'
    kpn_file = 'examples/slx/app/audio_filter/audio_filter.cpn.xml'
    platform_file = 'examples/slx/platforms/multidsp.platform'
    trace_dir = 'examples/slx/app/audio_filter/multidsp/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file, slx_version)
    platform = SlxPlatform('SlxPlatform', platform_file, '2017.04')
    trace_generator = SlxTraceReader(trace_dir, slx_version, 'SlxKpnGraph.')

    return [kpn, platform, trace_generator, trace_generator]


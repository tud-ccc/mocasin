from pykpn.mapper.gbm_fullmapper import GroupBasedMapper_Testing

from pykpn.tgff.tgffSimulation import PlatformFromTgff, KpnGraphFromTgff, TraceGeneratorWrapper


from pykpn.slx.platform import SlxPlatform
from pykpn.slx.trace import SlxTraceReader
from pykpn.slx.kpn import SlxKpnGraph


def main():
    
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
    '''
    slx_version = '2017.10'
    kpn_file = 'examples/slx/app/speaker_recognition/speaker_recognition.cpn.xml'
    platform_file = 'examples/slx/platforms/exynos.platform'
    trace_dir = 'examples/slx/app/speaker_recognition/exynos/traces'

    kpn = SlxKpnGraph('SlxKpnGraph',  kpn_file, slx_version)
    platform = SlxPlatform('SlxPlatform', platform_file, '2017.04')
    trace_generator = SlxTraceReader(trace_dir, slx_version, 'SlxKpnGraph.')
    '''

    mapper = GroupBasedMapper_Testing(kpn, platform, trace_generator)

    result = mapper.generate_mapping()

    print(result.to_list())


if __name__ == '__main__':
    main()

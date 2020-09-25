# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from pykpn.tgff.trace import TgffTraceGenerator
from pykpn.tgff.tgffParser.parser import Parser
from pykpn.platforms.exynos990 import DesignerPlatformExynos990
from pykpn.platforms.generic_bus import DesignerPlatformBus
from pykpn.platforms.generic_mesh import DesignerPlatformMesh
from pykpn.platforms.odroid import DesignerPlatformOdroid
from pykpn.platforms.mppa_coolidge import DesignerPlatformCoolidge
from pykpn.platforms.multi_cluster import DesignerPlatformMultiCluster


import logging
log = logging.getLogger(__name__)

_parsed_tgff_files = {}

class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""
    pass


class KpnGraphFromTgff:
    """New, since we want to return a common.kpn instance instead of am TgffToKpnGraph instance
    """
    def __new__(cls, tgff_file, name):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update( {tgff_file : Parser().parse_file(tgff_file)} )
        
        tgff_graphs = _parsed_tgff_files[tgff_file][0]
        
        if name not in tgff_graphs:
            raise TgffReferenceError()
        
        return tgff_graphs[name].to_kpn_graph()


class TraceGeneratorWrapper:
    def __new__(cls, tgff_file, graph_name, repetition=1):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update( {tgff_file : Parser().parse_file(tgff_file)} )
        
        tgff_components = _parsed_tgff_files[tgff_file]
        processor_dict = {}

        for processor in tgff_components[1]:
            processor_dict.update({processor.type : processor})

        trace_generator = TgffTraceGenerator(processor_dict, tgff_components[0][graph_name], repetition)
        
        return trace_generator
    

class PlatformFromTgff:
    def __new__(cls, platform_type, processor_1, processor_2, processor_3, processor_4, tgff_file):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update( {tgff_file : Parser().parse_file(tgff_file)} )
        
        tgff_processors = _parsed_tgff_files[tgff_file][1]

        processor_dict = {}

        for proc in tgff_processors:
            processor_dict.update({proc.type : proc})


        if platform_type == 'bus':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return DesignerPlatformBus(processor_dict[processor_1])

        elif platform_type == 'parallella':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return DesignerPlatformMesh(processor_dict[processor_1], processor_dict[processor_2])

        elif platform_type == 'odroid':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return DesignerPlatformOdroid(processor_dict[processor_1],
                                                processor_dict[processor_2])

        elif platform_type == 'exynos990':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_3.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_4.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return DesignerPlatformExynos990(processor_dict[processor_1],
                                                   processor_dict[processor_2],
                                                   processor_dict[processor_3],
                                                   processor_dict[processor_4])
        elif platform_type == 'coolidge':

            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return DesignerPlatformCoolidge(processor_dict[processor_1], processor_dict[processor_2])

        elif platform_type == 'multi_cluster':
            if int(processor_1.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            if int(processor_2.split('_')[1]) >= len(tgff_processors):
                raise TgffReferenceError()

            return DesignerPlatformMultiCluster(processor_dict[processor_1], processor_dict[processor_2])


        else:
            raise RuntimeError('You have to implement this type first!')



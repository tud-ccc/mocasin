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
    



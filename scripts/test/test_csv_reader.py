# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit


import os
import unittest
import pytest

from pykpn.slx.config import SlxSimulationConfig
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.util import plot
from pykpn.util.csv_reader import DataReader

class test_CSVReader(unittest.TestCase):
    
    def test_plot(self):
        configFilePath = "apps/audio_filter/exynos/config.ini"
        csvFilePath = "scripts/test/testValues.csv"
        destination = "scripts/test/testplot"
        applicationString = "audio_filter"
        
        platform = None
        kpns = {}
        
    
        try:
            # parse the config file
            config = SlxSimulationConfig(configFilePath)
            slx_version = config.slx_version

            # create the platform
            if config.platform_class is not None:
                platform = config.platform_class()
            else:
                platform_name = os.path.splitext(os.path.basename(config.platform_xml))[0]
                
                platform = SlxPlatform(platform_name, config.platform_xml, slx_version)

        # create all graphs
            for app_config in config.applications:
                app_name = app_config.name
                kpns[app_name] = SlxKpnGraph(app_name, app_config.cpn_xml, slx_version)
        except:
            raise RuntimeError("Unable to parse the given config file")
    
        if platform == None or kpns[applicationString] == None:
            raise RuntimeError("Platform or KpnGraph not successfully initialized")
    
        dataReader = DataReader(platform,
                            csvFilePath,
                            kpns[applicationString],
                            "default",
                            "default",
                            "default")
    
        mappings = dataReader.formMappings()
    
        compareProperty = []
        mappingList = []

        for key in mappings:
            mappingList.append(mappings[key][0])
            compareProperty.append(float(mappings[key][1]))
        
        if not os.environ.get('DISPLAY', '') == '':
            plot.visualize_mapping_space(mappingList, compareProperty, destination)
            fileExists = os.path.isfile(destination + ".pdf")
            assert(fileExists == True)
            os.remove(destination + ".pdf")
        
        else:
            assert(len(mappingList) > 0)
            assert(len(compareProperty) > 0)
            assert(len(mappingList) == len(compareProperty))
            
        
        
        

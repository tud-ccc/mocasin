# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens


import argparse
import os
from pykpn.slx.config import SlxSimulationConfig
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.util import plot
from pykpn.util.csv_reader import DataReader


def main():
    """This script takes a csv file and an SLX config file as input and generates an graph where the mapping space is shown with reduced
    dimensions, while maintaining the distances between mappings.
    """
    parser = argparse.ArgumentParser(description='Plots mappings saved in csv files.')

    parser.add_argument('filePath', metavar='P', type=str, help='Path to the CSV file')

    parser.add_argument('configFile', metavar='C', type=str,
                        help='The path to the Slx config file for the used platform')

    parser.add_argument('application', metavar='A', type=str, help='The application that was running')

    parser.add_argument('--property',
                        metavar='O',
                        type=str,
                        default='wall_clock_time',
                        help='the measured property, mappings will be compared by')

    parser.add_argument('--prefix',
                        metavar='PR',
                        type=str,
                        default='default',
                        help='affix for process names in the CSV file, in case they are not exactly the same as in the application description')

    parser.add_argument('--suffix',
                        metavar='SU',
                        type=str,
                        default='default',
                        help='suffix for process names in the CSV file, in case they are not exactly the same as in the application description')
    args = parser.parse_args()

    config_dict = {
        'filePath' : args.filePath,
        'configFile' : args.configFile,
        'app_name' :  args.application,
        'property' : args.property,
        'prefix': args.prefix,
        'suffix' :  args.suffix
    }
    log.warn('Using this script is deprecated. Use the pykpn_manager instead.')
    csv_plot(config_dict)
    # Prepare config

def csv_plot(cfg):
    platform = None
    kpns = {}

    try:
        # parse the config file
        if 'configFile' in cfg:
            config = SlxSimulationConfig(cfg['configFile'])
        else:
            config = SlxSimulationConfig(config_dict=cfg)

        slx_version = config.slx_version

        # create the platform
        if config.platform_class is not None:
            platform = config.platform_class()
        else:
            platform_name = os.path.splitext(
                os.path.basename(config.platform_xml))[0]
            platform = SlxPlatform(platform_name, config.platform_xml,
                                   slx_version)

        # create all graphs
        for app_config in config.applications:
            app_name = app_config.name
            kpns[app_name] = SlxKpnGraph(app_name,
                                         app_config.cpn_xml,
                                         slx_version)
    except:
        raise RuntimeError("Unable to parse the given config file")
    
    if platform == None or kpns[cfg['app_name']] == None:
        raise RuntimeError("Platform or KpnGraph not successfully initialized")
    
    dataReader = DataReader(platform,
                            cfg['filePath'],
                            kpns[cfg['app_name']],
                            cfg['property'],
                            cfg['prefix'],
                            cfg['suffix'])
    
    mappings = dataReader.formMappings()
    
    compareProperty = []
    mappingList = []

    for key in mappings:
        mappingList.append(mappings[key][0])
        compareProperty.append(float(mappings[key][1]))
        
    plot.visualize_mapping_space(mappingList, compareProperty)

if __name__ == "__main__":
    main()


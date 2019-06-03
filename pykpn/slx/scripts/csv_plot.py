import argparse
import os
from pykpn.slx.config import SlxSimulationConfig
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.util import plot
from pykpn.util.csv_reader import DataReader

parser = argparse.ArgumentParser(description='Plots mappings saved in csv files.')

parser.add_argument('filePath', metavar='P', type=str, help='Path to the CSV file')

parser.add_argument('configFile', metavar='C', type=str, help='The path to the Slx config file for the used platform')

parser.add_argument('application', metavar='A', type=str, help='The application that was running')

parser.add_argument('--property', 
                    metavar='O', 
                    type=str, 
                    default= 'wall_clock_time',
                    help='the measured property, mappings will be compared by')

parser.add_argument('--prefix', 
                    metavar='PR', 
                    type=str, 
                    default= 'default',
                    help='affix for process names in the CSV file, in case they are not exactly the same as in the application description')

parser.add_argument('--suffix', 
                    metavar='SU', 
                    type=str, 
                    default= 'default',
                    help='suffix for process names in the CSV file, in case they are not exactly the same as in the application description')

if __name__ == "__main__":
    args = parser.parse_args()
    
    platform = None
    kpns = {}
    
    try:
        # parse the config file
        config = SlxSimulationConfig(args.configFile)
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
    
    if platform == None or kpns[args.application] == None:
        raise RuntimeError("Platform or KpnGraph not successfully initialized")
    
    dataReader = DataReader(platform,
                            args.filePath,
                            kpns[args.application],
                            args.property,
                            args.prefix,
                            args.suffix)
    
    mappings = dataReader.formMappings()
    
    compareProperty = []
    mappingList = []

    for key in mappings:
        mappingList.append(mappings[key][0])
        compareProperty.append(float(mappings[key][1]))
        
    plot.visualize_mapping_space(mappingList, compareProperty)
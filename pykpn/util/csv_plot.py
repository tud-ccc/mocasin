import csv
import argparse
from slx.platform import SlxPlatform
from slx.kpn import SlxKpnGraph
from mapper.random import RandomMapping
import matplotlib.pyplot as plt

from pykpn.util import plot
from pykpn.common.mapping import Mapping

class DataReader():
    def __init__(self, filepath, platformpath):
        self._mDataDict = {}
        self._mMappingDict  = {}
        
        self._mPlatform = SlxPlatform('SlxPlatform', platformpath, '2017.04')
        self._mKpnInstance = SlxKpnGraph('SlxKpnGraph',  '../../apps/audio_filter.cpn.xml','2017.04')
        
        with open(filepath) as csvFile:
            reader = csv.DictReader(csvFile)
            i = 0
            for row in reader:
                self._mDataDict.update({i : {'fft_l' : row['t_fft_l'],
                                            'fft_r' : row['t_fft_r'],
                                            'filter_l' : row['t_filter_l'],
                                            'filter_r' : row ['t_filter_r'],
                                            'ifft_l' : row['t_ifft_l'],
                                            'ifft_r' : row['t_ifft_r'],
                                            'sink' : row['t_sink'],
                                            'src' : row['t_src'],
                                            'wall_clock_time' : row['wall_clock_time']}})
                i += 1
        
                
    def printDataDict(self):
        for entry in self._mDataDict:
            print(self._mDataDict[entry])
            
    def printMappingDict(self):
        for entry in self._mMappingDict:
            print(self._mMappingDict[entry][0].to_string())
            print('wall_clock_time : ' + self._mMappingDict[entry][1])
        
    def formMappings(self):
        for entry in self._mDataDict:
            mapping = Mapping(self._mKpnInstance, self._mPlatform)
            
            from_list = []
            
            for key in self._mDataDict[entry]:
                if key != 'wall_clock_time':
                    as_string = self._mDataDict[entry][key].split()
                    as_number = int(as_string[len(as_string-2)] + as_string[len(as_string-1)])
                    from_list.append(as_number)
            self._mMappingDict.update({entry : (mapping, self._mDataDict[entry]['wall_clock_time'])})
        return self._mMappingDict
    

parser = argparse.ArgumentParser(description='Converts csv file to mapping objects and plots them.')
parser.add_argument('filepath', metavar='F', type=str, help='Path to the csv file')
parser.add_argument('platformpath', metavar='P', type=str, help='Path to the xml description of the platform')

if __name__ == "__main__":
    args = parser.parse_args()
    dataReader = DataReader(parser.parse_args().filepath, parser.parse_args().platformpath)
    mappings = dataReader.formMappings()
    
    exec_times = []
    mapping_list = []
    
    mPlatform = SlxPlatform('SlxPlatform', parser.parse_args().platformpath, '2017.04')
    mKpnInstance = SlxKpnGraph('SlxKpnGraph',  '../../apps/audio_filter.cpn.xml','2017.04')
    test = RandomMapping(mKpnInstance,mPlatform).to_list()
    for key in mappings:
        #mapping_list.append(mappings[key][0])
        mapping_list.append(RandomMapping(mKpnInstance,mPlatform))
        exec_times.append(float(mappings[key][1]))
        
    plot.visualize_mapping_space(mapping_list, exec_times)

    
    
    
    
    
    
    
    
    
    
    
import csv
import argparse
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from _collections import OrderedDict

from pykpn.util import plot
from pykpn.common.mapping import Mapping

class DataReader():
    def __init__(self, platform,
                    application,
                    filePath,
                    platformPath='default',
                    kpnPath='default',
                    attribute='default',
                    processPrefix='default',
                    processSuffix='default'):
        
        self._mProcessNames = []
        self._mDataDict = {}
        self._mMappingDict  = OrderedDict()
        
        if platformPath != 'default':
            self._mPlatform = SlxPlatform('SlxPlatform', platformPath, '2017.04')
        else:
            path = '../../apps/' + application + '/' + platform + '/' + platform + '.platform'
            self._mPlatform = SlxPlatform('SlxPlatform', path, '2017.04')
        
        if kpnPath != 'default':
            self._mKpnInstance = SlxKpnGraph('SlxKpnGraph', kpnPath, '2017.04')
        else:
            path = '../../apps/' + application + '.cpn.xml'
            self._mKpnInstance = SlxKpnGraph('SlxKpnGraph', path,'2017.04')
        for process in self._mKpnInstance.processes():
            self._mProcessNames.append(process.name)
        
        if attribute == 'default':
            self._desiredProperty = 'wall_clock_time'
        else:
            self._desiredProperty = attribute
        
        if processPrefix == 'default':
            self._prefix = 't_'
        else:
            self._prefix = processPrefix
            
        if processSuffix == 'default':
            self._suffix = ''
        else:
            self._suffix = processSuffix
        
        with open(filePath) as csvFile:
            reader = csv.DictReader(csvFile)
            i = 0
            for row in reader:
                toUpdate = {i : {}}
                for name in self._mProcessNames:
                    toUpdate[i].update({ name : row[self._prefix + name + self._suffix]})
                toUpdate[i].update({self._desiredProperty : row[self._desiredProperty]})
                self._mDataDict.update(toUpdate)  
                i += 1
        
                
    def printDataDict(self):
        for entry in self._mDataDict:
            print(self._mDataDict[entry])
            
    def printMappingDict(self):
        for entry in self._mMappingDict:
            print(self._mMappingDict[entry][0].to_string())
            print('wall_clock_time : ' + self._mMappingDict[entry][1])
    
    def getMappings(self):
        return
    
    def formMappings(self):
        for entry in self._mDataDict:
            mapping = Mapping(self._mKpnInstance, self._mPlatform)
            fromList = []
            
            for key in self._mDataDict[entry]:
                if key != self._desiredProperty:
                    asString = list(self._mDataDict[entry][key])
                    asNumber = ''
                    
                    i = len(asString)
                    while(i > 0):
                        i -= 1
                        try:
                            int(asString[i])
                            asNumber = asString[i] + asNumber
                        except:
                            break
                        
                    asNumber = int(asNumber)
                    fromList.append(asNumber)
            
            if fromList != []:
                mapping.from_list(fromList)
            self._mMappingDict.update({entry : (mapping, self._mDataDict[entry][self._desiredProperty])})
        return self._mMappingDict
    

parser = argparse.ArgumentParser(description='Converts CSV file to mapping objects and plots them.')

parser.add_argument('platform', metavar='T', type=str, help='The platform the application was running on')

parser.add_argument('application', metavar='A', type=str, help='The application that was running')

parser.add_argument('filePath', metavar='F', type=str, help='Path to the CSV file')

parser.add_argument('--platformPath', 
                    metavar='P', 
                    type=str, 
                    default= 'default',
                    help='path to the XML description of the platform')

parser.add_argument('--kpnPath', 
                    metavar='K', 
                    type=str, 
                    default= 'default',
                    help='path to the XML description of the applications KPN graph')

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
    dataReader = DataReader(args.platform,
                            args.application,
                            args.filePath,
                            args.platformPath,
                            args.kpnPath,
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
    
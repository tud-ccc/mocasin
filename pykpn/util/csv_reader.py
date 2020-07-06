import csv
import zipfile
import os

from _collections import OrderedDict
from pykpn.common.mapping import Mapping
from pykpn.common.platform import Platform
from pykpn.common.kpn import KpnGraph
from pykpn.mapper.partial import ComFullMapper, ProcPartialMapper


class DataReader():
    def __init__(self, platform, kpnGraph, cfg):

        filePath = cfg['csv_file']
        attribute = cfg['property']
        processPrefix = cfg['prefix']
        processSuffix = cfg['suffix']
        if not isinstance(platform, Platform):
            raise RuntimeError("Platform object is not valid")
        
        if not isinstance(kpnGraph, KpnGraph):
            raise RuntimeError("KpnGraph object is not valid")
        
        self._mProcessNames = []
        self._mDataDict = {}
        self._mMappingDict  = OrderedDict()
        self._mPlatform = platform
        self._mKpnInstance = kpnGraph
        self._mComMapper = ComFullMapper(kpnGraph,platform,cfg)
        self._mMapper = ProcPartialMapper(kpnGraph,platform,self._mComMapper)

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
        
        pathAsList = filePath.split('/')
        lastElement = pathAsList[len(pathAsList)-1]
        if lastElement.split('.')[len(lastElement.split('.'))-1] == 'zip':
            with zipfile.ZipFile(filePath, 'r') as zipFile:
                i = 0
                for file in zipFile.namelist():
                    extractet = zipFile.extract(file)
                    with open(extractet) as csvFile:
                        reader = csv.DictReader(csvFile)
                        for row in reader:
                            toUpdate = {i : {}}
                            for name in self._mProcessNames:
                                toUpdate[i].update({ name : row[self._prefix + name + self._suffix]})
                            toUpdate[i].update({self._desiredProperty : row[self._desiredProperty]})
                            self._mDataDict.update(toUpdate)  
                            i += 1
                    os.remove(extractet)
        else:
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
    
    def formMappings(self):
        for entry in self._mDataDict:
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
                mapping = self._mMapper.generate_mapping(fromList)
            else:
                mapping = Mapping(self._mKpnInstance,self._mPlatform)
            self._mMappingDict.update({entry : (mapping, self._mDataDict[entry][self._desiredProperty])})
        return self._mMappingDict
    
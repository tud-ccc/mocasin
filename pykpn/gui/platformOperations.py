#author Felix Teweleit

from pykpn.common.platform import __init__
from numpy import integer

class platformOperations (object):
    '''
    contains the necessary operations to extract the information from am platform class needed
    to draw it properly
    '''
    
    
    '''
    takes the processor dictionary of an platform and converts it in a dictionary with a key for every class of processors which contains a list of the processors 
    of the class      
    '''
    @staticmethod
    def getProcessorScheme(self, processorDict):
        recognizedClasses = {}
        
        for processor in processorDict:
            if not processor.type in recognizedClasses:
                recognizedClasses[processor.type] = []
                recognizedClasses[processor.type].append(processor.name) 
            else:
                recognizedClasses[processor.type].append(processor.name)
        
        return recognizedClasses
    
    
    '''
    does the same as getProcessorScheme() but also sorts the processors by there indices if they are given in the name
    '''
    @staticmethod
    def getSortedProcessorScheme(self, processorDict):     
        recognizedClasses = self.getProcessorScheme(self, processorDict)
        orderedClasses = []
        processorClasses= []
        for processorClass in recognizedClasses:
            processorClasses.append(processorClass)
            processorList = []
            for processor in recognizedClasses[processorClass]:
                tmpList = list(processor)
                tmpString = ''
                for item in tmpList:
                    if item.isdigit():
                        tmpString += item
                value = int(tmpString)
                processorList.append([value, processor])
            ordered = []
            for toAppend in processorList:
                if len(ordered) == 0:
                    ordered.append(toAppend)
                else:
                    for item in ordered:
                        inserted = False
                        if item[0] > toAppend[0]:
                            ordered.insert(ordered.index(item), toAppend)
                            inserted = True
                            break
                        else:
                            pass
                    if not inserted:
                        ordered.append(toAppend)
            for item in ordered:
                item.reverse()
                item.pop()
            orderedClasses.append(ordered)
        return (processorClasses, orderedClasses)
                    
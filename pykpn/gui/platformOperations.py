#author Felix Teweleit
from SimPy.tkconsole import members
from listOperations import listOperations


class platformOperations (object):
    '''
    contains the necessary operations to extract the information from am platform class needed
    to draw it properly
    '''
    
    
    '''
    takes the processor dictionary of an platform and converts it in tupel with a list for of class of processors and a list of the processors 
    of each class      
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
        classes = []
        processors = []
        for key in recognizedClasses:
            classes.append(key)
            processors.append(recognizedClasses[key])
        
        return (classes, processors)
    
    
    '''
    takes a List of processing units and, if there name includes there index, give them back in an ordered List
    '''
    @staticmethod
    def getSortedProcessorScheme(self, peList):     
        processors = []
        for pe in peList:
            tmpList = list(pe)
            tmpString = ''
            for item in tmpList:
                if item.isdigit():
                    tmpString += item
            value = int(tmpString)
            processors.append([value, pe])
        ordered = []
        for toAppend in processors:
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
        finalList = []
        for item in ordered:
            finalList.append(item[1])
        return finalList
    
    '''
    takes a list of processing Elements and returns a list only containing the names of the elements as strings
    '''
    @staticmethod
    def peToString(self, peList):
        stringList = []
        for processor in peList:
            stringList.append(processor.name)
        return stringList
    
    '''
    takes a primtive and returns a list, containing all processing units that either consume or produce for this primitive. As an aspect for security you have to also pass a list of processing
    elements that may can be used by the primitive, otherwise they will not be added to the list
    '''
    @staticmethod
    def getMembersOfPrimitive(self, peList, primitive):
        members = []
        for consumer in primitive.consumers:
            if peList.count(consumer.name) > 0: 
                if members.count(consumer.name) == 0:
                    members.append(consumer.name)
        for producer in primitive.producers:
            if peList.count(producer.name) > 0:
                if members.count(producer.name) == 0:
                    members.append(producer.name)
        return members
    
    '''
    takes a list of all processing units of the platform and a list of all primitives of the platform and returns a list of tuples, where each tuple consists of the name of the primitive and 
    the list of included processing units, if a primitive includes all elements of an other primitive the tuple of the second primitive will be included in the list of the first one
    '''
    @staticmethod
    def getPlatformDescription(self, peList, primitives):
        i = 1   #var to hold the amount of members in the primitive, start with two because one is special case and handled below
        primitiveStructure = []
        peList = self.peToString(self, peList)
        while(0 < len(primitives)):
            primitivesCopy = list(primitives)
            for primitive in primitivesCopy:
                members = self.getMembersOfPrimitive(self, peList, primitive)
                if len(members) == i:
                    tempMemberSet = []
                    for member in members:
                        if not listOperations.containsItem(self, tempMemberSet, member):
                            isInserted = False
                            for entry in primitiveStructure:
                                if listOperations.containsItem(self, entry[1], member):
                                    tempMemberSet.append(entry)
                                    primitiveStructure.pop(primitiveStructure.index(entry))
                                    isInserted = True
                            if not isInserted:
                                tempMemberSet.append(member)
                    primitiveStructure.append((primitive.name, tempMemberSet))
                    primitives.pop(primitives.index(primitive))
                else:
                    pass
            i += 1
            
        return primitiveStructure
            
        
#author Felix Teweleit
from pykpn.gui.listOperations import listOperations

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
    takes a primitive and returns a list, containing all processing units that either consume or produce for this primitive. As an aspect for security you have to also pass a list of processing
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
        i = 1   
        primitiveStructure = []
        primitives = list(primitives)
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
    
    '''
    method takes an platform an checks for each primitive if there is an other primitive which connects the same pe's. it returns a list containing lists containing 
    all primitives that are equal to another
    '''
    @staticmethod
    def findEqualPrimitives(self, platform):
        primitives = list(platform.primitives())
        peList = self.peToString(self, platform.processors())
        primitiveList =  []
        for primitive in primitives:
            if primitiveList == []:
                primitiveList.append([primitive])
            else:
                isInserted = False
                for item in primitiveList:
                    if self.getMembersOfPrimitive(self, peList, primitive) == self.getMembersOfPrimitive(self, peList, item[0]):
                        item.append(primitive)
                        isInserted = True
                        break
                if not isInserted:
                    primitiveList.append([primitive])
        primitiveNames = []
        for item in primitiveList:
            if isinstance(item, list):
                tmpList = []
                for primitive in item:
                    tmpList.append(primitive.name)
                primitiveNames.append(tmpList)
            else:
                primitiveNames.append(item.name)
        return primitiveNames
    
    
    '''
    this method takes a platform description and a list generated by the findEqualPrimitives method and merges each primitives that contain the same pe's 
    together in one primitive
    '''
    @staticmethod
    def mergeEqualPrimitives(self, platformDescription, equalList):
        copy = platformDescription
        mergedDescription = []
        if isinstance(platformDescription, list):
            for item in platformDescription:
                if isinstance(item, tuple):
                    
                    noc = False
                    for equalSheet in equalList:
                            if listOperations.containsItem(listOperations, equalSheet, item[0]) and len(equalSheet) > 2:
                                noc = True
                    if noc:
                        newItem = ('network_on_chip', [])
                    else:
                        newItem = (item[0],[])
                    
                    if len(item[1]) == 1 and isinstance(item[1][0], tuple):
                        for toAppend in self.mergeEqualPrimitives(self, item[1][0][1], equalList):
                            newItem[1].append(toAppend)
                    elif len(item[1]) == 1 and not isinstance(item[1][0], tuple):
                        newItem[1].append(item[1][0])
                    elif len(item[1])>1:
                        for innerItem in item[1]:
                            if(isinstance(innerItem, tuple)):
                                newInnerItem = (innerItem[0],self.mergeEqualPrimitives(self, innerItem[1], equalList))
                                newItem[1].append(newInnerItem)
                            else:
                                newItem[1].append(innerItem)
                    mergedDescription.append(newItem)
                else:
                    mergedDescription.append(item)
            
            if mergedDescription != copy:
                mergedDescription = self.mergeEqualPrimitives(self, mergedDescription, equalList)
            return mergedDescription        
        else:
            raise RuntimeError('you are trying to merge something, that is rather a list or an tuple. Please stop!')
    
    '''
    this method is basically a wrapper for the organizePEs method, it just searches for the noc entry platform
    description and then calls the organizePEs method on this entry
    '''    
    @staticmethod
    def createNocMatrix(self, platformDescription, platform):
        newDescription = []
        for element in platformDescription:
            if isinstance(element, tuple):
                if element[0] == 'network_on_chip':
                    element = (element[0], self.organizePEs(self, element[1], platform.to_adjacency_dict()))
                    newDescription.append(element)
                else:
                    element = (element[0], self.createNocMatrix(self, element[1], platform))
                    newDescription.append(element)
            else:
                newDescription.append(element)
        return newDescription
    
    '''
    this method creates a list of PEs which can be later converted in to a Matrix via the convertToMatrix method in the list operation class. Each PE will be located next to the
    PEs it has i physical link to
    '''
    @staticmethod
    def organizePEs(self, peList, adjacencyDict):
        peValues = []
        for entry in adjacencyDict:
            if listOperations.containsItem(listOperations, peList, entry):
                minimalCost = 1000000000 #this is just a number so high, that there must be a value below
                peWithMinimalCost = []
                for tupel in adjacencyDict[entry]:
                    if tupel[1] < minimalCost and tupel[1] > 0:
                        minimalCost = tupel[1]
                        peWithMinimalCost = []
                    if tupel[1] == minimalCost:
                        peWithMinimalCost.append(tupel[0])
                peValues.append([entry, len(peWithMinimalCost), peWithMinimalCost])
        
        
        organizedPEs = []
        firstRow = True
        rowLength = 0
        lastAppended = 0        #keep the amount of neighbors of the last appended PE and the PE before that, to check if new row had begun 
        lastlastAppended = 0
        while(len(peValues) > 0):
            
            if len(organizedPEs) == 0:
                for entry in peValues:
                    if entry[1] == 2:
                        organizedPEs.append(entry[0])
                        peValues.pop(peValues.index(entry))
                        lastAppended = entry[1]
                        break
                continue
            
            
            candidates = []
            
            if firstRow:
                if lastAppended < lastlastAppended:
                    rowLength = len(organizedPEs)
                    firstRow = False
                    lastEntry = organizedPEs[len(organizedPEs) - rowLength]
                else:
                    lastEntry = organizedPEs[len(organizedPEs) - 1]
                
                for entry in peValues:
                    if listOperations.containsItem(listOperations, entry[2], lastEntry) and (entry[1] == 2 or entry[1] == 3):
                        candidates.append(entry)
                
            if not firstRow:
                if lastAppended < lastlastAppended:
                    lastEntry = organizedPEs[len(organizedPEs) - rowLength]
                else:
                    lastEntry = organizedPEs[len(organizedPEs) - 1]
            
                for entry in peValues:
                    if listOperations.containsItem(listOperations, entry[2], lastEntry):
                        candidates.append(entry)
            
            if len(candidates) == 0:
                raise RuntimeError('No neighbor found for PE: ' + lastEntry + ' in NOC')
            
            elif len(candidates) == 1:
                organizedPEs.append(candidates[0][0])
                peValues.pop(peValues.index(candidates[0]))
                lastlastAppended = lastAppended
                lastAppended = candidates[0][1]
            
            else:
                toAppend = self.lovedNeighbor(self, candidates, organizedPEs)
                organizedPEs.append(toAppend[0])
                peValues.pop(peValues.index(toAppend))
                lastlastAppended = lastAppended
                lastAppended = toAppend[1]
                continue
        return organizedPEs

    '''
    help function to determine which PE has the most physical links in to the existing noc structure
    '''
    @staticmethod
    def lovedNeighbor(self, candidates, domicile):
        amountOfNeighbors = []
        for candidate in candidates:
            i = 0
            for neighbor in candidate[2]:
                if listOperations.containsItem(listOperations, domicile, neighbor):
                    i += 1
            amountOfNeighbors.append((i, candidate))
        
        favourite = amountOfNeighbors[0]
        
        for neighbor in amountOfNeighbors:
            if neighbor[0] > favourite[0]:
                favourite = neighbor
        
        return favourite[1]

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
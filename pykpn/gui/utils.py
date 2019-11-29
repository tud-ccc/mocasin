# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from collections import Sequence
from itertools import chain, count

class listOperations(object):
    """Class contains custom functions to operate on lists, that are needed to prepare platforms and mappings to be drawn.
    """
    
    @staticmethod
    def convertToMatrix(givenList):
        """Converts a list in a square matrix, represented by a list, that contains a list for each row with an entry for each element in that row.
        :param list[] givenList: The list that should be converted. The type of elements does not matter.
        :returns: The matrix represented by a list of lists.
        :rtype list[list[]]:
        """
        i = 2 
        while(i*i < len(givenList)):
            i = i + 1
        if(i*i == len(givenList)): 
            animationMatrix = []
            actualRow = 0
            entryToAdd = 0
            while(actualRow < i):
                actualRow += 1
                actualColumn = 0
                tmpList = []
                while(actualColumn < i):
                    tmpList.append(givenList[entryToAdd])
                    actualColumn += 1
                    entryToAdd += 1
                animationMatrix.append(tmpList)
            return animationMatrix
        else:
            j = 1
            while not ((len(givenList)-j)/i).is_integer():
                j += 1
            k = (len(givenList)-j) / i
            animationMatrix = []
            actualRow = 0
            entryToAdd = 0
            while(actualRow < k):
                tmpList = []
                actualRow += 1
                actualColumn = 0
                while(actualColumn < i):
                    tmpList.append(givenList[entryToAdd])
                    entryToAdd += 1
                    actualColumn += 1
                animationMatrix.append(tmpList)
            tmpList = []
            while(j > 0):
                tmpList.append(givenList[len(givenList)-(j)])
                j -= 1
            animationMatrix.append(tmpList)
            return animationMatrix
    
    @staticmethod
    def getDimension(givenMatrix):
        """Returns the maximal dimension of a matrix.
        :param list[list[]] givenMatrix: The matrix represented by a list containing a list for each row with an entry for each element in that row.
                                         The type of the items does not matter.
        :returns: The maximal dimension of that matrix.
        :rtype int:
        """
        j = 1
        if not isinstance(givenMatrix, list):
            return 1
        for entry in givenMatrix:
            if isinstance(entry, list):
                if len(entry) > j:
                    j = len(entry)
            else:
                continue
        return j
    
    @staticmethod
    def containsItem(givenList, element):
        """Checks if the given list contains the given element. The element can be in sub-lists or tuples or lists in tuples contained by the given list.
        :param list[list[], (,list[]), ] givenList: A list consisting of items, lists or tuples containing list. The type of the items does not matter.
        :param element: The element searched for. The type of the element does not matter.
        :returns: If the element is somewhere in the given list or not.
        :rtype bool:
        """
        if not isinstance(givenList, list) and not isinstance(givenList, tuple):
            if givenList == element:
                return True
            else:
                return False
        else:
            if isinstance(givenList, list):
                for item in givenList:
                    if listOperations.containsItem(item, element):
                        return True
            elif isinstance(givenList, tuple):
                if listOperations.containsItem(givenList[0], element):
                    return True
                if listOperations.containsItem(givenList[1], element):
                    return True
        return False        

    @staticmethod
    def depth(seq):
        seq = iter(seq)
        try:
            for level in count():
                seq = chain([next(seq)], seq)
                seq = chain.from_iterable(s for s in seq if isinstance(s, Sequence))
        except StopIteration:
            return level
    
class platformOperations (object):
    """Contains functions to operate on attributes of an pykpn Platform object or created platform descriptions. Necessary for platforms to be drawn.
    """
    
    @staticmethod
    def getSortedProcessorScheme(peList):
        """Sorts a list of processing elements by there indices if they are contained in there names.
        :param list[str] peList: List of names of processing elements.
        :returns: A list containing the same processing elements but now in order if there indices.
        :rtype list[str]:
        """     
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
    
    @staticmethod
    def peToString(peList):
        """Returns a list of just the names of processing elements for a list of pykpn Processors.
        :param list[Processor]: The list of pykpn Processor objects.
        :returns: A list of just the names of the Processor objects.
        :rtype list [str]:
        """
        stringList = []
        for processor in peList:
            stringList.append(processor.name)
        return stringList
    
    @staticmethod
    def getMembersOfPrimitive(primitive):
        """Returns a list of all consumers or producers for a primitive.
        :param Primitive primitive: The primitive for which the consumers and producers should be found.
        :returns: A list of processing elements that either produce or consume on this primitive.
        :rtype list[Processor]:
        """
        members = []
        for consumer in primitive.consumers:
            if members.count(consumer.name) == 0:
                members.append(consumer.name)
        for producer in primitive.producers:
            if members.count(producer.name) == 0:
                members.append(producer.name)
        return members
    
    @staticmethod
    def getPlatformDescription(peList, primitives):
        """Returns a hierarchic list of tuples where each tuple contains the name of a primitive and a list of minor primitives or processing elements.
        :param list[Processor] peList: The list of all processing elements of the platform.
        :param list[Primitive] primitives: A list of all primitives of the platform.
        :returns: A list of tuples containing primitive names and a list of their minor primitives or processing elements.
        :rtype list[(str, [(str, [str])])]:  
        """
        i = 1   
        primitiveStructure = []
        primitives = list(primitives)
        peList = platformOperations.peToString(peList)
        while(0 < len(primitives)):
            primitivesCopy = list(primitives)
            for primitive in primitivesCopy:
                members = platformOperations.getMembersOfPrimitive(primitive)
                if len(members) == i:
                    tempMemberSet = []
                    for member in members:
                        if not listOperations.containsItem(tempMemberSet, member):
                            isInserted = False
                            for entry in primitiveStructure:
                                if listOperations.containsItem(entry[1], member):
                                    tempMemberSet.append(entry)
                                    primitiveStructure.pop(primitiveStructure.index(entry))
                                    isInserted = True
                            if not isInserted:
                                tempMemberSet.append(member)
                    name = primitive.name.split("_")
                    newName = ""
                    for fragment in name:
                        if fragment == 'putget':
                            continue
                        else:
                            if len(newName) == 0:
                                newName += fragment
                            else:
                                newName += "_" + fragment
                    primitiveStructure.append((newName, tempMemberSet))
                    primitives.pop(primitives.index(primitive))
                else:
                    pass
            i += 1
            
        return primitiveStructure
    
    @staticmethod
    def findEqualPrimitives(platform):
        """Find for a platform all primitives which connects exactly the same processing elements.
        :param Platform platform: A pykpn Platform object.
        :returns: A list containing lists containing all primitives which connect the same processing elements.
        :rtype list[list[str]]:
        """
        primitives = list(platform.primitives())
        primitiveList =  []
        for primitive in primitives:
            if primitiveList == []:
                primitiveList.append([primitive])
            else:
                isInserted = False
                for item in primitiveList:
                    if platformOperations.getMembersOfPrimitive(primitive) == platformOperations.getMembersOfPrimitive(item[0]):
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
    
    @staticmethod
    def mergeEqualPrimitives(platformDescription, equalList):
        """Merges all primitives that are equal in a platform description into one primitive.
        :param list[(str, [(str, [str])])] platformDescription: A list of tuples containing primitive names and a list of their minor primitives or processing elements.
        :param list[list[str]] equalList: A list containing a list which contains all primitives connecting exactly the same processing elements. 
        """
        copy = platformDescription
        mergedDescription = []
        if isinstance(platformDescription, list):
            for item in platformDescription:
                if isinstance(item, tuple):
                    noc = False
                    for equalSheet in equalList:
                            if listOperations.containsItem(equalSheet, item[0]) and len(equalSheet) > 2:
                                noc = True
                                break
                    if noc:
                        newItem = ('network_on_chip', [])
                    else:
                        newItem = (item[0],[])
                    if len(item[1]) == 1 and isinstance(item[1][0], tuple):
                        for toAppend in platformOperations.mergeEqualPrimitives(item[1][0][1], equalList):
                            newItem[1].append(toAppend)
                    elif len(item[1]) == 1 and not isinstance(item[1][0], tuple):
                        newItem[1].append(item[1][0])
                    elif len(item[1])>1:
                        for innerItem in item[1]:
                            if(isinstance(innerItem, tuple)) and len(innerItem[1]) == 1:
                                newInnerItem = ('network_on_chip',platformOperations.mergeEqualPrimitives(innerItem[1], equalList))
                                newItem[1].append(newInnerItem)
                            elif(isinstance(innerItem, tuple)):
                                newInnerItem = (innerItem[0],platformOperations.mergeEqualPrimitives(innerItem[1], equalList))
                                newItem[1].append(newInnerItem)
                            else:
                                newItem[1].append(innerItem)
                    mergedDescription.append(newItem)
                else:
                    mergedDescription.append(item)
            
            if mergedDescription != copy:
                mergedDescription = platformOperations.mergeEqualPrimitives(mergedDescription, equalList)
            return mergedDescription        
        else:
            raise RuntimeError('you are trying to merge something, that is rather a list or an tuple. Please stop!')
        
    @staticmethod
    def createNocMatrix(platformDescription, platform):
        """Searches for the network on chip component in a platform and organizes the processing elements on it.
        :param list[(str, [(str, [str])])] platformDescription: A list of tuples containing primitive names and a list of their minor primitives or processing elements.
        :param Platform platform: A pykpn Platform object.
        :returns: A platform description that lists of processing elements are ready to be drawn.
        :rtype list[(str, [(str, [str])])]:
        """
        newDescription = []
        for element in platformDescription:
            if isinstance(element, tuple):
                if element[0] == 'network_on_chip':
                    element = (element[0], platformOperations.organizePEs(element[1], platform.to_adjacency_dict()))
                    newDescription.append(element)
                else:
                    element = (element[0], platformOperations.createNocMatrix(element[1], platform))
                    newDescription.append(element)
            else:
                newDescription.append(element)
        return newDescription
    
    @staticmethod
    def organizePEs(peList, adjacencyDict):
        """Organizes the processing elements in the given list in a way, that every processing element has a physical link to its neighbor.
        :param list[str] peList: List of names of processing elements.
        :param dict{str, (str, int)} adjacencyDict: Dictionary with names of processing elements as key and tuples of names of processing elements and there communications costs
                                                    between each other.
        :returns: A list of processing elements where every processing element has a physical link to its neighbor.
        :rtype list[str]:
        """
        peValues = []
        for entry in adjacencyDict:
            if listOperations.containsItem(peList, entry):
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
                    if listOperations.containsItem(entry[2], lastEntry) and (entry[1] == 2 or entry[1] == 3):
                        candidates.append(entry)
                
            if not firstRow:
                if lastAppended < lastlastAppended:
                    lastEntry = organizedPEs[len(organizedPEs) - rowLength]
                else:
                    lastEntry = organizedPEs[len(organizedPEs) - 1]
            
                for entry in peValues:
                    if listOperations.containsItem(entry[2], lastEntry):
                        candidates.append(entry)
            
            if len(candidates) == 0:
                raise RuntimeError('No neighbor found for PE: ' + lastEntry + ' in NOC')
            
            elif len(candidates) == 1:
                organizedPEs.append(candidates[0][0])
                peValues.pop(peValues.index(candidates[0]))
                lastlastAppended = lastAppended
                lastAppended = candidates[0][1]
            
            else:
                toAppend = platformOperations.lovedNeighbor(candidates, organizedPEs)
                organizedPEs.append(toAppend[0])
                peValues.pop(peValues.index(toAppend))
                lastlastAppended = lastAppended
                lastAppended = toAppend[1]
                continue
        return organizedPEs

    @staticmethod
    def lovedNeighbor(candidates, domicile):
        """Calculates which of the processing elements have the most neighbors.
        :param list[str] candidates: List of names of processing elements.
        :param list[str] domicile: List of names of all processing elements of the platform.
        :returns: Name of the processing element with the most neighbors.
        :rtype str:
        """
        amountOfNeighbors = []
        for candidate in candidates:
            i = 0
            for neighbor in candidate[2]:
                if listOperations.containsItem(domicile, neighbor):
                    i += 1
            amountOfNeighbors.append((i, candidate))
        
        favourite = amountOfNeighbors[0]
        
        for neighbor in amountOfNeighbors:
            if neighbor[0] > favourite[0]:
                favourite = neighbor
        
        return favourite[1]
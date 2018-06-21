#author Felix Teweleit


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
    does the same as getProcessorScheme() but also sorts the processors by there indices if they are given in the name
    '''
    @staticmethod
    def getSortedProcessorScheme(self, processorDict):     
        recognizedClasses = self.getProcessorScheme(self, processorDict)
        
        orderedClasses = []
        for processorClass in recognizedClasses[0]:
            processorList = []
            for processor in recognizedClasses[1][recognizedClasses[0].index(processorClass)]:
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
            finalList = []
            for item in ordered:
                finalList.append(item[1])
            orderedClasses.append(finalList)
        return (recognizedClasses[0], orderedClasses)
    
    
    '''
    takes a list of processing elements of the same class and the dict of primitives of the platform, then it sorts the pe's  by 
    the primitives they are part of 
    '''
    @staticmethod
    def sortByPrimitives(self, peList, primitives):
        recognizedPrimitives = []
        memberAmount = []
        
        for primitive in primitives:
            members = []
            for consumer in primitive.consumers:
                if peList.count(consumer.name) > 0 :
                    if recognizedPrimitives.count(primitive.name) == 0:
                        recognizedPrimitives.append(primitive.name) 
                    if members.count(consumer.name) == 0:
                        members.append(consumer.name)

            for producer in primitive.producers:
                if peList.count(producer.name) > 0:
                    if recognizedPrimitives.count(primitive.name) == 0:
                        recognizedPrimitives.append(primitive.name)
                    if members.count(producer.name) == 0:
                        members.append(producer.name)
            if len(members) > 0:
                memberAmount.append(len(members))
                
        primitivesWithAmount = []
        i = 0
        while(i < len(recognizedPrimitives)):
            if len(primitivesWithAmount) == 0:
                primitivesWithAmount.append([recognizedPrimitives[i], memberAmount[i]])
            else:
                isInserted = False
                for primitive in primitivesWithAmount:
                    if memberAmount[i] > primitive[1]:
                        primitivesWithAmount.insert(primitivesWithAmount.index(primitive), [recognizedPrimitives[i], memberAmount[i]])
                        isInserted = True
                        break
                    else:
                        pass
                if not isInserted:
                    primitivesWithAmount.append([recognizedPrimitives[i], memberAmount[i]])
            i += 1
            
        i = len(primitivesWithAmount) - 1 #use of magic number 1 because len gives total length but the index is counted 0 based
        return primitivesWithAmount
    
    
    
    
    
    
    
        
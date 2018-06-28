#author Felix Teweleit
from mercurial.revset import contains

class listOperations(object):
    '''
    contains the necessary operations to interpret and convert the input list in a matrix for the later animation
    '''
    
    
    '''
    checks if the list contains only items in range of 0 to 10
    '''
    @staticmethod
    def checkList(self, givenList):
        if not isinstance(givenList, list):
            return False
        for i in givenList:
            if i not in range(10):
                return False
        if len(givenList) < 3:
            return False
        return True
    
    
    '''
    takes a list as parameter and converts it to a square matrix, where the last row maybe will have fewer items 
    '''
    @staticmethod
    def convertToMatrix(self, givenList):
        i = 2 #holds the amount of rows and columns for the matrix, minimum is two
        while(i*i < len(givenList)):
            i = i + 1
        if(i*i == len(givenList)): #in case matrix is a square matrix 
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
            #in case matrix is not a square matrix and the last row is not complete, j holds the elements in the last row
            j = 1
            while not isinstance(((len(givenList)-j)/i), int):
                j += 1  #calculate amount of elements in the last row 
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
    
    
    '''
    returns the max dimension of the matrix to calculate the animation raster, j holds the actual dimension
    for example: for a 3x4 Matrix getDimension would return 4 
    '''
    @staticmethod
    def getDimension(self, givenMatrix):
        j = 1
        for entry in givenMatrix:
            if isinstance(entry, list):
                if len(entry) > j:
                    j = len(entry)
            else:
                continue
        return j
    
    
    '''
    checks if a list contains somewhere the given item, even if the list contains other lists which may contain the searched item
    '''
    @staticmethod
    def containsItem(self, givenList, element):
        if not isinstance(givenList, list) and not isinstance(givenList, tuple):
            if givenList == element:
                return True
            else:
                return False
        else:
            if isinstance(givenList, list):
                for item in givenList:
                    if listOperations.containsItem(listOperations, item, element):
                        return True
            elif isinstance(givenList, tuple):
                if listOperations.containsItem(listOperations, givenList[0], element):
                    return True
                if listOperations.containsItem(listOperations, givenList[1], element):
                    return True
        return False        
            
            
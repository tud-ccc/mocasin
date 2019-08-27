# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.gui.utils import listOperations
import math

def ringTopology(elementList):
    """Creates a the adjacency list for a ring topology out of a linear list of 
    all elements in the network.
    :param list[string] elementList: A list of all elements in the network.
    """
    adjacencyList = {}
    
    for position in range(0, len(elementList)):    
        if position == 0:
            adjacencyList.update({ elementList[position] : [elementList[len(elementList) - 1], elementList[1]] })
        
        elif position == (len(elementList) - 1):
            adjacencyList.update({ elementList[position] : [elementList[position - 1], elementList[0]] })
        
        else:
            adjacencyList.update({ elementList[position] : [elementList[position - 1], elementList[position + 1]] })
    
    return adjacencyList
        

def meshTopology(elementList):
    """Creates a the adjacency list for a full meshed topology out of a linear
    list of all elements in the network.
    :param list[string] elementList: A list of all elements in the network.
    """
    adjacencyList = {}
    
    for pe in elementList:
        adjacentTo = []
        for otherPe in elementList:
            if pe != otherPe:
                adjacentTo.append(otherPe)
        adjacencyList.update({pe : adjacentTo})
        
    return adjacencyList

def torusTopology(elementList):
    """Creates a the adjacency list for a full meshed topology out of a linear
    list of all elements in the network.
    :param list[string] elementList: A list of all elements in the network.
    """
    if not math.sqrt(len(elementList)) % 1 == 0:
        raise RuntimeError("You need a square number amount of elements for a torus topology!")
    
    if len(elementList) == 4:
        return ringTopology(elementList)
    
    matrix = listOperations.convertToMatrix(elementList)
    dimension = len(matrix)
    maxIndex = dimension - 1
    adjacencyList = {}
    
    for rowPosition in range(0, dimension):
        for columnPosition in range(0, dimension):
            adjacentTo = []
            
            if rowPosition == 0 and columnPosition == 0:
                adjacentTo.append(matrix[rowPosition][maxIndex])
                adjacentTo.append(matrix[rowPosition][1])
                adjacentTo.append(matrix[maxIndex][columnPosition])
                adjacentTo.append(matrix[1][columnPosition])    
            
            elif rowPosition == 0 and columnPosition == maxIndex:
                adjacentTo.append(matrix[rowPosition][maxIndex - 1])
                adjacentTo.append(matrix[rowPosition][0])
                adjacentTo.append(matrix[maxIndex][columnPosition])
                adjacentTo.append(matrix[1][columnPosition])
                
            elif rowPosition == 0:
                adjacentTo.append(matrix[rowPosition][columnPosition - 1])
                adjacentTo.append(matrix[rowPosition][columnPosition + 1])
                adjacentTo.append(matrix[maxIndex][columnPosition])
                adjacentTo.append(matrix[1][columnPosition])
                
            elif rowPosition == maxIndex and columnPosition == 0:
                adjacentTo.append(matrix[rowPosition][maxIndex])
                adjacentTo.append(matrix[rowPosition][1])
                adjacentTo.append(matrix[rowPosition - 1][columnPosition])
                adjacentTo.append(matrix[0][columnPosition])
                
            elif rowPosition == maxIndex and columnPosition == maxIndex:
                adjacentTo.append(matrix[rowPosition][columnPosition - 1])
                adjacentTo.append(matrix[rowPosition][0])
                adjacentTo.append(matrix[rowPosition - 1][columnPosition])
                adjacentTo.append(matrix[0][columnPosition])
                
            elif rowPosition == maxIndex:
                adjacentTo.append(matrix[rowPosition][columnPosition - 1])
                adjacentTo.append(matrix[rowPosition][columnPosition + 1])
                adjacentTo.append(matrix[rowPosition - 1][columnPosition])
                adjacentTo.append(matrix[0][columnPosition])
            
            elif columnPosition == 0:
                adjacentTo.append(matrix[rowPosition][maxIndex])
                adjacentTo.append(matrix[rowPosition][1])
                adjacentTo.append(matrix[rowPosition - 1][columnPosition])
                adjacentTo.append(matrix[rowPosition + 1][columnPosition])
            
            elif columnPosition == maxIndex:
                adjacentTo.append(matrix[rowPosition][columnPosition - 1])
                adjacentTo.append(matrix[rowPosition][0])
                adjacentTo.append(matrix[rowPosition - 1][columnPosition])
                adjacentTo.append(matrix[rowPosition + 1][columnPosition])
                
            else:
                adjacentTo.append(matrix[rowPosition][columnPosition - 1])
                adjacentTo.append(matrix[rowPosition][columnPosition + 1])
                adjacentTo.append(matrix[rowPosition - 1][columnPosition])
                adjacentTo.append(matrix[rowPosition + 1][columnPosition])
            
            adjacencyList.update({matrix[rowPosition][columnPosition] : adjacentTo})
    
    return adjacencyList








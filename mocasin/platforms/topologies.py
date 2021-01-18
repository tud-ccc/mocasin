# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andrés Goens

from mocasin.gui.utils import listOperations
import math


def ringTopology(elementList):
    """Creates a the adjacency list for a ring topology out of a linear list of
    all elements in the network.
    :param list[string] elementList: A list of all elements in the network.
    """
    adjacencyList = {}

    for position in range(0, len(elementList)):
        if position == 0:
            adjacencyList.update(
                {
                    elementList[position]: [
                        elementList[len(elementList) - 1],
                        elementList[1],
                    ]
                }
            )

        elif position == (len(elementList) - 1):
            adjacencyList.update(
                {
                    elementList[position]: [
                        elementList[position - 1],
                        elementList[0],
                    ]
                }
            )

        else:
            adjacencyList.update(
                {
                    elementList[position]: [
                        elementList[position - 1],
                        elementList[position + 1],
                    ]
                }
            )

    return adjacencyList


def starTopology(elementList):
    """Creates a the adjacency list for a star topology out of a linear list of
    all elements in the network. The first element is the center.
    :param list[string] elementList: A list of all elements in the network.
    """
    adjacencyList = {}
    adjacent_to_first = []
    for position in range(1, len(elementList)):
        adjacent_to_first.append(elementList[position])
        adjacencyList.update({elementList[position]: [elementList[0]]})
    adjacencyList.update({elementList[0]: adjacent_to_first})
    return adjacencyList


def meshTopology(elementList):
    """Creates a the adjacency list for a mesh topology out of a linear
    list of all elements in the network. A mesh topology is a regular
    rectangular structure where every element except the border elements has
    exactly four neigbors (N,E,S,W). Number of elements must be a square.
    :param list[string] elementList: A list of all elements in the network.
    """
    n_squared = len(elementList)
    n = math.sqrt(n_squared)
    assert n.is_integer()
    n = int(n)
    adjacencyList = {}
    for x in range(n):
        for y in range(n):
            adjacent = []
            if x % n != 0:
                adjacent.append(elementList[y * n + (x - 1)])
            if x % n != (n - 1):
                adjacent.append(elementList[y * n + (x + 1)])
            if y % n != 0:
                adjacent.append(elementList[(y - 1) * n + x])
            if y % n != (n - 1):
                adjacent.append(elementList[(y + 1) * n + x])
            adjacencyList.update({elementList[y * n + x]: adjacent})
    return adjacencyList


def fullyConnectedTopology(elementList):
    """Creates a the adjacency list for a fully conected topology out of a linear
    list of all elements in the network.
    :param list[string] elementList: A list of all elements in the network.
    """
    adjacencyList = {}

    for pe in elementList:
        adjacentTo = []
        for otherPe in elementList:
            if pe != otherPe:
                adjacentTo.append(otherPe)
        adjacencyList.update({pe: adjacentTo})

    return adjacencyList


def torusTopology(elementList):
    """Creates a the adjacency list for a full meshed topology out of a linear
    list of all elements in the network.
    :param list[string] elementList: A list of all elements in the network.
    """
    if not math.sqrt(len(elementList)) % 1 == 0:
        raise RuntimeError(
            "You need a square number amount of elements for a torus topology!"
        )

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

            adjacencyList.update(
                {matrix[rowPosition][columnPosition]: adjacentTo}
            )

    return adjacencyList

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

"""
This script contains helpful independent methods, which are needed for
functionality in other scripts of the platform package.
"""


def simpleDijkstra(adjacencyList, source, target):
    """
    This method performs the Dijkstra algorithm on simple graphs, given as an
    adjacency list.
    :param list[list[int] adjacencyList: A list where the indexes of elements in the outer list are
    equal to the index of the graph node. The integers in the inner list are equal to the indexes
    of graph nodes the outer node has an unweighted edge to.
    :param int source: The source node from which we want to determine the path.
    :param int target: The target node to which we want to determine the path.
    :returns: The list of nodes we need to visit to reach target from source.
    :rtype list[int]:
    """
    if isinstance(adjacencyList, dict):
        for element in adjacencyList:
            if not isinstance(adjacencyList[element], list):
                return None
    else:
        return None

    if adjacencyList[source] == []:
        return None

    distances = {}

    for node in adjacencyList:
        if not node == source:
            distances.update({node: None})
        else:
            distances.update({node: (0, [source])})

    visitedNodes = [source]
    currentPath = [source]
    currentNode = source

    while not currentNode == target:
        for reachable in adjacencyList[currentNode]:
            if distances[reachable] == None:
                distances.update(
                    {
                        reachable: (
                            distances[currentNode][0] + 1,
                            currentPath + [reachable],
                        )
                    }
                )
            if distances[currentNode][0] + 1 < distances[reachable][0]:
                distances.update(
                    {
                        reachable: (
                            distances[currentNode] + 1,
                            currentPath + [reachable],
                        )
                    }
                )

        nextNode = None
        for node in distances:
            if not distances[node] == None:
                if not node in visitedNodes and nextNode == None:
                    nextNode = node
                elif not node in visitedNodes:
                    if distances[node][0] < distances[nextNode][0]:
                        nextNode = node

        if nextNode == None:
            return None
        else:
            currentPath = distances[nextNode][1]
            currentNode = nextNode
            visitedNodes.append(nextNode)
    return currentPath

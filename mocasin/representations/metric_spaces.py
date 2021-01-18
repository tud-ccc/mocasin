# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Andres Goens

from __future__ import print_function
import logging
import numpy as np
from sys import exit, stdout
from numpy.random import randint
from itertools import product
from . import permutations as perm


class FiniteMetricSpace:
    def __init__(self, matrix):
        try:
            self.D = np.array(matrix)
        except Exception as ex:
            logging.error(
                "An error ocurred while initializing a finite metric space with a distance matrix.\n"
                + str(ex)
            )
            exit(1)

        dims = self.D.shape
        if not len(dims) == 2:
            logging.error("Distances must be given as a matrix")
            return None
        if not dims[1] == dims[0]:
            logging.error("Distances must be given as a square matrix")
            return None
        self.n = dims[0]

    def dist(self, x, y):
        return self.D[x, y]

    def _ballNaive(self, p, r):
        points = []
        for i in range(self.n):
            if self.dist(p, i) <= r:
                points.append(i)
        return points

    def ball(self, p, r):
        return self._ballNaive(p, r)

    def uniformFromBall(self, p, r, npoints=1):
        return self._uniformFromBallNaive(p, r, npoints=npoints)

    def _uniformFromBallNaive(self, p, r, npoints=1):
        ball = self.ball(p, r)
        point_positions = randint(0, len(ball) - 1, size=npoints)
        points = [ball[i] for i in point_positions]
        return points

    def uniform(self):
        return randint(0, self.n - 1)


class FiniteMetricSpaceLP(FiniteMetricSpace):
    def __init__(self, M, d=2, p=1):
        self.D = None
        self.M = M
        self.d = d
        self.n = M.n ** d
        self.p = p

    def dist(self, x, y):
        if type(x) is int and type(y) is int:
            if self.D is None:
                return self._distCalc(self.int2Tuple(x), self.int2Tuple(y))
            else:
                return self.D[x, y]

        elif type(x) == list and type(y) == list:
            if self.D != None:
                x_l = self.tuple2Int(x)
                y_l = self.tuple2Int(y)
                return self.D[x_l, y_l]
            else:
                return FiniteMetricSpaceLP._distCalc(self, x, y)
        else:
            logging.error(
                "An error occurred while trying to calculate the distance of two points (wrong types?)\n"
                + str(x)
                + "\n"
                + str(y)
            )
            exit(1)

    def tuple2Int(self, x):
        return sum([xi * (self.M.n ** i) for (i, xi) in enumerate(x)])

    def int2Tuple(self, x):
        res = [0] * self.d

        # modified from euclidean algorithm
        rem = x
        i = self.d - 1
        while rem != 0:
            res[i], rem = divmod(rem, self.M.n ** i)
            i = i - 1
        return res

    def _distCalc(self, x, y):
        assert len(x) == self.d
        assert len(y) == self.d
        dist_tuple = [self.M.dist(xi, yi) for (xi, yi) in zip(x, y)]
        if self.p > 100:
            return max(dist_tuple)
        else:
            return np.power(
                sum(map(lambda x: np.power(x, self.p), dist_tuple)),
                1 / float(self.p),
            )

    def _populateD(self):
        logging.debug("Populating D...")
        stdout.flush()
        self.D = np.zeros((self.n, self.n))
        for (x, y) in product(
            product(range(self.M.n), repeat=self.d),
            product(range(self.M.n), repeat=self.d),
        ):
            x_l = self.tuple2Int(x)
            y_l = self.tuple2Int(y)
            self.D[x_l, y_l] = self._distCalc(x, y)
        logging.debug("done.")

    def ball(self, p, r):
        if type(p) is list:
            point = self.tuple2Int(p)
        elif type(p) is int:
            point = p
        elif type(p) is float:
            point = int(p)
        else:
            logging.error(
                "An error occurred while calculating the ball, unknown point\n"
                + str(p)
            )
            exit(1)
        return FiniteMetricSpace.ball(self, point, r)

    def uniform(self):
        res = []
        for i in range(0, self.d):
            res.append(self.M.uniform())
        return res


class FiniteMetricSpaceSym(FiniteMetricSpace):
    def __init__(self, M, G):
        self.D = None
        assert isinstance(M, FiniteMetricSpace)
        self.M = M
        assert isinstance(G, perm.PermutationGroup)
        self.G = G
        orbits = G.enumerate_orbits()
        self.elem2orb = {}
        self.orb2elem = {}
        for i, orb in enumerate(orbits):
            self.elem2orb[i] = orb
            for elem in orb:
                self.orb2elem[elem] = i
        self.n = i + 1  # == len(orbits)

    def dist(self, x, y):
        if type(x) is int and type(y) is int:
            if self.D is None:
                return self._distCalc(self.elem2orb[x], self.orb2elem[y])
            else:
                return self.D[x, y]

        elif type(x) == list and type(y) == list:
            if self.D != None:
                x_l = self.orb2elem[x[0]]
                y_l = self.orb2elem[y[0]]
                return self.D[x_l, y_l]
            else:
                x_orb = self.elem2orb[self.orb2elem[x[0]]]
                y_orb = self.elem2orb[self.orb2elem[y[0]]]
                return self._distCalc(list(x_orb), list(y_orb))
        else:
            logging.error(
                "An error occurred while trying to calculate the distance of two points (wrong types?)\n"
                + str(x)
                + "\n"
                + str(y)
            )
            exit(1)

    def _distCalc(self, x, y):
        # lists (sets) -> (partial) orbits on self.M
        # ints -> points on the new set
        # since G is the orthogonal group of the distance,
        # it is enough to iterate over one orbit
        dists = map(
            lambda xs: self.M.dist(xs, y[0]), self.elem2orb[self.orb2elem[x[0]]]
        )
        return min(dists)

    def _populateD(self):
        # print("Populating D...",end='')
        if self.n == -1:
            self.n = len(
                self.G.enumerate_orbits()
            )  # should I remove this per default? Could be very expensive!
        stdout.flush()
        self.D = np.zeros((self.n, self.n))
        for (x, y) in product(range(self.n), repeat=2):
            self.D[x, y] = self._distCalc(
                list(self.elem2orb[x]), list(self.elem2orb[y])
            )
        # print("done.")

    def elem2Tuple(self, elem):
        return min(self.elem2orb[elem])

    def ball(self, p, r):
        # print("calculating ball around point p " + str(p) + " with radius " + str(r))
        if type(p) is list:
            point = self.orb2elem[tuple(p)]
        elif type(p) is int:
            point = p
        elif type(p) is float or np.float64:
            point = int(p)
        else:
            logging.error(
                "An error occurred while calculating the ball, unknown point\n"
                + str(p)
                + "\n"
                + type(p)
            )
            exit(1)
        return FiniteMetricSpace.ball(self, point, r)

    def int2Tuple(self, point):
        return self.elem2Tuple(point)


class FiniteMetricSpaceLPSym(FiniteMetricSpaceLP, FiniteMetricSpaceSym):
    def __init__(self, M, G=None, d=2, p=1):
        if isinstance(M, FiniteMetricSpaceSym):
            G = M.G
            M = M.M  # take the base space (no symmetries)

        if G is None:
            G = perm.TrivialGroup(M.n)
        FiniteMetricSpaceLP.__init__(self, M, d=d, p=p)
        self.G = perm.DuplicateGroup(G, times=d)
        # print("LP, n: " + str(self.n))
        orbits = G.enumerate_tuple_orbits(d)
        self.elem2orb = {}
        self.orb2elem = {}
        for i, orb in enumerate(orbits):
            self.elem2orb[i] = orb
            for elem in orb:
                self.orb2elem[elem] = i
        self.n = i + 1  # == len(orbits)
        # print("LPSym, n: " + str(self.n))

    # three types of elemnts:
    # (1) int : representation in the size of the metric space
    # (2) list of ints: tuples in M^d (no symmetries)
    # (3) lists of lists of ints: orbits of the action on M^d (w/symmetries)

    def dist(self, x, y):
        if type(x) is int and type(y) is int:  # (1)
            if self.D is None:
                return self._distCalc(
                    list(self.elem2orb[x]), list(self.elem2orb[y])
                )
            else:
                return self.D[x, y]

        elif type(x) == list and type(y) == list:
            if type(x[0]) == list and type(y[0]) == list:  # (3)
                if self.D != None:
                    x_l = self.orb2elem[x[0]]
                    y_l = self.orb2elem[y[0]]
                    return self.D[x_l, y_l]
                else:
                    return self._distCalc(x, y)
            elif type(x[0]) == int and type(y[0]) == int:  # (2)
                if self.D != None:
                    x_l = self.orb2elem[self.elem2orb[x]]
                    y_l = self.orb2elem[self.elem2orb[y]]
                    return self.D[x_l, y_l]
                else:
                    return self._distCalc([x], [y])

        else:
            logging.error(
                "An error occurred while trying to calculate the distance of two points (wrong types?)\n"
                + str(x)
                + "\n"
                + str(y)
            )
            exit(1)

    def _distCalc(self, x, y):
        # we need to iterate over the orbits of *tuples*
        # again one is enough
        print(x)
        orb = list(self.elem2orb[self.orb2elem[tuple(x[0])]])
        dists = map(
            lambda xs: FiniteMetricSpaceLP.dist(self, list(xs), list(y[0])), orb
        )
        # print(list(map( lambda xs : (FiniteMetricSpaceLP.dist(self,list(xs),y[0]),(xs,tuple(y[0]))), self.elem2orb[self.orb2elem[tuple(x[0])]])))
        return min(dists)

    def ball(self, p, r):
        return FiniteMetricSpaceSym.ball(self, p, r)

    def int2Tuple(self, point):
        return FiniteMetricSpaceSym.elem2Tuple(self, point)


def dijkstra(graph, node_from):
    inf = float("inf")
    unvisited = set(graph.keys())
    distances = {}
    for node in graph:
        distances[node] = inf
    distances[node_from] = 0
    current = node_from

    while len(unvisited) != 0:
        for (neighbor, dist) in graph[current]:
            if neighbor in unvisited:
                tentative_distance = distances[current] + dist
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance

        min_dist = inf
        next_node = None
        unvisited.remove(current)
        for unvisited_node in unvisited:
            if distances[unvisited_node] < min_dist:
                min_dist = distances[unvisited_node]
                next_node = unvisited_node

        current = next_node
    return distances


def make_graph_symmetric(graph):
    graph_dict = {}
    for node_from in graph:
        graph_dict[node_from] = {}
        for (node_to, cost) in graph[node_from]:
            graph_dict[node_from][node_to] = cost

    symmetric_graph = {}
    for node_from in graph_dict:
        symmetric_graph[node_from] = []
        for node_to in graph_dict[node_from]:
            avg = (
                graph_dict[node_from][node_to] + graph_dict[node_to][node_from]
            ) / 2.0
            symmetric_graph[node_from].append((node_to, round(avg)))
    return symmetric_graph


def arch_to_distance_metric(
    architecture,
    scaling=True,
    heterogeneity=True,
    cycles=10000,
    min_dist_factor=0.1,
):
    if heterogeneity:
        primitives_graph = architecture.to_primitive_latency_dict()

    inf = float("inf")
    n = 0
    nodes_correspondence = {}
    nc_inv = {}
    if heterogeneity:
        times_named = {}
        for node in architecture.processors():
            nodes_correspondence[n] = node.name
            nc_inv[node.name] = n
            n += 1
            times_named[node.name] = node.frequency_domain.cycles_to_ticks(
                cycles
            )
        for node in primitives_graph:
            nodes_correspondence[n] = node
            nc_inv[node] = n
            n += 1
            times_named[node] = min(
                [val for val in primitives_graph[node].values() if val != 0]
            )
    else:  # mcsoc'18 variant
        arch_graph = architecture.to_adjacency_dict()
        graph = make_graph_symmetric(arch_graph)
        dist_metric_named = {}
        for node in graph:
            nodes_correspondence[n] = node
            nc_inv[node] = n
            n += 1
            dist_metric_named[node] = dijkstra(graph, node)

    if scaling:
        if heterogeneity:  # new method
            scaling_factor = np.mean(
                [times_named[node] for node in times_named.keys()]
            )
            for node in times_named:
                times_named[node] /= float(scaling_factor)
        else:  # mcsoc'18
            scaling_factor = np.mean(
                [
                    dist_metric_named[node_from][node_to]
                    for node_from in dist_metric_named.keys()
                    for node_to in dist_metric_named[node_from].keys()
                ]
            )
            for node_from in graph:
                for node_to in dist_metric_named[node_from]:
                    dist_metric_named[node_from][node_to] /= float(
                        scaling_factor
                    )
    if heterogeneity:
        min_dist = min([times_named[node] for node in times_named])

    # We use the corresp. dictionaries to make sure we don't mess up the order
    res = []
    for node_from in range(0, n):
        line = [inf] * n
        if heterogeneity:
            for node_to in range(0, n):
                # this makes no sense when node_to and node_from are one of each,
                # a primitive and proc,but we leave it so the embedding can be calculated.
                node_to_named = nodes_correspondence[node_to]
                node_from_named = nodes_correspondence[node_from]
                delta = np.abs(
                    times_named[node_to_named] - times_named[node_from_named]
                )
                if node_to != node_from:
                    delta = delta + min_dist * min_dist_factor
                line[nc_inv[node_to_named]] = delta
        else:
            for node_to_named in dist_metric_named[
                nodes_correspondence[node_from]
            ]:
                line[nc_inv[node_to_named]] = dist_metric_named[
                    nodes_correspondence[node_from]
                ][node_to_named]
        res.append(line)
    return res, nodes_correspondence, nc_inv


def arch_to_distance_metric_naive(arch, scaling=True):
    arch_graph = arch.to_adjacency_dict()
    inf = float("inf")
    n = 0
    nodes_correspondence = {}
    nc_inv = {}
    dist_metric_named = {}
    graph = make_graph_symmetric(arch_graph)
    for node in graph:
        nodes_correspondence[n] = node
        nc_inv[node] = n
        n += 1
        dist_metric_named[node] = dijkstra(graph, node)
    if scaling:
        scaling_factor = np.mean(
            [
                dist_metric_named[node_from][node_to]
                for node_from in dist_metric_named.keys()
                for node_to in dist_metric_named[node_from].keys()
            ]
        )
        for node_from in graph:
            for node_to in dist_metric_named[node_from]:
                dist_metric_named[node_from][node_to] /= float(scaling_factor)

    # We use the corresp. dictionaries to make sure we don't mess up the order
    res = []
    for node_from in range(0, n):
        line = [inf] * n
        for node_to_named in dist_metric_named[nodes_correspondence[node_from]]:
            line[nc_inv[node_to_named]] = dist_metric_named[
                nodes_correspondence[node_from]
            ][node_to_named]
        res.append(line)
    return res, nodes_correspondence, nc_inv

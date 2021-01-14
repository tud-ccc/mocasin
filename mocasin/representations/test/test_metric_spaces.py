# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Felix Teweleit

from mocasin.representations.metric_spaces import (
    dijkstra,
    arch_to_distance_metric_naive,
    FiniteMetricSpaceLP,
    FiniteMetricSpaceLPSym,
)
from mocasin.representations.embeddings import isMetricSpaceMatrix
import numpy as np


class TestMetricSpaces(object):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dijkstra(self, exampleDijkstra):
        distances = dijkstra(exampleDijkstra, "N0")
        assert distances["N0"] == 0
        assert distances["N1"] == 35
        assert distances["N2"] == 15
        assert distances["N3"] == 45
        assert distances["N4"] == 49
        assert distances["N5"] == 41

    def test_arch_graph_to_distance_metric(self, exampleDijkstraArch):
        (
            distance_metric,
            nodes_correspondence,
            nc_inv,
        ) = arch_to_distance_metric_naive(exampleDijkstraArch)
        for node in nodes_correspondence:
            assert nc_inv[nodes_correspondence[node]] == node
        for node in nc_inv:
            assert nodes_correspondence[nc_inv[node]] == node
        assert isMetricSpaceMatrix(np.array(distance_metric))

    def test_finiteMetricSpace_uniformFromBall(self, exampleClusterArch, N):
        testSpace = exampleClusterArch
        p = 3
        r = 1
        runs = testSpace.uniformFromBall(p, r, N)
        result = list(
            zip(
                range(testSpace.n),
                map(
                    lambda x: len(x) / float(N),
                    [
                        [run for run in runs if run == i]
                        for i in range(testSpace.n)
                    ],
                ),
            )
        )
        for (i, prob) in result:
            dist = testSpace.dist(i, p)
            if np.isclose(prob, 0):
                assert dist > r or (dist == 0 and i == p)
            else:
                assert testSpace.dist(i, p) <= r

    def test_finiteMetricSpaceLP_ball1(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)

        result = len(testProdSpace.ball([3, 2, 7], 4))
        assert result == 1072

    def test_finiteMetricSpaceLP_ball2(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)
        oneBall = testProdSpace.ball([3, 2, 7], 1)

        result = list(map(testProdSpace.int2Tuple, oneBall))
        assert result == [
            [3, 2, 4],
            [3, 2, 5],
            [3, 2, 6],
            [3, 0, 7],
            [3, 1, 7],
            [0, 2, 7],
            [1, 2, 7],
            [2, 2, 7],
            [3, 2, 7],
            [3, 3, 7],
        ]

    def test_finiteMetricSpaceLP_uniformFromBall1(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3, 2, 7], 4, 10)

        assert len(uniformFromFourBall) == 10

        for value in uniformFromFourBall:
            assert (
                testProdSpace.dist(testProdSpace.tuple2Int([3, 2, 7]), value)
                <= 4.0
            )

    def test_finiteMetricSpaceLP_uniformFromBall2(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3, 2, 7], 4, 10)

        result = list(map(testProdSpace.int2Tuple, uniformFromFourBall))
        result = list(map(testProdSpace.tuple2Int, result))
        assert result == uniformFromFourBall

    def test_finiteMetricSpaceLP_calc(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)

        result = testProdSpace._distCalc([3, 2, 7], [3, 0, 4])
        assert result == 2.0

    def test_finiteMetricSpaceLP_dist(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)
        uniformFromFourBall = testProdSpace.uniformFromBall([3, 2, 7], 4, 10)

        result = []
        for j in uniformFromFourBall:
            result.append(
                testProdSpace.dist(testProdSpace.tuple2Int([3, 2, 7]), j)
            )

        assert len(result) == 10

        for value in result:
            assert value <= 4.0

    def test_finiteMetricSpaceLP_uniform(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)

        result = testProdSpace.uniform()
        for value in result:
            assert (
                testProdSpace.dist([3, 2, 7], testProdSpace.int2Tuple(value))
                <= 5
            )

    def test_finiteMetricSpaceLP_oneBall(self, exampleClusterArch):
        testSpace = exampleClusterArch
        testProdSpace = FiniteMetricSpaceLP(testSpace, d=3)
        oneBall = testProdSpace.ball([3, 2, 7], 1)

        assert len(oneBall) == 10

    def test_FiniteMetricSpaceLPSym_length(self, exampleClusterArchSymmetries):
        result = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries, d=2).n
        assert result == 20

    def test_dist_1(self, exampleClusterArchSymmetries):
        result = exampleClusterArchSymmetries.dist([3], [4])
        assert result == 2

    def test_dist_2(self, exampleClusterArchSymmetries):
        result = exampleClusterArchSymmetries.dist([3], [0])
        assert result == 0

    def test_dist_3(self, exampleClusterArchSymmetries):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries, d=3)

        result = testSymSpace.dist([3, 2, 7], [3, 0, 4])
        assert result == 0.0

    def test_dist_4(self, exampleClusterArchSymmetries):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries, d=3)

        result = testSymSpace.dist([3, 4, 7], [3, 0, 4])
        assert result == 2.0

    def test_dist_5(self, exampleClusterArchSymmetries):
        testSymSpace = FiniteMetricSpaceLPSym(exampleClusterArchSymmetries, d=3)

        result = testSymSpace.dist([3, 4, 3], [5, 11, 4])
        assert result == 6.0

    def test_tuple_orbit(self, autExampleClusterArch):
        result = autExampleClusterArch.tuple_orbit([3, 4, 3])
        assert result == frozenset(
            {
                (3, 4, 3),
                (0, 7, 0),
                (2, 6, 2),
                (1, 7, 1),
                (2, 7, 2),
                (1, 4, 1),
                (2, 4, 2),
                (0, 4, 0),
                (1, 6, 1),
                (3, 5, 3),
                (3, 6, 3),
                (1, 5, 1),
                (0, 5, 0),
                (2, 5, 2),
                (3, 7, 3),
                (0, 6, 0),
            }
        )


# TODO: add tests for the new metric

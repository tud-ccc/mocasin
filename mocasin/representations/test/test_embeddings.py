# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Felix Teweleit


from mocasin.representations.embeddings import (
    MetricSpaceEmbeddingBase,
    MetricSpaceEmbedding,
    _f_emb_approx,
)
from mocasin.representations.metric_spaces import FiniteMetricSpaceLP
import numpy as np


class TestEmbeddings(object):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_approx(self, exampleClusterArch, N):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)

        for _ in range(N):
            result = E.approx(np.random.random(E._k), rg=(0, E._k))
            found = False
            for vec in E.iotainv.keys():
                if np.allclose(vec, result):
                    found = True
            assert found

    def test_Evec(self, exampleClusterArch, dimension):
        M = exampleClusterArch
        MLP = FiniteMetricSpaceLP(M, dimension, p=2)
        Evec = MetricSpaceEmbedding(M, dimension)
        in1 = [1, 0, 1, 1, 3]
        in2 = [0, 0, 2, 1, 0]
        dist = MLP.dist(in1, in2)

        evec1 = Evec.i(in1)
        evec2 = Evec.i(in2)
        assert len(evec1) == dimension
        assert len(evec1[0]) == M.n
        dist_embedded = np.linalg.norm(
            np.array(evec1).flatten() - np.array(evec2).flatten()
        )
        assert (
            dist / Evec.distortion < dist_embedded
            and dist_embedded < dist * Evec.distortion
        )

    def test_Evec_inv(self, exampleClusterArch, dimension):
        M = exampleClusterArch
        Evec = MetricSpaceEmbedding(M, dimension)

        result = Evec.inv(Evec.i([1, 0, 1, 1, 3]))
        assert list(np.around(result).astype(int)) == [1, 0, 1, 1, 3]

    def test_Evec_invapprox(self, exampleClusterArch, dimension):
        M = exampleClusterArch
        E = MetricSpaceEmbeddingBase(M)
        Evec = MetricSpaceEmbedding(M, dimension)
        result = Evec.invapprox(np.random.random((dimension * E._k)).flatten())

        for value in result:
            assert value >= 0 and value < 16

    def test_Par_invapprox(self, exampleParallella16, dimension):
        Par = MetricSpaceEmbedding(exampleParallella16, dimension)
        result = Par.invapprox(
            (10 * np.random.random((dimension, Par._k))).flatten()
        )
        for value in result:
            assert value >= 0 and value < 18

    def test_calculate_embedding_matrix(self, D):
        L, d = np.array(
            MetricSpaceEmbeddingBase.calculateEmbeddingMatrix(D), dtype=object
        )
        # print(f"Found embedding with distortion {d}")
        n = D.shape[0]
        iota = dict()
        for i in range(n):
            iota[i] = L[i]
        for i in range(n):
            for j in range(n):
                dist = D[i, j]
                sigma_embedding_dist = np.linalg.norm(
                    iota[i].flatten() - iota[j].flatten()
                )
                assert (
                    dist <= sigma_embedding_dist
                    and sigma_embedding_dist <= d * dist
                )

    def test_numba_acceleration_functions(self, d, k, split_d, split_k, n):
        iota = np.random.rand(n, k)
        vec = np.random.rand(d)
        res = _f_emb_approx(vec, d, k, split_d, split_k, iota, n)
        assert res.shape == (d, k)

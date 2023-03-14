# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Andres Goens

from __future__ import print_function
import numpy as np
import numba as nb
import cvxpy as cvx
import math
import random
from os.path import exists
import json

# import fjlt.fjlt as fjlt
# TODO: use fjlt to (automatically) lower the dimension of embedding
from mocasin.representations import metric_spaces as metric
from mocasin.util import logging
import mocasin.util.random_distributions.lp as lp


log = logging.getLogger(__name__)


#  An embedding \iota: M \hookrightarrow R^k
#  will be calculated and realized as a lookup-table.
#  This does not scale for large metric spaces as well.
#
#  However: the idea is to do this for the small space M
#  and then handle the case M^d \hat \iota R^{kd} specially.


#  from: https://jeremykun.com/2016/02/08/big-dimensions-and-what-you-can-do-about-it/0/
def randomSubspace(subspaceDimension, ambientDimension):
    return np.random.normal(0, 1, size=(subspaceDimension, ambientDimension))


def project(v, subspace):
    subspaceDimension = len(subspace)
    return (1 / math.sqrt(subspaceDimension)) * subspace.dot(v)


def jlt(data, subspaceDimension):
    ambientDimension = len(data[0])
    A = randomSubspace(subspaceDimension, ambientDimension)
    return (1 / math.sqrt(subspaceDimension)) * A.dot(data.T).T


def jlt_search(D, E, target_dist, num_tries=30):
    dim = 2
    dim_orig = len(E[0])
    found = False
    while not found and dim < dim_orig:
        log.info(f"jlt search: increasing dimension to {dim}")
        for _ in range(num_tries):
            candidate = jlt(E, dim)
            cur_distortion = check_distortion(D, candidate)
            log.debug(f"jlt search: found distortion of {cur_distortion}")
            if cur_distortion < target_dist:
                found = True
                break
        dim = dim * 2
    if found:
        return np.array(candidate), cur_distortion
    else:
        return E, check_distortion(D, E)


def check_distortion(D, E):
    distortion = 1
    it = np.nditer(np.array(D), flags=["multi_index"])
    for dist in it:
        x, y = it.multi_index
        distance_vecs = np.linalg.norm(E[x] - E[y])
        if dist != 0 and distance_vecs != 0:
            distort = np.abs(distance_vecs / dist)
            distort = max(distort, 1 / distort)
        elif distance_vecs != 0:  # dist = 0
            distort = 1 + np.abs(distance_vecs)
        else:  # both 0
            distort = 0
        if distort > distortion:
            distortion = distort
    return distortion


# To whomever someday has the misfortune of having to mantain this code:
# I'm sorry. These functions are confusing. I'll try my best to explain them.
# The basic idea here is speeding up the approximation of a vector in the
# representation to the closest vector representing an actual mapping.
# It's split in two functions that we compile with the numba JIT,
# the base case (from the MetricSpaceEmbeddingBase class) and the full
# one. The base case just takes a vector and a range, as well as the
# lookup matrix iota. The range represents the indices we care about in
# the vector, since we split the vector in two parts, one for the PEs
# and one for the channels. We basically take the vector with the least
# distance to the one we want to approximate and that's our approximation.
#
@nb.njit(fastmath=True, cache=True)
def _f_base_approx(vec, rg, iota):
    min = np.inf
    idx = -1
    for i in range(rg[0], rg[1]):
        distsq = 0
        for j in range(vec.shape[0]):
            distsq += (iota[i, j] - vec[j]) ** 2
            # we don't need to take the square root,
            # since we just care about the minimizing index
        if distsq < min:
            min = distsq
            idx = i
    return iota[idx]


# For the general case we do the splitting into a mapping of proceses to PEs
# and a mapping of channels to primitives. That's why we have the two values,
# split_k and split_d. The value k is for the number of PEs and primitives,
# and split_k tells us where the PEs end and the primitives start. The d
# value, on the other hand, represents the number of processes+channels,
# and split_d accordingly tells us where the processes end and the channels
# start
@nb.njit(fastmath=True, parallel=True, cache=True)
def _f_emb_approx(vec, d, k, split_d, split_k, iota, n):
    res = np.empty((d, k))
    for i in nb.prange(d):
        comp = np.empty(k)
        for j in nb.prange(k):
            comp[j] = vec[k * i + j]

        if i < split_d:
            value = _f_base_approx(comp, (0, split_k), iota)
        else:
            value = _f_base_approx(comp, (split_k, n), iota)
        res[i] = value
    return res


class MetricSpaceEmbeddingBase:
    def __init__(
        self,
        M,
        embedding_matrix_path=None,
        verbose=False,
        target_distortion=1.1,
        disable_embedding_test=False,
        jlt_tries=30,
    ):
        assert isinstance(M, metric.FiniteMetricSpace)
        self.M = M
        self.target_distortion = target_distortion
        self.jlt_tries = jlt_tries

        # First: calculate a good embedding by solving an optimization problem
        if embedding_matrix_path is not None:
            if exists(embedding_matrix_path):
                try:
                    with open(embedding_matrix_path, "r") as f:
                        contents = json.loads(f.read())
                        E = np.array(contents["matrix"])
                        E.reshape(contents["shape"])
                        read_distortion = contents["distortion"]
                        if read_distortion > self.target_distortion:
                            valid = False
                        elif not disable_embedding_test:
                            dist = check_distortion(M.D, E)
                            valid = dist <= self.target_distortion
                            if valid:
                                self.distortion = dist
                        else:  # embedding test disabled
                            log.warning("Using embedding without testing.")
                            valid = True
                # The call to check_distortion may throw various exceptions.
                # By intercepting all, we can detect any errors in the
                # validation process, produce a warning for the user and
                # continue operation by recalculating the matrix
                except Exception as e:
                    valid = False  # could not read json
                    if isinstance(e, TypeError):
                        log.warning(
                            "Could not read embedding JSON file (error "
                            f"parsing). {e}"
                        )
                    else:
                        log.warning(
                            "An unknown error occurred while reading the "
                            "embedding JSON file. Did you provide the correct"
                            f"file for the given platform? ({e})"
                        )
                    log.warning("Recalculating...")
                    dist = np.inf

                if dist != np.inf and dist > self.target_distortion:
                    log.warning(
                        "Stored embedding is matrix invalid "
                        f"(distortion {dist} > {self.target_distortion}). "
                        "Recalculating..."
                    )
                    valid = False

                if not valid:
                    E, self.distortion = self.calculateEmbeddingMatrix(
                        np.array(M.D),
                        verbose=verbose,
                        target_dist=self.target_distortion,
                        jlt_tries=self.jlt_tries,
                    )
            else:  # path does not exist but is not None
                log.warning(
                    "No embedding matrix stored. Calculating it now ..."
                    "(this might take some time)"
                )
                E, self.distortion = self.calculateEmbeddingMatrix(
                    np.array(M.D),
                    verbose=verbose,
                    target_dist=self.target_distortion,
                    jlt_tries=self.jlt_tries,
                )

        else:  # path is None
            E, self.distortion = self.calculateEmbeddingMatrix(
                np.array(M.D),
                target_dist=self.target_distortion,
                jlt_tries=self.jlt_tries,
                verbose=verbose,
            )

        self._k = E.shape[1]
        # Populate look-up table
        self.iota = dict()
        self.iotainv = dict()  # Poor-man's bidirectional map

        for i in range(M.n):
            self.iota[i] = tuple(E[i])
            self.iotainv[tuple(E[i])] = i

        self._f_iota = np.array(
            list([self.iota[i] for i in range(M.n)])
        ).reshape([M.n, self._k])

    def i(self, i):
        assert 0 <= i and i <= self.M.n
        return self.iota[i]

    def inv(self, j):
        assert j in self.iotainv.keys()
        return self.iotainv[tuple(j)]

    @staticmethod
    def calculateEmbeddingMatrix(
        D, verbose=False, target_dist=1.1, jlt_tries=30
    ):
        assert isMetricSpaceMatrix(D)
        n = D.shape[0]
        if int(cvx.__version__.split(".")[0]) == 0:
            Q = cvx.Semidef(n)
            d = cvx.NonNegative()
        else:
            Q = cvx.Variable(shape=(n, n), PSD=True)
            d = cvx.Variable(shape=(1, 1), nonneg=True)
        # print(D)

        # c = matrix(([1]*n))
        log.debug("Generating constraints for embedding:")
        log.debug(f"Distance matrix: {D}")
        constraints = []
        for i in range(n):
            for j in range(i, n):
                constraints += [D[i, j] ** 2 <= Q[i, i] + Q[j, j] - 2 * Q[i, j]]
                constraints += [
                    Q[i, i] + Q[j, j] - 2 * Q[i, j] <= d * D[i, j] ** 2
                ]
                log.debug(
                    f"adding constraint: "
                    f"{D[i,j]}**2 <= Q{[i,i]} + Q{[j,j]} - 2*Q{[i,j]}"
                )
                log.debug(
                    f"adding constraint: "
                    f"Q{[i,i]} + Q{[j,j]} - 2*Q{[i,j]} <= d * {D[i,j]}**2 "
                )

        obj = cvx.Minimize(d)
        prob = cvx.Problem(obj, constraints)
        solvers = cvx.installed_solvers()
        if "MOSEK" in solvers:
            log.info("Solving problem with MOSEK solver")
            prob.solve(solver=cvx.MOSEK, verbose=verbose)
        elif "CVXOPT" in solvers:
            prob.solve(
                solver=cvx.CVXOPT,
                kktsolver=cvx.ROBUST_KKTSOLVER,
                verbose=verbose,
            )
            log.info("Solving problem with CVXOPT solver")
        else:
            prob.solve(verbose=verbose)
            log.warning(
                "CVXOPT not installed. Solving problem with default solver."
            )
        if prob.status != cvx.OPTIMAL:
            log.warning(
                "embedding optimization status non-optimal: " + str(prob.status)
            )
            return None, None
        # print(Q.value)
        # print(np.linalg.eigvals(np.matrix(Q.value)))
        # print(np.linalg.eigh(np.matrix(Q.value)))
        # print(type(np.matrix(Q.value)))
        # print(np.matrix(Q.value))
        try:
            L = np.linalg.cholesky(np.array(Q.value))
        except np.linalg.LinAlgError:
            eigenvals, eigenvecs = np.linalg.eigh(np.array(Q.value))
            min_eigenv = min(eigenvals)
            if min_eigenv < 0:
                log.warning(
                    f"Warning, matrix not positive semidefinite."
                    f"Trying to correct for numerical errors with minimal "
                    f"eigenvalue: {min_eigenv} "
                    f"(max. eigenvalue:{max(eigenvals)})."
                )

                Q_new_t = (
                    np.transpose(eigenvecs) @ np.array(Q.value) @ eigenvecs
                )
                # print(eigenvals)
                # print(Q_new_t) # should be = diagonal(eigenvalues)
                # print(np.transpose(eigenvecs) * eigenvecs)
                # should be = Identity matrix
                Q_new_t += np.diag([-min_eigenv] * len(eigenvals))
                Q_new = eigenvecs @ Q_new_t @ np.transpose(eigenvecs)
                L = np.linalg.cholesky(Q_new)

        log.debug(f"Shape of lower-triangular matrix L: {L.shape}")
        lowerdim, d = jlt_search(D, L, target_dist, num_tries=jlt_tries)
        # print(lowerdim)
        # return L,d.value
        return lowerdim, d

    def approx(self, vec, rg):
        return _f_base_approx(np.array(vec), rg, self._f_iota)

    def invapprox(self, vec):
        approx = self.approx(vec)
        return self.inv(approx)

    def dump_json(self, filename):
        with open(filename, "w") as f:
            contents = {
                "matrix": self._f_iota.tolist(),
                "shape": self._f_iota.shape,
                "distortion": self.distortion,
            }
            f.write(json.dumps(contents))


@nb.njit(fastmath=True, parallel=True, cache=True)
def dist_1(mat, vec):
    res = np.empty(mat.shape[0], dtype=mat.dtype)
    for i in nb.prange(mat.shape[0]):
        acc = 0
        for j in range(mat.shape[1]):
            acc += (mat[i, j] - vec[j]) ** 2
        res[i] = np.sqrt(acc)
    return res


class MetricSpaceEmbedding(MetricSpaceEmbeddingBase):
    def __init__(
        self,
        M,
        d=1,
        embedding_matrix_path=None,
        verbose=False,
        jlt_tries=30,
        target_distortion=1.1,
        disable_embedding_test=False,
    ):
        MetricSpaceEmbeddingBase.__init__(
            self,
            M,
            embedding_matrix_path=embedding_matrix_path,
            target_distortion=target_distortion,
            jlt_tries=jlt_tries,
            verbose=verbose,
            disable_embedding_test=disable_embedding_test,
        )
        self._d = d
        if not hasattr(self, "_split_d"):
            self._split_d = d
        if not hasattr(self, "_split_k"):
            self._split_k = M.n

    def i(self, vec):
        # iota^d: elementwise iota
        assert type(vec) is list
        res = []
        for i in vec:
            res.append(self.iota[i])
        return res

    def inv(self, vec):
        # (iota^d)^{-1}: also elementwise
        assert type(vec) is list
        res = []
        for i in vec:
            res.append(self.iotainv[tuple(i)])
        return res

    def approx(self, i_vec):
        # since the subspaces for every component are orthogonal
        # we can find the minimal vectors componentwise
        if type(i_vec) is np.ndarray:
            vec = i_vec.flatten()
        elif type(i_vec) is list or type(i_vec) is tuple:
            vec = np.array(i_vec).flatten()
        else:
            log.error(f"approx: Type error, unrecognized type ({type(i_vec)})")
            log.error(f"i_vec: {i_vec}")
            raise RuntimeError("unrecognized type.")
        assert vec.shape[0] == self._k * self._d or log.error(
            f"length of vector ({vec.shape[0]}) does not fit to dimensions "
            f"({self._k} * {self._d})"
        )
        res = _f_emb_approx(
            vec,
            self._d,
            self._k,
            self._split_d,
            self._split_k,
            self._f_iota,
            self.M.n,
        )
        return res

    def invapprox(self, vec):
        if type(vec) is list:
            flat_vec = [item for sublist in vec for item in sublist]
        else:
            flat_vec = vec.flatten()
        return self.inv(self.approx(flat_vec).tolist())

    def uniformVector(self):
        k = len(self.iota)
        res = []
        for i in range(0, self._d):
            idx = random.randint(0, k - 1)
            res.append(list(self.iota[idx]))
        return res

    def uniformFromBall(self, p, r, npoints=1):
        # assumes p is flat (for optimization)
        vecs = []
        for _ in range(npoints):
            v = (
                np.array(p)
                + np.array(
                    r * lp.uniform_from_p_ball(p=self.p, n=self._k * self._d)
                )
            ).tolist()
            vecs.append(self.approx(v))

        return vecs


def isMetricSpaceMatrix(D):
    size = D.shape
    n = size[0]
    dimensions = size[0] == size[1]
    # check that matrix is symmetric:
    m = D.transpose() - D
    symmetric = np.allclose(m, np.zeros((n, n)))
    # check that matrix is non-degenerate (and non-negative):
    nondegenerate = True
    for i in range(n):
        for j in range(n):
            if i == j:
                nondegenerate = nondegenerate and (D[i, j] == 0)
            else:
                nondegenerate = nondegenerate and (D[i, j] > 0)
    # triangle inequality (which is O(n**3)...)
    triangle = True
    for x in range(n):
        for y in range(n):
            for z in range(n):
                triangle = triangle and (D[x, y] + D[y, z] >= D[x, z])

    return dimensions and symmetric and nondegenerate and triangle

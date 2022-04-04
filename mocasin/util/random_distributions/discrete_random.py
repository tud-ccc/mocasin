# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens

import numpy as np
import matplotlib.pyplot as plt


def _discrete_random(dims, mu, r, Q, func):
    # r is in the euclidean norm now
    assert type(dims) == list
    for dim in dims:
        assert type(dim) == int
    assert type(mu) == list or type(mu) == np.ndarray
    assert len(mu) == len(dims)
    for comp in mu:
        assert isinstance(comp, (int, np.integer))
    assert type(Q) == np.ndarray
    n = sum(dims)
    Sigma = float(r**2) * Q @ np.transpose(Q)
    # T eigenvectors as transformation matrix
    eigenvals, T = np.linalg.eig(Sigma)

    transformed, median_vec = func(
        dims, eigenvals
    )  # func should not be exposed outside (values might change)

    centered = []
    for i, dim in enumerate(dims):
        centered.append([transformed[i] - median_vec[i]])
    retransformed = np.transpose(T) @ np.array(centered)

    res = []
    for i, dim in enumerate(dims):
        moved = int(mu[i] + retransformed[i]) % dim
        res.append(moved)

    # transform back to the original basis

    return res


def _discrete_gauss_plain(dims, eigenvals):
    i = 0
    ps = []
    median_vec = []
    for _, sigmasq in np.ndenumerate(eigenvals):
        sigma = np.sqrt(sigmasq)
        if (1 - 4 * sigma / dims[i]) > 0:
            p = (1 + np.sqrt(1 - 4 * sigma / dims[i])) / 2
        else:
            # print("Warning: r and Q incompatible with space, yield sigma(" + str(sigma) + ")too large for dimension (" + str(dims[i]) + ")! ")
            p = 1 / 2
        ps.append(p)
        i += 1
    result = []
    for i, dim in enumerate(dims):
        result.append(np.random.binomial(dim, ps[i]))
        median_vec.append(ps[i] * dim)

    return result, median_vec


def _discrete_uniform_plain(dims, eigenvals):
    result = []
    median_vec = []
    for i, ev in enumerate(eigenvals):
        result.append(np.random.randint(int(ev + 0.5)))
        median_vec.append((int(ev + 0.5) - 1) / 2.0)
    return result, median_vec


def discrete_gauss(dims, mu, r, Q):
    return _discrete_random(dims, mu, r, Q, _discrete_gauss_plain)


def discrete_uniform(dims, mu, r, Q):
    return _discrete_random(dims, mu, r, Q, _discrete_uniform_plain)


def plot_distribution(ns, mu, Q, r, distribution, num_points=1000):
    print("")
    print("Testing plot distribution")
    print("-------------------------")
    raws = []
    res = dict()
    for i in range(0, ns[0] + 1):
        for j in range(0, ns[1] + 1):
            res[(i, j)] = 0

    for _ in range(0, num_points):
        rand = distribution(ns, mu, r, Q)
        raws.append(rand)
        i, j = rand[0], rand[1]
        res[(i, j)] += 1

    X, Y, Z = [], [], []

    for i in range(0, ns[0]):
        for j in range(0, ns[1]):
            if res[(i, j)] != 0:
                X.append(i)
                Y.append(j)
                Z.append(res[(i, j)])

    fig = plt.figure()  # projection='3d')
    ax = fig.add_subplot(111, projection="3d")
    plt.xlim((0, ns[0]))
    plt.ylim((0, ns[1]))
    ax.set_zlim((0, max(Z) + 1))

    ax.scatter(X, Y, Z)
    print("Mean: " + str(np.mean(raws, axis=0)))
    print("Std deviation estimate: " + str(np.std(raws, axis=0, ddof=1)))
    support = []
    for i in range(len(ns)):
        support.append(
            (
                min(
                    map(
                        lambda x: x[i],
                        [key for key in res.keys() if res[key] != 0],
                    )
                ),
                max(
                    map(
                        lambda x: x[i],
                        [key for key in res.keys() if res[key] != 0],
                    )
                ),
            )
        )
    print("Support: " + str(support))
    plt.show()

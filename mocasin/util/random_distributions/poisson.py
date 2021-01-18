# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens

import types
import numpy as np
import matplotlib.pyplot as plt

# from scipy.stats import multinomial
from mpl_toolkits.mplot3d import Axes3D


n = 16
p = 0.5
trials = 100000
mu = 8
sigmas = [1, 2, 3, 4, 5, 10]
fig, axes = plt.subplots(len(sigmas), sharex=True, sharey=True)
# for i,p in enumerate([0.3,0.4,0.5]):
# for i,(p,n_tot) in enumerate([(0.5,16),(0.5,48),(0.5,16016)]):
for i, sigma in enumerate(sigmas):
    n_tot = (int(4 * sigma ** 2 / float(n)) + 1) * n
    p = (1 + np.sqrt(1 - 4 * sigma ** 2 / float(n_tot))) / 2
    print(
        "i: "
        + str(i)
        + " sigma: "
        + str(sigma)
        + " n_tot: "
        + str(n_tot)
        + ", p: "
        + str(p)
    )

    points = map(
        lambda x: (x - int(n_tot * p + 0.5) + mu) % n,
        np.random.binomial(n_tot, p, trials),
    )
    xs = []
    for j in range(0, n):
        xs.append(len([point for point in points if point == j]))
    axes[i].scatter(range(0, n), xs)
    axes[i].set_xlim(0, n)
    # print(points)
    print(
        "calculated mean: "
        + str(np.mean(points))
        + ", deviation: "
        + str(np.std(points, ddof=1))
    )

plt.show()

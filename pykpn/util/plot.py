# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from third_party_dependencies.tsne import tsne
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm as cm


def visualize_mapping_space(mappings, exec_times):
    """Visualize a multi-dimensional mapping space using t-SNE

    Args:
        mappings (list[Mapping]): list of mappings
        exec_times (list[float]): list of execution times

    Note:
         The two lists `mappings` and `exec_times` are assumed to have the same
         order. This means that ``exec_times[idx]`` is expected to hold the
         execution time of the mapping ``exec_times[idx]``.
    """
    assert len(mappings) == len(exec_times)

    mapping_tuples = np.array(list(map(lambda o: o.to_list(), mappings)))
    X = tsne.tsne(mapping_tuples,
                  no_dims=2,
                  initial_dims=len(mappings[0].to_list()),
                  perplexity=20.0)

    plt.hexbin(X[:, 0], X[:, 1], C=exec_times, cmap=cm.viridis_r, bins=None)
    plt.colorbar()
    plt.show()

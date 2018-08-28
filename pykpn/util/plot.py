# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from third_party_dependencies.tsne import tsne
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from pykpn.util import annotate
from pykpn.representations.representations import RepresentationType, toRepresentation

#used for pydot -> networkx support
#import networkx.drawing.nx_pydot as nx
#import networkx as nwx


def visualize_mapping_space(mappings, exec_times, dest=None,representation_type=RepresentationType['SimpleVector']):
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
    
    #Code to derive mapping from dot graph:
    #Unfortunately with embarrising results :( 

    #graph.write_png('test_graph.png')
    #tmp = nx.from_pydot(mappings[0].to_pydot())
    #nwx.draw(tmp)
    #plt.show()

    annotes = []
    for e,m in zip(exec_times,mappings):
        a = "Execution Time: {0:10.1f}\n{1}".format(e,m.to_string())
        annotes.append(a)


    representation = representation_type.getClassType()(mappings[0].kpn,mappings[0].platform)
    #print(mapping_tuples)
    X = tsne.tsne(mapping_tuples,
                  no_dims=2,
                  initial_dims=len(toRepresentation(representation,mappings[0])),
                  perplexity=20.0)

    fig = plt.figure(figsize=(14,8))
    ax = fig.add_subplot(111)

    plt.hexbin(X[:, 0], X[:, 1], C=exec_times, cmap=cm.viridis_r, bins=None)
    
    #some magic adjustments to make room for legend and mapping string
    plt.subplots_adjust(right=0.6)
    plt.subplots_adjust(left=0.18)
    
    #add annotions on click
    af = annotate.AnnoteFinder(X[:,0],X[:,1], annotes, ax=ax)
    fig.canvas.mpl_connect('button_press_event', af)
    cbaxes = fig.add_axes([0.012, 0.1, 0.03, 0.8])
    plt.colorbar(cax=cbaxes)
    if dest == None:
        plt.show()
    else:
        fig.savefig(dest + ".pdf")

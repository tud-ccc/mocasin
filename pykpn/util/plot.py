# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from tsne import tsne
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from pykpn.util import annotate
from pykpn.representations.representations import RepresentationType 

import matplotlib.animation as animation
from matplotlib import colors as colors
from matplotlib import collections as coll

#used for pydot -> networkx support
#import networkx.drawing.nx_pydot as nx
#import networkx as nwx


def visualize_mapping_space(mappings, exec_times, show_plot=False,
                            representation_type=RepresentationType['SimpleVector'],
                            tick=0, history=0):
    """Visualize a multi-dimensional mapping space using t-SNE

    Args:
        mappings (list[Mapping]): list of mappings
        exec_times (list[float]): list of execution times

    Note:
         The two lists `mappings` and `exec_times` are assumed to have the same
         order. This means that ``exec_times[idx]`` is expected to hold the
         execution time of ``mapping[idx]``.
    """
    assert len(mappings) == len(exec_times)

    representation = representation_type.getClassType()(mappings[0].kpn,mappings[0].platform)
    mapping_tuples = np.array(list(map(representation.toRepresentation, mappings)))

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


    #print(mapping_tuples)
    # print("MAPPING TUPLES: {}".format(mapping_tuples[0]))
    X = tsne.tsne(mapping_tuples,
                  no_dims=2,
                  initial_dims=len(representation.toRepresentation(mappings[0])),
                  perplexity=20.0)

    fig = plt.figure(figsize=(14,8))
    ax = fig.add_subplot(111)

    #plt.hexbin(X[:, 0], X[:, 1], C=exec_times, cmap=cm.viridis_r, bins=None, alpha=1)
    scatt = plt.scatter(X[:, 0], X[:, 1], c=exec_times, cmap=cm.viridis_r)

    #some magic adjustments to make room for legend and mapping string
    plt.subplots_adjust(right=0.6)
    plt.subplots_adjust(left=0.18)
    
    #add annotions on click
    af = annotate.AnnoteFinder(X[:,0],X[:,1], annotes, ax=ax)
    fig.canvas.mpl_connect('button_press_event', af)
    cbaxes = fig.add_axes([0.012, 0.1, 0.03, 0.8])
    plt.colorbar(cax=cbaxes)

    if tick is not 0:
        frames = int((len(X)-history)/tick)

        def update(frame):
            mask = []
            mask += (['none'] * frame)
            mask += (['b'] * int(frame is not (frames+1)))
            mask += (['none'] * int((frames - frame - 1)))

            mask += (['none'] * int(frame * tick))
            mask += (['r'] * int(tick))
            mask += (['none'] * int((frames - frame - 1) * tick))
            scatt.set_edgecolor(mask)

        ani = animation.FuncAnimation(fig, update, frames+1, interval=1000)

    if show_plot:
        plt.show()
    fig.savefig("tsne.pdf")

    return plt

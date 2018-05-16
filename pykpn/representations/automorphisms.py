# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
 # Authors: Andres Goens

try:
  import pynauty as pynauty
except:
  pass

def to_labeled_edge_graph(g):
    original_nodes = list(g.keys())
    num_nodes = 0
    nodes_correspondence = {}
    edge_graph = {}
    coloring_values = {}

    #probably inefficient: first label, then add edges, but simpler.
    for node_from in g.keys():
        for (node_to, value) in g[node_from]:
            nodes_correspondence[num_nodes] = ((node_from,node_to),value)
            if value not in coloring_values:
                coloring_values[value] = []
            coloring_values[value].append(num_nodes)
            num_nodes = num_nodes + 1

        for i in nodes_correspondence:
            edge_graph[i] = []
            for j in nodes_correspondence:
                if nodes_correspondence[i][0][1] == nodes_correspondence[j][0][0]:  #node_to equals node_from 
                    edge_graph[i].append(j)
                
    coloring = list(map(lambda x : set(x), coloring_values.values()))

    return edge_graph, num_nodes, coloring , nodes_correspondence

def list_to_tuple_permutation(perm):
    n = len(perm)
    visited = [0]*n
    current = 0
    cycle = []
    res = []
    while min(visited) == 0:
        visited[current] = 1
        cycle.append(current)
        current = perm[current]
        if visited[current] == 1: #cycle finished
            if len(cycle) > 1:
                res.append(cycle)
            cycle = []
            i = 0
            while(i < n and visited[i] == 1):
                i = i + 1
            current = i
    return res

def edge_to_node_autgrp(aut,nodes_correspondence):
    new_gens = []
    new_nodes_correspondence = {}
    nnc_inv = {}
    m = len(aut[0])

    n = 0
    for node in nodes_correspondence:
        node_from = nodes_correspondence[node][0][0] 
        node_to = nodes_correspondence[node][0][1] 
        if node_from not in nnc_inv:
            nnc_inv[node_from] = n
            new_nodes_correspondence[n] = node_from
            n = n + 1
        if node_to not in nnc_inv:
            nnc_inv[node_to] = n
            new_nodes_correspondence[n] = node_to
            n = n + 1

    for gen in aut:
        new_gen = list(range(0,n))
        for i in range(0,m):
            perm_from = nodes_correspondence[i][0]
            perm_to = nodes_correspondence[gen[i]][0]

            #edge_from
            new_gen[nnc_inv[perm_from[0]]] = nnc_inv[perm_to[0]]

            #edge_to
            new_gen[nnc_inv[perm_from[1]]] = nnc_inv[perm_to[1]]
        if new_gen != list(range(0,n)):
            #print(list_to_tuple_permutation(gen))
            #print("\n")
            new_gens.append(new_gen)
    return new_gens, new_nodes_correspondence
    #kknew_correspondence = {}
    

# 0 : 12, 1 : 21, 2: 14, 3: 41, 4 : 43, 5 : 34, 6 : 23, 7 : 32
edge_graph_square = { 0 : [1,3], 1 : [0,7], 2: [3,1], 3 : [2,5],
                      4 : [2,5], 5 : [4,6], 6 : [0,7], 7 : [4,6] }

        
if __name__ == "__main__":
    print(list_to_tuple_permutation( [0,1,2,4,3,5])) # [[3, 4]]
    print(list_to_tuple_permutation( [5,4,3,2,1,0])) # [[0, 5], [1, 4], [2, 3]]
    print(list_to_tuple_permutation( [1,2,3,4,5,0])) # [[0, 1, 2, 3, 4, 5]]
    square_aut_grp = pynauty.autgrp(pynauty.Graph(8,True,edge_graph_square))
    print(str(list(map(list_to_tuple_permutation,square_aut_grp[0]))))

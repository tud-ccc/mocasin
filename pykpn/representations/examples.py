from pykpn.representations.metric_spaces import *
from pykpn.representations.permutations import *
import numpy as np

exampleClusterArch = FiniteMetricSpace( [ [0,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2],
                                          [1,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2],
                                          [1,1,0,1,2,2,2,2,2,2,2,2,2,2,2,2],
                                          [1,1,1,0,2,2,2,2,2,2,2,2,2,2,2,2],
                                          [2,2,2,2,0,1,1,1,2,2,2,2,2,2,2,2],
                                          [2,2,2,2,1,0,1,1,2,2,2,2,2,2,2,2],
                                          [2,2,2,2,1,1,0,1,2,2,2,2,2,2,2,2],
                                          [2,2,2,2,1,1,1,0,2,2,2,2,2,2,2,2],
                                          [2,2,2,2,2,2,2,2,0,1,1,1,2,2,2,2],
                                          [2,2,2,2,2,2,2,2,1,0,1,1,2,2,2,2],
                                          [2,2,2,2,2,2,2,2,1,1,0,1,2,2,2,2],
                                          [2,2,2,2,2,2,2,2,1,1,1,0,2,2,2,2],
                                          [2,2,2,2,2,2,2,2,2,2,2,2,0,1,1,1],
                                          [2,2,2,2,2,2,2,2,2,2,2,2,1,0,1,1],
                                          [2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,1],
                                          [2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,0]])


def generateExampleParallella(n,num_arm,dist_mem):
    mat = np.zeros((n*n+num_arm,n*n+num_arm))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    dist = abs(i-k) + abs(j-l)
                    mat[j*n+i,l*n+k] = dist
    for i in range(n*n,n*n+num_arm):
        mat[i,i] = 0
        for j in range(n*n):
            mat[i,j] = dist_mem
            mat[j,i] = dist_mem
        for j in range(i+1,n*n+num_arm):
            mat[i,j] = 1
            mat[j,i] = 1
    #print(mat)
    return FiniteMetricSpace(mat)


        

exampleParallella16 = generateExampleParallella(4,2,20)

S4 = perm.SymmetricGroupTranspositions(4)
autExampleClusterArch = perm.ProductGroup([S4,S4,S4,S4]) # this should actually be a wreath product...
exampleClusterArchSymmetries = FiniteMetricSpaceSym(exampleClusterArch,autExampleClusterArch)

# from: https://people.sc.fsu.edu/~jburkardt/m_src/dijkstra/dijkstra.html
#   N0--15--N2-100--N3
#     \      |     /
#      \     |    /
#       40  20  10
#         \  |  /
#          \ | /
#           N1
#           / \
#          /   \
#         6    25
#        /       \
#       /         \
#     N5----8-----N4
exampleDiijkstra = {'N0' : [('N1' , 40), ('N2' , 15)], 'N2' : [('N0' , 15), ('N3' , 100), ('N1' , 20)],
                    'N3' : [('N2' , 100), ('N1' , 10)], 'N1': [('N0' , 40), ('N2', 20), ('N3' , 10), ('N5' , 6), ('N4' , 25)],
                    'N4': [('N1' , 25),( 'N5' , 8)], 'N5' : [('N1' , 6), ('N4' , 8)]}






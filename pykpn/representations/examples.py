from representations.metric_spaces import *
from representations.permutations import *
import numpy as np

exampleClusterArch = finiteMetricSpace( [ [0,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2],
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
    return finiteMetricSpace(mat)


        

exampleParallella16 = generateExampleParallella(4,2,20)

S4 = perm.SymmetricGroupTranspositions(4)
autExampleClusterArch = perm.ProductGroup([S4,S4,S4,S4]) # this should actually be a wreath product...
exampleClusterArchSymmetries = finiteMetricSpaceSym(exampleClusterArch,autExampleClusterArch)




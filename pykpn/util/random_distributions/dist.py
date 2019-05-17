#Author: Andres Goens, 17.2.2017
import types
import numpy as np
import matplotlib.pyplot as plt
#from scipy.stats import multinomial
from mpl_toolkits.mplot3d import Axes3D

    
def discrete_gauss(dims, mu, r, Q):
    #r is in the euclidean norm now
    for dim in dims:
        assert(len(mu) == len(dims))
    for comp in mu:
        assert(type(Q) == np.matrix)
    ps = []
    n = sum( dims)
    Sigma = float(r**len(dims)) * Q 

    #T eigenvectors as transformation matrix

    eigenvals,T = np.linalg.eig(Sigma)
    i = 0
    n_tots = []

    for _, sigmasq in np.ndenumerate(eigenvals):
        n_tot = (int(4*sigmasq/float(dims[i])) + 1) * dims[i]
        n_tots.append(n_tot)
        p = (1 + np.sqrt(1 - 4 * sigmasq/float(n_tot)))/2
       # if (1 - 4 * sigma/dims[i]) > 0:
       #     p = (1 + np.sqrt(1- 4 * sigma/dims[i]))/2
       # else:
       #     print("Warning: r and Q incompatible with space, yield sigma(" + str(sigma) + ")too large for dimension (" + str(dims[i]) + ")! ")
       #     p = 1/2
        ps.append(p)
        i = i+1
        
    transformed = []
    for i,dim in enumerate(dims):
        transformed.append(np.random.binomial(n_tots[i],ps[i]) % dim)

    centered = []
    for i,n_tot in enumerate(n_tots):
        median = ps[i] * n_tot
        centered.append([transformed[i] - median])
    retransformed = (np.transpose(T)*np.matrix(centered)).A1

    res = []
    for i,dim in enumerate(dims):
        moved = int(mu[i] + retransformed[i]) % dim
        res.append(moved)

    # transform back to the original basis

    return res


ns = [16,16]
mu = [3,3]
Q = np.matrix([[1,0],[0,1]])
Q = np.matrix([[ 1.02062073,  0.20412415], [ 0.20412415,  1.02062073]]) # normed: [[5,1],[1,5]]
#Q = np.matrix([[ 0.33333333,  0.        ], [ 0.        ,  3.        ]])
#Q = np.matrix([[ 1.66666667,  1.33333333], [ 1.33333333,  1.66666667]]) # same as above, rotated 45^\circ
r = 2

# for _ in range(0,10):
#     rand = discrete_gauss(ns,mu,r,Q)
#     print(str(rand))

res = dict()
for i in range(0,ns[0]+1):    
    for j in range(0,ns[1]+1):    
        res[(i,j)] = 0

for _ in range(0,10000):
    rand = discrete_gauss(ns,mu,r,Q)
    i,j = rand[0], rand[1]
    res[(i,j)] += 1
    
X,Y,Z = [],[],[]

for i in range(0,ns[0]):    
    for j in range(0,ns[1]):    
        if res[(i,j)] != 0:
            X.append(i)
            Y.append(j)
            Z.append(res[(i,j)])

fig  = plt.figure() #projection='3d')
ax = fig.add_subplot(111, projection='3d')
plt.xlim((0,ns[0]))
plt.ylim((0,ns[1]))

ax.scatter(X,Y,Z)
plt.show()

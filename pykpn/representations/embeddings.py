# Copyright (C) 2017-2018 TU Dresden
# All Rights Reserved
#
# Author: Andres Goens

from __future__ import print_function
import numpy as np
import cvxpy as cvx
import random
#import fjlt.fjlt as fjlt #TODO: use fjlt to (automatically) lower the dimension of embedding
from . import permutations as perm
from . import metric_spaces as metric

DEFAULT_DISTORTION = 1.05

#  An embedding \iota: M \hookrightarrow R^k
#  will be calculated and realized as a lookup-table.
#  This does not scale for large metric spaces as well.
#
#  However: the idea is to do this for the small space M
#  and then handle the case M^d \hat \iota R^{kd} specially.
class MetricSpaceEmbeddingBase():
    def __init__(self,M,distortion=DEFAULT_DISTORTION):
        assert( isinstance(M,metric.FiniteMetricSpace))
        self.M = M
        self.distortion = distortion
        self.k = M.n

        #First: calculate a good embedding by solving an optimization problem
        E,self._k = self.calculateEmbeddingMatrix(np.matrix(M.D),distortion)
        #print(E)

        #Populate look-up table
        self.iota = dict()
        self.iotainv = dict() #Poor-man's bidirectional map

        for i in range(M.n):
            self.iota[i] = tuple(E.A[i])
            self.iotainv[tuple(E.A[i])] = i

    def i(self,i):
        assert(0 <= i and i <= self.M.n)
        return self.iota[i]

    def inv(self,j):
        assert(j in iotainv.keys())
        return self.iotainv[j]
    
    @staticmethod
    def calculateEmbeddingMatrix(D,distortion):
        size = D.shape
        assert(size[0] == size[1])
        n = size[0]
        Q = cvx.Semidef(n)
        #print(D)
        
        #c = matrix(([1]*n))
        constraints = []
        for i in range(n):
            for j in range(i,n):
               constraints += [D[i,j]**2 <= Q[i,i] + Q[j,j] - 2*Q[i,j]]
               constraints += [Q[i,i] + Q[j,j] - 2*Q[i,j] <= distortion**2 * D[i,j]**2 ]
        
        obj = cvx.Minimize(1)
        prob = cvx.Problem(obj,constraints)
        prob.solve()
        assert(prob.status == cvx.OPTIMAL or print("status:" + str(prob.status))) 
        #print(Q.value)
        #print(np.linalg.eigvals(np.matrix(Q.value)))
        #print(np.linalg.eigh(np.matrix(Q.value)))
        #print(type(np.matrix(Q.value)))
        #print(np.matrix(Q.value))
        try:
            L = np.linalg.cholesky(np.matrix(Q.value))
        except np.linalg.LinAlgError:
            eigenvals, eigenvecs = np.linalg.eigh(np.matrix(Q.value))
            min_eigenv = min(eigenvals)
            if min_eigenv < 0:
                print("Warning, matrix not positive semidefinite."
                      + "Trying to correct for numerical errors with minimal eigenvalue: "
                      + str(min_eigenv) + " (max. eigenvalue:" + str(max(eigenvals)) + ").")
                      
                Q_new_t = np.transpose(eigenvecs) * np.matrix(Q.value) * eigenvecs
                #print(eigenvals)
                #print(Q_new_t) # should be = diagonal(eigenvalues)
                # print(np.transpose(eigenvecs) * eigenvecs) # should be = Identity matrix
                Q_new_t += np.diag( [-min_eigenv]*len(eigenvals))
                Q_new = eigenvecs * Q_new_t * np.transpose(eigenvecs)
                L = np.linalg.cholesky(Q_new)

                      
        #print(L)
        #lowerdim = fjlt.fjlt(L,10,1)
        #print(lowerdim)
        return L,n

    def approx(self,vec):
        vecs = [list(self.iota[i]) for i in range(len(self.iota))]
        dists = [np.linalg.norm(np.array(v)-np.array(vec)) for v in vecs]
        idx = np.argmin(dists)
        #print(idx)
        return self.iota[idx]

    def invapprox(self,vec):
        return self.inv(self.approx(vec))




class MetricSpaceEmbedding(MetricSpaceEmbeddingBase):
    def __init__(self,M,d=1,distortion=DEFAULT_DISTORTION):
        MetricSpaceEmbeddingBase.__init__(self,M,distortion)
        self._d = d
    
    def i(self,vec):
        #iota^d: elementwise iota
        assert( type(vec) is list)
        res = []
        for i in vec:
           res.append(self.iota[i])
        return res

    def inv(self,vec):
        #(iota^d)^{-1}: also elementwise 
        assert( type(vec) is list)
        res = []
        for i in vec:
           res.append(self.iotainv[i])
        return res



    def approx(self,vec):
        #since the subspaces for every component are orthogonal
        #we can find the minimal vectors componentwise
        assert( type(vec) is list)
        assert( len(vec) == self._k * self._d)
        res = []
        for i in range(0,self._d):
            comp = []
            for j in range(0,self._k):
                comp.append(vec[self._k*i +j])

            res.append(MetricSpaceEmbeddingBase.approx(self,tuple(comp)))
        return res

    def invapprox(self,vec):
        return self.inv(self.approx(vec))

    def uniformVector(self):
        k = len(self.iota)
        res = []
        for i in range(0,self._d):
            idx = random.randint(0,k-1)
            res = res + list(self.iota[idx])
        return res
            

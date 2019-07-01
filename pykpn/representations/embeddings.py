# Copyright (C) 2017-2018 TU Dresden
# All Rights Reserved
#
# Author: Andres Goens

from __future__ import print_function
import numpy as np
import cvxpy as cvx
import itertools
import random
import logging
#import fjlt.fjlt as fjlt #TODO: use fjlt to (automatically) lower the dimension of embedding
from pykpn.representations import permutations as perm
from pykpn.representations import metric_spaces as metric
from pykpn.util import logging
import pykpn.util.random_distributions.lp as lp

log = logging.getLogger(__name__)

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
        if int(cvx.__version__[0]) < 1:
            Q = cvx.Semidef(n) #for cvxpy < 1.0
        else:
            Q = cvx.Variable((n, n), PSD=True)
        #print(D)
        
        #c = matrix(([1]*n))
        constraints = []
        for i in range(n):
            for j in range(i,n):
                constraints += [D[i,j]**2 <= Q[i,i] + Q[j,j] - 2*Q[i,j]]
                constraints += [Q[i,i] + Q[j,j] - 2*Q[i,j] <= distortion**2 * D[i,j]**2 ]
        
        obj = cvx.Minimize(1)
        prob = cvx.Problem(obj,constraints)
        solvers = cvx.installed_solvers()
        if 'MOSEK' in solvers:
            log.info("Solvig problem with MOSEK solver")
            prob.solve(solver=cvx.MOSEK)
        elif 'CVXOPT' in solvers:
            prob.solve(solver=cvx.CVXOPT,verbose=True)
            log.info("Solvig problem with CVXOPT solver")
        else:
            prob.solve(solver=cvx.CVXOPT,verbose=True)
            log.warning("CVXOPT not installed. Solvig problem with default solver.")
        if prob.status != cvx.OPTIMAL:
            log.warning("embedding optimization status non-optimal: " + str(prob.status)) 
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
                log.warning("Warning, matrix not positive semidefinite." +
                "Trying to correct for numerical errors with minimal eigenvalue: " +
                str(min_eigenv) + " (max. eigenvalue:" + str(max(eigenvals)) + ").")
                
                Q_new_t = np.transpose(eigenvecs) * np.matrix(Q.value) * eigenvecs
                #print(eigenvals)
                #print(Q_new_t) # should be = diagonal(eigenvalues)
                # print(np.transpose(eigenvecs) * eigenvecs) # should be = Identity matrix
                Q_new_t += np.diag( [-min_eigenv]*len(eigenvals))
                Q_new = eigenvecs * Q_new_t * np.transpose(eigenvecs)
                L = np.linalg.cholesky(Q_new)

                      
        log.debug(f"Shape of lower-triangular matrix L: {L.shape}")
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



    def approx(self,i_vec):
        #since the subspaces for every component are orthogonal
        #we can find the minimal vectors componentwise
        if type(i_vec) is np.ndarray:
            #is this the right way or k <-> d?
            assert(i_vec.shape == (self._k,self._d))
            vec = list(i_vec.flat)
        if type(i_vec) is list: 
            vec = i_vec
        else:
            assert("approx: Type error")
        assert( len(vec) == self._k * self._d or log.error(f"length of vector ({len(vec)}) does not fit to dimensions ({self._k} * {self._d})"))

        res = []
        for i in range(0,self._d):
            comp = []
            for j in range(0,self._k):
                comp.append(vec[self._k*i +j])

            res.append(MetricSpaceEmbeddingBase.approx(self,tuple(comp)))

        return res

    def invapprox(self,vec):
        flat_vec = [item for sublist in vec for item in sublist]
        return self.inv(self.approx(flat_vec))

    def uniformVector(self):
        k = len(self.iota)
        res = []
        for i in range(0,self._d):
            idx = random.randint(0,k-1)
            res.append(list(self.iota[idx]))
        return res

    def uniformFromBall(self,p,r,npoints=1):
        vecs = []
        for _ in range(npoints):
            #currently fixed at l1 norm (Manhattan)
            p_flat = [item for sublist in map(list,p) for item in sublist]
            #print(f"k : {self._k}, shape p: {np.array(p).shape},\n p: {p} \n p_flat: {p_flat}")
            v = (np.array(p_flat)+ np.array(r*lp.uniform_from_p_ball(p=1,n=self._k*self._d))).tolist()
            vecs.append(self.approx(v))
            
        return vecs 

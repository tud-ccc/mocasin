#Author: Andres Goens, 2017
from __future__ import print_function
import numpy as np
from sys import exit,stdout
from numpy.random import randint
from itertools import product
from . import permutations as perm

class finiteMetricSpace():
    def __init__(self,matrix):
        try:
            self.D = np.matrix(matrix)
        except Exception as ex:
            print("An error ocurred while initializing a finite metric space with a distance matrix.")
            print(str(ex))
            exit(1)

        dims = self.D.shape
        assert len(dims) == 2, "Distances must be given as a matrix"
        assert dims[1] == dims[0], "Distances must be given as a square matrix"
        self.n = dims[0]


    def dist(self,x,y):
        return self.D[x,y]

    def _ballNaive(self, p, r):
        points = []
        for i in range(self.n):
            if self.dist(p,i) <= r:
                points.append(i)
        return points

    def ball(self,p,r):
        return self._ballNaive(p,r)

    def uniformFromBall(self,p,r,npoints=1):
        return self._uniformFromBallNaive(p,r,npoints=npoints)

    def _uniformFromBallNaive(self,p,r,npoints=1):
        ball = self.ball(p,r)
        point_positions = randint(0,len(ball),size=npoints)
        points = [ ball[i] for i in point_positions]
        return points

class finiteMetricSpaceLP(finiteMetricSpace):
    def __init__(self,M,d=2,p=1):
        self.D = None
        self.M = M
        self.d = d
        self.n = M.n ** d
        self.p = p

    def dist(self,x,y):
        if type(x) is int and type(y) is int:
            if self.D is None:
                return self._distCalc(self.int2Tuple(x),self.int2Tuple(y))
            else:
                return self.D[x,y]

        elif (type(x) == list and type(y) == list):
            if self.D != None:
                x_l = self.tuple2Int(x)
                y_l = self.tuple2Int(y)
                return self.D[x_l,y_l]
            else:
                return finiteMetricSpaceLP._distCalc(self,x,y)
        else:
            print( "An error ocurred while trying to calculate the distance of two points (wrong types?)")
            print( str(x))
            print( str(y))
            exit(1)

    def tuple2Int(self,x):
        return sum( [xi*(self.M.n**i) for (i,xi) in enumerate(x)])

    def int2Tuple(self,x):
        res = [0]*self.d

        #modified from euclidean algorithm
        rem = x
        i = self.d-1
        while(rem != 0):
            res[i], rem = divmod(rem,self.M.n**i)
            i = i-1
        return res


    def _distCalc(self,x,y):
        assert len(x) == self.d
        assert len(y) == self.d
        dist_tuple = [self.M.dist(xi,yi) for (xi,yi) in zip(x,y)]
        if self.p > 100:
            return max(dist_tuple)
        else:
            return np.power(sum( map( lambda x : np.power(x,self.p), dist_tuple)),1/float(self.p))

    def _populateD(self):
        print("Populating D...",end='')
        stdout.flush()
        self.D = np.zeros((self.n,self.n))
        for (x,y) in product(product(range(self.M.n),repeat=self.d),product(range(self.M.n),repeat=self.d)):
            x_l = self.tuple2Int(x)
            y_l = self.tuple2Int(y)
            self.D[x_l,y_l] = self._distCalc(x,y)
        print("done.")

    def ball(self, p, r):
        if type(p) is list:
            point = self.tuple2Int(p)
        elif type(p) is int:
            point = p
        elif type(p) is float:
            point = int(p)
        else:
            print("An error ocurred while calculating the ball, unknown point")
            print(str(p))
            exit(1)
        return finiteMetricSpace.ball(self,point,r)

class finiteMetricSpaceSym(finiteMetricSpace):
    def __init__(self,M,G):
        self.D = None
        assert isinstance(M,finiteMetricSpace)
        self.M = M
        assert isinstance(G,perm.PermutationGroup)
        self.G = G
        orbits = G.enumerate_orbits()
        self.elem2orb = {}
        self.orb2elem = {}
        for i,orb in enumerate(orbits):
            self.elem2orb[i] = orb
            for elem in orb:
                self.orb2elem[elem] = i
        self.n = i+1 # == len(orbits)

    def dist(self,x,y):
        if type(x) is int and type(y) is int:
            if self.D is None:
                return self._distCalc(self.elem2orb[x],self.orb2elem[y])
            else:
                return self.D[x,y]

        elif type(x) == list and type(y) == list:
            if self.D != None:
                x_l = self.orb2elem[x[0]]
                y_l = self.orb2elem[y[0]]
                return self.D[x_l,y_l]
            else:
                x_orb = self.elem2orb[self.orb2elem[x[0]]]
                y_orb = self.elem2orb[self.orb2elem[y[0]]]
                return self._distCalc(list(x_orb),list(y_orb))
        else:
            print( "An error ocurred while trying to calculate the distance of two points (wrong types?)")
            print( str(x))
            print( str(y))
            exit(1)


    def _distCalc(self,x,y):
        # lists (sets) -> (partial) orbits on self.M
        # ints -> points on the new set
        #since G is the orthogonal group of the distance,
        #it is enough to iterate over one orbit
        dists = map( lambda xs : self.M.dist(xs,y[0]), self.elem2orb[self.orb2elem[x[0]]])
        return min(dists)

    def _populateD(self):
        print("Populating D...",end='')
        if self.n == -1:
            self.n = len( G.enumerate_orbits()) # should I remove this per default? Could be very expensive!
        stdout.flush()
        self.D = np.zeros((self.n,self.n))
        for (x,y) in product(range(self.n),repeat=2):
            self.D[x,y] = self._distCalc(x,y)
        print("done.")

    def elem2Tuple(self,elem):
        return min(self.elem2orb[elem])

    def ball(self, p, r):
        #print("calculating ball around point p " + str(p) + " with radius " + str(r))
        if type(p) is list:
            point = self.orb2elem[tuple(p)]
        elif type(p) is int:
            point = p
        elif type(p) is float or np.float64:
            point = int(p)
        else:
            print("An error ocurred while calculating the ball, unknown point")
            print(str(p))
            print(type(p))
            exit(1)
        return finiteMetricSpace.ball(self,point,r)

    def int2Tuple(self,point):
        return self.elem2Tuple(point)



class finiteMetricSpaceLPSym(finiteMetricSpaceLP,finiteMetricSpaceSym):
    def __init__(self,M,G=None,d=2,p=1):
        if isinstance(M,finiteMetricSpaceSym):
            G = M.G
            M = M.M # take the base space (no symmetries)

        if G is None:
            G = perm.TrivialGroup(M.n)
        finiteMetricSpaceLP.__init__(self,M,d=d,p=p)
        self.G =  perm.DuplicateGroup(G,times=d)
        #print("LP, n: " + str(self.n))
        orbits = G.enumerate_tuple_orbits(d)
        self.elem2orb = {}
        self.orb2elem = {}
        for i,orb in enumerate(orbits):
            self.elem2orb[i] = orb
            for elem in orb:
                self.orb2elem[elem] = i
        self.n = i+1 # == len(orbits)
        #print("LPSym, n: " + str(self.n))

    # three types of elemnts:
    # (1) int : representation in the size of the metric space
    # (2) list of insts: tuples in M^d (no symmetries)
    # (3) lists of lists of ints: orbits of the action on M^d (w/symmetries)

    def dist(self,x,y):
        if type(x) is int and type(y) is int: # (1)
            if self.D is None:
                return self._distCalc(list(self.elem2orb[x]),list(self.elem2orb[y]))
            else:
                return self.D[x,y]

        elif type(x) == list and type(y) == list:
            if type(x[0]) == list and type(y[0]) == list: # (3)
                if self.D != None:
                    x_l = self.orb2elem[x[0]]
                    y_l = self.orb2elem[y[0]]
                    return self.D[x_l,y_l]
                else:
                    return self._distCalc(x,y)
            elif type(x[0]) == int and type(y[0]) == int: # (2)
                if self.D != None:
                    x_l = self.orb2elem[self.elem2orb[x]]
                    y_l = self.orb2elem[self.elem2orb[y]]
                    return self.D[x_l,y_l]
                else:
                    return self._distCalc([x],[y])

        else:
            print( "An error ocurred while trying to calculate the distance of two points (wrong types?)")
            print( str(x))
            print( str(y))
            exit(1)

    def _distCalc(self,x,y):
        # we need to iterate over the orbits of *tuples*
        # again one is enough
        orb = list(self.elem2orb[self.orb2elem[tuple(x[0])]])
        dists = map( lambda xs : finiteMetricSpaceLP.dist(self,list(xs),list(y[0])), orb)
        #print(list(map( lambda xs : (finiteMetricSpaceLP.dist(self,list(xs),y[0]),(xs,tuple(y[0]))), self.elem2orb[self.orb2elem[tuple(x[0])]])))
        return min(dists)

    def ball(self, p, r):
        return finiteMetricSpaceSym.ball(self,p,r)

    def int2Tuple(self, point):
        return finiteMetricSpaceSym.elem2Tuple(self,point)




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
S4 = perm.SymmetricGroupTranspositions(4)
autExampleClusterArch = perm.ProductGroup([S4,S4,S4,S4]) # this should actually be a wreath product...
exampleClusterArchSymmetries = finiteMetricSpaceSym(exampleClusterArch,autExampleClusterArch)




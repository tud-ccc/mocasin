#Andres Goens, 11.4.17
from __future__ import print_function
import numpy as np
from sys import exit,stdout
from numpy.random import randint
from itertools import product

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

        elif type(x) == list and type(y) == list:
            if self.D != None:
                x_l = self.tuple2Int(x)
                y_l = self.tuple2Int(y)
                return self.D[x_l,y_l]
            else:
                return self._distCalc(x,y)
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
        else:
            print("An error ocurred while calculating the ball, unknown point")
            print(str(point))
            exit(1)
        return finiteMetricSpace.ball(self,point,r)




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




if __name__ == "__main__":

    N = 10000
    testSpace = exampleClusterArch
    runs = testSpace.uniformFromBall(3,1,N)
    print("probabilities for " + str(N) +" runs:  " + str(list(zip(range(4),map(lambda x : len(x)/float(N), [ [run for run in runs if run == i] for i in range(4)])))))

    testProdSpace = finiteMetricSpaceLP(testSpace,d=3)
    uniformFromFourBall = testProdSpace.uniformFromBall([3,2,7],4,10)
    print("uniform in ball [3,2,7], 4  (" + str(len(testProdSpace.ball([3,2,7],4))) +" elements): " + str(uniformFromFourBall) + " = " + str(list(map(testProdSpace.int2Tuple,uniformFromFourBall))))
    print("dist([3,2,7],[3,0,4] = " + str(testProdSpace._distCalc([3,2,7],[3,0,4])))
    print("; ".join( [ "dist( [3,2,7]," + str(testProdSpace.int2Tuple(j)) + ") = " + str(testProdSpace.dist(testProdSpace.tuple2Int([3,2,7]),j))  for j in uniformFromFourBall]))
    oneBall = testProdSpace.ball([3,2,7],1)
    print("the ball [3,2,7] , 1 (as tuples) " + str(list(map( testProdSpace.int2Tuple, oneBall ))))
    assert(len(oneBall)==10)

    #testLargeProdSpace = finiteMetricSpaceLP(testSpace,d=13)
    #uniformFromLargeBall = testLargeProdSpace.uniformFromBall([1,3,15,10,9,0,0,3,2,7,1,0,12],3,10)
    #print("uniform in ball [1,3,15,10,9,0,0,3,2,7,1,0,12], 3  (" + str(len(testProdSpace.ball([1,3,15,10,9,0,0,3,2,7,1,0,12],3))) +" elements): " + str(unifromFromLargeBall) + " = " + str(list(map(testProdSpace.int2Tuple,uniformFromLargeBall))))

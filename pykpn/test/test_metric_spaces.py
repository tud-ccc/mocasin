from pykpn.representations.metric_spaces import *
from pykpn.representations.examples import *

print("using dijkstra everywhere:" + str(arch_graph_to_distance_metric(exampleDiijkstra)))
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

testSymSpace = finiteMetricSpaceLPSym(exampleClusterArchSymmetries,d=3)
print("sym_space with d=2 has length: " + str(finiteMetricSpaceLPSym(exampleClusterArchSymmetries,d=2).n))
print("dist_sym(3,4) = " + str(exampleClusterArchSymmetries.dist([3],[4]))) # should be 2, 0 if we have wreath
print("dist_sym(3,0) = " + str(exampleClusterArchSymmetries.dist([3],[0]))) # should be 0
print("dist_sym([3,2,7],[3,0,4]) = " + str(testSymSpace.dist([3,2,7],[3,0,4]))) # should be 0
print("dist_sym([3,4,7],[3,0,4]) = " + str(testSymSpace.dist([3,4,7],[3,0,4]))) # should be 2
print("dist_sym([3,4,3],[5,11,4]) = " + str(testSymSpace.dist([3,4,3],[5,11,4]))) #should be 6, 1 if we have wreath
#print(autExampleClusterArch.tuple_orbit([3,4,3]))
#testLargeProdSpace = finiteMetricSpaceLP(testSpace,d=13)
#uniformFromLargeBall = testLargeProdSpace.uniformFromBall([1,3,15,10,9,0,0,3,2,7,1,0,12],3,10)
#print("uniform in ball [1,3,15,10,9,0,0,3,2,7,1,0,12], 3  (" + str(len(testProdSpace.ball([1,3,15,10,9,0,0,3,2,7,1,0,12],3))) +" elements): " + str(unifromFromLargeBall) + " = " + str(list(map(testProdSpace.int2Tuple,uniformFromLargeBall))))

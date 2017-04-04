import logging
import numpy as np

dim = 2
min_s = 0
max_s = 15


# start with full cube with the edges length of design space
# sample within cube (100x) definiert durch kantenlaenge
# baue cube mit p >= vorgabewert
# verarbeite cube mit meisten treffern weiter
# array mit fun names

def get_cube_volume():
    # matrix defined cube by two vectores
    # find cube in tree (for now its constant)
    cube = [5,6] # cube definition
    t = [1,1]    # transpose vector
    return {'t':t,'c':cube} 

def cube_sample():
    """ take uniform random sample from hypervolume """
    sample = []
    v = get_cube_volume()
    # find random sample within cube
    for i in range(0,len(v.get('c'))):
	sample.append(np.random.randint(0,v.get('c')[i]) + v.get('t')[i])
    return np.array(sample)

def cube_adaptation():
    # build cube for p value
    print "call of adaptation"

# specify a fesability test set    
def test_oracle(s):
    """ test oracle function (2-dim) """
    print "call of test oracle"
    if (len(s) != 2):
	print("test oracle requires a dimension of 2\n")
        return 0
    x = s[0]
    y = s[1]
    if ((x in range(1,4)) and (y in range(1,5))): # 1<=x<=3
	return 1
    else:
	return 0


import numpy as np
import pytest
from unittest.mock import Mock

from pykpn.design_centering.design_centering.dc_volume import *
import pykpn.design_centering.design_centering.dc_sample as sample
import pykpn.design_centering.design_centering.dc_oracle as oracle
import pykpn.design_centering.design_centering.designCentering as dc

from pykpn.common.kpn import KpnGraph, KpnProcess
from pykpn.common.platform import Platform, Processor, Scheduler
from pykpn.common.mapping import Mapping
import pykpn.util.random_distributions.discrete_random as rd
from scipy.linalg import sqrtm

import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from ..dc_volume import *

NUM_PROCS = 50
NUM_SAMPLES = 200
NUM_ITER = 20
POINT = [15,13]

#@pytest.fixture
def kpn():
    k = KpnGraph('a')
    k.add_process(KpnProcess('a'))
    k.add_process(KpnProcess('b'))
    return k

#@pytest.fixture
def platform(num_procs=NUM_PROCS):
    p = Platform('platform')
    procs = []
    for i in range(num_procs):
        proc = Processor(('processor' + str(i)), 'proctype', Mock())
        procs.append(proc)
        p.add_processor(proc)
    policies = [Mock()]
    sched = Scheduler('name',procs,policies)
    p.add_scheduler(sched)
    return p

#@pytest.fixture
def center(point=[1,2]):
    k = kpn()
    p = platform()
    m = Mapping(k,p)
    m.from_list(point)
    return m


#@pytest.fixture
def lp_vol(point=[1,2],transf=None):
    k = kpn()
    p = platform()
    dim = 2
    c = center(point=point)
    vol = LPVolume(c,dim,k,p,conf())
    if transf is not None:
        vol.transformation = transf
    return vol

#@pytest.fixture
def s_set():
    result = sample.SampleSet()
    n = 5
    for i in range(n):
        s = sample.Sample(sample=[i,i])
        s.setFeasibility(True)
        result.add_sample(s)
        
        s = sample.Sample(sample=[-i,i])
        s.setFeasibility(False)
        result.add_sample(s)
    return result

#https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

#@pytest.fixture
def conf():
    return AttrDict({'adapt_samples' : NUM_SAMPLES, 'max_step': 10, 'adaptable_center_weights' : False , 'radius' : 10})

def random_s_set_gen(n,procs,mu,Q,r,threshold=0.05,num_points=10):
    ns = [procs] * n

    # print np.linalg.det(Q)
    # print np.linalg.eig(Q)
    #eigenv,_ = np.linalg.eig(r**2 * Q*np.transpose(Q))
    #print("Eigenvalues of Cov: " + str(eigenv))

    #test discrete uniform plain
    result = sample.SampleSet()
    for i in range(NUM_SAMPLES):
        sample_vec = rd.discrete_gauss(ns,mu,r,np.matrix(Q))
        s = sample.Sample(sample=sample_vec)
        s.setFeasibility(True)
        result.add_sample(s)
    return result


#@pytest.fixture
def random_s_set_test_center():
    n = 2
    procs = NUM_PROCS
    mu = POINT
    #Q = np.matrix(sqrtm(np.matrix([[ 3., 0.], [0., 1/3.]]))) 
    Q = np.matrix(sqrtm(np.matrix([[ 1.66666667,  1.33333333], [ 1.33333333,  1.66666667]]))) # same as above, rotated 45^\circ
    r = 3
    return random_s_set_gen(n,procs,mu,Q,r)

def random_s_set_test_radius(r,center=POINT,r_set=3):
    n = 2
    procs = 50
    mu = [15,13]
    #Q = np.matrix(sqrtm(np.matrix([[ 3., 0.], [0., 1/3.]]))) 
    Q = np.matrix(sqrtm(np.matrix([[ 1.66666667,  1.33333333], [ 1.33333333,  1.66666667]]))) # same as above, rotated 45^\circ
    test_set = random_s_set_gen(n,procs,mu,Q,r)
    Qinv = np.linalg.inv(Q)
    for s in test_set.get_feasible():
        vecNotShifted = (np.array(s.sample2tuple()) - np.array(center))
        vec = np.dot(vecNotShifted , Qinv)
        dist = np.sqrt(np.dot(vec,vec.transpose()))
        if dist >= r_set:
            s.setFeasibility(False)

    return test_set

def random_s_set_test_covariance(Q,center=POINT):
    n = 2
    procs = 50
    mu = [15,13]
    r = 3
    #Q = np.matrix(sqrtm(np.matrix([[ 3., 0.], [0., 1/3.]]))) 
    Q_set = np.matrix(sqrtm(np.matrix([[ 1.66666667,  1.33333333], [ 1.33333333,  1.66666667]]))) # same as above, rotated 45^\circ
    test_set = random_s_set_gen(n,procs,mu,Q,r)
    Qinv = np.linalg.inv(Q_set)
    for s in test_set.get_feasible():
        vecNotShifted = (np.array(s.sample2tuple()) - np.array(center))
        vec = np.dot(vecNotShifted , Qinv)
        dist = np.sqrt(np.dot(vec,vec.transpose()))
       # print(dist)
        if dist >= r:
            s.setFeasibility(False)

    return test_set
        

def parse_s_set(s_set,center,coordinates):
    x = []
    y = []
    colors = []
    for s in s_set.get_feasible():
        x.append(s.sample2tuple()[coordinates[0]])
        y.append(s.sample2tuple()[coordinates[1]])
        colors.append(0)
    for s in s_set.get_infeasible():
        x.append(s.sample2tuple()[coordinates[0]])
        y.append(s.sample2tuple()[coordinates[1]])
        colors.append(1)
    x.append(center[coordinates[0]])
    y.append(center[coordinates[1]])
    colors.append(2)
    return x,y,colors

@pytest.mark.skip("Test can't succeed. Need fix by Goens.")
def test_center_adaptation():
    vol = lp_vol()
    points = []
    centers = [vol.center]

    for _ in range(NUM_ITER):
        sample_set = random_s_set_test_center()
        vol.adapt_center(sample_set)
        x,y,colors = parse_s_set(sample_set,vol.center,coordinates=[0,1])
        points.append((x,y,colors))
        centers.append(vol.center)
    print(centers)
    #visualize_s_sets(points)

@pytest.mark.skip("Test can't succeed. Need fix by Goens.")
def test_radius_adaptation():
    vol = lp_vol(point=POINT)
    print(vol.radius)
    points = []
    for _ in range(NUM_ITER):
        sample_set = random_s_set_test_radius(vol.radius)
        conf.adapt_samples=NUM_SAMPLES
        vol.adapt_volume(sample_set,0.65,Mock())
        print(vol.radius)
        x,y,colors = parse_s_set(sample_set,vol.center,coordinates=[0,1])
        points.append((x,y,colors))
    
@pytest.mark.skip("Test can't succeed. Need fix by Goens.")
def test_covariance_adaptation():
    vol = lp_vol(transf=np.identity(2))
    points = []
    for _ in range(NUM_ITER):
        sample_set = random_s_set_test_covariance(vol.covariance)
        conf.adapt_samples=NUM_SAMPLES
        vol.adapt_volume(sample_set,0.65,Mock())
        print(vol.covariance)
        x,y,colors = parse_s_set(sample_set,vol.center,coordinates=[0,1])
        points.append((x,y,colors))

    #visualize_s_sets(points)
    
    
@pytest.mark.skip("Test can't succeed. Need fix by Goens.")
def test_all_infeasible():
    vol = lp_vol(transf=np.identity(2))
    points = []
    sample_set = sample.SampleSet()
    conf.adapt_samples=NUM_SAMPLES
    vol.adapt_volume(sample_set,0.65,Mock())
    print(vol.covariance)


@pytest.mark.skip("Test can't succeed. Need fix by Goens.")
def visualize_s_sets(points,coordinates=[0,1],ns=[NUM_PROCS,NUM_PROCS]):
    fig, ax = plt.subplots()
    (x,y,colors) = points[0]
    plot = plt.scatter(x, y,  c=colors, alpha=0.5)
    axes = plt.gca()
    axes.set_xlim([0,ns[0]-1])
    axes.set_ylim([0,ns[0]-1])
    def animate(i):
        if i < len(points):
            (x,y,colors) = points[i]
        else:
            (x,y,colors) = points[len(points)]

        plot.set_offsets(np.c_[x,y])
        return plot,
    myAnimation = animation.FuncAnimation(fig, animate, interval=1000, blit=True, repeat=True)

    plt.show()


    plt.show()

def main():
    test_covariance_adaptation()

if __name__ == "__main__":
    main()

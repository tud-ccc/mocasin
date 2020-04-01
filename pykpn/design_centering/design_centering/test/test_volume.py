# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Author: Andrés Goens

import numpy as np
from unittest.mock import Mock

from pykpn.design_centering.design_centering.dc_volume import *
import pykpn.design_centering.design_centering.dc_sample as sample

import pykpn.util.random_distributions.discrete_random as rd

import matplotlib.pyplot as plt
import matplotlib.animation as animation



def random_s_set_gen(n,procs,mu,Q,r,num_samples,threshold=0.05,num_points=10):
    ns = [procs] * n

    # print np.linalg.det(Q)
    # print np.linalg.eig(Q)
    #eigenv,_ = np.linalg.eig(r**2 * Q*np.transpose(Q))
    #print("Eigenvalues of Cov: " + str(eigenv))

    #test discrete uniform plain
    result = sample.SampleSet()
    for i in range(num_samples):
        sample_vec = rd.discrete_gauss(ns,mu.astype(int),r,np.array(Q))
        s = sample.Sample(sample=sample_vec)
        s.setFeasibility(True)
        result.add_sample(s)
    return result

def random_s_set_test_center(dim,num_procs,mu,num_samples,Q,r):
    procs = num_procs
    s_set = random_s_set_gen(dim,procs,mu,Q,r,num_samples)
    component = np.random.randint(2)
    other_component = 1 - component
    for sample in s_set.get_samples():
        tup = sample.sample2simpleTuple()
        # skew upward
        if tup[component] > mu[component] and (tup[other_component] == mu[other_component]):
            sample.setFeasibility(True)
        else:
            sample.setFeasibility(False)
    return s_set

#generates random sets of points around a feasible circle with radius r_set
def random_s_set_test_radius(r,point,dim,num_procs,num_samples,Q,r_set):
    test_set = random_s_set_gen(dim,num_procs,point,Q,r,num_samples)
    Qinv = np.linalg.inv(Q)
    for s in test_set.get_feasible():
        vecNotShifted = (np.array(s.sample2tuple()) - np.array(point))
        vec = np.dot(vecNotShifted , Qinv)
        dist = np.sqrt(np.dot(vec,vec.transpose()))
        if dist >= r_set:
            s.setFeasibility(False)

    return test_set

#center and radius should not really change
def random_s_set_test_covariance(Q,Q_target,dim,num_procs,r,mu,num_samples):
    test_set = random_s_set_gen(dim,num_procs,mu,Q,r,num_samples)
    Qinv = np.linalg.inv(Q_target)
    for s in test_set.get_feasible():
        vecNotShifted = (np.array(s.sample2tuple()) - np.array(mu))
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

def test_center_adaptation(vol_mu,num_iter,num_procs,num_samples,Q,r,seed):
    points = []
    centers = [vol_mu.center]
    dim = len(vol_mu.center)
    np.random.seed(seed)


    for _ in range(num_iter):
        sample_set = random_s_set_test_center(dim,num_procs,vol_mu.center,num_samples,Q,r)
        vol_mu.adapt_center(sample_set)
        x,y,colors = parse_s_set(sample_set,vol_mu.center,coordinates=[0,1])
        points.append((x,y,colors))
        centers.append(vol_mu.center)

    itercenters = iter(centers)
    old_center = next(itercenters)
    for center in itercenters:
        for new,old in zip(center,old_center):
            assert(new >= old)
    num_centers = len(set(map(tuple,centers)))
    assert num_centers > 1

#Note on the radius adaptation: if the p value hits perfectly the target_p,
#the radius will still vary a bit (albeit not much).
#This follows directly from the forumlas in the original paper.
#We can see this with the following Sage code, for example:
#var('N', 'mu', 'lambd', 'Beta')
#Beta = 0.6/((2+1.3)**2 + mu)
#f = (1+Beta*(1-mu/lambd))^mu * (1-Beta * mu/lambd)^(lambd-mu)
#plot(f(lambd=1000),(mu,0,1000))

def test_radius_adaptation(vol_mu,num_samples,seed,num_iter,num_procs,dim,Q,r_set,target_p,conf):
    np.random.seed(seed)
    #points = []
    radii = [vol_mu.radius]
    for _ in range(num_iter):
        sample_set = random_s_set_test_radius(vol_mu.radius,vol_mu.center,dim,num_procs,num_samples,Q,r_set) # (r,point,dim,num_procs,num_samples,Q,r_set)
        conf.adapt_samples=num_samples
        vol_mu.adapt_volume(sample_set,target_p,Mock())
        radii.append(vol_mu.radius)
        #x,y,colors = parse_s_set(sample_set,vol_mu.center,coordinates=[0,1])
        #points.append((x,y,colors))
    #distances to target p should improve:
    target_r = target_p * r_set #I don't know why this is. I feel it should be: r_set * target_p ** (-1./dim)
    iterradii = iter(radii)
    old_radius = next(iterradii)
    for new_radius in iterradii:
        dist_old = np.abs(target_r - old_radius)
        dist_new = np.abs(target_r - new_radius)
        assert(dist_old + 0.5 >= dist_new) #allow a (generous) 0.5 margin of error
        old_radius = new_radius

    #in the end (actual) p should be close to target_p
    #rel_vol_feasible = r_set**dim  #ignoring pi and such factors
    #rel_vol_found = vol_mu.radius**dim  #ignoring pi and such factors
    p = new_radius/r_set #again, no idea why it is this, I feel it should be: rel_vol_feasible / rel_vol_found
    assert np.isclose(p,target_p,atol=0.1)

    
def test_covariance_adaptation(seed,num_iter,num_samples,r_small,num_procs,vol_mu,Q,Q_not_rotated,conf):
    np.random.seed(seed)
    points = []
    mu = vol_mu.center
    vol_mu.covariance = Q
    r = r_small
    vol_mu.radius = r
    dim = len(mu)
    p_target = 0.65

    for _ in range(num_iter):
        #print(f"\n radius: {vol_mu.radius} ;covariance (det: {np.linalg.det(vol_mu.covariance)}): \n {vol_mu.covariance}")
        sample_set = random_s_set_test_covariance(vol_mu.covariance,Q_not_rotated,dim,num_procs,r,vol_mu.center,num_samples)
        conf.adapt_samples=num_samples
        vol_mu.adapt_volume(sample_set,p_target,Mock())
        if vol_mu.radius > r:
            p_target = 0.9
        else:
            p_target = 0.1
        #assert(np.isclose(np.linalg.det(vol_mu.covariance),1,rtol=0.1))

        #print(vol_mu.covariance)
        #x,y,colors = parse_s_set(sample_set,vol_mu.center,coordinates=[0,1])
        #points.append((x,y,colors))
    print(vol_mu.covariance)
    #visualize_s_sets(points)
    
    
def test_all_infeasible(lp_vol,num_samples,conf):
    sample_set = sample.SampleSet()
    conf.adapt_samples=num_samples
    cov = lp_vol.covariance
    radius = lp_vol.radius
    center = lp_vol.center
    lp_vol.adapt_volume(sample_set,0.65,Mock())
    #nothing should change, but algorithm should not crash
    assert np.alltrue(cov == lp_vol.covariance)
    assert radius == lp_vol.radius
    assert np.alltrue(center == lp_vol.center)


def visualize_s_sets(points,num_procs):
    ns=[num_procs,num_procs]
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

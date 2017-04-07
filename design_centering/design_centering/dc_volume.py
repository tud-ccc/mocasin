import sys
import logging
import numpy as np
import dc_settings as conf

class Volume(object):

    def __init__(self):
        print("create default volume")

    def adapt(vol):
        print("adapt volume")
        return vol
    
    def shrink(vol):
        print("shrink volume")
        return vol
        
class Cube(Volume):

    def __init__(self, center, dim):
        print("create cube")
        # define initial cube with radius 1 at the given center
        if (len(center) != dim):
            print("Dimensions do not match to the given center. (-1)")
            sys.exit(-1)
        self.center = list(center)
        self.radius = 0.5
        self.dim = dim

    def adapt(self, s_set, target_p):
        # take mean of feasible points as new center
        fs_set = list(map(lambda s: s.sample,  s_set.get_feasible()))
        m = np.mean(fs_set, axis=0)
        self.center = np.around(m)
        # adjust radius
        p = len(s_set.get_feasible()) / len(s_set.sample_set) 
        if (p > target_p):
            self.extend()
        else:
            self.shrink()
    
    def shrink(self):
        # shink volume by one on each border
        print("shrink cube")
        self.radius = self.radius - 1 if (self.radius - 1 > 0) else self.radius
    
    def extend(self):
        # extend volume by one on each border
        print("extend cube")
        self.radius = self.radius + 1 if (self.radius + 1 < conf.max_pe) else self.radius



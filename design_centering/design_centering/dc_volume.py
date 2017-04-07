import logging
import numpy as np

class Volume(object):

    def __init__(self):
        print("create default volume")

    def is_inside(sample):
        print("default volume has no members")
        return False
    
    def adapt(vol):
        print("adapt volume")
        return vol
    
    def shrink(vol):
        print("shrink volume")
        return vol
        

class Cube(Volume):
    
    def __init__(self, center, dim):
        print("create cube")

    def is_inside(sample):
        print ("sample is part of cube")
        return True

    def adapt(vol):
        print ("adapt cube")
        return vol
    
    def shrink(vol):
        print ("shrink cube")
        return vol



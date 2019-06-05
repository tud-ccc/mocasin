# Copyright (C) 2017-2018 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import sys
import logging
import numpy as np
from . import dc_settings as conf
from pykpn.representations.representations import RepresentationType, toRepresentation

from pykpn.util import logging

log = logging.getLogger(__name__)

DEFAULT_RADIUS = 0.5

class Volume(object):

    def __init__(self):
        log.debug("create default volume")

    def adapt(vol):
        log.debug("adapt volume")
        return vol

    def shrink(vol):
        log.debug("shrink volume")
        return vol

class Cube(Volume):

    def __init__(self, center, dim):
        # define initial cube with radius 1 at the given center
        if (len(center) != dim):
            log.error("Dimensions do not match to the given center. (-1)")
            sys.exit(-1)
        self.center = list(center)
        self.radius = DEFAULT_RADIUS
        self.dim = dim

    def adapt_center(self, s_set):
        fs_set = list(map(lambda s: s.sample,  s_set.get_feasible()))
        if not fs_set:
            return self.center
        # take mean of feasible points as new center
        m = np.mean(fs_set, axis=0)
        self.center = np.around(m).tolist()
        return self.center
    
    def correct_center(self, s_set, center, old_center):
        # shortest points to center
        d_cur = list(map(lambda s: [s.dist(center),s], s_set.get_feasible()))
        d_cur = sorted(d_cur, key=lambda x: x[0])
        nearest_samples=[]
        for s in d_cur:
            if (s[0] == d_cur[0][0]):
                nearest_samples.append(s[1])
        # take (first) shortest point to old center from that result
        d_old = list(map(lambda s: [s.dist(old_center),s], s_set.get_feasible()))
        d_old = sorted(d_old, key=lambda x: x[0])
        for s in d_old:
            if s[1] in nearest_samples:
                return s[1].sample
        return None

    def adapt_volume(self, s_set, target_p, s_val):
        fs_set = list(map(lambda s: s.sample,  s_set.get_feasible()))
        # adjust radius
        p = len(s_set.get_feasible()) / len(s_set.sample_set)
        log.debug("---------- adapt_volume() -----------")
        log.debug("p-factors: {} {}".format(s_set.get_feasible(), len(s_set.sample_set)))
        if (p >= target_p):
            # simple adaptation: cube does not support shape adaption
            log.debug ("extend at p: {:f} target_p {:f} r: {:f}".format(p, target_p, self.radius))
            self.extend(s_val)
        else:
            log.debug ("shrink at p: {:f} target_p {:f} r: {:f}".format(p, target_p, self.radius))
            self.shrink(s_val)
        return p

    def shrink(self, step):
        # shink volume by one on each border
        self.radius = self.radius - 1 if (self.radius - 1 > 0) else self.radius

    def extend(self, step):
        # extend volume by one on each border
        self.radius = self.radius + step*conf.max_step if (self.radius + step*conf.max_step < conf.max_pe) else self.radius


class VectorSpaceVolume(Volume):

    def __init__(self, center, dim, kpn, platform, representation_type=RepresentationType['SimpleVector'],p=2):
        if (len(center) != dim):
            log = logging.getLogger(__name__)
            log.exception("Dimensions do not match to the given center. (-1)")
            sys.exit(-1)
        if representation_type not in [RepresentationType['SimpleVector'],
                                       RepresentationType['FiniteMetricSpaceLP'],
                                       RepresentationType['FiniteMetricSpaceLPSym'],
                                       RepresentationType['MetricSpaceEmbedding'],
                                       RepresentationType['SymmetryEmbedding']]:
            log = logging.getLogger(__name__)
            log.exception("Representation not supported for VectorSpaceVolumes")
            sys.exit(-1)

        self.representation = representation_type.getClassType()(kpn,platform)
        self.kpn = kpn
        self.platform = platform
        mapping_center = Mapping(kpn,platform,list(center)) #TODO: check to do this right
        self.center = toRepresentation(self.representation,center)
        self.radius = DEFAULT_RADIUS
        self.dim = dim
        self.p = p #TODO: check, can I propagate this to the representations?
        


    #TODO: fix starting from here
    def adapt_center(self, s_set):
        #all feas. samples in s_set
        fs_set = list(map(lambda s: s.sample,  s_set.get_feasible()))
        if not fs_set:
            return self.center
        # take mean of feasible points as new center
        m = np.mean(fs_set, axis=0)
        log.debug("mean mapping {}".format(m))
        self.center = np.around(m)
        return self.center
    
    def correct_center(self, s_set, center, old_center):
        # shortest points to center
        d_cur = list(map(lambda s: [s.dist(center),s], s_set.get_feasible()))
        d_cur = sorted(d_cur, key=lambda x: x[0])
        nearest_samples=[]
        for s in d_cur:
            if (s[0] == d_cur[0][0]):
                nearest_samples.append(s[1])
        # take (first) shortest point to old center from that result
        d_old = list(map(lambda s: [s.dist(old_center),s], s_set.get_feasible()))
        d_old = sorted(d_old, key=lambda x: x[0])
        for s in d_old:
            if s[1] in nearest_samples:
                return s[1].sample
        return None

    def adapt_volume(self, s_set, target_p, s_val):
        fs_set = list(map(lambda s: s.sample,  s_set.get_feasible()))
        # adjust radius
        p = len(s_set.get_feasible()) / len(s_set.sample_set)
        log.debug("---------- adapt_volume() -----------")
        log.debug("p-factors: {} {}".format(s_set.get_feasible(), len(s_set.sample_set)))
        if (p >= target_p):
            # simple adaptation: cube does not support shape adaption
            log.debug ("extend at p: {:f} target_p {:f} r: {:f}".format(p, target_p, self.radius))
            self.extend(s_val)
        else:
            log.debug ("shrink at p: {:f} target_p {:f} r: {:f}".format(p, target_p, self.radius))
            self.shrink(s_val)
        return p

    def shrink(self, step):
        # shink volume by one on each border
        self.radius = self.radius - 1 if (self.radius - 1 > 0) else self.radius

    def extend(self, step):
        # extend volume by one on each border
        self.radius = self.radius + step*conf.max_step if (self.radius + step*conf.max_step < conf.max_pe) else self.radius

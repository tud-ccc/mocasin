import numpy as np
import random as rand

import design_centering.design_centering.dc_volume as dc_volume
import design_centering.design_centering.dc_settings as conf
from representations import finiteMetricSpace

from sys import exit


class Sample(list):
    def __init__(self,sample=None):
        self.feasible = False
        if sample is None:
            sample = []
        self.sample = sample

    def setFeasibility(self,feasibility):
        assert type(feasibility) is bool
        self.feasible = feasibility

    def getFeasibility(self,feasibility):
        return self.feasible

    def sample2tuple(self):
        return tuple(self.sample)

    def dist(self,s):
        return None

class SampleGenerator():
    def gen_samples_in_ball(self,vol,distr,nsamples=1):
        res = []
        for _ in range(nsamples):
            s = self.gen_sample_in_vol(vol,distr)
            res.append(Sample(s))
        return res

class GeometricSample(Sample):
    # This class overrides the self.sample and prvides a dist function
    def dist(self,s):
        # use Manhattan metric
        return np.linalg.norm(self.sample - s.sample, 2)

class SampleGeometricGen(SampleGenerator):

    def gen_samples_in_ball(self,vol,distr,nsamples=1):
        res = []
        for _ in range(nsamples):
            s = self.gen_sample_in_vol(vol,distr)
            res.append(GeometricSample(s))
        return res

    def gen_random_sample(self):
        for _d in vol.center:
            rand_val = self.uniform_distribution(0, conf.max_pe)
            self.sample.append(rand_val)


    def gen_sample_in_vol(self, vol, distr):
        #foreach element check if value is between center +/- radius
        sample = GeometricSample()
        for _d in vol.center:
            if (distr == "uniform"):
                rand_val = self.uniform_distribution(round(_d - vol.radius), round(_d + vol.radius))
                sample.append(rand_val)
            if (distr == "binomial"):
                rand_val = self.binomial_distribution(_d, vol.radius)
                sample.append(rand_val)
        return sample

    def uniform_distribution(self, min_s, max_s):
        return rand.randint(min_s, max_s)

    def binomial_distribution(self, c, r):
        upper = c + r
        lower = c - r
        if (upper > conf.max_pe):
            upper = conf.max_pe
        if (lower < 0):
            lower = 0
        val = -1
        while ( val < lower or val > upper):
            val = np.random.binomial(conf.max_pe-1, 0.5, 1)
        return val[0]

class MetricSpaceSampleGen(SampleGenerator):
    def __init__(self,M):
        self.M = M

    def gen_sample_in_vol(self,vol,distr):
        return self.gen_samples_in_ball(vol,distr,nsamples=1)

    def gen_samples_in_ball(self,ball,distr,nsamples=1):
        if distr != "uniform":
            print("Error!, distribution '" + str(distr) + "' not supported (yet).")
            exit(1)
        sample_ints =  self.M.uniformFromBall(ball.center,ball.radius,nsamples)
        #print(sample_ints)
        sample_list = list(map(lambda s: MetricSpaceSample(self.M,s), sample_ints))
        return sample_list


class MetricSpaceSample(Sample):
    # This class overrides the self.sample type from tuple to int
    # and uses the representation to convert to a tuple again
    def __init__(self,M,sample=None):
        assert isinstance(M,finiteMetricSpace)
        self.M = M
        Sample.__init__(self,None)
        self.sample = sample

    def sample2tuple(self):
        #print("M.n = " + str(self.M.n))
        return tuple(self.M.int2Tuple(int(self.sample)))


class SampleSet(object):

    def __init__(self):
        type(self).sample_set = []

    def add_sample(self, sample):
        type(self).sample_set.append(sample)

    def add_sample_list(self, samples):
        type(self).sample_set += samples

    def get_feasible(self):
        feasible_samples = []
        for _s in type(self).sample_set:
            if (_s.feasible):
                feasible_samples.append(_s)
        return feasible_samples

    def get_infeasible(self):
        infeasible_samples = []
        for _s in type(self).sample_set:
            if (not _s.feasible):
                infeasible_sample.append(_s)
        return infeasible_samples

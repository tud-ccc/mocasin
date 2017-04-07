import dc_volume
import numpy as np
import random as rand
import dc_settings as conf

class Sample(object):
    
    def __init__(self):
        print("init sample")
        self.feasible = False
        self.sample = []
    
    def gen_random_sample(self):
        print("generate random sample")
        for _d in vol.center:
            rand_val = self.uniform_distribution(0, conf.max_pe)
            self.sample.append(rand_val)


    def gen_sample_in_vol(self, vol, distr):
        print("generate random sample from vol")
        #foreach element check if value is between center +/- radius
        for _d in vol.center:
            if (distr == "uniform"):
                rand_val = self.uniform_distribution(round(_d - vol.radius), round(_d + vol.radius))
                self.sample.append(rand_val)
            if (distr == "binomial"):
                rand_val = self.binomial_distribution(_d, vol.radius)
                self.sample.append(rand_val)

    def sample2tuple(self):
        return tuple(self.sample)

    def uniform_distribution(self, min_s, max_s):
        return rand.randint(min_s, max_s)
    
    def binomial_distibution(self, c, r):
        upper = c + r 
        lower = c - r
        if (upper > conf.max_pe):
            upper = conf.max_pe
        if (lower < 0):
            lower = 0
        val = -1
        while ( val < lower or val > upper):
            val = np.random.binomial(conf.max_pe-1, 0.5, 1)
        return val

class SampleSet(object):
    
    def __init__(self):
        type(self).sample_set = []
    
    def add_sample(self, sample):
        type(self).sample_set.append(sample)
    
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

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import numpy as np
import random as rand

from pykpn.design_centering import volume
from pykpn.design_centering import oracle
from pykpn.representations.metric_spaces import FiniteMetricSpace
from pykpn.common.mapping import Mapping
from pykpn.representations.representations import RepresentationType, MetricSpaceRepresentation,\
    MetricEmbeddingRepresentation, SimpleVectorRepresentation, SymmetryRepresentation
import pykpn.util.random_distributions.lp as lp

from sys import exit

from pykpn.util import logging

log = logging.getLogger(__name__)

class Sample(list):
    def __init__(self,sample=None,sim_context=None, representation=None):
        """Describes a sample from a volume for a given representation. 

        :param sample: a vector describing the sample
        :type sample: Sample
        :sim_context: the context (platform, kpn etc.) set after simulation of the sample
        :type: SimulationContext
        :param representation_type: a representation type
        :type platform: RepresentationType
        """
        self.feasible = False
        if sample is None:
            sample = []
        self.sample = sample
        self.sim_context = sim_context
        self.representation = representation

    def setFeasibility(self,feasibility):
        assert type(feasibility) is bool
        self.feasible = feasibility

    def getSimContext(self):
        return self.sim_context

    def setSimContext(self,sim_context):
        self.sim_context = sim_context
    
    def getMapping(self, idx):
        return self.sim_context.app_contexts[idx].mapping

    def getFeasibility(self):
        return self.feasible

    def sample2tuple(self):
        return tuple(self.sample)

    def sample2simpleTuple(self):
        if self.representation == None:
            log.warning("sample2tuple(): no representation set - return simple tuple for sample")
            return tuple(self.sample)
        #print ("Tuple::::: {}".format(tuple(representation._elem2SimpleVec(self.sample))))
        return tuple(self.representation._elem2SimpleVec(self.sample))

    def dist(self,s):
        return None
    
    # returns a spacialized string represantation
    def __str__(self):
        return "Sample: {}".format(tuple(self.sample))
    def __unicode__(self):
        return "Sample: {}".format(tuple(self.sample))
    def __repr__(self):
        return "Sample: {}".format(tuple(self.sample))


class SampleGeneratorBase():
    def __init__(self, conf):
        self.conf = conf

    def gen_samples_in_ball(self,vol,distr,nsamples=1):
        res = []
        for _ in range(nsamples):
            s = self.gen_sample_in_vol(vol,distr)
            res.append(Sample(s))
        return res

class GeometricSample(Sample):
    # This class defines a geometric sample as subclass from Sample
    # provides a specialized dist function
    def dist(self,s):
        # use Manhattan metric
        return np.linalg.norm(self.sample - s.sample, 2)

class SampleGeometricGen(SampleGeneratorBase):

    def __init__(self, conf):
        super().__init__(conf)

    def gen_samples_in_ball(self,vol,distr,nsamples=1):
        res = []
        for _ in range(nsamples):
            s = self.gen_sample_in_vol(vol,distr)
            res.append(GeometricSample(s))
        log.debug("\ngen sample in ball\n {}\n".format(res[0].sample2tuple()))
        return res

    def gen_random_sample(self):
        for _d in vol.center:
            rand_val = self.uniform_distribution(0, self.conf[1].max_pe)
            self.sample.append(rand_val)


    def gen_sample_in_vol(self, vol, distr):
        #foreach element check if value is between center +/- radius
        sample = GeometricSample()
        for _d in vol.center:
            if (distr == "uniform"):
                rand_val = self.uniform_distribution(round(_d - vol.radius), round(_d + vol.radius))
                sample.append(rand_val % 16)
            if (distr == "binomial"):
                rand_val = self.binomial_distribution(_d, vol.radius)
                sample.append(rand_val)
        #print("\n{} from {} distr.".format(sample,distr))
        return sample

    def uniform_distribution(self, min_s, max_s):
        return rand.randint(min_s, max_s)

    def binomial_distribution(self, c, r):
        upper = c + r
        lower = c - r
        if (upper > self.conf[1].max_pe):
            upper = self.conf[1].max_pe
        if (lower < 0):
            lower = 0
        val = -1
        while ( val < lower or val > upper):
            val = np.random.binomial(self.conf[1].max_pe-1, 0.5, 1)
        return val[0]

class VectorSampleGen(SampleGeneratorBase):
    def __init__(self,representation, conf):
        super().__init__(conf)
        self.representation = representation

    def gen_sample_in_vol(self,vol,distr):
        return self.gen_samples_in_ball(vol,distr,nsamples=1)

    def gen_samples_in_ball(self,ball,distr,nsamples=1):
        if distr != "uniform":
            log.error("Error!, distribution '" + str(distr) + "' not supported (yet).")
            exit(1)
        sample_ints = self.representation._uniformFromBall(ball.center,ball.radius,nsamples)
        sample_list = list(map(lambda s: MetricSpaceSample(self.representation,s), sample_ints))
        return sample_list


class VectorSpaceSample(Sample):
    # This class overrides the self.sample type from tuple to int
    # and uses the representation to convert to a tuple again
    def __init__(self,rep,sample=None):
        #assert isinstance(rep,FiniteMetricSpace) or log.error(f"Sampling from metric space with representation: {rep}")
        self.representation = rep 
        Sample.__init__(self,None)
        self.sample = sample

    def sample2tuple(self):
        #print("M.n = " + str(self.M.n))
        return tuple(self.representation.int2Tuple(int(self.sample)))

class MetricSpaceSampleGen(SampleGeneratorBase):
    def __init__(self,representation, conf):
        super().__init__(conf)
        self.representation = representation

    def gen_sample_in_vol(self,vol,distr):
        return self.gen_samples_in_ball(vol,distr,nsamples=1)

    #TODO: this seems it would be better housed in volume than here.
    def gen_samples_in_ball(self,vol,distr,nsamples=1):
        if distr != "uniform":
            log.error("Error!, distribution '" + str(distr) + "' not supported (yet).")
            exit(1)
        sample_list = []
        for _ in range(nsamples):
            lp_random_vector = lp.uniform_from_p_ball(p=vol.norm_p,n=vol.dim)
            scaled_vector = vol.radius * lp_random_vector
            transformed_vector = vol.covariance @ scaled_vector
            new_sample_vector = vol.center + transformed_vector
            sample_ints = self.representation.approximate(new_sample_vector)
            new_sample = MetricSpaceSample(self.representation,sample_ints)
            sample_list.append(new_sample)
            distance = self.representation._distance(sample_ints,vol.center)
            if distance > vol.radius:
                log.warning(f"Generated vector with distance ({distance}) greater than radius ({vol.radius}).")
            log.debug(f"Generated sample (distance: {distance}):\n {sample_ints}")
        return sample_list


class MetricSpaceSample(Sample):
    # This class overrides the self.sample type from tuple to int
    # and uses the representation to convert to a tuple again
    def __init__(self,rep,sample=None):
        #assert isinstance(rep,FiniteMetricSpace) or log.error(f"Sampling from metric space with representation: {rep}")
        Sample.__init__(self,None)
        self.sample = sample 
        self.representation = rep 

    def sample2tuple(self):
        #print("M.n = " + str(self.M.n))
        return tuple(self.sample)


class SampleSet(object):

    def __init__(self):
        # list of all samples
        type(self).sample_set = []
        # list of all samples per iteration
        type(self).sample_groups = []

    def add_sample(self, sample):
        type(self).sample_set.append(sample)

    def add_sample_list(self, samples):
        type(self).sample_set += samples
    
    def add_sample_group(self, samples):
        type(self).sample_groups.append(samples)

    def get_samples(self):
        return type(self).sample_set

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
                infeasible_samples.append(_s)
        return infeasible_samples

def SampleGen(representation, conf):
    if representation == "GeomDummy":
        return SampleGeometricGen(conf)
    elif isinstance(representation,MetricSpaceRepresentation):
        return MetricSpaceSampleGen(representation, conf)
    elif isinstance(representation,MetricEmbeddingRepresentation):
        return MetricSpaceSampleGen(representation, conf)
    elif isinstance(representation,SimpleVectorRepresentation):
        return MetricSpaceSampleGen(representation, conf)
    elif isinstance(representation,SymmetryRepresentation):
        return MetricSpaceSampleGen(representation, conf)
    else:
        log.error(f"Sample generator type not found:{generator_type}")
        exit(1)
    
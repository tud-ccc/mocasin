# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import numpy as np

from mocasin.design_centering import oracle
from mocasin.design_centering import sample as dc_sample
from mocasin.design_centering import util as dc_util
from mocasin.util import logging
from mocasin.representations import MappingRepresentation
import sys

log = logging.getLogger(__name__)


class DesignCentering(object):
    def __init__(self, init_vol, oracle, sample_generator, representation,
                 hitting_probability=[0.4, 0.5, 0.5, 0.7, 0.9],
                 hitting_probability_threshold=0.7, deg_p_polynomial=2, deg_s_polynomial=2,
                 step_width=[0.9, 0.7, 0.6, 0.5, 0.1], adapt_samples=10, max_samples=50,
                 record_samples=False, show_polynomials=False, distr='uniform',
                 keep_metrics=True, max_pe=16):
        self.vol = init_vol
        self.oracle = oracle
        self.representation = representation
        self.samples = {}
        self.sample_generator = sample_generator
        self.adapt_samples = adapt_samples
        self.vol.adapt_samples = adapt_samples
        self.max_samples = max_samples
        self.record_samples = record_samples
        self.show_polynomials = show_polynomials
        self.distr = distr
        self.keep_metrics = keep_metrics
        self.max_pe = max_pe
        self.p_value = self.__adapt_poly(hitting_probability, deg_p_polynomial)
        self.s_value = self.__adapt_poly(step_width, deg_s_polynomial)
        if hitting_probability_threshold <= 1:
            self.p_threshold = hitting_probability_threshold
        else:
            log.error(f"Hitting probability threshold ({hitting_probability_threshold}) is unreachable (>1)")
            sys.exit(1)

    def __adapt_poly(self, support_values, deg):
        num = len(support_values)
        x_interval = self.max_samples/(num - 1)
        x = []
        y = []
        ret = []

        for _i in range(0, num, 1):
            x.append(_i * x_interval)
            y.append(support_values[_i])

        coeff = np.polyfit(x, y, deg)
        poly = np.poly1d(coeff)

        for _j in range(0, self.max_samples, 1):
            ret.append(poly(_j))

        if self.show_polynomials:
            tp = dc_util.ThingPlotter()
            tp.plot_curve(ret, self.max_samples)

        return ret

    def __has_duplicate(self, samples):
        seen = set()
        uniq_samples = []
        for s in samples:
            s = s.sample2simpleTuple()
            if s not in seen:
                seen.add(s)
                uniq_samples.append(s)
        return len(uniq_samples)

    def ds_explore(self):
        """ explore design space (main loop of the DC algorithm) """
        history = {'samples' : [], 'centers' : [], 'radii' : []}

        #check starting center
        center = self.vol.center
        current_center = dc_sample.Sample(sample=center, representation=self.representation)
        best_area = 0
        best_center = current_center

        for i in range(0, self.max_samples, self.adapt_samples):
            s = self.sample_generator
            log.debug("dc: Current iteration {}".format(i))
            s_set = dc_sample.SampleSet()
            samples = s.gen_samples_in_ball(self.vol, self.distr, nsamples=self.adapt_samples)
            dup = self.adapt_samples - self.__has_duplicate(samples)

            if dup > 0:
                log.warning("DC: Sample-list of {} elements has {} duplicates.".format(self.adapt_samples, dup))
            
            #put samples as paramater in simulation
            log.info("dc: Input samples:\n {} ".format(samples))
            samples = self.oracle.validate_set(samples) # validate multiple samples
            log.info("dc: Output samples:\n {}".format(samples))

            s_set.add_sample_list(samples)
            s_set.add_sample_group(samples)

            log.debug("dc: Output fesaible samples:\n {}".format(s_set.get_feasible()))
            center = self.vol.adapt_center(s_set)
            #center = list(map(int, center))
            current_center = dc_sample.Sample(sample=center, representation=self.representation)
            self.oracle.validate_set([current_center])

            if not current_center.getFeasibility():
                log.warning("DC iteration with a non-feasible center")

            # if not self.oracle.validate(dc_sample.GeometricSample(center)): #this breaks the rest!
            #     c_cur = dc_sample.GeometricSample(center)
            #     c_old = dc_sample.GeometricSample(old_center)
            #     new_center = self.vol.correct_center(s_set, c_cur, c_old)
            #     print("Correction of infeasible center: {} take {} instead".format(center, new_center))
            cur_p = self.vol.adapt_volume(s_set, self.p_value[i], self.s_value[i])
            log.debug("dc: center: {} radius: {:f} p_emp: {}, target_p {}".format(self.vol.center,
                                                                                  self.vol.radius,
                                                                                  cur_p,
                                                                                  self.p_value[i]))
            area = cur_p * self.vol.radius**self.vol.true_dim

            if cur_p >= self.p_threshold and area >= best_area and current_center.getFeasibility():
                best_area = area
                best_center = center
                log.info(f"found a better center (radius {self.vol.radius}, p {cur_p}). updating.")

            if self.record_samples:
                for sample in samples:
                    history['samples'].append(sample)
                history['centers'].append(current_center)
                history['radii'].append(self.vol.radius)

        if best_area == 0:
            log.error("Could not find a center within hitting probability threshold."
                      "Returning last center candidate found.")
            best_center = center

        #modify last sample
        #TODO build mapping from center (this destroys parallel execution)
        center_sample = dc_sample.Sample(sample=best_center, representation=self.representation)
        center_sample_result = self.oracle.validate_set([center_sample])

        log.debug("dc: center sample: {} {} {}".format(str(center_sample_result), str(center_sample), str(center)))

        return center_sample_result[0], history

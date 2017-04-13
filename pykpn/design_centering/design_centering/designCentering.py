#!/usr/bin/python
import re
import sys
import json
import logging
from . import dc_oracle
from . import dc_sample
from . import dc_volume
from . import dc_settings as conf
import numpy as np
import matplotlib.pyplot as plt
from ... import representations as reps

class ThingPlotter(object):
    def plot_samples(self,samples):
        """ Plot sample points of the from [(x1,x2,...,xn), Boolean] """
        for _sample in samples:
            if samples[_sample]:
                plt.plot(_sample[0], _sample[1],"o", color='b')
            else:
                plt.plot(_sample[0], _sample[1],"o", color='r')
        plt.xticks(range(0, conf.max_pe, 1))
        plt.yticks(range(0, conf.max_pe, 1))
        plt.show()

    def plot_curve(self, data):
        interval = int(conf.max_samples/10)
        for _j in range(0, conf.max_samples, 1):
            plt.plot(_j, data[_j],"o", color='b')
        plt.xticks(range(0, conf.max_samples, interval))
        plt.yticks(np.arange(0, 1, 0.1))
        plt.show()

class DesignCentering(object):

    def __init__(self, init_vol, distr, oracle):
        np.random.seed(conf.random_seed)
        type(self).distr = distr
        type(self).vol = init_vol
        type(self).oracle = oracle
        type(self).samples = {}
        type(self).p_value = self.__adapt_poly(conf.hitting_propability, conf.deg_p_polynomial)
        type(self).s_value = self.__adapt_poly(conf.step_width, conf.deg_s_polynomial)

    def __adapt_poly(self, support_values, deg):
        tp = ThingPlotter()
        num = len(support_values)
        x_interval = (conf.max_samples/(num - 1))
        x = []
        y = []
        ret = []
        for _i in range(0,num,1):
            x.append(_i * x_interval)
            y.append(support_values[_i])
        coeff = np.polyfit(x, y, deg)
        poly = np.poly1d(coeff)
        for _j in range(0, conf.max_samples, 1):
            ret.append(poly(_j))
        if (conf.show_polynomials):
            tp.plot_curve(ret)
        return ret

    def ds_explore(self):
        """ explore design space (main loop of the DC algorithm) """
        for i in range(0, conf.max_samples, conf.adapt_samples):
            s_set = dc_sample.SampleSet()
            s = dc_sample.SampleGeometricGen()
            #M = finiteMetricSpaceLP(exampleClusterArch,d=2)
            #M = reps.finiteMetricSpaceLPSym(reps.exampleClusterArchSymmetries,d=2)
            #s = dc_sample.MetricSpaceSampleGen(M)

            samples = s.gen_samples_in_ball(type(self).vol, type(self).distr, conf.adapt_samples)
            #print(str([s.sample for s in samples]))
            for s in samples:
                s.feasible = type(self).oracle.validate(s)

            s_set.add_sample_list(samples)

            for s in samples:
                # add to internal overall sample set
                type(self).samples.update({s.sample2tuple():s.feasible})

            #print(s_set.get_feasible())
            old_center = type(self).vol.center
            center = type(self).vol.adapt_center(s_set)
            if not type(self).oracle.validate(dc_sample.GeometricSample(center)): #this breaks the rest!
                c_cur = dc_sample.GeometricSample(center)
                c_old = dc_sample.GeometricSample(old_center)
                new_center = type(self).vol.correct_center(s_set, c_cur, c_old)
                print("Correction of infeasible center: {} take {} instead".format(center, new_center))
            cur_p = type(self).vol.adapt_volume(s_set, type(self).p_value[i], type(self).s_value[i])
            logging.debug(" center: {} radius: {:f} p: {}".format(type(self).vol.center, type(self).vol.radius, cur_p))
            print("center: {} radius: {:f} p: {}".format(type(self).vol.center, type(self).vol.radius, cur_p))


def main():
    argv = sys.argv
    print("===== run DC =====")
    logging.basicConfig(filename="dc.log", filemode = 'w', level=logging.DEBUG)
    tp = ThingPlotter()

    if (len(argv) > 1):
        # read cmd-line and settings
        try:
            center = json.loads(argv[1])
        except ValueError:
            print(" {:s} is not a vector \n".format(argv[1]))
            sys.stderr.write("JSON decoding failed (in function main) \n")

        if (conf.shape == "cube"):
            v = dc_volume.Cube(center, len(center))

        # run DC algorithm
        dc = DesignCentering(v, conf.distr, dc_oracle.Oracle())
        dc.ds_explore()

        # plot explored design space
        if True:
            tp.plot_samples(dc.samples)
        logging.info(" >>> center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
        print(">>> center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
    else:
        print("usage: python designCentering [x1,x2,...,xn]\n")


    return 0

if __name__ == "__main__":
    main()


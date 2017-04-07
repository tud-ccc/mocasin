#!/usr/bin/python
import re
import sys
import json
import logging
import dc_oracle
import dc_sample
import dc_volume
import dc_settings as conf
import numpy as np
import matplotlib.pyplot as plt

class DesignCentering(object):

    def __init__(self, init_vol, distr, oracle):
        type(self).distr = distr
        type(self).vol = init_vol
        type(self).oracle = oracle
        type(self).samples = {}
        type(self).p_value = self.__adapt_p_value()

    def __adapt_p_value(self):
        num_p = len(conf.hitting_propability)
        x_interval = (conf.max_samples/(num_p - 1))
        x = []
        y = []
        p_v = []
        for _i in range(0,num_p,1):
            x.append(_i * x_interval)
            y.append(conf.hitting_propability[_i])
        coeff = np.polyfit(x, y, 2)
        poly = np.poly1d(coeff)
        for _j in range(0, conf.max_samples, 1):
            p_v.append(poly(_j))
        if (conf.show_polynom):
            self.__plot_p_curve(p_v)
        return p_v

    def __plot_p_curve(self, p):
        interval = int(conf.max_samples/10)
        for _j in range(0, conf.max_samples, 1):
            plt.plot(_j, p[_j],"o", color='b')
        plt.xticks(range(0, conf.max_samples, interval))
        plt.yticks(np.arange(0, 1, 0.1))
        plt.show()

    def ds_explore(self):
        """ explore design space (main loop of the DC algorithm) """
        for i in range(0, conf.max_samples, conf.adapt_samples):
            s_set = dc_sample.SampleSet()
            for j in range(0, conf.adapt_samples):
                s = dc_sample.Sample()
                s.gen_sample_in_vol(type(self).vol, type(self).distr)
                s.feasible = type(self).oracle.validate(s)
                s_set.add_sample(s)
            if (len(s_set.get_feasible()) > 0):
                type(self).vol.adapt(s_set, type(self).p_value[i])
            else:
                type(self).vol.shrink()
            print("center: {} radius: {:f}".format(type(self).vol.center, type(self).vol.radius))
            
            type(self).samples.update({s.sample2tuple():s.feasible})

    def plot_samples(self):
        for _sample in type(self).samples:
            if type(self).samples[_sample]:
                plt.plot(_sample[0], _sample[1],"o", color='b')
            else:
                plt.plot(_sample[0], _sample[1],"o", color='r')
        plt.xticks(range(0, conf.max_pe, 1))
        plt.yticks(range(0, conf.max_pe, 1))
        plt.show()


def main(argv):
    print("===== run DC =====")
    logging.basicConfig(filename="dc.log", level=logging.DEBUG)
    logging.debug(" mu: {:f} radius: {:f}".format(1.1, 3.14))
    if (len(argv) > 1):
        # read cmd-line and settings
        try:
            center = json.loads(argv[1])
        except ValueError:
            print(" {:s} is not a vector \n".format(argv[1]))
            sys.stderr.write("JSON decoding failed (in read file) \n")
        
        if (conf.shape == "cube"):
            v = dc_volume.Cube(center, len(center))

        # run DC algorithm
        dc = DesignCentering(v, conf.distr, dc_oracle.Oracle())
        dc.ds_explore()
        
        # plot explored design space
        dc.plot_samples()
        print("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
    else:
        print("usage: python designCentering [x1,x2,...,xn]\n")

    
    return 0

if __name__ == "__main__":
    main(sys.argv)


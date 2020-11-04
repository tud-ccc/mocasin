# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import json
import glob
import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

class ThingPlotter(object):
    def plot_samples(self, samples, max_pe):
        """ Plot sample points of the from [(x1,x2,...,xn), Boolean] """
        for _sample in samples:
            if samples[_sample]:
                plt.plot(_sample[0], _sample[1], "o", color='b')
            else:
                plt.plot(_sample[0], _sample[1], "o", color='r')
        plt.xticks(range(0, max_pe, 1))
        plt.yticks(range(0, max_pe, 1))

        #Where is pert_res_list supposed to come from?
        center_x = sorted(pert_res_list)
        plt.show()

    def plot_curve(self, data, max_samples):
        interval = int(max_samples/10)
        for _j in range(0, max_samples, 1):
            plt.plot(_j, data[_j], "o", color='b')

        plt.xticks(range(0, max_samples, interval))
        plt.yticks(np.arange(0, 1, 0.1))
        plt.show()

    def plot_perturbations(self, pert_res_list, out_dir=None):
        # the first list element is the center
        x = []
        y = []

        for i, p in enumerate(sorted(pert_res_list, reverse=True)):
            if p is pert_res_list[0]:
                center_x = i
                break
                
        center_y = pert_res_list[0]

        for i, p in enumerate(sorted(pert_res_list, reverse=True)):
            x.append(i)
            y.append(p)

        fig = plt.figure(figsize=(14, 8))
        plt.scatter(x, y)
        plt.scatter(center_x, center_y, color='r')
        plt.xlabel("Mappings")
        plt.ylabel("Perturbations Passed")

        if out_dir is None:
            plt.show()
        else:
            fig.savefig(out_dir)



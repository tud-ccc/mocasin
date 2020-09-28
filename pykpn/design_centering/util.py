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


def write_dc_to_csv(dc_info, filename):
    if not os.path.exists(filename):
        with open(filename, 'w+', newline='') as file:
            fieldnames = list(dc_info[0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in dc_info:
                writer.writerow(row)
    else:
        raise RuntimeError(f" file {filename} already exists")


def read_multiple_dc_jsons(pattern):
    files = glob.glob(pattern)
    dcs = []

    for filename in files:
        dc = read_dc_json(filename)
        dcs.append(dc)

    return [row for run in dcs for row in run]

def read_dc_json(filename):
    dc_data = []

    with open(filename, 'r') as file:
        raw = json.load(file)
        config = {
                'representation' : raw['config']['representation'],
                'perturbation_type' : raw['config']['perturbation_type'],
                'random_seed' : raw['config']['random_seed'],
                'threshold' : raw['config']['threshold'],
                'distribution' : raw['config']['distr'],
                'start_time' :  raw['config']['start_time'],
                'app' :  raw['config']['app'],
                'platform' :  raw['config']['platform'],
                #'adaptable_center_weights' : _raw['config']['adaptable_center_weigths'],
        }
        radius = raw['config']['starting_radius']
        #if 'periodic_boundary_conditions' in raw['config']:
        #        config['periodic_boundary_conditions'] =  raw['config']['periodic_boundary_conditions']

        #start with center so that all fields (eg. pert. stability) get proper values from csv reader
        if 'radius' in raw['center']:
            radius = raw['center']['radius']
        mapping_data = {
            'mapping': raw['center']['mapping'],
            'center': True,
            'perturbation': False,
            'feasible': raw['center']['feasible'],
            'runtime': raw['center']['runtime'],
            'radius' : radius,
            'dc_iteration': int(raw['config']['max_samples'] / raw['config']['adapt_samples']),
            'perturbation_stability': None}
        if 'passed' in raw['center']:
            mapping_data['perturbation_stability']  = raw['center']['passed']
        dc_data.append({**config, **mapping_data})
        if 'samples' in raw:
            for i,dc_iteration in enumerate(raw['samples']):
                for sample_key in raw['samples'][dc_iteration]:
                    sample = raw['samples'][dc_iteration][sample_key]
                    if sample_key == 'center':
                        center = True
                    else:
                        center = False
                    if 'radius' in sample:
                        radius = sample['radius']
                    mapping_data = {
                        'mapping': sample['mapping'],
                        'center': center,
                        'perturbation': False,
                        'feasible': sample['feasible'],
                        'runtime': sample['runtime'],
                        'dc_iteration': dc_iteration,
                        'radius': radius,
                        'perturbation_stability': ''}
                    dc_data.append({**config, **mapping_data})

        if 'pert' in raw['center']:
            for i,sample_key in enumerate(raw['center']['pert']):
                sample = raw['center']['pert'][sample_key]
                mapping_data = {
                    'mapping': sample['mapping'],
                    'center': False,
                    'perturbation': True,
                    'feasible': sample['feasible'],
                    'runtime': sample['runtime'],
                    'dc_iteration': int(raw['config']['max_samples'] / raw['config']['adapt_samples']),
                    'perturbation_stability': ''}
                dc_data.append({**config, **mapping_data})
    return dc_data

if __name__ ==  "__main__":
    from sys import argv
    dcs  = read_multiple_dc_jsons(argv[1])
    print(f"Parsed {len(dcs)} json files... writing to {argv[2]}.")
    write_dc_to_csv(dcs,argv[2])

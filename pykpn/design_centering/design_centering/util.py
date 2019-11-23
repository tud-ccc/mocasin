import json
import glob
import csv
import os
import sys

def write_dc_to_csv(dc_info,filename):
    if not os.path.exists(filename):
        with open(filename,'w+', newline='') as file:
            fieldnames = list(dc_info[0].keys())
            writer = csv.DictWriter(file,fieldnames=fieldnames)
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
        raw =  json.load(file)
        config = {
                'representation' : raw['config']['representation'],
                'random_seed' : raw['config']['random_seed'],
                'threshold' : raw['config']['threshold'],
                'distribution' : raw['config']['distr'],
                'start_time' :  raw['config']['start_time'],
                'app' :  raw['config']['app'],
                'platform' :  raw['config']['platform'],
                'starting_radius' :  raw['config']['starting_radius'],
                #'adaptable_center_weights' : _raw['config']['adaptable_center_weigths'],
        }
        if 'periodic_boundary_conditions' in raw['config']:
                config['periodic_boundary_conditions'] =  raw['config']['periodic_boundary_conditions']

        #start with center so that all fields (eg. pert. stability) get proper values from csv reader
        mapping_data = {
            'mapping': raw['center']['mapping'],
            'center': True,
            'perturbation': False,
            'feasible': raw['center']['feasible'],
            'runtime': raw['center']['runtime'],
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
                    mapping_data = {
                        'mapping': sample['mapping'],
                        'center': center,
                        'perturbation': False,
                        'feasible': sample['feasible'],
                        'runtime': sample['runtime'],
                        'dc_iteration': dc_iteration,
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
    write_dc_to_csv(dcs,argv[2])

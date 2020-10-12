#!/usr/bin/env python3

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

import yaml
import csv
from os import listdir
from os.path import abspath, isdir, join

def parse_override_string(override_string):
    #has format: key1=value1,value2,...,valueN,key2=...
    parameters_lists = [x.split(',') for x in override_string.split('=')]
    #has format: [[key1],[value1,value2,...,valueN,key2],...]
    parameters = {}
    #special case for beginig
    key = parameters_lists[0][0]
    #dont iterate until end (special case)
    for l in parameters_lists[1:-1]:
        values = l[:-1]
        parameters[key] = values
        key = l[-1]
    #treat special case at the end
    parameters[key] = parameters_lists[-1]
    return parameters

def write_to_csv(keys,results,csv_out):
    with open(csv_out,'w') as f:
        writer = csv.DictWriter(f,keys)
        writer.writeheader()
        for res in results:
            writer.writerow(res)


def read_multirun(path,outputs_parsers = None,output_format = 'csv'):
    if outputs_parsers is None:
        outputs_parsers = []
    multirun_file  = abspath(path) + "/multirun.yaml"
    with open(multirun_file,'r') as f:
        multirun_config = yaml.load(f,Loader=yaml.SafeLoader)
    parameters_str = multirun_config['hydra']['job']['override_dirname']
    multirun_parameters = parse_override_string(parameters_str)
    keys = set(multirun_parameters.keys())

    directories = filter(isdir, [join(path,dir) for dir in listdir(path)])
    csv_out = path.replace('/','.') + "." + output_format

    results = []
    for dir in directories:
        with open(dir + "/.hydra/hydra.yaml") as f:
            iteration_config = yaml.load(f, Loader=yaml.SafeLoader)
            parameters_str= iteration_config['hydra']['job']['override_dirname']
            parameters = parse_override_string(parameters_str)
            results_dict = {}
            for param in parameters:
                results_dict[param] = parameters[param][0]

        for parser in outputs_parsers:
            outputs,newkeys = parser(dir)
            results_dict = {**results_dict,**outputs}
            keys = keys.union(newkeys)
        results.append(results_dict)
    if output_format == 'csv':
        write_to_csv(keys,results,csv_out)
    else:
        raise RuntimeError(f"Output format {output_format} not supported.")


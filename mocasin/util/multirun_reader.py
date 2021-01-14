#!/usr/bin/env python3

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

import yaml
import csv
import h5py
import os

from mocasin.util import logging
log = logging.getLogger(__name__)

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
        if type(values) == list and len(values) > 1:
            # TODO: make multiple keys instead
            values = [','.join(values)]
        parameters[key] = values
        key = l[-1]
    #treat special case at the end
    parameters[key] = parameters_lists[-1]
    return parameters

def write_to_csv(keys,results_dict,csv_out):
    results = []
    for file in results_dict:
        new_vals = [results_dict[file]['params']]
        for parser in results_dict[file]['parsers']:
            outputs = results_dict[file]['parsers'][parser]
            if type(outputs) == list:
                updated = []
                for val in new_vals:
                    for out in outputs:
                        updated.append({**val, **out})
                new_vals = updated
            elif type(outputs) == dict:
                updated = []
                for val in new_vals:
                    updated.append({**val, **outputs})
                new_vals = updated
            else:
                log.error(f"Parser error, invalid results: {outputs}")
                raise RuntimeError

        results = results + new_vals
    with open(csv_out,'w') as f:
        writer = csv.DictWriter(f,keys)
        writer.writeheader()
        for res in results:
            writer.writerow(res)

def write_to_h5(results,h5_out):
    f = h5py.File(h5_out,'w')
    for dir_full in results:
        dir = dir_full.replace('/','.')
        f.create_group(dir)
        for param in results[dir_full]['params']:
            f[dir].attrs[param] = results[dir_full]['params'][param]
        for parser in results[dir_full]['parsers']:
            f[dir].create_group(parser)
            res = results[dir_full]['parsers'][parser]
            if type(res) == dict:
                for param in res:
                    f[dir][parser].attrs[param] = res[param]
            elif type(res) == list:
                for i,vals in enumerate(res):
                    f[dir][parser].create_group(str(i))
                    for param in vals:
                        f[dir][parser][str(i)].attrs[param] = res[i][param]

    f.close()


def read_multirun(path,outputs_parsers = None,output_format = 'csv',output_filename=None):

    if outputs_parsers is None:
        outputs_parsers = []
    multirun_file  = os.path.abspath(path) + "/multirun.yaml"
    with open(multirun_file,'r') as f:
        multirun_config = yaml.load(f,Loader=yaml.SafeLoader)
    parameters_str = multirun_config['hydra']['job']['override_dirname']
    multirun_parameters = parse_override_string(parameters_str)
    keys = set(multirun_parameters.keys())

    directories = filter(os.path.isdir, [os.path.join(path,dir) for dir in os.listdir(path)])
    if output_filename is None:
        out_file = path.replace('/','.') + "." + output_format
    else:
        out_file = output_filename + "." + output_format

    results = {}
    for dir in directories:
        with open(dir + "/.hydra/hydra.yaml") as f:
            iteration_config = yaml.load(f, Loader=yaml.SafeLoader)
            parameters_str= iteration_config['hydra']['job']['override_dirname']
            parameters = parse_override_string(parameters_str)
            results_dict = {}
            for param in parameters:
                results_dict[param] = parameters[param][0]
        results[dir] = { 'params' : results_dict , 'parsers' : {}}

        for parser in outputs_parsers:
            outputs,newkeys = parser(dir)
            results[dir]['parsers'][parser.__name__] = outputs
            keys = keys.union(newkeys)
    if output_format == 'csv':
        write_to_csv(keys,results,out_file)
    elif output_format == 'h5':
        write_to_h5(results,out_file)
    else:
        raise RuntimeError(f"Output format {output_format} not supported.")

def total_time_estimator(dir):
    times = []
    for subdir,_,files in os.walk(dir):
        for file in files:
            fname = os.path.join(subdir,file)
            times.append(os.path.getctime(fname))
            times.append(os.path.getmtime(fname))
    estimated_time = max(times) - min(times)
    results = {'estimated_total_time' : estimated_time}
    return results, list(results.keys())

#!/usr/bin/python
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import mapping_utils as mu
import json
import logging
import time
import sys
import config as conf
import re

def cache_read(file_name):
    infile = open(file_name, "r")
    mapgen = mu.PartialMapper(conf.default_path)
    mapping = []
    log_cache = {}
    result = False
    for l in infile:
        tmp = re.split(":", l)
        if ("Input" in tmp):
            try:
                mapping = json.loads(tmp[3])
            except ValueError:
                sys.stderr.write("JSON decoding failed (in read file oracle) ")
	    if (len(mapping) > conf.num_pr):
		mapping = mapgen.extmap2map(mapping)
            try:
	        l = next(infile)
	    except StopIteration:
	        print "StopIteration"
	        return
        tmp = re.split(":", l)
        if ("Output" in tmp):
	    result = float(tmp[3]) 

	log_cache.update({tuple(mapping):result})
    return log_cache

def cache_lookup(mapping, log_cache):
    mapgen = mu.PartialMapper(conf.default_path)
    if (len(mapping) > conf.num_pr):
	mapping = mapgen.extmap2map(mapping)
    if log_cache:
	if tuple(mapping) in log_cache:
	    return log_cache[tuple(mapping)]
	else: 
	    return None
    return None

def run_oracle(mapping):
    mapgen = mu.PartialMapper(conf.default_path)
    # read log file into cache
    cache = cache_read(conf.log_path)
    
    if (len(mapping) <= conf.num_pr):
	mapping = mapgen.map2extmap(mapping)

    # lookup cache for mapping
    if (conf.use_oracle_cache):
	res = cache_lookup(mapping, cache)
    else:
	res = None
	
    if res is not None:
	#print "short eval"
	return res
    else:
	#print "long eval"
	logging.debug("Input:  {:s}".format(mapgen.extmap2map(mapping)))
	pr2pe_map = mapgen.generatePr2PeMap(mapping)
	mapgen.export2XML(conf.xml_path ,pr2pe_map)
	# trace the new mapping
	maptest = mu.MappingTester()
	trace_out = maptest.trace(conf.xml_path, conf.tool_path, conf.benchmark)
	res = maptest.extract_TraceResults(trace_out)
	logging.debug("Output: {:f}".format(res))  
	return res

def run_oracle_parallel(mappings, num_threads):
    # generate new mapping-XML similar to a given defult mapping
    i = 0
    async_res = []
    res = []
    pool = ThreadPool(processes = num_threads)

    #print mappings
    for mapping in mappings:
        logging.debug("Input:  {:s}".format(mapping))
	i = i + 1
	mapgen = mu.PartialMapper(conf.default_path)
        if (len(mapping) <= conf.num_pr):
	    mapping = mapgen.map2extmap(mapping)
	pr2pe_map = mapgen.generatePr2PeMap(mapping)
	mapgen.export2XML("{:s}.{:d}.xml".format(conf.xml_root, i) ,pr2pe_map)
	
        # trace the new mapping
        maptest = mu.MappingTester()
        async_res.append(pool.apply_async(maptest.trace, ("{:s}.{:d}.xml".format(conf.xml_root, i), conf.tool_path, conf.benchmark)))
        #logging.debug("Output: {:f}".format(res))  
    
    pool.close()
    pool.join()

    for ar in async_res:
        res.append(maptest.extract_TraceResults(ar.get()))
    return res

def main(argv):
    logging.basicConfig(filename=conf.log_path, level=logging.DEBUG)

    try:
        #logging.debug("argv: " + sys.argv[1])
        mapping = json.loads(sys.argv[1])
	#mapping = mapping + static_mapping_part
    except ValueError:
        sys.stderr.write("JSON decoding failed")

    return run_oracle(mapping)

if __name__ == "__main__":
    if (main(sys.argv) < conf.threshold):
	sys.stdout.write('1')
	sys.stdout.flush()
    else:
	sys.stdout.write('0')
	sys.stdout.flush()
    sys.stdout.close()

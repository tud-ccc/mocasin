#!/usr/bin/python
import sys, getopt
import math as m
import projection as prj
import mapping_utils as mu
import config as conf
import oracle as delphi
import random as rand
import logging
import json
import re
import copy as cp

class PertubationGenerator(object):
    
    @staticmethod
    def new_clusterMemCore(c_in):
        """ Returns a new random core within the cluster """
	c_out = c_in
        if (c_in < 4):
	    while (c_out == c_in): c_out = rand.randint(0,3)
        elif (c_in < 8):
	    while (c_out == c_in): c_out = rand.randint(4,7)
	elif (c_in < 12):
	    while (c_out == c_in): c_out = rand.randint(8,11)
        elif (c_in < 15):
	    while (c_out == c_in): c_out = rand.randint(12,15)
        return c_out

    @staticmethod
    def new_sharedMemCore(c_in):
        """ Return the (equivalent) core of a new random cluster """
        cluster = 0
	new_cluster = 0
        if (c_in < 4):
	    cluster = 0
        elif (c_in < 8):
	    cluster = 1
	elif (c_in < 12):
	    cluster = 2
        elif (c_in < 15):
	    cluster = 3
	while (new_cluster == cluster): 
	    new_cluster = rand.randint(0,3)
	
	c_out = (c_in + (abs(cluster - new_cluster) * 4)) % 15
        return c_out

    @staticmethod
    def arch_dist(a,b):
        if (conf.comm_network[a][b] == 50):
	    return 0
        if (conf.comm_network[a][b] == 250): 
	    return 1
        if (conf.comm_network[a][b] == 500): 
	    return 2

    @staticmethod
    def euclid_dist(a,b):
         return abs(b-a)

    @staticmethod
    def check_dist_infinite(map1, map2):
        dist_inf = 0
        for a,b in zip(map1,map2):
	    dist_inf = max(dist_inf, abs(PertubationGenerator.arch_dist(a,b)))
	return dist_inf

    @staticmethod
    def check_dist_manhatten(map1, map2):
        dist_man = 0
        for a,b in zip(map1,map2):
	    dist_man = dist_man + abs(PertubationGenerator.arch_dist(a,b))
	return dist_man
    
    @staticmethod
    def check_dist_euclid(map1,map2):
        dist_euc = 0
        for a,b in zip(map1,map2):
	    dist_euc = dist_euc + m.pow(PertubationGenerator.arch_dist(a,b),2)
	return m.sqrt(dist_euc)

    @staticmethod
    def gen_random_mapping(s):
        """ Generates a random mapping """
        rand.seed(s)
	return [rand.randint(0,15),
	        rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15),
		rand.randint(0,15)]

    @staticmethod
    def gen_mappingForDist(s, dist, mapping_in):
        """Retrun a new mapping for a given distance"""
	m = cp.deepcopy(mapping_in)
        rand.seed(s)

        #print mapping_in
	#print dist
	#TODO: change this to gain exact results
	while (PertubationGenerator.check_dist_manhatten(m, mapping_in) <= dist):
	    idx = rand.randint(0, conf.num_pr-1)
	    pe_i = m[idx] # takes core from random vector position
	    if (rand.randint(0,1)):
		m[idx] = PertubationGenerator.new_clusterMemCore(pe_i)
	    else:
		m[idx] = PertubationGenerator.new_sharedMemCore(pe_i)
            #print m
	    #print mapping_in
	    #print PertubationGenerator.check_dist_manhatten(m, mapping_in)
	#print m
        return m

    @staticmethod
    def singleCoreMove(mapping, s):
        """ Takes a core at a random position of the mapping vector and maps it, 
	    and all other occurece of this core, to one random other core.
	    
	    Args:
	        The mapping vector to be modfied
		A random seed
	    Returns:
	        The modified mapping vector
	"""
        rand.seed(s)
        t = rand.randint(0, conf.max_pe) # random target core
	r = mapping[rand.randint(0, conf.num_pr-1)] # takes core from random vector position
	new_mapping = [x if x != r else t for x in mapping] # replace this core(s)
        return new_mapping
    
    @staticmethod
    def singleCoreArchMove(mapping, s):
        """ Takes a core at a random position of the mapping vector and maps it to a adjacent core 
	    (according to the given architecture).
	    
	    Args:
	        The mapping vector to be modfied
		A random seed
	    Returns:
	        The modified mapping vector
	"""
	m = cp.deepcopy(mapping)
        rand.seed(s)
	idx = rand.randint(0, conf.num_pr-1)
	r = mapping[idx] # takes core from random vector position
	if (r == 3):
	    m[idx] = r + 4 # replace this core with a neighbouring core
	elif (r == 7):
	    m[idx] = r + 4 # replace this core with a neighbouring core
	elif (r == 11):
	    m[idx] = r + 4 # replace this core with a neighbouring core
	elif (r == 15):
	    m[idx] = r - 1 # replace this core with a neighbouring core
	else:
	    m[idx] = r + 1 # replace this core with a neighbouring core
        return m
    
    @staticmethod
    def multiCoreMove(mapping, s, n):
        """ Moves multiple cores to annoter position """
        rand.seed(s)
	r = rand.randint(0,1000)
	for i in range(0,n):
	    mapping = PertubationGenerator.singleCoreArchMove(mapping, r + i)
        return mapping
	
    @staticmethod
    def doubleCoreArchMove(mapping, s):
        return PertubationGenerator.multiCoreMove(mapping, s, 2)
    
    @staticmethod
    def tripleCoreArchMove(mapping, s):
        return PertubationGenerator.multiCoreMove(mapping, s, 3)
    
    @staticmethod
    def quadCoreArchMove(mapping, s):
        return PertubationGenerator.multiCoreMove(mapping, s, 4)
    
    @staticmethod
    def read_logs(value_class, file_name):
        file = open(file_name, "r")
	mapping = []
	log_map = []
	log_hash = {}

	for l in file.readlines():
	    tmp = re.split(":", l)
	    if ("{:s} Input".format(value_class) in tmp):
		try:
		    mapping = json.loads(tmp[3].strip(" Dist"))
		except ValueError:
		    print(tmp[3].strip(" Dist"))
		    sys.stderr.write("JSON decoding failed (in read file) ")
		#eliminate cloned values
                log_hash.update({tuple(mapping): float(tmp[5]) < conf.threshold})
		#log_map.append((tuple(mapping), float(tmp[5]) < conf.threshold))

        for item in log_hash:
	    log_map.append((item, log_hash[item]))
	return log_map

	
    @staticmethod
    def calculate_simple_scatter_plot(start, log, log_file, p):
       # dist:(#feasable,#infeasable)
       data = {}
       log_map = []
       if (log_file != ""):
	   log_db = PertubationGenerator.read_logs(log, log_file)

       # add DC
       result = delphi.run_oracle(start)
       log_map.append((conf.test_set[0],result < conf.threshold))
       #print log_map

       
       #calculate for DC
       #add random mappings
       for i in range(1,2):
            testrange = i * 2
            for j in range(0,testrange):
                mapping = PertubationGenerator.gen_mappingForDist(j+42, i, start)
		#if mapping in log_db
                #print mapping
		#print mapping
		#mapping = (2, 2, 8, 4, 1, 6, 9, 6, 13, 10)
		cached_mapping = [item for item in log_db if item[0] == tuple(mapping)]
		if (cached_mapping != []):
		    log_map.append((cached_mapping[0][0],cached_mapping[0][1]))
		else: 
		    result = delphi.run_oracle(mapping)
		    # generate mapping and add them to the output data set
		    log_map.append((mapping,result < conf.threshold))
		    logging.debug("{:s} Input:   {:s}   Dist: {:d} Output: {:f}".format(log,mapping,i,result))

       logging.debug("======================================================================================")
       #log_map = PertubationGenerator.read_logs(log, log_file)
       
       #print log_map


       # # gather data for histogram from output list of DC-algorithm
       for mapping, bool_res in log_map: 
	   key = PertubationGenerator.check_dist_manhatten(start,mapping)
	   if (key in data):
	       if bool_res:
		   data[key][0] = data[key][0] + 1
               else:
		   data[key][1] = data[key][1] + 1
           else:
	       if bool_res:
	 	   data.update({key:[1,0]})
               else:
		   data.update({key:[0,1]})
       
       # # draw simple histogram
       print data
       p.simple_scatter(data, log)


def main(argv):
   # commandline parsing
   scat = 0
   pert = 0
   convert = 0
   try:
      opts, args = getopt.getopt(argv,"hpsc")
   except getopt.GetoptError:
      print 'pertubation.py [-h|-p|-s|-c [<mapping>]]'
      sys.exit(2)
   if opts == []:
      print 'pertubation.py [-h|-p|-s|-c [<mapping>]]'
   for opt, arg in opts:
      if opt == '-h':
         print 'pertubation.py [-h|-p|-s|-c [<mapping>]]'
         sys.exit()
      elif opt == '-p': #pertubation
         pert = 1
      elif opt == '-s': #scatter diagram
         scat = 1
      elif opt == '-c': #convert coordinates
         convert = 1
   # end commandline parsing
   
   results = []
   p = prj.ProjectionGenerator()
   
   if (convert):
       mapping = []
       try:
	   mapping = json.loads(sys.argv[2])
       except ValueError:
           sys.stderr.write("JSON decoding failed (in convert) ")
       mapgen = mu.PartialMapper(conf.default_path)

       if (len(mapping) > conf.num_pr):
	   print mapgen.extmap2map(mapping)
       else:
	   print mapgen.map2extmap(mapping)

       return
   
   
   if (scat):
       logging.basicConfig(filename="pertubation_radius_2.log", level=logging.DEBUG)

       PertubationGenerator.calculate_simple_scatter_plot(conf.test_set[0], "pertubation_radius_96","pertubation_radius_2.log",p)
       #PertubationGenerator.calculate_simple_scatter_plot([12, 3, 8, 8, 8, 12, 12, 7, 2, 11], "pertubation_radius_dc_broken",p)
       #PertubationGenerator.calculate_simple_scatter_plot([12, 9, 9, 11, 10, 6, 6, 10, 3, 9], "pertubation_radius_offcenter",p)
       #PertubationGenerator.calculate_simple_scatter_plot([3, 1, 8, 4, 1, 7, 9, 5, 14, 7], "pertubation_radius_veryoffcenter",p)
       #PertubationGenerator.calculate_simple_scatter_plot([10, 3, 8, 7, 8, 6, 9, 4, 2, 7], "pertubation_radius_bad",p)
       p.pshow()
   
   log_map = p.read_LogFile(conf.log_path, conf.threshold)
   abort = 0
   initial_seed = conf.random_seed

   if (pert):    
       logging.basicConfig(filename="pertubation.log", level=logging.DEBUG)
       for mapping, bool_res in log_map:
           if (bool_res and abort < 20):
               abort = abort + 1
               conf.test_set.append(mapping)

       for mapping in conf.test_set:
           passed = 0
           seed = initial_seed
           mapping_q = []
           for pert in conf.pertubations:
               seed = seed + 1
               #print mapping
               #tmp = pert(mapping, seed)
               #rint tmp
               mapping_q.append(pert(mapping,seed))
               #print mapping_q
           
           # run parallel oracle
           #print mapping_q
           res_q = delphi.run_oracle_parallel(mapping_q, len(conf.pertubations))
	   print res_q
           
           for res in res_q:
               if (conf.threshold > res):
                   passed = passed + 1
                   logging.debug("result: {:f} passed: {:d}".format(res, passed))
           results.append(float(passed)/float(len(conf.pertubations)))
           logging.debug("-------------------------")

       
       print results



       dc = results[0]


       results.sort()
       print results

       p.bar_chart(dc, results, x_len=len(conf.test_set))

if __name__ == "__main__": main(sys.argv[1:])


#!/usr/bin/python
import sys
import random as rand

from pykpn.design_centering.design_centering import dc_sample
from . import dc_oracle
from pykpn.mapper import rand_partialmapper as rand_pm
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.mapper.proc_partialmapper import ProcPartialMapper
from pykpn.mapper.rand_partialmapper import RandomPartialMapper

from pykpn.util import logging

log = logging.getLogger(__name__)

class PerturbationManager(object):

    def __init__(self, config ,num_mappings=0, num_tests=0):
        self.config = config
        self.num_mappings = num_mappings
        self.num_perturbations = num_tests
        self.sim = dc_oracle.Simulation(config)
        self.platform = self.sim.platform
        self.kpn = self.sim.kpn

    def create_randomMappings(self):
        """ Creates a defined number of unique random mappings """
        mapping_set = set([])
        while len(mapping_set) < self.num_mappings:
            mg = rand_pm.RandomPartialMapper(self.kpn, self.platform, self.config.random_seed)
            mapping_set.add(mg.generate_mapping())
        return mapping_set

    def apply_singlePerturbation(self, mapping, history,seed=None):
        """ Creates a defined number of unique single core perturbations 
            Therefore, the mapping is interpreted as vector with the 
            processor cores assigned to the vector elements.
        """

        # check for single application
        rand_part_mapper = RandomPartialMapper(self.kpn, self.platform, self.config.random_seed)
        proc_part_mapper = ProcPartialMapper(self.kpn, self.platform, rand_part_mapper)

        if seed is not None:
            rand.seed(seed)
        pe = rand.randint(0, len(list(self.platform.processors()))-1)
        process = rand.randint(0, len(list(self.kpn.processes()))-1)
        
        vec = []
        #assign cores to vector
        pe_mapping = proc_part_mapper.get_pe_name_mapping()
        log.debug(str(pe_mapping))
        for p in self.kpn.processes():
            log.debug(mapping.affinity(p).name) 
            vec.append(pe_mapping[mapping.affinity(p).name])

        log.debug("vec: {} ".format(vec))
        #permutate vector
        log.debug("pr: {} vec: {}".format(process, vec))
        vec[process] = pe

        while True:
            pert_mapping = proc_part_mapper.generate_mapping(vec, history)
            if pert_mapping:
                break;

        return pert_mapping

    def run_perturbation(self, mapping, pert_fun):
        """ 
        Runs the perturbation test with the defined Perturbation Method.
        The given mapping is evaluated by comparing it to randomly generated mappings. 
        """

        history = []
        results = []
        samples = []
        for i in range(0, self.num_perturbations):
            mapping = pert_fun(mapping, history)
            history.append(mapping)
            sample = dc_sample.Sample(mapping.to_list())
            samples.append(sample)
        self.sim.prepare_sim_contexts_for_samples(samples)

        results = list(map(self.sim.run_simulation, samples)) #these should be samples

        exec_times = []
        for r in results:
            exec_times.append(float(r.sim_context.exec_time / 1000000000.0))
        
        feasible = []
        for e in exec_times:
            if (e > self.config.threshold):
                feasible.append(False)
            else:
                feasible.append(True)

        log.debug("exec. Times: {} Feasible: {} History: {}".format(exec_times, feasible, history))
        # generate gridpoint from history by wighting feasible and infeasible
        simple_res = 100 * len([i for i in feasible if i is True]) / len(feasible)
        complex_res = {}
        for i in range(0, self.num_perturbations):
            complex_res['p' + str(i)] = {}
            complex_res['p' + str(i)]['mapping'] = history[i].to_list()
            complex_res['p' + str(i)]['runtime'] = exec_times[i]
            complex_res['p' + str(i)]['feasible'] = feasible[i]

        return simple_res,complex_res


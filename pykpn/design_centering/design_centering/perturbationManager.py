#!/usr/bin/python
import sys
import random as rand
from . import dc_settings as conf
from . import dc_oracle
from pykpn.mapper import rand_mapgen as rand_mg
from pykpn.slx.config import SlxSimulationConfig
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.mapper.rand_mapgen import RandomMappingGenerator
from pykpn.mapper.dc_mapgen import DC_MappingGenerator

from pykpn.util import logging

log = logging.getLogger(__name__)

class PerturbationManager(object):

    def __init__(self, config ,num_mappings=0, num_tests=0):
        self.config = config
        self.num_mappings = num_mappings
        self.num_perturbations = num_tests
        self.sim = dc_oracle.Simulation(config)
        self.platform = self.sim.get_platform()
        self.kpns = self.sim.get_kpns()

    def create_randomMappings(self):
        """ Creates a defined number of unique random mappings """
        mapping_set = set([])
        while len(mapping_set) < self.num_mappings:
            mg = rand_mg.RandomMappingGenerator(self.kpns[0], self.platform)
            mapping_set.add(mg.generate_mapping())
        return mapping_set

    def apply_singlePerturbation(self, mapping, seed, history):
        """ Creates a defined number of unique single core perturbations 
            Therefore, the mapping is interpreted as vector with the 
            processor cores assigned to the vector elements.
        """

        # check for single application
        randMapGen = RandomMappingGenerator(self.kpns[0], self.platform)
        dcMapGen = DC_MappingGenerator(self.kpns[0], self.platform, randMapGen)

        rand.seed = seed
        pe = rand.randint(0, len(list(self.platform.processors()))-1)
        process = rand.randint(0, len(list(self.kpns[0].processes()))-1)
        
        vec = []
        #assign cores to vector
        pe_mapping = dcMapGen.get_pe_name_mapping()
        log.debug(str(pe_mapping))
        for p in self.kpns[0].processes():
            log.debug(mapping.affinity(p).name) 
            vec.append(pe_mapping[mapping.affinity(p).name])

        log.debug("vec: {} ".format(vec))
        #permutate vector
        log.debug("pr: {} vec: {}".format(process, vec))
        vec[process] = pe

        while True:
            pert_mapping = dcMapGen.generate_mapping(vec, history)
            if pert_mapping:
                break;

        return pert_mapping

    def run_perturbation(self, mapping, pert_fun):
        """ 
        Runs the perturbation test with the defined Perturbation Method.
        The given mapping is evaluated by comparing it to randomly generated mappings. 
        """
        # Assume that only one application runs on the simulated platform 
        assert(len(self.kpns) == 1)
        kpn = self.kpns[0]
        
        history = []
        results = []
        sim_contexts = []
        for i in range(0, self.num_perturbations):
            mapping = pert_fun(mapping, rand.randint(0,sys.maxsize), history)
            history.append(mapping)
            sim_contexts.append(self.sim.prepare_sim_context(self.platform, kpn, mapping))

        results = list(map(self.sim.run_simulation, sim_contexts))

        exec_times = []
        for r in results:
            exec_times.append(float(r.exec_time / 1000000000.0))
        
        feasible = []
        for e in exec_times:
            if (e > self.config[1].threshold):
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


# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import sys
import random as rand
import pint

from pykpn.design_centering import sample as dc_sample
from pykpn.design_centering import oracle
from pykpn.mapper import rand_partialmapper as rand_pm
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.mapper.proc_partialmapper import ProcPartialMapper
from pykpn.mapper.rand_partialmapper import RandomPartialMapper
from pykpn.representations import representations as reps


from pykpn.util import logging

log = logging.getLogger(__name__)

class PerturbationManager(object):

    def __init__(self, config ,num_mappings=0, num_tests=0):
        self.config = config
        self.num_mappings = num_mappings
        self.num_perturbations = num_tests
        self.sim = oracle.Simulation(config)
        self.platform = self.sim.platform
        self.kpn = self.sim.kpn
        self.perturbation_ball_num = config['perturbation_ball_num']
        self.iteration_max = config['perturbation_max_iters']
        self.radius = config['radius']
        #if config['representation'] != "GeomDummy":
        #    representation_type = reps.RepresentationType[config['representation']]
        #    self.representation = (representation_type.getClassType())(self.kpn,self.platform)
        #TODO: (FIXME) Perturbation manager only works in simple vector representation (for now)
        self.representation = (reps.RepresentationType['SimpleVector'].getClassType())(self.kpn, self.platform)

    def create_randomMappings(self):
        """ Creates a defined number of unique random mappings """
        mapping_set = set([])
        while len(mapping_set) < self.num_mappings:
            mg = rand_pm.RandomPartialMapper(self.kpn, self.platform)
            mapping_set.add(mg.generate_mapping())
        return mapping_set

    def apply_singlePerturbation(self, mapping, history):
        """ Creates a defined number of unique single core perturbations
            Therefore, the mapping is interpreted as vector with the 
            processor cores assigned to the vector elements.
        """
        rand_part_mapper = RandomPartialMapper(self.kpn, self.platform)
        proc_part_mapper = ProcPartialMapper(self.kpn, self.platform, rand_part_mapper)
        iteration_max = self.iteration_max

        pe = rand.randint(0, len(list(self.platform.processors()))-1)
        process = rand.randint(0, len(list(self.kpn.processes()))-1)

        vec = []
        #assign cores to vector
        pe_mapping = proc_part_mapper.get_pe_name_mapping()
        log.debug(str(pe_mapping))
        for p in self.kpn.processes():
            log.debug(mapping.affinity(p).name) 
            vec.append(pe_mapping[mapping.affinity(p).name])

        log.debug("Process: {} PE: {} vec: {}".format(process, pe, vec))
        vec[process] = pe
        log.debug("Perturbated vec: {}".format(vec))

        # The code above can produce identical perturbations, the following loop should prevent this:
        timeout = 0
        while timeout < iteration_max:
            perturbated_mapping = proc_part_mapper.generate_mapping(vec, history)
            if perturbated_mapping:
                break;
            timeout += 1
        if timeout == iteration_max:
            log.error("Could not find a new perturbation")
            sys.exit(1)

        return perturbated_mapping

    def applyPerturbationRepresentation(self,mapping_obj,history):
        """ Creates perturbations functions using the representation.
        """
        mapping = self.representation.toRepresentation(mapping_obj)
        log.debug(f"Finding (representation-based) perturbation for mapping {mapping}")
        iteration_max = self.iteration_max
        if history is None:
            history = []
        radius = self.radius
        timeout = 0
        while timeout < iteration_max:
            perturbation_ball = self.representation._uniformFromBall(mapping,radius,self.perturbation_ball_num)
            for m in perturbation_ball:
                if m != mapping:
                    if len(history) == 0:
                        log.debug("Perturbated vec (rep): {}".format(m))
                        return (self.representation.fromRepresentation(m))
                    else:
                        for hist_map in history:
                            if self.representation.toRepresentation(hist_map) != m:
                                log.debug("Perturbated vec (rep): {}".format(m))
                                return(self.representation.fromRepresentation(m))
                            else:
                                log.debug(f"mapping {m} already in history")
            timeout += 1
            if timeout % 10 == 0:
                radius *= 1.5
                log.debug(f"increasing perturbation radius to {radius}")
        if timeout == iteration_max:
            log.error("Could not find a new perturbation")
            sys.exit(1)

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
            sample = dc_sample.Sample(mapping.to_list(),representation=self.representation)
            samples.append(sample)
        self.sim.prepare_sim_contexts_for_samples(samples)

        results = list(map(self.sim.run_simulation, samples)) #these should be samples

        exec_times = []
        for r in results:
            exec_times.append(float(r.sim_context.exec_time))
        
        feasible = []
        for e in exec_times:
            ureg = pint.UnitRegistry()
            threshold = ureg(self.config.threshold).to(ureg.ps).magnitude
            if (e > threshold):
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


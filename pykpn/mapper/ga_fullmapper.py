# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

from pykpn.util import logging
from pykpn.representations.representations import RepresentationType
from pykpn.mapper.rand_partialmapper import RandomPartialMapper
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
import deap
from deap import creator,tools,base,algorithms
import random
import numpy as np
import timeit
import simpy
import hydra
import pickle

log = logging.getLogger(__name__)

class GeneticFullMapper(object):
    """Generates a full mapping by using genetic algorithms.
    """
    def random_mapping(self):
        mapping = self.random_mapper.generate_mapping()
        as_rep = self.representation.toRepresentation(mapping)
        return list(as_rep)


    def mapping_crossover(self,m1,m2):
        return self.representation._crossover(m1,m2,self.crossover_rate)

    def mapping_mutation(self,mapping):
        #m_obj = self.representation.fromRepresentation(list((mapping)))
        radius = self.config['radius']
        while(1):
            new_mappings = self.representation._uniformFromBall(mapping,radius,20)
            for m in new_mappings:
                if list(m) != list(mapping):
                    for i in range(len(mapping)):
                        mapping[i] = m[i]
                        return mapping,
            radius *= 1.1
            if radius > 10000 * self.config['radius']:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")

    def evaluate_mapping(self,mapping):
        tup = tuple(mapping)
        log.info(f"evaluating mapping: {tup}...")
        if tup in self.mapping_cache:
            log.info(f"... from cache: {self.mapping_cache[tup]}")
            self.statistics['mappings_cached'] += 1
            return self.mapping_cache[tup],
        else:
            self.statistics['mappings_evaluated'] += 1
            time = timeit.default_timer()
            m_obj = self.representation.fromRepresentation(np.array(tup))
            trace = hydra.utils.instantiate(self.config['trace'])
            env = simpy.Environment()
            app = RuntimeKpnApplication(name=self.kpn.name,
                                    kpn_graph=self.kpn,
                                    mapping=m_obj,
                                    trace_generator=trace,
                                    env=env,)
            system = RuntimeSystem(self.platform, [app], env)
            system.simulate()
            exec_time = float(env.now) / 1000000000.0
            self.mapping_cache[tup] = exec_time
            time = timeit.default_timer() - time
            self.statistics['simulation_time'] += time
            log.info(f"... from simulation: {exec_time}.")
            return (exec_time,)

    def __init__(self, config):
        """Generates a partial mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type fullGererator: OmniConf
        """
        random.seed(config['random_seed'])
        np.random.seed(config['random_seed'])
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = hydra.utils.instantiate(config['kpn'])
        self.platform = hydra.utils.instantiate(config['platform'])
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config,seed=None)
        self.mapping_cache = {}
        self.crossover_rate = self.config['crossover_rate']
        if self.crossover_rate > len(self.kpn.processes()):
            log.error("Crossover rate cannot be higher than number of processes in application")
            raise RuntimeError("Invalid crossover rate")
        self.statistics = { 'mappings_evaluated' : 0, 'mappings_cached' : 0, 'simulation_time' : 0, 'representation_time' : 0}
        rep_type_str = config['representation']
        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform)
        self.representation = representation

        if 'FitnessMin' not in deap.creator.__dict__:
            deap.creator.create("FitnessMin", deap.base.Fitness, weights=(-1.0,))
        if 'Individual' not in deap.creator.__dict__:
            deap.creator.create("Individual", list, fitness=deap.creator.FitnessMin)
        toolbox = deap.base.Toolbox()
        toolbox.register("attribute", random.random)
        toolbox.register("mapping", self.random_mapping)
        toolbox.register("individual", deap.tools.initIterate, deap.creator.Individual, toolbox.mapping)
        toolbox.register("population", deap.tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", self.mapping_crossover)
        toolbox.register("mutate", self.mapping_mutation)
        toolbox.register("evaluate", self.evaluate_mapping)
        toolbox.register("select", deap.tools.selTournament, tournsize=self.config['tournsize'])

        self.evolutionary_toolbox = toolbox
        self.hof = deap.tools.HallOfFame(1)
        stats = deap.tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        self.evolutionary_stats = stats

        if config.initials == 'random':
            self.population = toolbox.population(n=self.config['pop_size'])
        else:
            log.error("Initials not supported yet")
            raise RuntimeError('GeneticFullMapper: Initials not supported')
            #toolbox.register("individual_guess", self.initIndividual, creator.Individual)
            #toolbox.register("population_guess", self.initPopulation, list, toolbox.individual_guess, initials,pop_size)
            #population = toolbox.population_guess()

    def run_genetic_algorithm(self):
        toolbox = self.evolutionary_toolbox
        stats = self.evolutionary_stats
        hof = self.hof
        pop_size = self.config['pop_size']
        num_gens = self.config['num_gens']
        cxpb = self.config['cxpb']
        mutpb = self.config['mutpb']

        population = self.population

        if self.config.mupluslambda:
            population, logbook = deap.algorithms.eaMuPlusLambda(population,toolbox,mu=pop_size,lambda_=3*pop_size,
                                                  cxpb=cxpb, mutpb=mutpb, ngen=num_gens, stats=stats, halloffame=hof,verbose=False)
            log.info(logbook.stream)
        else:
            population, logbook = deap.algorithms.eaMuCommaLambda(population,toolbox,mu=pop_size,lambda_=3*pop_size,
                                              cxpb=cxpb, mutpb=mutpb, ngen=num_gens, stats=stats, halloffame=hof,verbose=False)
            log.info(logbook.stream)

        return population,logbook,hof


    def generate_mapping(self):
        """ Generates a full mapping using a genetic algorithm
        """
        _,logbook,hof = self.run_genetic_algorithm()
        mapping = hof[0]
        #log.info(self.statistics)
        print(self.statistics)
        with open('evolutionary_logbook.pickle','wb') as f:
            pickle.dump(logbook,f)
        result = self.representation.fromRepresentation(np.array(mapping))
        self.cleanup()
        return result
    
    def cleanup(self):
        print("cleaning up")
        toolbox = self.evolutionary_toolbox
        toolbox.unregister("attribute")
        toolbox.unregister("mapping")
        toolbox.unregister("individual")
        toolbox.unregister("population")
        toolbox.unregister("mate")
        toolbox.unregister("mutate")
        toolbox.unregister("evaluate")
        toolbox.unregister("select")
        stats = self.evolutionary_stats
        self.evolutionary_stats = None
        del stats
        del deap.creator.FitnessMin
        del deap.creator.Individual

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

from pykpn.util import logging
from pykpn.representations.representations import RepresentationType
from deap import base, creator, tools
from pykpn.mapper.rand_partialmapper import RandomPartialMapper
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem
from deap.algorithms import eaMuCommaLambda,eaMuPlusLambda
import random
import numpy
import simpy
import hydra

log = logging.getLogger(__name__)

class GeneticFullMapper(object):
    """Generates a full mapping by using genetic algorithms.
    """
    def random_mapping(self):
        mapping = self.random_mapper.generate_mapping()
        as_rep = self.representation.toRepresentation(mapping)
        return list(as_rep)


    def mapping_crossover(self,m1,m2,k=2):
        #TODO: make a representation-specific crossover operator
        assert len(m1) == len(m2)
        crossover_points = random.sample(range(len(m1)),k)
        swap = False
        new_m1 = []
        new_m2 = []
        for i in range(len(m1)):
            if i in crossover_points:
                swap = not swap
            if swap:
                new_m1.append(m2[i])
                new_m2.append(m1[i])
            else:
                new_m1.append(m1[i])
                new_m2.append(m2[i])
        return new_m1,new_m2

    def mapping_mutation(self,mapping):
        m_obj = self.representation.fromRepresentation(mapping)
        radius = self.config['radius']
        while(1):
            new_mappings = self.representation.uniformFrommBall(m_obj,radius,20)
            for m in new_mappings:
                if self.representation.toRepresentation(m) != mapping:
                    return self.representation.toRepresentation(m)
            radius *= 1.1
            if radius > 10000 * self.config['radius']:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")
    def evaluate_mapping(self,mapping):
        print(mapping)
        m_obj = self.representation.fromRepresentation(mapping)
        env = simpy.Environment()
        app = RuntimeKpnApplication(name=self.kpn.name,
                                kpn_graph=self.kpn,
                                mapping=m_obj,
                                trace_generator=self.trace,
                                env=env,)
        system = RuntimeSystem(self.platform, [app], env)
        system.simulate()
        exec_time = float(env.now) / 1000000000.0
        return exec_time




    def __init__(self, config):
        """Generates a partial mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type fullGererator: OmniConf
        """
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = hydra.utils.instantiate(config['kpn'])
        self.platform = hydra.utils.instantiate(config['platform'])
        self.trace = hydra.utils.instantiate(config['trace'])
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config)
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

        creator.create("FitnessMin", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()
        toolbox.register("attribute", random.random)
        toolbox.register("mapping", self.random_mapping)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.mapping)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", self.mapping_crossover)
        toolbox.register("mutate", self.mapping_mutation)
        toolbox.register("evaluate", self.evaluate_mapping)
        toolbox.register("select", tools.selTournament, tournsize=self.config['tournsize'])

        self.evolutionary_toolbox = toolbox
        self.hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
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
        verbose = True #TODO: get from config

        population = self.population

        if self.config.mupluslambda:
            population, logbook = eaMuPlusLambda(population,toolbox,mu=pop_size,lambda_=3*pop_size,
                                                  cxpb=cxpb, mutpb=mutpb, ngen=num_gens, stats=stats, halloffame=hof,verbose=verbose)
        else:
            population, logbook = eaMuCommaLambda(population,toolbox,mu=pop_size,lambda_=3*pop_size,
                                              cxpb=cxpb, mutpb=mutpb, ngen=num_gens, stats=stats, halloffame=hof,verbose=verbose)

        return population,logbook,hof

    def generate_mapping(self):
        """ Generates a full mapping using a genetic algorithm
        """
        _,_,hof = self.run_genetic_algorithm()
        mapping = hof[0] #TODO: convert to proper mapping
        return mapping

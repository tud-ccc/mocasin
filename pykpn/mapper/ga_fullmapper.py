# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

from pykpn.util import logging
from deap import base, creator, tools
from deap.algorithms import eaMuCommaLambda,eaMuPlusLambda

log = logging.getLogger(__name__)

class GeneticFullMapper(object):
    """Generates a full mapping by using genetic algorithms.
    """
    def random_mapping(self):
        #TODO: Implement
        return some_random_mapping


    def mapping_crossover(self,ass1,ass2,k=2):
        #TODO: Implement
        return ass1,ass2

    def mapping_mutation(self,ass):
        #TODO: Implement
        return ass

    def __init__(self, kpn, platform, config):
        """Generates a partial mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type fullGererator: OmniConf
        """
        self.full_mapper = True # flag indicating the mapper type
        self.platform = platform
        self.kpn = kpn
        self.config = config

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()
        toolbox.register("attribute", random.random)
        toolbox.register("mapping", self.random_mapping)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.mapping)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", self.mapping_crossover)
        toolbox.register("mutate", self.mapping_mutation)
        toolbox.register("evaluate", self.evaluate_mapping)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)

        self.evolutionary_toolbox = toolbox
        self.evolutionary_stats = stats
        self.hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        self.stats = stats

        if config.initials is None:
            self.population = toolbox.population(n=pop_size)
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
        stats = self.stats

        if self.conf.mupluslambda:
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

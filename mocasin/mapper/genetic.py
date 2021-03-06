# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Robert Khasanov

from mocasin.util import logging
from mocasin.mapper.utils import SimulationManager
from mocasin.mapper.random import RandomPartialMapper
from mocasin.representations import MappingRepresentation

import deap
from deap import creator, tools, base, algorithms
import enum
from hydra.utils import instantiate
import random
import numpy as np
import pickle


log = logging.getLogger(__name__)


class Objectives(enum.Flag):
    """Objective flags for multi-objective design-space exploration."""

    NONE = 0
    EXEC_TIME = enum.auto()
    RESOURCES = enum.auto()
    ENERGY = enum.auto()

    @classmethod
    def from_string_list(cls, objectives):
        """Initialize Objectives object from a list of strings"""
        flags = Objectives.NONE
        for obj in objectives:
            if obj == "exec_time":
                flags |= cls.EXEC_TIME
                continue
            if obj == "energy":
                flags |= cls.ENERGY
                continue
            if obj == "resources":
                flags |= cls.RESOURCES
                continue
            raise RuntimeError(f"Unexpected objective {obj}")
        return flags


class GeneticMapper(object):
    """Generates a full mapping by using genetic algorithms."""

    def __init__(
        self,
        graph,
        platform,
        trace,
        representation,
        initials="random",
        objectives=["exec_time"],
        pop_size=10,
        num_gens=5,
        mutpb=0.5,
        cxpb=0.35,
        tournsize=4,
        mupluslambda=True,
        crossover_rate=1,
        radius=2.0,
        random_seed=42,
        record_statistics=True,
        dump_cache=False,
        chunk_size=10,
        progress=False,
        parallel=True,
        jobs=4,
    ):
        """Generates a partial mapping for a given platform and dataflow application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param initials: what initial population to use (e.g. random)
        :type initials: string
        :param objectives: Optimization objectives
        :type objectives: list of strings
        :param pop_size: Population size
        :type pop_size: int
        :param num_gens: Number of generations
        :type num_gens: int
        :param mutpb: Probability of mutation
        :type mutpb: float
        :param cxpb: Crossover probability
        :type cxpb: float
        :param tournsize: Size of tournament for selection
        :type tournsize: int
        :param mupluslambda: Use mu+lambda algorithm? if False: mu,lambda
        :type mupluslambda: bool
        :param crossover_rate: The number of crossovers in the crossover operator
        :type crossover_rate: int
        :param radius: The radius for searching mutations
        :type radius: float
        :param random_seed: A random seed for the RNG
        :type random_seed: int
        :param record_statistics: Record statistics on mappings evaluated?
        :type record_statistics: bool
        :param dump_cache: Dump the mapping cache?
        :type dump_cache: bool
        :param chunk_size: Size of chunks for parallel simulation
        :type chunk_size: int
        :param progress: Display simulation progress visually?
        :type progress: bool
        :param parallel: Execute simulations in parallel?
        :type parallel: bool
        :param jobs: Number of jobs for parallel simulation
        :type jobs: int
        """
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.full_mapper = True  # flag indicating the mapper type
        self.graph = graph
        self.platform = platform
        self.crossover_rate = crossover_rate
        self.objectives = Objectives.from_string_list(objectives)
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.mutpb = mutpb
        self.cxpb = cxpb
        self.mupluslambda = mupluslambda
        self.dump_cache = dump_cache
        self.radius = radius
        self.progress = progress

        objective_resources = Objectives.RESOURCES in self.objectives
        self.random_mapper = RandomPartialMapper(
            self.graph, self.platform, resources_first=objective_resources
        )

        if Objectives.ENERGY in self.objectives:
            if not self.platform.has_power_model():
                log.warning(
                    "The platform does not have a power model, excluding "
                    "energy consumption from the objectives."
                )
                self.objectives ^= Objectives.ENERGY

        if self.objectives == Objectives.NONE:
            raise RuntimeError(
                "Trying to initalize genetic algorithm without objectives"
            )

        if self.crossover_rate > len(self.graph.processes()):
            log.error(
                "Crossover rate cannot be higher than number of processes "
                "in application"
            )
            raise RuntimeError("Invalid crossover rate")

        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not issubclass(type(type(representation)), MappingRepresentation):
            representation = instantiate(representation, graph, platform)
        self.representation = representation
        self.simulation_manager = SimulationManager(
            self.representation,
            trace,
            jobs,
            parallel,
            progress,
            chunk_size,
            record_statistics,
        )

        if "FitnessMin" not in deap.creator.__dict__:
            num_params = 0
            if Objectives.EXEC_TIME in self.objectives:
                num_params += 1
            if Objectives.ENERGY in self.objectives:
                num_params += 1
            if Objectives.RESOURCES in self.objectives:
                num_params += len(self.platform.get_processor_types())
            # this will weigh a milisecond as equivalent to an additional core
            # todo: add a general parameter for controlling weights
            deap.creator.create(
                "FitnessMin", deap.base.Fitness, weights=num_params * (-1.0,)
            )

        if "Individual" not in deap.creator.__dict__:
            deap.creator.create(
                "Individual", list, fitness=deap.creator.FitnessMin
            )

        toolbox = deap.base.Toolbox()
        toolbox.register("attribute", random.random)
        toolbox.register("mapping", self.random_mapping)
        toolbox.register(
            "individual",
            deap.tools.initIterate,
            deap.creator.Individual,
            toolbox.mapping,
        )
        toolbox.register(
            "population", deap.tools.initRepeat, list, toolbox.individual
        )
        toolbox.register("mate", self.mapping_crossover)
        toolbox.register("mutate", self.mapping_mutation)
        toolbox.register("evaluate", self.evaluate_mapping)
        toolbox.register(
            "select", deap.tools.selTournament, tournsize=tournsize
        )

        self.evolutionary_toolbox = toolbox
        self.hof = (
            deap.tools.ParetoFront()
        )  # todo: we could add symmetry comparison (or other similarity) here
        stats = deap.tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        self.evolutionary_stats = stats

        if initials == "random":
            self.population = toolbox.population(n=self.pop_size)
        else:
            log.error("Initials not supported yet")
            raise RuntimeError("GeneticMapper: Initials not supported")
            # toolbox.register("individual_guess", self.initIndividual, creator.Individual)
            # toolbox.register("population_guess", self.initPopulation, list, toolbox.individual_guess, initials,pop_size)
            # population = toolbox.population_guess()

    def evaluate_mapping(self, mapping):
        result = []
        simres = self.simulation_manager.simulate([list(mapping)])[0]
        if Objectives.EXEC_TIME in self.objectives:
            result.append(simres.exec_time)
        if Objectives.ENERGY in self.objectives:
            result.append(simres.dynamic_energy)
        if Objectives.RESOURCES in self.objectives:
            mapping_obj = self.representation.fromRepresentation(list(mapping))
            resource_dict = mapping_obj.to_resourceDict()
            for core_type in resource_dict:
                result.append(resource_dict[core_type])
        return tuple(result)

    def random_mapping(self):
        mapping = self.random_mapper.generate_mapping()
        if (
            hasattr(self.representation, "canonical_operations")
            and not self.representation.canonical_operations
        ):
            as_rep = self.representation.toRepresentationNoncanonical(mapping)
        else:
            as_rep = self.representation.toRepresentation(mapping)
        return list(as_rep)

    def mapping_crossover(self, m1, m2):
        return self.representation._crossover(m1, m2, self.crossover_rate)

    def mapping_mutation(self, mapping):
        # m_obj = self.representation.fromRepresentation(list((mapping)))
        radius = self.radius
        while 1:
            new_mappings = self.representation._uniformFromBall(
                mapping, radius, 20
            )
            for m in new_mappings:
                if list(m) != list(mapping):
                    for i in range(len(mapping)):
                        # we do this since mapping is a DEAP Individual data structure
                        mapping[i] = m[i]
                    return (mapping,)
            radius *= 1.1
            if radius > 10000 * self.radius:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")

    def run_genetic_algorithm(self):
        toolbox = self.evolutionary_toolbox
        stats = self.evolutionary_stats
        hof = self.hof
        pop_size = self.pop_size
        num_gens = self.num_gens
        cxpb = self.cxpb
        mutpb = self.mutpb
        population = self.population

        if self.mupluslambda:
            population, logbook = deap.algorithms.eaMuPlusLambda(
                population,
                toolbox,
                mu=pop_size,
                lambda_=3 * pop_size,
                cxpb=cxpb,
                mutpb=mutpb,
                ngen=num_gens,
                stats=stats,
                halloffame=hof,
                verbose=self.progress,
            )
            log.info(logbook.stream)
        else:
            population, logbook = deap.algorithms.eaMuCommaLambda(
                population,
                toolbox,
                mu=pop_size,
                lambda_=3 * pop_size,
                cxpb=cxpb,
                mutpb=mutpb,
                ngen=num_gens,
                stats=stats,
                halloffame=hof,
                verbose=self.progress,
            )
            log.info(logbook.stream)

        return population, logbook, hof

    def generate_mapping(self):
        """Generates a full mapping using a genetic algorithm"""
        _, logbook, hof = self.run_genetic_algorithm()
        mapping = hof[0]
        self.simulation_manager.statistics.log_statistics()
        with open("evolutionary_logbook.txt", "w") as f:
            f.write(str(logbook))
        result = self.representation.fromRepresentation(np.array(mapping))
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump("mapping_cache.csv")
        self.cleanup()
        return result

    def generate_pareto_front(self):
        """Generates a pareto front of (full) mappings using a genetic algorithm
        the input parameters determine the criteria with which the pareto
        front is going to be built.
        """
        _, logbook, hof = self.run_genetic_algorithm()
        results = []
        self.simulation_manager.statistics.log_statistics()
        with open("evolutionary_logbook.pickle", "wb") as f:
            pickle.dump(logbook, f)
        for mapping in hof:
            mapping_object = self.representation.fromRepresentation(
                np.array(mapping)
            )
            self.simulation_manager.append_mapping_metadata(mapping_object)
            results.append(mapping_object)
        self.simulation_manager.statistics.to_file()
        if self.dump_cache:
            self.simulation_manager.dump("mapping_cache.csv")
        self.cleanup()
        return results

    def cleanup(self):
        log.info("cleaning up")
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

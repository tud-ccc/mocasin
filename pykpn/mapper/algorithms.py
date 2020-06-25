# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Gerald Hempel, Felix Teweleit

import deap
import hydra
import random
import numpy as np
import pickle
import copy

from pykpn.util import logging
from pykpn.representations.representations import RepresentationType
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.utils import MappingCache, DerivedPrimitive
from pykpn.common.mapping import Mapping, ProcessMappingInfo, ChannelMappingInfo, SchedulerMappingInfo
from pykpn.common.trace import TraceGraph
from pykpn.mapper.utils import Statistics
from collections import Counter

from deap import creator, tools, base, algorithms

log = logging.getLogger(__name__)

class GeneticFullMapper(object):
    """Generates a full mapping by using genetic algorithms.
    """
    def __init__(self, kpn,platform, config):
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
        self.kpn = kpn
        self.platform = platform
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn, self.platform, config, seed=None)
        self.crossover_rate = self.config['crossover_rate']

        if self.crossover_rate > len(self.kpn.processes()):
            log.error("Crossover rate cannot be higher than number of processes in application")
            raise RuntimeError("Invalid crossover rate")

        rep_type_str = config['representation']

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation
        self.mapping_cache = MappingCache(self.representation,config)

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

        if config['initials'] == 'random':
            self.population = toolbox.population(n=self.config['pop_size'])
        else:
            log.error("Initials not supported yet")
            raise RuntimeError('GeneticFullMapper: Initials not supported')
            #toolbox.register("individual_guess", self.initIndividual, creator.Individual)
            #toolbox.register("population_guess", self.initPopulation, list, toolbox.individual_guess, initials,pop_size)
            #population = toolbox.population_guess()

    def evaluate_mapping(self,mapping):
        #wrapper to make it into a 1-tuple because DEAP needs that
        return self.mapping_cache.evaluate_mapping(mapping),

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
                        #we do this since mapping is a DEAP Individual data structure
                        mapping[i] = m[i]
                    return mapping,
            radius *= 1.1
            if radius > 10000 * self.config['radius']:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")


    def run_genetic_algorithm(self):
        toolbox = self.evolutionary_toolbox
        stats = self.evolutionary_stats
        hof = self.hof
        pop_size = self.config['pop_size']
        num_gens = self.config['num_gens']
        cxpb = self.config['cxpb']
        mutpb = self.config['mutpb']

        population = self.population

        if self.config['mupluslambda']:
            population, logbook = deap.algorithms.eaMuPlusLambda(population, toolbox, mu=pop_size, lambda_=3*pop_size,
                                                                 cxpb=cxpb, mutpb=mutpb, ngen=num_gens, stats=stats,
                                                                 halloffame=hof, verbose=False)
            log.info(logbook.stream)
        else:
            population, logbook = deap.algorithms.eaMuCommaLambda(population, toolbox, mu=pop_size, lambda_=3*pop_size,
                                                                  cxpb=cxpb, mutpb=mutpb, ngen=num_gens, stats=stats,
                                                                  halloffame=hof, verbose=False)
            log.info(logbook.stream)

        return population,logbook,hof

    def generate_mapping(self):
        """ Generates a full mapping using a genetic algorithm
        """
        _,logbook,hof = self.run_genetic_algorithm()
        mapping = hof[0]
        self.mapping_cache.statistics.log_statistics()
        with open('evolutionary_logbook.pickle','wb') as f:
            pickle.dump(logbook,f)
        result = self.representation.fromRepresentation(np.array(mapping))
        self.mapping_cache.statistics.to_file()
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

class GroupBasedMapper:
    """Exposed interface of the mapper implementing the group based mapping algorithm.

    This class resembles the interface for the group based mapper that should be used
    by any user or application. The concrete implementation of the mapper is hidden an
    attribute of this class to enhance readability and handle the resetting of the
    used trace generator between each method call to the mapper. Doing it this way,
    the user can use the same trace generator for the whole appliocation and does not
    have to create multiple instances.
    """
    def __init__(self, kpn, platform, config, bx_m=1, bx_p=0.95, by_m=0.5, by_p=0.75):
        """Creates a new instance of a group based full mapper.

        Args:
        kpn (pykpn.common.kpn.KpnGraph): The kpn graph of the application that should be mapped.
        platform (pykpn.common.platform.Platform): The platform to which the application should be
            mapped.
        trace_generator (pykpn.common.trace.TraceGenerator): The generator object for the trace of
            the application that should be mapped.
        bx_m (float): A parameter for the occupation measurement of memory. The default value is adopted
            from the paper, introducing this algorithm.
        bx_m (float): A parameter for the occupation measurement of memory. The default value is adopted
            from the paper, introducing this algorithm.
        by_m (float): A parameter for the occupation measurement of memory. The default value is adopted
            from the paper, introducing this algorithm.
        by_p (float): A parameter for the occupation measurement of processors. The default value is adopted
            from the paper, introducing this algorithm.
        critical_kpn_elements ([str]): A list of the kpn elements on the critical path through the trace
            graph of the application. Is used to prioritize the assignment of different kpn elements.
        """
        trace_generator = hydra.utils.instantiate(config['trace'])

        self.statistics = Statistics(log, len(kpn.processes()), config['record_statistics'])

        self.trace_generator = trace_generator

        self.trace_generator.reset()

        self._internal_mapper = _GroupBasedMapper(kpn, platform, trace_generator, bx_m, bx_p, by_m, by_p)

        self.trace_generator.reset()

    def generate_mapping(self):
        self.trace_generator.reset()

        #performs the main algorithm were groups of hw resources are assigned to kpn elements
        self._internal_mapper.determine_group_mapping()

        #maps the processes of the kpn graph to specific resources of the pre assigned hw groups
        self._internal_mapper.map_processes()

        #maps the channels of the kpn graph to specific resources of the pre assigned hw groups
        #respecting the already mapped kpn processes
        self._internal_mapper.map_channels()

        #maps the schedulers of the platform according to a simple heuristic
        self._internal_mapper.map_schedulers()

        self.trace_generator.reset()

        self.statistics.mapping_evaluated(0)

        self.statistics.to_file()

        return self._internal_mapper.get_mapping()

class GroupBasedMapper_Testing(GroupBasedMapper):
    """This class implements the same functionality as the normal gbm_mapper, it just drops the hydra based
    initialisation and statistics feature in order to be accessible for unit tests.
    """
    def __init__(self, kpn, platform, trace_generator, ):
        self.trace_generator = trace_generator

        self.trace_generator.reset()

        self._internal_mapper = _GroupBasedMapper(kpn, platform, trace_generator, bx_m=1, bx_p=0.95, by_m=0.5, by_p=0.75)

        self.trace_generator.reset()

    def generate_mapping(self):
        self.trace_generator.reset()

        self._internal_mapper.determine_group_mapping()

        self._internal_mapper.map_processes()

        self._internal_mapper.map_channels()

        self._internal_mapper.map_schedulers()

        self.trace_generator.reset()

        return self._internal_mapper.get_mapping()

class _GroupBasedMapper:
    """A full mapper, implementing a joint mapping algorithm for processes and channels.

    The group based mapper generates a complete mapping for a given combination of platform
    and kpn graph. Processes and channels are first mapped to groups of hardware resources, with
    no specific prioritization. After the assignment of the most important kpn elements a mapping
    object is generated.

    Attributes:
        kpn (pykpn.commpn.kpn.KpnGraph): The kpn graph for which the mapping should be generated.
        platform (pykpn.common.platform.Platform): The platform on which the kpn graph should be
            mapped.
        processors (dict{str : [pykpn.common.platform.Processor]}): The processors of the platform,
            ordered into groups, where all processors of the some group exhibit the same timing
            characteristic.
        primitives (dict{int : pykpn.mapper.gbm_fullmapper.DerivedPrimtive]}): The DerivedPrimitives,
            derived from the primitives of the platform. Ordered into groups where primitives in the
            same group exhibit the same timing characteristic.
        process_mapping ({str : [str]}): A dictionary that holds the name of the existing processes as
            keys and the identifiers of all currently assigned hardware groups as values.
        channel_mapping ({str : [int]}): A dictionary, that holds the names of existing channels as
            keys and the identifiers of all currently assigned hardware groups as values.
        trace_graph (pykpn.common.trace.TraceGraph): The trace graph of the application. The graph is
            used to perform some dependency analysis between the applications tasks and channels.
        bx_m (float): A parameter for the occupation measurement of memory.
        bx_p (float): A parameter for the occupation measurement of processors.
        by_m (float):A parameter for the occupation measurement of memory.
        by_p (float):A parameter for the occupation measurement of processors.
    """


    def __init__(self, kpn, platform, trace_generator, bx_m=1, bx_p=0.95, by_m=0.5, by_p=0.75):
        """Creates a new instance of a group based full mapper.

        Args:
        kpn (pykpn.common.kpn.KpnGraph): The kpn graph of the application that should be mapped.
        platform (pykpn.common.platform.Platform): The platform to which the application should be
            mapped.
        trace_generator (pykpn.common.trace.TraceGenerator): The generator object for the trace of
            the application that should be mapped.
        bx_m (float): A parameter for the occupation measurement of memory. The default value is adopted
            from the paper, introducing this algorithm.
        bx_m (float): A parameter for the occupation measurement of memory. The default value is adopted
            from the paper, introducing this algorithm.
        by_m (float): A parameter for the occupation measurement of memory. The default value is adopted
            from the paper, introducing this algorithm.
        by_p (float): A parameter for the occupation measurement of processors. The default value is adopted
            from the paper, introducing this algorithm.
        critical_kpn_elements ([str]): A list of the kpn elements on the critical path through the trace
            graph of the application. Is used to prioritize the assignment of different kpn elements.
        """
        self.kpn = kpn
        self.platform = platform

        self.processors = {}
        self.primitives = {}

        self.process_mapping = {}
        self.channel_mapping = {}

        self.trace_generator = trace_generator
        self.trace_graph = None

        self.mapping = Mapping(self.kpn, self.platform)
        self.processes_to_map = self.kpn.process_names()

        self.bx_m = bx_m
        self.bx_p = bx_p
        self.by_m = by_m
        self.by_p = by_p

        #order the processors into resource groups
        self.processors = self.create_processor_groups(self.platform.processors())

        #order derived primitives into primitive groups
        self.drvd_primitives, self.primitives = self.create_primitive_groups(self.platform.primitives())

        #create initial process mapping
        #processor can be mapped to every processor group
        for process in self.kpn.processes():
            self.process_mapping.update( {process.name : list(self.processors.keys())} )

        #create initial channel mapping
        #channel can be mapped to every primitive group
        for channel in self.kpn.channels():
            self.channel_mapping.update( {channel.name : list(self.primitives.keys())} )

        #generate trace graph, initial mappings are handed in to set edge weights
        self.trace_graph = TraceGraph(kpn,
                                      trace_generator,
                                      self.process_mapping,
                                      self.channel_mapping,
                                      self.processors,
                                      self.primitives)

        #determine all kpn elements on the critical path through the critical path
        self.critical_kpn_elements, _, _ = self.trace_graph.determine_critical_path_elements()
        self.trace_generator.reset()


    def determine_group_mapping(self):
        while self.can_make_proposal():
            proposal = self.make_proposal()

            if not self._assess(proposal):
                proposal_key = list(proposal.keys())[0]

                if proposal_key in self.process_mapping:
                    proposal_value = list(self.process_mapping[proposal_key])
                    proposal_value.remove(proposal[proposal_key][0])

                if proposal_key in self.channel_mapping:
                    proposal_value = list(self.channel_mapping[proposal_key])
                    proposal_value.remove(proposal[proposal_key][0])

                if not self._assess({proposal_key : proposal_value}, False):
                    raise RuntimeError("Critical error during mapping generation!")


    def map_processes(self):
        #holds tuples containing groups of processes that have to be
        #mapped together alongside their priority
        process_priorities = []

        #holds for each processor to which at least one process has been
        #assigned the accumulated processing time
        processor_usage = {}

        induced_groups = self._search_induced_groups()


        for group in induced_groups:
            priority = len(group) / len(self.process_mapping[group[0]])
            process_priorities.append((priority, group))


        for process_name in self.processes_to_map:
            priority = 1 / (len(self.process_mapping[process_name]))
            process_priorities.append( (priority, [process_name]) )

        process_priorities.sort(reverse=True)

        #map all processes
        while process_priorities:
            #determine the process group with the highest priority
            map_next = process_priorities.pop(0)

            #in case an induced group have to be mapped
            chosen_processor = None

            for process in map_next[1]:

                #find the processor in the assignment set, which provides
                #the best timing characteristic for the process
                mapping_candidate = (float("inf"), None, None)

                for cluster_id in self.process_mapping[process]:

                    for processor in self.processors[cluster_id]:

                        if chosen_processor is not None and processor != chosen_processor:
                            continue

                        new_timing = float("inf")
                        if processor not in processor_usage:
                            new_timing = self._accumulated_process_time(process, processor.type)
                        else:
                            new_timing = processor_usage[processor] + \
                                         self._accumulated_process_time(process, processor.type)



                        if not self._is_suitable(process, processor) and chosen_processor is None:
                            continue

                        if new_timing < mapping_candidate[0]:
                            mapping_candidate = (new_timing, processor)

                chosen_processor = mapping_candidate[1]
                scheduler = list(self.platform.find_scheduler_for_processor(mapping_candidate[1]))[0]
                affinity = mapping_candidate[1]
                priority = 0
                info = ProcessMappingInfo(scheduler, affinity, priority)

                self.mapping.add_process_info(self.kpn.find_process(process), info)

                processor_usage.update( {mapping_candidate[1] : mapping_candidate[0]} )


    def map_channels(self):
        #map all channels
        channels = list(self.kpn.channels())

        while channels:
            map_next = channels.pop()
            prim_group_ids = list(self.channel_mapping[map_next.name])
            prim_group_ids.sort()
            candidate = None
            suitable = False

            for group_id in prim_group_ids:

                for prim in self.primitives[group_id]:

                    if prim.source == self.mapping.affinity(map_next.source):
                        candidate = prim.ref_primitive
                        suitable = True
                        for sink in map_next.sinks:
                            if self.mapping.affinity(sink) not in candidate.consumers:
                                suitable = False
                                candidate = None
                                break

                        if suitable:
                            break

                if suitable:
                    break

            if candidate is None:
                raise RuntimeError("Can not find a suitable channel mapping for existing processor mapping")

            capacity = 16
            info = ChannelMappingInfo(candidate, capacity)
            self.mapping.add_channel_info(map_next, info)


    def map_schedulers(self):
        #map all schedulers
        for scheduler in self.platform.schedulers():
            info = SchedulerMappingInfo(scheduler.policies[0], None)
            self.mapping.add_scheduler_info(scheduler, info)


    def get_mapping(self):
        return self.mapping

    def create_primitive_groups(self, primitives):
        derived_primitives = []

        for primitive in primitives:

            for source_proc in primitive.producers:

                for sink_proc in primitive.consumers:
                    derived_primitives.append(DerivedPrimitive(source_proc,
                                                               sink_proc,
                                                               primitive))

        return derived_primitives, self.group_drvd_primitives(derived_primitives)

    def group_drvd_primitives(self, drvd_prims):
        prim_groups = {}

        for prim in drvd_prims:

            if prim.cost not in prim_groups:
                prim_groups.update({prim.cost : [prim]})
            else:
                prim_groups[prim.cost].append(prim)

        return prim_groups


    def create_processor_groups(self, processors):
        proc_groups = {}

        for processor in processors:

            if not processor.type in proc_groups:
                proc_groups.update( {processor.type : [processor]} )
            else:
                proc_groups[processor.type].append(processor)

        return proc_groups


    def can_make_proposal(self):
        self.critical_kpn_elements, _, _ = self.trace_graph.determine_critical_path_elements()

        for element in self.critical_kpn_elements:

            if (element in self.process_mapping and
                    len(self.process_mapping[element]) > 1):
                return True

            if (element in self.channel_mapping and
                    len(self.channel_mapping[element]) > 1):
                return True

        return False


    def make_proposal(self):
        self.critical_kpn_elements, timing, _ = self.trace_graph.determine_critical_path_elements()
        new_element_mapping = None

        for element in self.critical_kpn_elements:

            if element in self.process_mapping and len(self.process_mapping[element]) > 1:

                for group_id in self.process_mapping[element]:
                    new_timing = self.trace_graph.change_element_mapping(element,
                                                                         {element : [group_id]},
                                                                         self.processors)

                    if new_timing <= timing:
                        timing = new_timing
                        new_element_mapping = {element : [group_id]}

            if element in self.channel_mapping and len(self.channel_mapping[element]) > 1:

                for group_id in self.channel_mapping[element]:
                    new_timing = self.trace_graph.change_element_mapping(element,
                                                                         {element : [group_id]},
                                                                         self.primitives)

                    if new_timing <= timing:
                        timing = new_timing
                        new_element_mapping = {element : [group_id]}

        if new_element_mapping is not None:
            return new_element_mapping
        else:
            raise RuntimeError('Can not make new proposal for unknown reason!')


    def _assess(self, proposal, load_control=True):
        tmp_cpy_processes = copy.copy(self.process_mapping)
        tmp_cpy_channels = copy.copy(self.channel_mapping)

        self._propagate(proposal)

        error_in_element = False

        for assigned_groups in self.process_mapping.values():

            if not assigned_groups:
                error_in_element = True
                break

        for assigned_groups in self.channel_mapping.values():

            if not assigned_groups:
                error_in_element = True
                break

        if not self._load_control(proposal) and load_control:
            error_in_element = True

        if not error_in_element:
            #if proposal succeeds, all propagated changes are conveyed
            #to the trace graph
            for process in self.process_mapping:
                self.trace_graph.change_element_mapping(process,
                                                        self.process_mapping,
                                                        self.processors,
                                                        True)

            for channel in self.channel_mapping:
                self.trace_graph.change_element_mapping(channel,
                                                        self.channel_mapping,
                                                        self.primitives,
                                                        True)

            return True
        else:
            self.process_mapping = tmp_cpy_processes
            self.channel_mapping = tmp_cpy_channels

        return False


    def _propagate(self, proposal):
        """Add doc here
        """
        for kpn_element in proposal:

            if kpn_element in self.process_mapping:
                #apply the proposal
                self.process_mapping.update(proposal)

                #find all incoming and outgoing channels
                in_channels = []
                out_channels = []

                for channel in self.kpn.channels():

                    if kpn_element == channel.source.name:
                        out_channels.append(channel.name)

                    for process in channel.sinks:

                        if kpn_element == process.name:
                            in_channels.append(channel.name)

                #find all primitives capable of communicate between processors of the
                #assigned hardware groups for incoming and outgoing channels
                in_prims = []
                out_prims = []

                for proc_class in proposal[kpn_element]:

                    for drvd_prim in self.drvd_primitives:

                        if drvd_prim.source in self.processors[proc_class]:
                            out_prims.append(drvd_prim)

                        if drvd_prim.sink in self.processors[proc_class]:
                            in_prims.append(drvd_prim)

                #transfer these primitives into new hardware groups
                #also it is checked if the each primitive group has the
                #same amount of primitives in it. Otherwise it is dropped
                in_prim_groups = self.group_drvd_primitives(in_prims)

                out_prim_groups = self.group_drvd_primitives(out_prims)

                #propagate in_prims to associated incoming channels
                for channel in in_channels:

                    if not Counter(self.channel_mapping[channel]) == Counter(list(in_prim_groups.keys())):

                        #with the following snippet we assure, that the assignment set
                        #of the incoming channel only can be reduced.
                        to_update = []
                        for prim_group in in_prim_groups:
                            if prim_group in self.channel_mapping[channel]:
                                to_update.append(prim_group)

                        self._propagate({channel : to_update})

                #propagate out_prims to associated outgoing channels
                for channel in out_channels:

                    if not Counter(self.channel_mapping[channel]) == Counter(list(out_prim_groups.keys())):

                        #with the following snippet we assure, that the assignment set
                        #of the outgoing channel only can be reduced.
                        to_update = []
                        for prim_group in out_prim_groups:
                            if prim_group in self.channel_mapping[channel]:
                                to_update.append(prim_group)

                        self._propagate({channel : to_update})

            if kpn_element in self.channel_mapping:
                #case a new mapping for a KPN channel is proposed

                #apply the proposal
                self.channel_mapping.update(proposal)

                #find processes communicating via this channel
                source_processes = []
                sink_processes = []

                for process in self.kpn.processes():

                    for channel in process.incoming_channels:

                        if kpn_element == channel.name:
                            sink_processes.append(process.name)

                    for channel in process.outgoing_channels:

                        if kpn_element == channel.name:
                            source_processes.append(process.name)

                #find all processors which can communicate via
                #the proposed primitives
                source_processors = []
                sink_processors = []

                for prim_class in proposal[kpn_element]:

                    for prim in self.primitives[prim_class]:

                        if not prim.source in source_processors:
                            source_processors.append(prim.source)

                        if not prim.sink in sink_processors:
                            sink_processors.append(prim.sink)

                #transfer these processors into new hardware groups
                source_processor_groups = self.create_processor_groups(source_processors)
                sink_processor_groups = self.create_processor_groups(sink_processors)

                #propagate source processors to associated source processes
                for process in source_processes:
                    #with the following snippet we assure, that the assignment set
                    #of the source processor only can be reduced.
                    to_update = []
                    for processor_group in source_processor_groups:
                        if processor_group in self.process_mapping[process]:
                            to_update.append(processor_group)

                    if not Counter(self.process_mapping[process]) == Counter(to_update):
                        self._propagate({process : to_update})

                #propagate sink processor to associated sink processes
                for process in sink_processes:
                    #with the following snippet we assure, that the assignment set
                    #of the sink processor only can be reduced.
                    to_update = []
                    for processor_group in sink_processor_groups:
                        if processor_group in self.process_mapping[process]:
                            to_update.append(processor_group)

                    if not Counter(self.process_mapping[process]) == Counter(to_update):
                        self._propagate({process : to_update})


    def _load_control(self, proposal):
        #load control only ensures that the utilization for a group
        #stays below a threshold if the newly proposed hardware groups
        #are reduced TO one group. Not BY one group.
        if len(list(proposal.values())[0]) > 1:
            return True

        threshold = 0
        utilization = 0

        for kpn_element in proposal:

            if kpn_element in self.process_mapping:
                #case a new mapping for a KPN process is proposed

                #determine size of hardware group
                group_size = len(self.processors[proposal[kpn_element][0]])

                #determine size of assigned processes
                assigned_elems = []

                for process in self.process_mapping:

                    if proposal[kpn_element][0] in self.process_mapping[process]:
                        assigned_elems.append(process)


                if len(assigned_elems) >= group_size:
                    #calculate threshold
                    threshold = (self.bx_p * len(assigned_elems)) / (len(assigned_elems) + group_size
                                                                     * ((self.bx_p/self.by_p) - 1))

                    makespan = self._application_makespan()
                    process_time = self._accumulated_process_time(kpn_element, proposal[kpn_element][0])

                    #calculate utilization
                    utilization = process_time / (group_size * makespan)
                else:
                    return True

            if kpn_element in self.channel_mapping:
                #case a new mapping for a KPN channel is proposed

                assigned_elems = 0

                for assignment in self.channel_mapping.values():
                    if proposal[kpn_element][0] in assignment:
                        assigned_elems += 1

                cr_in_group = []

                #counting amount of communication resources used by the
                #assigned primitive group
                for primitive in self.primitives[proposal[kpn_element][0]]:

                    for phase_list in primitive.ref_primitive.consume_phases.values():

                        for phase in phase_list:

                            for comm_resource in phase.resources:

                                if comm_resource.name not in cr_in_group:
                                    cr_in_group.append(comm_resource.name)

                    for phase_list in primitive.ref_primitive.produce_phases.values():

                        for phase in phase_list:

                            for comm_resource in phase.resources:

                                if not comm_resource.name in cr_in_group:
                                    cr_in_group.append(comm_resource.name)

                group_size = len(cr_in_group)

                threshold = (self.bx_m * assigned_elems) / (assigned_elems + group_size * ((self.bx_m/self.by_m) - 1))

                channels_of_group = []

                for channel in self.channel_mapping:

                    if (proposal[kpn_element][0] in self.channel_mapping[channel] and
                            len(self.channel_mapping[channel]) == 1):
                        channels_of_group.append(channel)

                utilization = len(channels_of_group) / group_size

        if utilization >= threshold:
            return False

        return True

    def _search_induced_groups(self):
        induced_groups = []
        for channel_mapping in self.channel_mapping.items():
            map_together = []
            induces_group = True

            for prim_group_id in channel_mapping[1]:

                for primitive in self.primitives[prim_group_id]:

                    if not primitive.source == primitive.sink:
                        induces_group = False
                        break
            if induces_group:
                channel = self.kpn.find_channel(channel_mapping[0])
                map_together.append(channel.source.name)

                if channel.source.name in self.processes_to_map:
                    self.processes_to_map.remove(channel.source.name)

                for sink in channel.sinks:
                    map_together.append(sink.name)

                    if sink.name in self.processes_to_map:
                        self.processes_to_map.remove(sink.name)

                induced_groups.append(map_together)

        return self._merge_groups(induced_groups)


    def _select_node(self, ready_set):
        #In case a specific selection heuristic should be implemented
        return ready_set.pop(0)


    def _application_makespan(self):
        current_makespan = 0

        #start node of graph is always scheduled
        scheduled_set = ['V_s']
        vertices_set = list(self.trace_graph.nodes)
        ready_set = []

        for node in vertices_set:

            if (all(pred in scheduled_set for pred in list(self.trace_graph.predecessors(node))) and
                    not node == 'V_s'):
                ready_set.append(node)

        while Counter(scheduled_set) != Counter(vertices_set):
            next_node = self._select_node(ready_set)
            scheduled_set.append(next_node)

            pessimistic_time = 0
            for edge in self.trace_graph.in_edges(next_node):
                if self.trace_graph.edges[edge[0], next_node]['weight'] > pessimistic_time:
                    pessimistic_time = self.trace_graph.edges[edge[0], next_node]['weight']

            current_makespan += pessimistic_time

            for node in self.trace_graph.successors(next_node):
                if all(pred in scheduled_set for pred in list(self.trace_graph.predecessors(node))):
                    ready_set.append(node)

        return current_makespan


    def _accumulated_process_time(self, kpn_process, processor_class):
        self.trace_generator.reset()

        accumulated_time = 0
        processor = self.processors[processor_class][0]

        trace_segment = self.trace_generator.next_segment(self.kpn.name+"."+kpn_process, processor.type)

        while not trace_segment.terminate:

            if trace_segment.processing_cycles:
                accumulated_time += processor.ticks(trace_segment.processing_cycles)

            trace_segment = self.trace_generator.next_segment(self.kpn.name+"."+kpn_process, processor.type)

        return accumulated_time


    def _merge_groups(self, group):
        merged_groups = []

        while group:
            check_next = group.pop()
            tmp_list = list(group)
            changed = False

            for element in tmp_list:
                if any(identifier in element for identifier in check_next):
                    for identifier in element:
                        if identifier not in check_next:
                            check_next.append(identifier)
                            changed = True
                    group.remove(element)
            if not changed:
                merged_groups.append(check_next)
            else:
                group.append(check_next)

        return merged_groups

    def _is_suitable(self, process, processor):
        in_channels = self.kpn.find_process(process).incoming_channels
        out_channels = self.kpn.find_process(process).outgoing_channels

        available_in_prims = []

        for channel in in_channels:

            for prim_group_id in self.channel_mapping[channel.name]:

                for prim in self.primitives[prim_group_id]:
                    available_in_prims.append(prim)

        available_out_prims = []

        for channel in out_channels:

            for prim_group_id in self.channel_mapping[channel.name]:

                for prim in self.primitives[prim_group_id]:
                    available_out_prims.append(prim)

        suitable_in = False

        if not available_in_prims:
            suitable_in = True

        for prim in available_in_prims:

            if processor == prim.sink:
                suitable_in = True

        suitable_out = False

        if not available_out_prims:
            suitable_out = True

        for prim in available_out_prims:

            if processor == prim.source:
                suitable_out = True

        return suitable_in and suitable_out

class GradientDescentFullMapper(object):
    """Generates a full mapping by using a gradient descent on the mapping space.
    """
    def __init__(self, kpn,platform,config):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type config: OmniConf
        """
        random.seed(config['random_seed'])
        np.random.seed(config['random_seed'])
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = kpn
        self.platform = platform
        self.num_PEs = len(platform.processors())
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config,seed=None)
        self.gd_iterations = config['gd_iterations']
        self.stepsize = config['stepsize']
        self.statistics = Statistics(log, len(self.kpn.processes()), config['record_statistics'])
        rep_type_str = config['representation']

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation
        self.mapping_cache = MappingCache(representation,config)

    def generate_mapping(self):
        """ Generates a full mapping using gradient descent
        """
        mapping_obj = self.random_mapper.generate_mapping()
        mapping = self.representation.toRepresentation(mapping_obj)

        self.dim = len(mapping)
        cur_exec_time = self.mapping_cache.evaluate_mapping(mapping)
        self.best_mapping = mapping
        self.best_exec_time = cur_exec_time

        for _ in range(self.gd_iterations):
            grad = self.calculate_gradient(mapping,cur_exec_time)

            if np.allclose(grad,np.zeros(self.dim)): #found local minimum
                break
            mapping = mapping + (self.stepsize / self.best_exec_time) * (-grad)
            mapping = self.representation.approximate(np.array(mapping))

            cur_exec_time = self.mapping_cache.evaluate_mapping(mapping)

            if cur_exec_time < self.best_exec_time:
                self.best_exec_time = cur_exec_time
                self.best_mapping = mapping

        self.best_mapping = np.array(self.representation.approximate(np.array(self.best_mapping)))
        self.statistics.log_statistics()
        self.statistics.to_file()

        return self.representation.fromRepresentation(self.best_mapping)


    def calculate_gradient(self,mapping,cur_exec_time):
        grad = np.zeros(self.dim)
        for i in range(self.dim):
            evec = np.zeros(self.dim)
            if mapping[i] == 0:
                evec[i] = 1.
                exec_time = self.mapping_cache.evaluate_mapping(mapping + evec)
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                gr = exec_time - cur_exec_time
                grad[i] = max(gr, 0)  # can go below 0 here
            elif mapping[i] == self.num_PEs - 1:
                evec[i] = -1.
                exec_time = self.mapping_cache.evaluate_mapping(mapping + evec)
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                gr = cur_exec_time - exec_time  # because of the -h in the denominator of the difference quotient
                grad[i] = min(gr, 0)  # can't go above self.num_PEs-1 here

            else:
                evec[i] = 1.
                exec_time = self.mapping_cache.evaluate_mapping(mapping + evec)
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                diff_plus = exec_time - cur_exec_time
                evec[i] = -1.
                exec_time = self.mapping_cache.evaluate_mapping(mapping + evec)
                if exec_time < self.best_exec_time:
                    self.best_exec_time = exec_time
                    self.best_mapping = mapping + evec
                diff_minus = cur_exec_time - exec_time  # because of the -h in the denominator of the difference quotient
                grad[i] = (diff_plus + diff_minus) / 2
        return grad

class SimulatedAnnealingFullMapper(object):
    """Generates a full mapping by using a simulated annealing algorithm from:
    Orsila, H., Kangas, T., Salminen, E., Hämäläinen, T. D., & Hännikäinen, M. (2007).
    Automated memory-aware application distribution for multi-processor system-on-chips.
    Journal of Systems Architecture, 53(11), 795-815.e.
    """
    def __init__(self, kpn,platform,config):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type config: OmniConf
        """
        random.seed(config['random_seed'])
        np.random.seed(config['random_seed'])
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = kpn
        self.platform = platform
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config,seed=None)
        self.statistics = Statistics(log, len(self.kpn.processes()),config['record_statistics'])
        self.initial_temperature = config['initial_temperature']
        self.final_temperature = config['final_temperature']
        self.max_rejections = len(self.kpn.processes()) * (len(self.platform.processors()) - 1) #R_max = L
        self.p = config['temperature_proportionality_constant']
        if not (self.p < 1 and self.p > 0):
            log.error(f"Temperature proportionality constant {self.p} not suitable, "
                      f"it should be close to, but smaller than 1 (algorithm probably won't terminate).")


        rep_type_str = config['representation']

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation
        self.mapping_cache = MappingCache(representation,config)

    def temperature_cooling(self,temperature,iter):
        return self.initial_temperature*self.p**np.floor(iter/self.max_rejections)

    def query_accept(self,time,temperature):
        normalized_probability = 1 / (np.exp(time/(0.5*temperature*self.initial_cost)))
        return normalized_probability

    def move(self,mapping,temperature):
        radius = self.config['radius']
        while(1):
            new_mappings = self.representation._uniformFromBall(mapping,radius,20)
            for m in new_mappings:
                if list(m) != list(mapping):
                    return m
            radius *= 1.1
            if radius > 10000 * self.config['radius']:
                log.error("Could not mutate mapping")
                raise RuntimeError("Could not mutate mapping")


    def generate_mapping(self):
        """ Generates a full mapping using simulated anealing
        """
        mapping_obj = self.random_mapper.generate_mapping()
        mapping = self.representation.toRepresentation(mapping_obj)

        last_mapping = mapping
        last_exec_time = self.mapping_cache.evaluate_mapping(mapping)
        self.initial_cost = last_exec_time
        best_mapping = mapping
        best_exec_time = last_exec_time
        rejections = 0

        iter = 0
        temperature = self.initial_temperature
        while rejections < self.max_rejections:
            temperature = self.temperature_cooling(temperature,iter)
            log.info(f"Current temperature {temperature}")
            mapping = self.move(last_mapping,temperature)
            cur_exec_time = self.mapping_cache.evaluate_mapping(mapping)
            faster = cur_exec_time < last_exec_time
            if not faster and cur_exec_time != last_exec_time:
                prob = self.query_accept(cur_exec_time - last_exec_time, temperature)
                rand = random.random()
                accept_randomly = prob > rand
            else:
                accept_randomly = False #don't accept if no movement.
            if faster or accept_randomly:
                #accept
                if cur_exec_time < best_exec_time:
                    best_exec_time = cur_exec_time
                    best_mapping = mapping
                last_mapping = mapping
                last_exec_time = cur_exec_time
                rejections = 0
            else:
                #reject
                if temperature <= self.final_temperature:
                    rejections += 1
            iter += 1
        self.statistics.log_statistics()
        self.statistics.to_file()

        return self.representation.fromRepresentation(best_mapping)

class TabuSearchFullMapper(object):
    """Generates a full mapping by using a tabu search on the mapping space.

    """
    def __init__(self, kpn,platform,config):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param config: the hyrda configuration
        :type config: OmniConf
        """
        random.seed(config['random_seed'])
        np.random.seed(config['random_seed'])
        self.full_mapper = True # flag indicating the mapper type
        self.kpn = kpn
        self.platform = platform
        self.config = config
        self.random_mapper = RandomPartialMapper(self.kpn,self.platform,config,seed=None)
        self.max_iterations = config['max_iterations']
        self.iteration_size = config['iteration_size']
        self.tabu_tenure = config['tabu_tenure']
        self.move_set_size = config['move_set_size']
        self.radius = config['radius']
        self.tabu_moves = dict()
        self.statistics = Statistics(log, len(self.kpn.processes()), config['record_statistics'])
        rep_type_str = config['representation']

        if rep_type_str not in dir(RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(
                dir(RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")

            representation = (representation_type.getClassType())(self.kpn, self.platform,self.config)

        self.representation = representation
        self.mapping_cache = MappingCache(representation,config)

    def update_candidate_moves(self,mapping):
        new_mappings = self.representation._uniformFromBall(mapping, self.radius, self.move_set_size)
        new_mappings = map(np.array, new_mappings)
        moves = set([(tuple(new_mapping - np.array(mapping)),
                      self.mapping_cache.evaluate_mapping(new_mapping)) for new_mapping in new_mappings])
        missing = self.move_set_size - len(moves)
        retries = 0
        while missing > 0 and retries < 10:
            new_mappings = self.representation._uniformFromBall(mapping, self.radius, missing)
            moves = moves.union( set([(tuple(np.array(new_mapping)-np.array(mapping)),
                                       self.mapping_cache.evaluate_mapping(new_mapping))
                                      for new_mapping in new_mappings]) )
            missing = self.move_set_size - len(moves)
            retries += 1
        if missing > 0:
            log.warning(f"Running with smaller move list  (by {missing} moves). The radius might be set too small?")
        self.moves = moves

    def move(self, best):
        delete = []
        for move in self.tabu_moves:
            self.tabu_moves[move] -= 1
            if self.tabu_moves[move] <= 0:
                delete.append(move)

        tabu = set(self.tabu_moves.keys())
        for move in delete:
            del self.tabu_moves[move]

        moves_sorted =  sorted(list(self.moves), key = lambda x : x[1])
        if moves_sorted[0][1] < best:
            self.tabu_moves[ moves_sorted[0][0] ] = self.tabu_tenure
            return moves_sorted[0]
        else:
            no_move = np.zeros(len(moves_sorted[0][0]))
            non_tabu = [m for m in moves_sorted if m[0] not in tabu.union(no_move)]
            #no need to re-sort:
            # https://stackoverflow.com/questions/1286167/is-the-order-of-results-coming-from-a-list-comprehension-guaranteed
            if len(non_tabu) > 0:
                self.tabu_moves[non_tabu[0][0]] = self.tabu_tenure
                return non_tabu[0]
            else:
                self.tabu_moves[moves_sorted[0][0]] = self.tabu_tenure
                return moves_sorted[0]



    def diversify(self,mapping):
        new_mappings = self.representation._uniformFromBall(mapping, 3*self.radius, self.move_set_size)
        new_mappings = map(np.array, new_mappings)
        moves = [(tuple(mapping - new_mapping),self.mapping_cache.evaluate_mapping(new_mapping)) for new_mapping in new_mappings]
        return(sorted(moves,key= lambda x : x[1])[0])



    def generate_mapping(self):
        """ Generates a full mapping using gradient descent
        """
        mapping_obj = self.random_mapper.generate_mapping()
        cur_mapping = self.representation.toRepresentation(mapping_obj)

        best_mapping = cur_mapping
        best_exec_time = self.mapping_cache.evaluate_mapping(cur_mapping)
        since_last_improvement = 0

        for iter in range(self.max_iterations):
            while since_last_improvement < self.iteration_size:
                self.update_candidate_moves(cur_mapping)
                move,cur_exec_time = self.move(best_exec_time) #updates tabu set
                cur_mapping = cur_mapping + np.array(move)
                since_last_improvement += 1
                if cur_exec_time < best_exec_time:
                    since_last_improvement = 0
                    best_exec_time = cur_exec_time
                    best_mapping = cur_mapping

            since_last_improvement = 0
            move, cur_exec_time = self.diversify(cur_mapping)
            cur_mapping = cur_mapping + np.array(move)

        self.statistics.log_statistics()
        self.statistics.to_file()

        return self.representation.fromRepresentation(np.array(best_mapping))


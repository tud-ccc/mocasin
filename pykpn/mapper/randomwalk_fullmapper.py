#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens

import random
import timeit
import multiprocessing as mp
import hydra
import simpy

from pykpn.mapper.random_mapper import RandomMapping
from pykpn.simulate.application import RuntimeKpnApplication
from pykpn.simulate.system import RuntimeSystem

from pykpn.util import logging

log = logging.getLogger(__name__)

class ApplicationContext(object):

    def __init__(self, name=None, kpn=None, mapping=None, trace_reader=None,
                 start_time=None):
        self.name = name
        self.kpn = kpn
        self.mapping = mapping
        self.trace_reader = trace_reader
        self.start_time = start_time


class SimulationContext(object):

    def __init__(self, platform=None, app_contexts=None):
        self.platform = platform
        if app_contexts is None:
            self.app_contexts = []
        else:
            self.app_contexts = app_contexts
        self.exec_time = None

def run_simualtion(sim_context):
    # Create simulation environment
    env = simpy.Environment()

    # create the applications
    applications = []
    mappings = {}
    for ac in sim_context.app_contexts:
        app = RuntimeKpnApplication(ac.name, ac.kpn, ac.mapping,
                                    ac.trace_reader, env, ac.start_time)
        applications.append(app)
        mappings[ac.name] = ac.mapping

    # Create the system
    system = RuntimeSystem(sim_context.platform, applications, env)

    # run the simulation
    system.simulate()
    system.check_errors()

    sim_context.exec_time = env.now

    return sim_context

class RandomWalkFullMapper(object):
    """Generates a full mapping via a random walk

    This class is used to generate a mapping for a given
    platform and KPN application, via a random walk through
    the mapping space.
    It produces multiple random mappings and simulates each mapping in
    order to find the 'best' mapping. As outlined below, the script expects
    multiple configuration parameters to be available.
    **Hydra Parameters**:
        * **jobs:** the number of parallel jobs
        * **num_operations:** the total number of mappings to be generated
    """

    def __init__(self, kpn, platform,config):
        """Generates a random mapping for a given platform and KPN application. 
        Args:
           cfg(~omegaconf.dictconfig.DictConfig): the hydra configuration object
        """
        self.full_mapper = True
        self.platform = platform
        self.kpn = kpn
        self.config = config

    def generate_mapping(self):
        """ Generates a mapping via a random walk
        """

        start = timeit.default_timer()
        # Create a list of 'simulations'. These are later executed by multiple
        # worker processes.
        simulations = []
        for i in range(0, self.config['num_iterations']):
            # create a simulation context
            sim_context = SimulationContext(self.platform)

            # create the application context
            name = self.kpn.name
            app_context = ApplicationContext(name, kpn)

            app_context.start_time = 0

            # generate a random mapping
            app_context.representation = RepresentationType[rep_type_str]
            app_context.mapping = RandomMapping(kpn, platform)

            # create the trace reader
            app_context.trace_reader = hydra.utils.instantiate(cfg['trace'])

            sim_context.app_contexts.append(app_context)

            simulations.append(sim_context)

        # run the simulations and search for the best mapping
        pool = mp.Pool(processes=cfg['jobs'])

        # execute the simulations in parallel
        if cfg['progress']:
            import tqdm
            results = list(tqdm.tqdm(pool.imap(run_simualtion, simulations,
                                               chunksize=10),
                                     total=num_iterations))
        else:
            results = list(pool.map(run_simualtion, simulations, chunksize=10))

        # calculate the execution times in milliseconds and look for the best
        # result
        best_result = results[0]
        exec_times = []  # keep a list of exec_times for later
        for r in results:
            exec_times.append(float(r.exec_time / 1000000000.0))
            if r.exec_time < best_result.exec_time:
                best_result = r

        # When we reach this point, all simulations completed

        stop = timeit.default_timer()
        print('Tried %d random mappings in %0.1fs' %
              (len(results), stop - start))
        exec_time = float(best_result.exec_time / 1000000000.0)
        print('Best simulated execution time: %0.1fms' % (exec_time))
        #generate new mapping if no partial mapping is given
        if not part_mapping:
            part_mapping = Mapping(self.kpn, self.platform)

        # check if the platform/kpn is equivalent
        if not part_mapping.platform is self.platform or not part_mapping.kpn is self.kpn:
            raise RuntimeError('rand_map: Try to map partial mapping of platform,KPN %s,%s to %s,%s',
                             part_mapping.platform.name, part_mapping.kpn.name, 
                             self.platform.name, self.kpn.name)


        
        # configure policy of schedulers
        for s in self.platform.schedulers():
            i = random.randrange(0, len(s.policies))
            policy = s.policies[i]
            info = SchedulerMappingInfo(policy, None)
            part_mapping.add_scheduler_info(s, info)
            log.debug('rand_map: configure scheduler %s to use the %s policy',
                      s.name, policy.name)
        
        # map processes
        processes = part_mapping.get_unmapped_processes()
        #print("remaining process list: {}".format(processes))
        for p in processes:
            i = random.randrange(0, len(self.platform.schedulers()))
            scheduler = list(self.platform.schedulers())[i]
            i = random.randrange(0, len(scheduler.processors))
            affinity = scheduler.processors[i]
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            part_mapping.add_process_info(p, info)
            log.debug('rand_map: map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)          
        
        # map channels
        channels = part_mapping.get_unmapped_channels()
        for c in channels:
            capacity = 4 # fixed channel bound this may cause problems
            suitable_primitives = []
            for p in part_mapping.platform.primitives():
                src = part_mapping.process_info(c.source).affinity
                sinks = [part_mapping.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError('rand_map: Mapping failed! No suitable primitive for '
                                   'communication from %s to %s found!' %
                                   (src.name, str(sinks)))
            i = random.randrange(0, len(suitable_primitives))
            primitive = suitable_primitives[i]
            info = ChannelMappingInfo(primitive, capacity)
            part_mapping.add_channel_info(c, info)
            log.debug('rand_map: map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity)) 

        # finally check if the mapping is fully specified
        assert not part_mapping.get_unmapped_processes()
        assert not part_mapping.get_unmapped_channels()
        return part_mapping


# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import numpy as np
from sortedcontainers import SortedList
import hydra

from pykpn.common.mapping import Mapping, ProcessMappingInfo
from pykpn.util import logging
from pykpn.mapper.random import RandomPartialMapper
from pykpn.mapper.partial import ComPartialMapper
from pykpn.mapper.utils import Statistics


log = logging.getLogger(__name__)


def trace_summary(kpn, platform, trace):
    summary = {}
    p_types = set()
    for p in platform.processors():
        p_types = p_types.union(set([p.type]))
    for p_type in p_types:
        trace.reset()
        for proc in kpn.processes():
            tot = 0
            seg = trace.next_segment(proc.name,p_type)
            while not seg.terminate:
                tot += seg.processing_cycles
                seg = trace.next_segment(proc.name, p_type)
            summary[(proc.name,p_type)] = tot
    return summary

class StaticCFSMapper(object):
    """Generates a full mapping by using a static method similar to the Linux CFS scheduler.
    See: http://people.redhat.com/mingo/cfs-scheduler/sched-design-CFS.txt
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
        trace_generator = hydra.utils.instantiate(config['trace'])
        self.trace_summary = trace_summary(kpn,platform,trace_generator)
        self.randMapGen = RandomPartialMapper(self.kpn, self.platform, config)
        self.comMapGen = ComPartialMapper(self.kpn, self.platform, self.randMapGen)
        #self.statistics = Statistics()

    def generate_mapping(self,restricted = None):
        """ Generates a full mapping using a static algorithm
        inspired by Linux' GBM
        """
        mapping = Mapping(self.kpn,self.platform)
        core_types = dict(self.platform.core_types())
        processes = {}
        if restricted is None:
            restricted = []

        for type in core_types:
            processes[type] = SortedList()
        #use best time at first and update depending on the proc. that is next
            for p in self.kpn.processes():
              processes[type].add( (self.trace_summary[(p.name,type)], p.name ))

        finished = False #to avoid converting the lists every time
        while not finished:
            #round robin
            for core in self.platform.processors():
                if core.name in restricted:
                    continue
                _,p = processes[core.type].pop()

                #map process to core
                scheduler = list(self.platform.schedulers())[0]
                affinity = core
                process = [pr for pr in self.kpn.processes() if pr.name == p][0]
                priority = 0
                info = ProcessMappingInfo(scheduler, affinity, priority)
                mapping.add_process_info(process, info)

                #remove process from the other lists
                for type in core_types:
                    if core.type == type:
                        continue
                    to_remove = [(time,p) for (time,p) in processes[type] if p == process.name]
                    assert(len(to_remove)) == 1
                    processes[type].remove(to_remove[0])

                if len(processes[core.type]) == 0:
                    finished = True
                    break

        #finish mapping
        return self.comMapGen.generate_mapping(mapping)


# This file implements classes of Application tables
#
# Author: Robert Khasanov

import os
import pandas as pd
import math
import logging
import random

from pykpn.tetris.tetris.extra import NamedDimensionalNumber
from pykpn.tetris.tetris.tplatform import Platform
from pykpn.slx.kpn import SlxKpnGraph

from pykpn.common.mapping import Mapping as KpnMapping, SchedulerMappingInfo,ProcessMappingInfo, ChannelMappingInfo

log = logging.getLogger(__name__)

class CanonicalMapping:
    """A canonical mapping with energy/utility characteristics.

    Canonical mapping is a mapping which represents a set of equivalent mappings,
    which can be derived by applying transformations and keeps
    the same energy/utility characteristics.

    TODO: Add a name property
    
    Args:
        mapping (dict[str,str]): the binding of processes to processors
        time (float): the execution time of the mapping
        energy (float): the energy consumption of the mapping
        kpn_graph (pykpn.slx.kpn.SlxKpnGraph): the kpn graph of the application
        platform (Platform): the platform
    """
    def __init__(self, mapping: dict, time: float, energy: float, kpn_graph: SlxKpnGraph, platform: Platform):
        self.__time = time 
        self.__energy = energy
        
        if kpn_graph is None:
            self.__mapping = None
        else:
            assert isinstance(mapping, dict)
            self.__mapping = CanonicalMapping.__create_kpn_mapping(kpn_graph, platform.kpn_platform(), mapping)

        self.__core_types = {}
        assert platform is not None
        self.__core_types = self.__calc_core_types(platform)

    @staticmethod
    def __create_kpn_mapping(kpn_graph: SlxKpnGraph, platform: Platform, mapping: dict):
        """Create KPN mapping from a dict, the simple vector representation.

        Priority and policy chosen at random, and scheduler chosen randomly from the possible ones.
        Channels are chosen at random.
        Note that this function assumes the input is sane.

        Params:    
           kpn_graph (pykpn.slx.kpn.SlxKpnGraph): the kpn graph of the application
           platform (Platform): the platform
           mapping (dict[str,str]): the binding of processes to processors
        """
        kpn_mapping = KpnMapping(kpn_graph, platform)
        processors = list(platform.processors())
        all_schedulers = list(platform.schedulers())
        all_primitives = list(platform.primitives())

        # configure schedulers
        for s in all_schedulers:
            i = random.randrange(0, len(s.policies))
            policy = s.policies[i]
            info = SchedulerMappingInfo(policy, None)
            kpn_mapping.add_scheduler_info(s, info)
            log.debug('configure scheduler %s to use the %s policy',
                      s.name, policy.name)
            
        # map processes
        for p in kpn_graph.processes():
            assert p.name in mapping, "Process {} is not in mapping = {}".format(p.name, mapping)
            pe_name = mapping[p.name]
            pe = platform.find_processor(pe_name)
            schedulers = [ sched for sched in all_schedulers if pe in sched.processors]
            j = random.randrange(0, len(schedulers))
            scheduler = schedulers[j]
            affinity = pe
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            kpn_mapping.add_process_info(p, info)
            log.debug('map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)

        # map channels
        for i,c in enumerate(kpn_graph.channels(),start=i+1):
            capacity = 4
            suitable_primitives = []
            for p in all_primitives:
                src = kpn_mapping.process_info(c.source).affinity
                sinks = [kpn_mapping.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError('Mapping failed! No suitable primitive for '
                                   'communication from %s to %s found!' %
                                   (src.name, str(sinks)))

            assert len(mapping) == len(kpn_graph.processes())
            if len(suitable_primitives) == 1:
                primitive = suitable_primitives[0]
            else:
                idx = random.randrange(0, len(suitable_primitives)-1)
                primitive = suitable_primitives[idx]

            info = ChannelMappingInfo(primitive, capacity)
            kpn_mapping.add_channel_info(c, info)
            log.debug('map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity))

        return kpn_mapping

    def __calc_core_types(self, platform):
        if self.__mapping is not None:
            ps = {self.__mapping.affinity(p) for p in self.__mapping.kpn.processes()}
        else:
            ps = {}
        ct = NamedDimensionalNumber(platform.core_types(), init_only_names = True)
        for p in ps:
            pp = platform.find_processor(p.name)
            ct[pp.type] += 1
        return ct


    def time(self, start_cratio = 0.0, end_cratio = 1.0) -> float:
        """Returns the execution time of the mapping, needed to proceed from
           `start_cratio` till `end_cratio`.
        """
        return self.__time * (end_cratio - start_cratio)

    def energy(self, start_cratio = 0.0, end_cratio = 1.0) -> float:
        """Returns the energy consumption of the mapping, needed to proceed from
           `start_cratio` till `end_cratio`.
        """
        return self.__energy * (end_cratio - start_cratio)

    @property
    def core_types(self):
        return NamedDimensionalNumber(self.__core_types)

    @classmethod
    def make_idle(cls, platform):
        return cls(None, math.inf, 0.0, None, platform)

class Application:
    CPN_FILENAME = "cpn.xml"
    MAPPINGS_SUFFIX = ".mappings.csv"

    def __init__(self, name: str, path: str, platform: Platform, add_idle = False):
        assert os.path.isdir(path)
        self.name = name
        cpn_path = os.path.join(path, Application.CPN_FILENAME)
        mappings_path = os.path.join(path, platform.name + Application.MAPPINGS_SUFFIX)
        self.__kpn_graph = SlxKpnGraph('SlxKpnGraph', cpn_path, '2017.04')

        # Read mappings file
        mdf = pd.read_csv(mappings_path)
        mappings = mdf.set_index('mapping').to_dict('index')
        self.mappings = {}
        for name, m in mappings.items():
            time = m['executionTime']
            energy = m['totalEnergy']
            mapping = {k[2:]:v for k,v in m.items() if k.startswith("t_")}
            self.mappings[name] = CanonicalMapping(mapping, time, energy, self.__kpn_graph, platform)




    def add_idle(self, platform):
        self.mappings['__idle__'] = CanonicalMapping.make_idle(platform)

    def best_case_energy(self, start_cratio = 0.0, end_cratio = 1.0):
        return min([v.energy(start_cratio = start_cratio, end_cratio = end_cratio) for k,v in self.mappings.items() if k != "__idle__"])

    def best_case_time(self, start_cratio = 0.0, end_cratio = 1.0):
        return min([v.time(start_cratio = start_cratio, end_cratio = end_cratio) for k,v in self.mappings.items() if k != "__idle__"])

class AppTable:
    def __init__(self, platform, allow_idle = False):
        self.__apps = []
        self.__allow_idle = allow_idle

        self.__platform = platform

    def add(self, app):
        assert isinstance(app, Application)
        if self.__allow_idle:
            app.add_idle(self.__platform)
        self.__apps.append(app)

    def __getitem__(self, name):
        assert isinstance(name, str)
        for a in self.__apps:
            if a.name == name:
                return a
        assert False, "No application with name '{}'".format(name)

    def read_applications(self, path):
        assert os.path.isdir(path), "The folder '{}' does not exist".format(path)
        log.info("Reading applications:")
        for name in os.listdir(path):
            app_folder = os.path.join(path,name)
            if not os.path.isdir(app_folder):
                continue
            app = Application(name, app_folder, self.__platform)
            self.add(app)
            log.info("   * {}".format(name))

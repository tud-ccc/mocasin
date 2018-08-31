# Authors: Gerald Hempel

from pykpn.common import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)


log = logging.getLogger(__name__)

class DC_MappingGenerator(object):
    """Generates a partial mapping derived from a vector

    This class is used to generate a partial mapping for a given
    platform and KPN application. 
    """

    def __init__(self, kpn, platform, fullGenerator):
        """Generates a partial mapping for a given platform and KPN application. 

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param fullGenerator: the associated full mapping generator
        :type fullGererator: MappingGenerator
        """
        self.full_mapper = False # flag indicating the mapper type
        self.platform = platform
        self.kpn = kpn
        self.fullGenerator = fullGenerator
        self.mapping = Mapping(kpn, platform)
        pes = sorted(list(self.platform.processors()))
        self.pe_vec_mapping = dict(zip(pes,[n for n in range(0, len(pes))]))
        # build a reverse dict of the pe_vec_mapping dictionary (since it is a one-to-one dict)
        self.vec_pe_mapping = dict([(self.pe_vec_mapping[key],key) for key in self.pe_vec_mapping])

    def get_pe_name_mapping(self):
        """Return the used mapping of PE names to integers"""
        res = {}
        for key in self.pe_vec_mapping:
            res[key.name] = self.pe_vec_mapping[key]
        return res

    def generate_mapping(self, vec, map_history = []):
        """ Generates an unique partial mapping for a numeric vector

        The generated mapping is derived form a numeric vector 
        that describes the mapping. Each value in the vector stand 
        for a Process -> PE mapping.

        :param vec: a vector describing the mapping
        :type vec: tuple of integers
        :param map_history: exclution list of already generated mappings
        :type map_history: list of mappings
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a random process mapping.
        """
        log.debug('dc_map: start mapping generation for {} on {} with {}'
                   .format(self.kpn.name,self.platform.name,vec))

        # map processes to scheduler and processor
        for i,p in enumerate(self.kpn.processes()):
            # choose the desired processor from list
            pe = self.vec_pe_mapping[vec[i]]
            # choose the first scheduler from list
            scheduler = list(self.platform.find_scheduler_for_processor(pe))[0]
            # set the affinity of the scheduler to the choosen PE
            affinity = pe
            # always set priority to 0
            priority = 0
            info = ProcessMappingInfo(scheduler, affinity, priority)
            # configure mapping
            self.mapping.add_process_info(p, info)
            log.debug('dc_map: map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)
            if self.mapping in map_history:
                return None
            else:
                return self.fullGenerator.generate_mapping(self.mapping)

        




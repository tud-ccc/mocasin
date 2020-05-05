# Authors: Gerald Hempel, Andres Goens

from pykpn.util import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)

log = logging.getLogger(__name__)

class ProcPartialMapper(object):
    """Generates a partial mapping derived from a vector(tuple) 

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
        :type fullGererator: PartialMapper
        """
        self.full_mapper = False # flag indicating the mapper type
        self.platform = platform
        self.kpn = kpn
        self.fullGenerator = fullGenerator
        pes = sorted(list(self.platform.processors()),key=(lambda p : p.name))
        self.pe_vec_mapping = dict(zip(pes,[n for n in range(0, len(pes))]))
        # build a reverse dict of the pe_vec_mapping dictionary (since it is a one-to-one dict)
        self.vec_pe_mapping = dict([(self.pe_vec_mapping[key],key) for key in self.pe_vec_mapping])

    def get_pe_name_mapping(self):
        """Return the used mapping of PE names to integers"""
        res = {}
        for key in self.pe_vec_mapping:
            res[key.name] = self.pe_vec_mapping[key]
        return res

    @staticmethod
    def generate_pe_mapping_from_simple_vector(vec,kpn,platform,vec_pe_mapping):
        mapping = Mapping(kpn, platform)

        # map processes to scheduler and processor
        for i,p in enumerate(kpn.processes()):
            # choose the desired processor from list
            pe = vec_pe_mapping[vec[i]]
            # choose the first scheduler from list
            scheduler = list(platform.find_scheduler_for_processor(pe))[0]
            # set the affinity of the scheduler to the choosen PE
            affinity = pe
            # always set priority to 0
            priority = 0
            info = ProcessMappingInfo(scheduler, affinity, priority)
            # configure mapping
            mapping.add_process_info(p, info)
        return mapping

    def generate_mapping(self, vec, map_history = None):
        """ Generates an unique partial mapping for a numeric vector

        The generated mapping is derived from a numeric vector
        that describes the mapping. Each value in the vector stands
        for a Process -> PE mapping.

        :param reprVec: a vector describing the mapping in the initilized representation
        :type reprVec: tuple describing the representation
        :param map_history: exclution list of already generated mappings
        :type map_history: list of mappings
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a process mapping.
        """
        #TODO: This should be adapted to use representations

        log.debug('ProcPartialMapper: start mapping generation for {} on {} with simpleVec: {}'
                   .format(self.kpn.name,self.platform.name,vec))

        if map_history is None:
            map_history = []

        #TODO: raise not implemented exception for input of part_mapping

         # raise NotImplementedError(
         #       'The slx trace reader does not support version %s' % version)

        # generate new mapping
        mapping = ProcPartialMapper.generate_pe_mapping_from_simple_vector(vec,self.kpn,self.platform,self.vec_pe_mapping)
        if mapping in map_history:
            return None
        else:
            return self.fullGenerator.generate_mapping(mapping)




# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

from pykpn.util import logging
from pykpn.common.mapping import ChannelMappingInfo, Mapping, ProcessMappingInfo, SchedulerMappingInfo

log = logging.getLogger(__name__)

class ComPartialMapper(object):
    """Generates a partial mapping by placing communication primitives.
    This generator either requires a partial mapping as input that already
    provides a placement of processes or performs a deterministic placement of processes
    for an incomplete mapping. The generated mapping provides a best effort
    placement of communication primitives.

    This class is used to generate a partial mapping for a given
    platform and KPN application.
    """

    def __init__(self, kpn, platform, full_generator):
        """Generates a partial mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param fullGenerator: the associated full mapping generator
        :type fullGererator: FullMapper
        """
        self.full_mapper = False # flag indicating the mapper type
        self.platform = platform
        self.kpn = kpn
        self.full_generator = full_generator

    def generate_mapping(self, part_mapping=None):
        res = ComPartialMapper.generate_mapping_static(self.kpn, self.platform, part_mapping=part_mapping)
        return self.full_generator.generate_mapping(res)

    @staticmethod
    def generate_mapping_static(kpn, platform, part_mapping=None):
        """ Generates an partial mapping from a given partial mapping

        The generated mapping provides a best effort placement of
        communication structures. The rest is deterministically chosen
        to the first available option.

        :param mapping: a partial mapping with placed processes or an empty mapping
        :type mapping: mapping
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a process mapping (for partial mappings
            with incomplete process mappings).
        """

        #generate new mapping if no partial mapping is given
        if not part_mapping:
            part_mapping = Mapping(kpn, platform)

        # map processes to scheduler and processor if not already done
        processes = part_mapping.get_unmapped_processes()
        for p in processes:
            scheduler = list(platform.schedulers())[0]
            affinity = scheduler.processors[0]
            priority = 0
            info = ProcessMappingInfo(scheduler, affinity, priority)
            part_mapping.add_process_info(p, info)
            log.debug('com_map: map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)

            # map communication primitives
        channels = part_mapping.get_unmapped_channels()
        for c in channels:
            capacity = 16 # fixed channel bound this may cause problems
            suitable_primitives = []
            src = part_mapping.process_info(c.source).affinity
            sinks = [part_mapping.process_info(s).affinity for s in c.sinks]
            for p in part_mapping.platform.primitives():
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError('com_map: Mapping failed! No suitable primitive for '
                                   'communication from %s to %s found!' %
                                   (src.name, str(sinks)))

            primitive = ComPartialMapper._get_minimal_costs(suitable_primitives, c, src, sinks)
            info = ChannelMappingInfo(primitive, capacity)
            part_mapping.add_channel_info(c, info)
            log.debug('com_map: map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity))

        return part_mapping

    @staticmethod
    def _get_minimal_costs(primitives, channel, src, sinks):
        """ Returns the primitive with the minimum of static costs.
            For channels with multiple sinks, the average cost is minimized.
        """
        costs = []
        if len(sinks) == 1:
            for p in primitives:
                costs.append(p.static_costs(src, sinks[0], channel.token_size))
            return primitives[costs.index(min(costs))]

        if len(sinks) > 1:
            avr_costs = []
            for p in primitives:
                for s in sinks:
                    costs.append(p.static_costs(src, s, channel.token_size))
                avr_costs.append(sum(costs))
            return primitives[avr_costs.index(min(avr_costs))]
        else:
            # should never happen
            return None


class ProcPartialMapper(object):
    """Generates a partial mapping derived from a vector(tuple)

    This class is used to generate a partial mapping for a given
    platform and KPN application.
    """

    def __init__(self, kpn, platform, full_generator):
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
        self.full_generator = full_generator
        pes = sorted(list(self.platform.processors()), key=(lambda p : p.name))
        self.pe_vec_mapping = dict(zip(pes, [n for n in range(0, len(pes))]))
        # build a reverse dict of the pe_vec_mapping dictionary (since it is a one-to-one dict)
        self.vec_pe_mapping = dict([(self.pe_vec_mapping[key], key) for key in self.pe_vec_mapping])

    def get_pe_name_mapping(self):
        """Return the used mapping of PE names to integers"""
        res = {}
        for key in self.pe_vec_mapping:
            res[key.name] = self.pe_vec_mapping[key]
        return res

    @staticmethod
    def generate_pe_mapping_from_simple_vector(vec, kpn, platform, vec_pe_mapping):
        mapping = Mapping(kpn, platform)

        # map processes to scheduler and processor
        for i, p in enumerate(kpn.processes()):
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

    def generate_mapping(self, vec, map_history=None):
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
                  .format(self.kpn.name, self.platform.name, vec))

        if map_history is None:
            map_history = []

        #TODO: raise not implemented exception for input of part_mapping

        # raise NotImplementedError(
        #       'The slx trace reader does not support version %s' % version)

        # generate new mapping
        mapping = ProcPartialMapper.generate_pe_mapping_from_simple_vector(vec,
                                                                           self.kpn,
                                                                           self.platform,
                                                                           self.vec_pe_mapping)
        if mapping in map_history:
            return None
        else:
            return self.full_generator.generate_mapping(mapping)

class ComFullMapper(object):
    """Generates a full mapping by placing communication primitives.
    This generator either requires a partial mapping as input that already
    provides a placement of processes or performs a deterministic placement of processes
    for an incomplete mapping. Schedulers are all set to the first option.
    The generated mapping provides a best effort placement of communication primitives.
    TODO: the schedulers should first check for unmapped schedulers and only
        deterministically map the missing ones.

    This class is used to generate a full mapping for a given
    platform and KPN application.
    """
    def __init__(self, kpn, platform, config):
        """Generates a partial mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param fullGenerator: the associated full mapping generator
        :type fullGererator: FullMapper
        """
        self.full_mapper = True # flag indicating the mapper type
        self.platform = platform
        self.kpn = kpn
        self.config = config

    def generate_mapping(self, part_mapping=None):
        # configure policy of schedulers
        if part_mapping is None:
            part_mapping = Mapping(self.kpn, self.platform)
        for s in self.platform.schedulers():
            policy = s.policies[0]
            info = SchedulerMappingInfo(policy, None)
            part_mapping.add_scheduler_info(s, info)
            log.debug('configure scheduler %s to use the %s policy',
                      s.name, policy.name)
        return ComPartialMapper.generate_mapping_static(self.kpn, self.platform, part_mapping=part_mapping)


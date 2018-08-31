# Authors: Gerald Hempel
import random

from pykpn.common import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)

log = logging.getLogger(__name__)

class ComMappingGenerator(object):
    """Generates a partial mapping by placing communication primitives.
    This generator either requires a partial mapping as input that already
    provides a placement of processes or performs a random placement of processes 
    for an incomplete mapping. The generated mapping provides a best effort 
    placement of communication primitives.

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
    
    def generate_mapping(self, part_mapping=None):
        """ Generates an partial mapping from a given partial mapping

        The generated mapping provides a best effort placement of 
        communication structures. If the initial mapping is empty the 
        process-mapping is rendomly determined.
        
        :param mapping: a partial mapping with placed processes or an empty mapping
        :type mapping: mapping
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a random process mapping.
        """
        if not part_mapping:
            part_mapping = self.mapping
            
        # map processes to scheduler and processor if not already done
        processes = part_mapping.get_unmapped_processes()
        for p in processes:
            i = random.randrange(0, len(self.platform.schedulers()))
            scheduler = list(self.platform.schedulers())[i]
            i = random.randrange(0, len(scheduler.processors))
            affinity = scheduler.processors[i]
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            part_mapping.add_process_info(p, info)
            self.mapping.add_process_info(p, info)
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

            primitive = self._get_minimal_costs(suitable_primitives, c, src, sinks)
            info = ChannelMappingInfo(primitive, capacity)
            part_mapping.add_channel_info(c, info)
            log.debug('com_map: map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity)) 

        self.mapping = part_mapping
        return self.fullGenerator.generate_mapping(self.mapping)

    def _get_minimal_costs(self,primitives, channel, src, sinks):
        """ Returns the primitive with the minimum of static costs. 
            For channels with multiple sinks, the average cost is minimized.
        """
        costs = []
        if len(sinks) == 1:
            for p in primitives:
               costs.append(p.static_costs(src,sinks[0],channel.token_size))
            return primitives[costs.index(min(costs))]

        if len(sinks) > 1:
            avr_costs = []
            for p in primitives:
                for s in sinks:
                    costs.append(p.static_costs(src,s,channel.token_size))
                avr_costs.append(sum(costs))
            return primitives[avr_costs.index(min(avr_costs))]
        else: # should never happen
            return None




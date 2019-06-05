# Authors: Gerald Hempel

from pykpn.util import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)


log = logging.getLogger(__name__)


class MappingGenerator(Mapping):
    """A mapping derived from a vector

    When this class is initialized, it generates a mapping for a given
    platform and KPN application. The generated mapping is derived form a 
    numeric vector that describes the mapping.
    """

    def __init__(self, kpn, platform, vec):
        """Generate a mapping for a numeric vector

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param vec: a vector describing the mapping
        :type vec: tuple of integers
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a random process mapping.
        """

        super().__init__(kpn, platform)

        log.debug('start mapping generator for {} on {} with {}'.format(kpn.name,platform.name,vec))


        pes = sorted(list(platform.processors()))
        # map processes to scheduler and processor
        for i,p in enumerate(kpn.processes()):
            # always choose the desired processor from list
            pe = pes[vec.sample2tuple()[i]]
            # always choose first scheduler from list
            scheduler = list(platform.find_scheduler_for_processor(pe))[0]
            # always choose first processor from list
            #print("{} Processes: {} Scheduler: {} PE: {}  {}".format(i,p.name,
            #      list(platform.find_scheduler_for_processor(pe))[0].name, scheduler.processors,vec))
            #affinity = scheduler.processors[0]
            affinity = pe
            # always set priority to 0
            priority = 0
            info = ProcessMappingInfo(scheduler, affinity, priority)
            self.add_process_info(p, info)
            log.debug('map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)            
        
        #print("map policies")
        # configure policy of schedulers
        for s in platform.schedulers():
            # always choose first policy from list for each scheduler 
            policy = s.policies[0]
            info = SchedulerMappingInfo(policy, None)
            self.add_scheduler_info(s, info)
            #print('configure scheduler %s to use the %s policy',
            #          s.name, policy.name)
            log.debug('configure scheduler %s to use the %s policy',
                      s.name, policy.name)

        #print("map channels")
        # map channels
        for c in kpn.channels():
            capacity = 4 # fixed channel bound this may cause problems
            suitable_primitives = []
            for p in platform.primitives():
                src = self.process_info(c.source).affinity
                sinks = [self.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError('Mapping failed! No suitable primitive for '
                                   'communication from %s to %s found!' %
                                   (src.name, str(sinks)))
            # alway select first suitabel primitive
            primitive = suitable_primitives[0]
            info = ChannelMappingInfo(primitive, capacity)
            self.add_channel_info(c, info)
            #print('map channel %s to the primitive %s and bound to %d '
            #          'tokens' % (c.name, primitive.name, capacity))        
            log.debug('map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity)) 

        log.debug(">>>>>> Mapping toList: {}".format(super().to_list()))
        log.debug(super().get_numPEs())


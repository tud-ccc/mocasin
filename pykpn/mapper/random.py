# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import random

from pykpn.common import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)


log = logging.getLogger(__name__)


class RandomMapping(Mapping):
    """A random mapping

    When this class is initialized, it generates a random mapping for a given
    platform and kpn application. The random module is used for pseudo number
    generation. You can call ``random.seed(<...>)`` before instantiating this
    class in order to achieve reproducible results.

    The implementation of this class is not perfect. Here is a list of known
    problems:

    * Does not select a scheduling policy parameter if it is required.
    * First maps a process to a scheduler and then selects the
      affinity. This way, processes are expected to be evenly distributed
      between schedulers and not between processors. It is likely that a
      processor with it's on scheduler receives more workload than a
      processor that shares the scheduler with other processors.
    * How to select channel bounds?
    """

    def __init__(self, kpn, platform):
        """Generate a random mapping

        :param kpn: a kpn graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a random process mapping.
        """
        super().__init__(kpn, platform)

        log.debug('start random mapper for %s on %s', kpn.name, platform.name)

        # configure schedulers
        for s in platform.schedulers():
            i = random.randrange(0, len(s.policies))
            policy = s.policies[i]
            info = SchedulerMappingInfo(policy, None)
            self.add_scheduler_info(s, info)
            log.debug('configure scheduler %s to use the %s policy',
                      s.name, policy.name)

        # map processes
        for p in kpn.processes():
            i = random.randrange(0, len(platform.schedulers()))
            scheduler = list(platform.schedulers())[i]
            i = random.randrange(0, len(scheduler.processors))
            affinity = scheduler.processors[i]
            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            self.add_process_info(p, info)
            log.debug('map process %s to scheduler %s and processor %s '
                      '(priority: %d)', p.name, scheduler.name, affinity.name,
                      priority)

        # map channels
        for c in kpn.channels():
            capacity = 4
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
            i = random.randrange(0, len(suitable_primitives))
            primitive = suitable_primitives[i]
            info = ChannelMappingInfo(primitive, capacity)
            self.add_channel_info(c, info)
            log.debug('map channel %s to the primitive %s and bound to %d '
                      'tokens' % (c.name, primitive.name, capacity))

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens, Gerald Hempel

import random

from pykpn.util import logging
from pykpn.common.mapping import ChannelMappingInfo, Mapping, ProcessMappingInfo

log = logging.getLogger(__name__)


class RandomPartialMapper(object):
    """Generates a random mapping

    This class is used to generate a random mapping for a given
    platform and KPN application.
    """

    def __init__(self, kpn, platform, config, seed=None):
        """Generates a random mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        """
        if seed is not None:
            random.seed(seed)
        self.seed = seed
        self.config = config
        self.full_mapper = True
        self.platform = platform
        self.kpn = kpn

    def generate_mapping(self, part_mapping = None):
        """ Generates a random mapping

        The generated mapping takes a partial mapping (that may also be empty)
        as starting point. All open mapping decissions were taken by generated
        randomness derived from the given seed.

        :param seed: initial seed for the random generator
        :type seed: integer
        :param part_mapping: partial mapping to start from
        :type part_mapping: Mapping
        """

        #generate new mapping if no partial mapping is given
        if not part_mapping:
            part_mapping = Mapping(self.kpn, self.platform)

        # check if the platform/kpn is equivalent
        if not part_mapping.platform is self.platform or not part_mapping.kpn is self.kpn:
            raise RuntimeError('rand_map: Try to map partial mapping of platform,KPN %s,%s to %s,%s',
                               part_mapping.platform.name, part_mapping.kpn.name,
                               self.platform.name, self.kpn.name)

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


class RandomMapper(RandomPartialMapper):
    """Generates a random mapping
    This class is a FullMapper wrapper
    for RandomPartialMapper.
    """
    def __init__(self, kpn, platform, config):
        super().__init__(kpn, platform, config, seed=config['random_seed'])

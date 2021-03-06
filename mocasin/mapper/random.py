# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Gerald Hempel

import random

from mocasin.util import logging
from mocasin.common.mapping import (
    ChannelMappingInfo,
    Mapping,
    ProcessMappingInfo,
)

log = logging.getLogger(__name__)


class RandomPartialMapper(object):
    """Generates a random mapping.

    This class is used to generate a random mapping for a given
    platform and dataflow graph
    """

    def __init__(self, graph, platform, seed=None, resources_first=False):
        """Generate a random mapping for a given platform and dataflow application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        :param seed: a random seed for the RNG
        :type seed: int
        :param resources_first: Changes the generation method to first choose
        processors, and then assign processes only to those processors
        :type resources_first: bool
        """
        if seed is not None:
            random.seed(seed)
        self.seed = seed
        self.resources_first = resources_first
        self.full_mapper = True
        self.platform = platform
        self.graph = graph

    def generate_mapping(self, part_mapping=None):
        """Generate a random mapping.

        The generated mapping takes a partial mapping (that may also be empty)
        as starting point. All open mapping decissions were taken by generated
        randomness derived from the given seed.

        :param seed: initial seed for the random generator
        :type seed: integer
        :param part_mapping: partial mapping to start from
        :type part_mapping: Mapping
        """
        # generate new mapping if no partial mapping is given
        if not part_mapping:
            part_mapping = Mapping(self.graph, self.platform)

        # check if the platform/graph is equivalent
        if (
            part_mapping.platform is not self.platform
            or part_mapping.graph is not self.graph
        ):
            raise RuntimeError(
                "rand_map: Try to map partial mapping of platform,dataflow "
                f"{part_mapping.platform.name},{part_mapping.graph.name} to "
                f"{self.platform.name},{self.graph.name}",
            )

        available_processors = list(self.platform.processors())
        if self.resources_first:
            num = random.randint(1, len(available_processors))
            available_processors = random.sample(available_processors, num)

        # map processes
        processes = part_mapping.get_unmapped_processes()
        # print("remaining process list: {}".format(processes))
        for p in processes:
            affinity = None
            scheduler_list = list(self.platform.schedulers())
            while affinity is None and len(scheduler_list) > 0:
                i = random.randrange(0, len(scheduler_list))
                scheduler = scheduler_list.pop(i)
                processors = [
                    proc
                    for proc in scheduler.processors
                    if proc in available_processors
                ]
                if len(processors) == 0:
                    continue
                i = random.randrange(0, len(processors))
                affinity = processors[i]
            if affinity is None:
                raise RuntimeError(
                    f"Could not find an appropriate scheduler for any of "
                    f"the processors: {available_processors}"
                )

            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            part_mapping.add_process_info(p, info)
            log.debug(
                "rand_map: map process %s to scheduler %s and processor %s "
                "(priority: %d)",
                p.name,
                scheduler.name,
                affinity.name,
                priority,
            )

        # map channels
        channels = part_mapping.get_unmapped_channels()
        for c in channels:
            capacity = 16  # fixed channel bound this may cause problems
            suitable_primitives = []
            for p in part_mapping.platform.primitives():
                src = part_mapping.process_info(c.source).affinity
                sinks = [part_mapping.process_info(s).affinity for s in c.sinks]
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError(
                    "rand_map: Mapping failed! No suitable primitive for "
                    "communication from %s to %s found!"
                    % (src.name, str(sinks))
                )
            i = random.randrange(0, len(suitable_primitives))
            primitive = suitable_primitives[i]
            info = ChannelMappingInfo(primitive, capacity)
            part_mapping.add_channel_info(c, info)
            log.debug(
                "rand_map: map channel %s to the primitive %s and bound to %d "
                "tokens" % (c.name, primitive.name, capacity)
            )

            # finally check if the mapping is fully specified
        assert not part_mapping.get_unmapped_processes()
        assert not part_mapping.get_unmapped_channels()
        return part_mapping


class RandomPartialMapperHydra(RandomPartialMapper):
    """This class implements a new constructor for the random_partial mapper in
    order to handle the instantiation via a hydra config file.
    TODO: do we need this??
    """

    def __init__(self, graph, platform, config):
        random_seed = config["mapper"]["random_seed"]
        super(RandomPartialMapperHydra, self).__init__(
            graph, platform, seed=random_seed
        )


class RandomMapper(RandomPartialMapper):
    """Generate a random mapping.

    This class is a FullMapper wrapper for RandomPartialMapper.
    """

    def __init__(
        self, graph, platform, trace, representation, random_seed=None
    ):
        super().__init__(graph, platform, seed=random_seed)

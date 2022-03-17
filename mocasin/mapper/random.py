# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Gerald Hempel, Robert Khasanov

import random

from mocasin.common.mapping import (
    ChannelMappingInfo,
    Mapping,
    ProcessMappingInfo,
)
from mocasin.mapper import BaseMapper
from mocasin.util import logging


log = logging.getLogger(__name__)


class RandomPartialMapper(BaseMapper):
    """Generates a random mapping.

    This class is used to generate a random mapping for a given
    platform and dataflow graph
    """

    def __init__(self, platform, seed=None, resources_first=False):
        """Generate a random mapping for a given platform and application.

        :param platform: a platform
        :type platform: Platform
        :param seed: a random seed for the RNG
        :type seed: int
        :param resources_first: Changes the generation method to first choose
        processors, and then assign processes only to those processors
        :type resources_first: bool
        """
        super().__init__(platform, full_mapper=True)
        if seed is not None:
            random.seed(seed)
        self.seed = seed
        self.resources_first = resources_first

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        """Generate a random mapping.

        The generated mapping takes a partial mapping (that may also be empty)
        as starting point. All open mapping decissions were taken by generated
        randomness derived from the given seed.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param partial_mapping: partial mapping to start from
        :type partial_mapping: Mapping
        """
        # generate new mapping if no partial mapping is given
        if not partial_mapping:
            partial_mapping = Mapping(graph, self.platform)

        # check if the platform/graph is equivalent
        if (
            partial_mapping.platform is not self.platform
            or partial_mapping.graph is not graph
        ):
            raise RuntimeError(
                "rand_map: Try to map partial mapping of platform,dataflow "
                f"{partial_mapping.platform.name},{partial_mapping.graph.name} "
                f"to {self.platform.name},{graph.name}",
            )

        # if no processors supplied
        if not processors:
            processors = list(self.platform.processors())

        if self.resources_first:
            num = random.randint(1, len(processors))
            processors = random.sample(processors, num)

        # map processes
        processes = partial_mapping.get_unmapped_processes()
        # print("remaining process list: {}".format(processes))
        for p in processes:
            affinity = None
            scheduler_list = list(self.platform.schedulers())
            while affinity is None and len(scheduler_list) > 0:
                i = random.randrange(0, len(scheduler_list))
                scheduler = scheduler_list.pop(i)
                procs = [
                    proc for proc in scheduler.processors if proc in processors
                ]
                if len(procs) == 0:
                    continue
                i = random.randrange(0, len(procs))
                affinity = procs[i]
            if affinity is None:
                raise RuntimeError(
                    f"Could not find an appropriate scheduler for any of "
                    f"the processors: {processors}"
                )

            priority = random.randrange(0, 20)
            info = ProcessMappingInfo(scheduler, affinity, priority)
            partial_mapping.add_process_info(p, info)
            log.debug(
                "rand_map: map process %s to scheduler %s and processor %s "
                "(priority: %d)",
                p.name,
                scheduler.name,
                affinity.name,
                priority,
            )

        # map channels
        channels = partial_mapping.get_unmapped_channels()
        for c in channels:
            capacity = 16  # fixed channel bound this may cause problems
            suitable_primitives = []
            for p in partial_mapping.platform.primitives():
                src = partial_mapping.process_info(c.source).affinity
                sinks = [
                    partial_mapping.process_info(s).affinity for s in c.sinks
                ]
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
            partial_mapping.add_channel_info(c, info)
            log.debug(
                "rand_map: map channel %s to the primitive %s and bound to %d "
                "tokens" % (c.name, primitive.name, capacity)
            )

            # finally check if the mapping is fully specified
        assert not partial_mapping.get_unmapped_processes()
        assert not partial_mapping.get_unmapped_channels()
        return partial_mapping


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

    def __init__(self, platform, random_seed=None):
        super().__init__(platform, seed=random_seed)

# Copyright (C) 2019-2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Gerald Hempel, Robert Khasanov


from mocasin.common.mapping import (
    ChannelMappingInfo,
    Mapping,
    ProcessMappingInfo,
)
from mocasin.mapper import BaseMapper
from mocasin.util import logging

log = logging.getLogger(__name__)


class DefaultFullMapper(BaseMapper):
    """Generates a default mapping.

    The mapping is generated by selecting the first available option everywhere.

    Args:
        platform (Platform): a platform
    """

    def __init__(self, platform):
        super().__init__(platform, full_mapper=True)

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        """Generates a random mapping

        The generated mapping takes a partial mapping (that may also be empty)
        as starting point. All open mapping decisions are taken by selecting the
        first option randomness derived from the given seed.

        Args:
            graph (DataflowGraph): a dataflow graph
            trace (TraceGenerator, optional): a trace generator
            representation (MappingRepresentation, optional): a mapping
                representation object
            processors (:obj:`list` of :obj:`Processor`, optional): a list of
                processors to map to. Not yet supported.
            partial_mapping (Mapping, optional): a partial mapping to complete

        Returns:
            Mapping: the generated mapping.

        """

        if processors:
            raise NotImplementedError(
                "This mapper does not support `processors` argument"
            )

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
                f"to {self.platform.name},{graph.name}"
            )

        # map processes
        processes = partial_mapping.get_unmapped_processes()
        # print("remaining process list: {}".format(processes))
        for p in processes:
            scheduler = list(self.platform.schedulers())[0]
            affinity = scheduler.processors[0]
            priority = 0
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
            capacity = 4  # fixed channel bound this may cause problems
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
            primitive = suitable_primitives[0]
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

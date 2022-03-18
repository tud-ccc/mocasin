# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Gerald Hempel, Andres Goens, Robert Khasanov

from mocasin.common.mapping import (
    ChannelMappingInfo,
    Mapping,
    ProcessMappingInfo,
)
from mocasin.mapper import BaseMapper
from mocasin.util import logging

log = logging.getLogger(__name__)


class ComPartialMapper(BaseMapper):
    """Generates a partial mapping by placing communication primitives.
    This generator either requires a partial mapping as input that already
    provides a placement of processes or performs a deterministic placement of
    processes for an incomplete mapping. The generated mapping provides a best
    effort placement of communication primitives.

    This class is used to generate a partial mapping for a given platform and
    dataflow application.
    """

    def __init__(self, platform, full_generator):
        """Generates a partial mapping for a given platform and dataflow
        application.

        :param platform: a platform
        :type platform: Platform
        :param fullGenerator: the associated full mapping generator
        :type fullGererator: FullMapper
        """
        super().__init__(platform, full_mapper=False)
        self.full_generator = full_generator

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        if processors:
            raise NotImplementedError(
                "This mapper does not support `processors` argument"
            )
        res = ComPartialMapper.generate_mapping_static(
            graph, self.platform, partial_mapping=partial_mapping
        )
        return self.full_generator.generate_mapping(
            graph,
            trace=trace,
            representation=representation,
            processors=processors,
            partial_mapping=res,
        )

    @staticmethod
    def generate_mapping_static(graph, platform, partial_mapping=None):
        """Generate a partial mapping from a given partial mapping.

        The generated mapping provides a best effort placement of communication
        structures. The rest is deterministically chosen to the first available
        option.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        :param partial_mapping: a partial mapping with placed processes or an
            empty mapping
        :type partial_mapping: mapping
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a process mapping (for partial mappings
            with incomplete process mappings).
        """
        # RK: this function seems to generate the full mapping

        # generate new mapping if no partial mapping is given
        if not partial_mapping:
            partial_mapping = Mapping(graph, platform)

        # map processes to scheduler and processor if not already done
        processes = partial_mapping.get_unmapped_processes()
        for p in processes:
            scheduler = list(platform.schedulers())[0]
            affinity = scheduler.processors[0]
            priority = 0
            info = ProcessMappingInfo(scheduler, affinity, priority)
            partial_mapping.add_process_info(p, info)
            log.debug(
                "com_map: map process %s to scheduler %s and processor %s "
                "(priority: %d)",
                p.name,
                scheduler.name,
                affinity.name,
                priority,
            )

        # map communication primitives
        channels = partial_mapping.get_unmapped_channels()
        for c in channels:
            capacity = 16  # fixed channel bound this may cause problems
            suitable_primitives = []
            src = partial_mapping.process_info(c.source).affinity
            sinks = [partial_mapping.process_info(s).affinity for s in c.sinks]
            for p in partial_mapping.platform.primitives():
                if p.is_suitable(src, sinks):
                    suitable_primitives.append(p)
            if len(suitable_primitives) == 0:
                raise RuntimeError(
                    "com_map: Mapping failed! No suitable primitive for "
                    "communication from %s to %s found!"
                    % (src.name, str(sinks))
                )

            primitive = ComPartialMapper._get_minimal_costs(
                suitable_primitives, c, src, sinks
            )
            info = ChannelMappingInfo(primitive, capacity)
            partial_mapping.add_channel_info(c, info)
            log.debug(
                "com_map: map channel %s to the primitive %s and bound to %d "
                "tokens" % (c.name, primitive.name, capacity)
            )
        return partial_mapping

    @staticmethod
    def _get_minimal_costs(primitives, channel, src, sinks):
        """Returns the primitive with the minimum of static costs.
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
    """Generates a partial mapping derived from a vector(tuple).
    If the tuple is longer than the num. of processors, it takes
    the rest to be channels.

    This class is used to generate a partial mapping for a given
    platform and dataflow application.
    """

    def __init__(self, graph, platform, full_generator):
        """Generate a partial mapping for a given platform and dataflow
        application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        :param fullGenerator: the associated full mapping generator
        :type fullGererator: PartialMapper
        """
        self.full_mapper = False  # flag indicating the mapper type
        self.platform = platform
        self.graph = graph
        self.full_generator = full_generator
        pes = sorted(list(self.platform.processors()), key=(lambda p: p.name))
        cps = sorted(list(self.platform.primitives()), key=(lambda p: p.name))
        self.pe_vec_mapping = dict(zip(pes, [i for i in range(0, len(pes))]))
        self.cp_vec_mapping = dict(
            zip(cps, [i + len(pes) for i in range(0, len(cps))])
        )
        # build a reverse dict of the dicts (since it is a one-to-one dict)
        # build a reverse dict of the pe_vec_mapping dict
        # (since it is a one-to-one dict)
        self.vec_pe_mapping = dict(
            [(self.pe_vec_mapping[key], key) for key in self.pe_vec_mapping]
        )
        self.vec_cp_mapping = dict(
            [(self.cp_vec_mapping[key], key) for key in self.cp_vec_mapping]
        )

    def get_pe_name_mapping(self):
        """Return the used mapping of PE names to integers"""
        res = {}
        for key in self.pe_vec_mapping:
            res[key.name] = self.pe_vec_mapping[key]
        return res

    def get_cp_name_mapping(self):
        """Return the used mapping of PE names to integers"""
        res = {}
        for key in self.cp_vec_mapping:
            res[key.name] = self.cp_vec_mapping[key]
        return res

    @staticmethod
    def generate_pe_mapping_from_simple_vector(
        vec, graph, platform, vec_pe_mapping, vec_cp_mapping
    ):
        mapping = Mapping(graph, platform)

        # map processes to scheduler and processor
        for i, p in enumerate(
            sorted(graph.processes(), key=(lambda pr: pr.name))
        ):
            # choose the desired processor from list
            pe = vec_pe_mapping[vec[i]]
            # choose the first scheduler from list
            scheduler = platform.find_scheduler_for_processor(pe)
            # set the affinity of the scheduler to the choosen PE
            affinity = pe
            # always set priority to 0
            priority = 0
            info = ProcessMappingInfo(scheduler, affinity, priority)
            # configure mapping
            mapping.add_process_info(p, info)
        if len(vec) > len(graph.processes()):
            if len(vec) != (len(graph.processes()) + len(graph.channels())):
                log.error(
                    f"Invalid mapping vector size. "
                    f"Should be {len(graph.processes())}"
                    f" or {len(graph.processes()) + len(graph.channels())}"
                )
                raise RuntimeError

            n = len(graph.processes())
            for j, c in enumerate(
                sorted(graph.channels(), key=(lambda ch: ch.name))
            ):
                i = j + n
                primitive = vec_cp_mapping[vec[i]]
                capacity = 16  # fixed channel bound this may cause problems
                info = ChannelMappingInfo(primitive, capacity)
                mapping.add_channel_info(c, info)
                log.debug(
                    f"com_map: map channel {c.name} to the primitive "
                    f"{primitive.name} and bound to {capacity} tokens"
                )

        return mapping

    def generate_mapping(self, vec, map_history=None):
        """Generates an unique partial mapping for a numeric vector

        The generated mapping is derived from a numeric vector that describes
        the mapping. Each value in the vector stands for a Process -> PE
        mapping.

        :param reprVec: a vector describing the mapping in the initilized
            representation
        :type reprVec: tuple describing the representation
        :param map_history: exclution list of already generated mappings
        :type map_history: list of mappings
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a process mapping.
        """
        # TODO: This should be adapted to use representations

        log.debug(
            f"ProcPartialMapper: start mapping generation for {self.graph.name}"
            f" on {self.platform.name} with simpleVec: {vec}"
        )

        if map_history is None:
            map_history = []

        # TODO: raise not implemented exception for input of part_mapping

        # generate new mapping
        mapping = ProcPartialMapper.generate_pe_mapping_from_simple_vector(
            vec,
            self.graph,
            self.platform,
            self.vec_pe_mapping,
            self.vec_cp_mapping,
        )
        if mapping in map_history:
            return None
        else:
            return self.full_generator.generate_mapping(
                self.graph, partial_mapping=mapping
            )


class ComFullMapper(BaseMapper):
    """Generates a full mapping by placing communication primitivesi.

    This generator either requires a partial mapping as input that already
    provides a placement of processes or performs a deterministic placement of
    processes for an incomplete mapping. Schedulers are all set to the first
    option. The generated mapping provides a best effort placement of
    communication primitives.

    TODO: the schedulers should first check for unmapped schedulers and only
        deterministically map the missing ones.

    This class is used to generate a full mapping for a given platform and
    dataflow application.
    """

    def __init__(self, platform):
        """Generates a partial mapping for a given platform and dataflow
        application.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        :param fullGenerator: the associated full mapping generator
        :type fullGererator: FullMapper
        """
        super().__init__(platform, full_mapper=True)

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        """Generate mapping.

        Args:
        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param processors: list of processors to map to.
        :type processors: a list[Processor]
        :param partial_mapping: a partial mapping to complete
        :type partial_mapping: Mapping
        """
        # configure policy of schedulers
        if partial_mapping is None:
            partial_mapping = Mapping(graph, self.platform)

        return ComPartialMapper.generate_mapping_static(
            graph, self.platform, partial_mapping=partial_mapping
        )


class InputTupleFullMapper:
    """Generates a mapping from a list given as input"""

    def __init__(self, graph, platform, trace, representation, input_tuple):
        """Generates a default mapping for a given platform and dataflow
        application.

        If (some) channels are missing, they are mapped in a best-effort
        fashion.

        :param graph: a dataflow graph
        :type graph: DataflowGraph
        :param platform: a platform
        :type platform: Platform
        """
        self.full_mapper = True
        self.platform = platform
        self.graph = graph
        if (
            len(graph.processes())
            <= len(input_tuple)
            < len(graph.processes()) + len(graph.channels())
        ):
            self.mapping_list = input_tuple
            com_mapper = ComFullMapper(graph, platform)
            self.proc_mapper = ProcPartialMapper(graph, platform, com_mapper)
        else:
            log.error(
                f"Invalid mapping list size: {len(input_tuple)} "
                f"(expected between {len(graph.processes())} and"
                f"{len(graph.processes())+len(graph.channels())} )"
            )
            raise RuntimeError

    def generate_mapping(self):
        """Generates a mapping from the input list

        :param seed: initial seed for the random generator
        :type seed: integer
        :param part_mapping: partial mapping to start from
        """
        return self.proc_mapper.generate_mapping(self.mapping_list)

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov


class BaseMapper:
    """Base mapper class.

    A flag `full_mapper` indicates whether the mapper generates a complete
    mapping.

    Args:
    :param platform: a platform
    :type platform: Platform
    :param full_mapper: a flag whether the mapper generates the full mapping
    :type full_mapper: bool
    """

    def __init__(self, platform, full_mapper=True):
        self.platform = platform
        self.full_mapper = full_mapper

    def generate_mapping(
        self,
        graph,
        trace=None,
        representation=None,
        processors=None,
        partial_mapping=None,
    ):
        """Generate mapping.

        Generate the mapping for a given graph, trace and representation. If a
        parameter `processors` is given, map processes to the processors listed
        in this argument. If `partial_mapping` is given, use this mapping as a
        starting mapping to complete.

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

        This needs to be overridden by a subclass.

        Raises:
            NotImplementedError
        """
        # Strange arguments in the following subclass:
        # * ProcPartialMapper: vec, map_history
        # TODO: Investigate this
        raise NotImplementedError()

    def generate_pareto_front(self):
        """Generate a Pareto front.

        This method provides default implementation of the Pareto-front
        generation by restricting the set of the resources.
        Some subclasses may provide its own implementation of the method.
        """
        raise NotImplementedError()

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.mapper.pareto import filter_pareto_front
from mocasin.mapper.utils import SimulationManager, SimulationManagerConfig


class BaseMapper:
    """Base mapper class.

    A flag `full_mapper` indicates whether the mapper generates a complete
    mapping.

    Args:
        platform (Platform): a platform
        full_mapper (bool, optional): a flag whether the mapper generates a full
            mapping. This flag should not be exposed to the user of the specific
            mapper, it should be set to a fixed values by each sub-class.
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

        Note:
            This method needs to be overridden by a subclass.

        Args:
            graph (DataflowGraph): a dataflow graph
            trace (TraceGenerator, optional): a trace generator
            representation (MappingRepresentation, optional): a mapping
                representation object
            processors (:obj:`list` of :obj:`Processor`, optional): a list of
                processors to map to.
            partial_mapping (Mapping, optional): a partial mapping to complete

        Returns:
            Mapping: the generated mapping.

        Raises:
            NotImplementedError: If the method was not overriden by a subclass.
        """
        # Strange arguments in the following subclass:
        # * ProcPartialMapper: vec, map_history
        # TODO: Investigate this
        raise NotImplementedError()

    def generate_pareto_front(
        self, graph, trace=None, representation=None, evaluate_metadata=False
    ):
        """Generate a Pareto front.

        This method provides default implementation of the Pareto-front
        generation by restricting the set of the resources.
        Some subclasses may provide its own implementation of the method.

        Args:
            graph (DataflowGraph): a dataflow graph
            trace (TraceGenerator, optional): a trace generator
            representation (MappingRepresentation, optional): a mapping
                representation object
            evaluate_metadata (bool, optional): The flag whther the generated
                mappings are evaluated with the simulator. After evaluation an
                additional Pareto-filtering is performed.

        Returns:
           :obj:`lst` of :obj:`Mapping`: the list of generated mappings
        """
        pareto = []
        pareto_processors = [[]]
        cores = {}

        # collect processors
        all_cores = list(self.platform.processors())
        for core_type, _ in self.platform.get_processor_types().items():
            cores[core_type] = [
                core for core in all_cores if core.type == core_type
            ]

        # Generate different combinations of processors
        for core_type, _ in self.platform.get_processor_types().items():
            new_res = []
            for r in pareto_processors:
                for i in range(len(cores[core_type])):
                    new_res.append(r + cores[core_type][: i + 1])
            pareto_processors = pareto_processors + new_res
        # Strip the empty element
        pareto_processors = pareto_processors[1:]

        for allowed_processors in pareto_processors:
            mapping = self.generate_mapping(
                graph,
                trace=trace,
                representation=representation,
                processors=allowed_processors,
            )
            if mapping:
                pareto.append(mapping)

        if not evaluate_metadata:
            return pareto

        # obtain simulation values
        simulation_manager = SimulationManager(
            self.platform,
            SimulationManagerConfig(jobs=None, parallel=True),
        )
        simulation_manager.simulate(graph, trace, representation, pareto)
        filtered = filter_pareto_front(pareto)

        return filtered

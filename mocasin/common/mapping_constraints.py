# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov


class MappingConstraints:
    """Describe the processors to which each process may be mapped.

    Constraints belong to a particular graph/platform pair. They are expanded
    to concrete platform processors when the object is created, so consumers
    do not need to interpret processor types from an execution trace.
    """

    def __init__(self, graph, platform, eligible_processors):
        self.graph = graph
        self.platform = platform
        self._eligible_processors = {
            process_name: tuple(processors)
            for process_name, processors in eligible_processors.items()
        }

    @classmethod
    def unrestricted(cls, graph, platform):
        """Allow every graph process to run on every platform processor."""
        processors = tuple(platform.processors())
        return cls(
            graph,
            platform,
            {process.name: processors for process in graph.processes()},
        )

    @classmethod
    def from_trace(cls, graph, platform, trace):
        """Create constraints from processor types available in a trace."""
        platform_processors = tuple(platform.processors())
        eligible_processors = {}
        for process in graph.processes():
            supported_types = trace.get_supported_processor_types(process.name)
            if supported_types is None:
                processors = platform_processors
            else:
                processors = tuple(
                    processor
                    for processor in platform_processors
                    if processor.type in supported_types
                )
            if not processors:
                supported = ", ".join(sorted(supported_types)) or "none"
                raise RuntimeError(
                    f"No eligible processor for process '{process.name}' "
                    f"(supported processor types: {supported})"
                )
            eligible_processors[process.name] = processors
        return cls(graph, platform, eligible_processors)

    @classmethod
    def from_hydra(cls, config, graph, platform, trace):
        """Create constraints according to a Hydra configuration."""
        from hydra.utils import instantiate

        constraints = instantiate(config.source, graph, platform)
        if not isinstance(constraints, cls):
            raise TypeError(
                "The configured constraints source must create "
                "MappingConstraints"
            )
        if config.filter_by_trace:
            trace_constraints = cls.from_trace(graph, platform, trace)
            constraints = constraints.intersection(trace_constraints)
        return constraints

    def intersection(self, other):
        """Intersect constraints for the same graph and platform objects."""
        if self.graph is not other.graph or self.platform is not other.platform:
            raise ValueError(
                "Mapping constraints must refer to the same graph and platform"
            )

        eligible_processors = {}
        for process in self.graph.processes():
            other_processors = set(other.eligible_processors(process))
            processors = tuple(
                processor
                for processor in self.eligible_processors(process)
                if processor in other_processors
            )
            if not processors:
                raise RuntimeError(
                    f"No eligible processor for process '{process.name}' "
                    "after intersecting mapping constraints"
                )
            eligible_processors[process.name] = processors

        return MappingConstraints(
            self.graph, self.platform, eligible_processors
        )

    def eligible_processors(self, process):
        """Return the processors to which ``process`` may be mapped."""
        process_name = process if isinstance(process, str) else process.name
        return self._eligible_processors[process_name]

    def eligible_processor_types(self, process):
        """Return the processor types to which ``process`` may be mapped."""
        return frozenset(
            processor.type for processor in self.eligible_processors(process)
        )

    def is_processor_eligible(self, process, processor):
        """Check whether ``process`` may be mapped to ``processor``."""
        return processor in self.eligible_processors(process)

    def is_mapping_eligible(self, mapping):
        """Check whether every process has an eligible processor affinity."""
        for process in mapping.graph.processes():
            info = mapping.process_info(process)
            if info is None or not self.is_processor_eligible(
                process, info.affinity
            ):
                return False
        return True

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Felix Teweleit

from mocasin.ontologies.simvec_mapper import SimpleVectorMapper


class MappingGenerator(object):
    """
    MappingGenerator Base Class
    Other mapping generators should derive from this.
    """

    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return None


class MappingGeneratorPartial(MappingGenerator):
    def __init__(self, partial_mapping, full_mapper):
        self.partial_mapping = partial_mapping
        self.full_mapper = full_mapper

    def __next__(self):
        next_mapping = next(self.full_mapper)
        return next_mapping


class MappingGeneratorOrbit(MappingGenerator):
    def __init__(self, representation, mapping):
        self.orbit_gen = representation.allEquivalent(mapping)
        self.representation = representation

    def __next__(self):
        next_mapping = next(self.orbit_gen)
        return next_mapping


class MappingGeneratorSimvec(MappingGenerator):
    def __init__(
        self,
        graph,
        platform,
        mappingConstraints,
        sharedCoreConstraints,
        processingConstraints,
        vec,
    ):
        self.mapper = SimpleVectorMapper(
            graph,
            platform,
            mappingConstraints,
            sharedCoreConstraints,
            processingConstraints,
            vec,
        )

    def __next__(self):
        next_mapping = next(self.mapper)
        return next_mapping

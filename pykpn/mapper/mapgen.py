#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Andrés Goens, Felix Teweleit

from pykpn.mapper.simvec_mapper import SimpleVectorMapper

"""
MappingGenerator Base Class
Other mapping generators should derive from this.
"""
class MappingGenerator(object):
    def __init__(self):
        pass
    def __iter__(self):
        return self
    def __next__(self):
        return None


class MappingGeneratorPartial(MappingGenerator):
    def __init__(self,partial_mapping,full_mapper):
        self.partial_mapping = partial_mapping
        self.full_mapper = full_mapper
    def __next__(self):
        next_mapping = next(self.full_mapper)
        return next_mapping

class MappingGeneratorOrbit(MappingGenerator):
    def __init__(self,representation,mapping):
        self.orbit_gen = representation.allEquivalent(representation.toRepresentation(mapping))
        self.representation = representation
        self.next_mapping_index = 0

    def __next__(self):
        try:
            next_mapping = self.orbit_gen[self.next_mapping_index]
        except:
            raise StopIteration()
        self.next_mapping_index += 1
        return next_mapping

class MappingGeneratorSimvec(MappingGenerator):
    def __init__(self, kpn, platform, mappingConstraints, sharedCoreConstraints, processingConstraints, vec):
        self.mapper = SimpleVectorMapper(kpn, platform, mappingConstraints, sharedCoreConstraints, processingConstraints, vec)
    
    def __next__(self):
        next_mapping = next(self.mapper)
        return next_mapping
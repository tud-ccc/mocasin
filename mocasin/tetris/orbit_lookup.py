# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.representations import SymmetryRepresentation


class OrbitLookupManager:
    """Orbit lookup manager.

    Calculating the orbit takes much time. This class is needed to reduce such
    overhead by caching the already calculated orbits.
    """

    def __init__(self, platform):
        self.platform = platform
        self._representations = {}
        self._orbits = {}
        pass

    def _calculate_orbit(self, graph, mapping):
        """Calcualtes the orbit for the mapping.

        Args:
            graph (DataflowGraph): a dataflow application
            mappings (Mapping): a mapping

        Returns: list of mappings, forming the orbit.
        """
        if graph not in self._representations:
            self._representations[graph] = SymmetryRepresentation(
                graph, self.platform
            )
        equivalent_mappings = self._representations[graph].allEquivalent(
            mapping
        )
        return equivalent_mappings

    def get_orbit(self, graph, mapping):
        """ Lookups the orbits, if not existed, calculates the orbit. """
        if graph not in self._orbits:
            self._orbits[graph] = {}
        if mapping not in self._orbits[graph]:
            self._orbits[graph][mapping] = self._calculate_orbit(graph, mapping)
        return self._orbits[graph][mapping]

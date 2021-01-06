# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.representations import SymmetryRepresentation


class OrbitLookupManager:
    """ Orbit lookup manager.

    Calculating the orbit takes much time. This class is needed to reduce such
    overhead by caching the already calculated orbits.
    """
    def __init__(self, platform):
        self.platform = platform
        self._representations = {}
        self._orbits = {}
        pass

    def _calculate_orbit(self, kpn, mapping):
        """ Calcualtes the orbit for the mapping.

        Args:
            kpn (KpnGraph): a kpn application
            mappings (Mapping): a mapping

        Returns: list of mappings, forming the orbit.
        """
        if kpn not in self._representations:
            self._representations[kpn] = SymmetryRepresentation(
                kpn, self.platform)
        equivalent_mappings = self._representations[kpn].allEquivalent(mapping)
        return equivalent_mappings

    def get_orbit(self, kpn, mapping):
        """ Lookups the orbits, if not existed, calculates the orbit. """
        if kpn not in self._orbits:
            self._orbits[kpn] = {}
        if mapping not in self._orbits[kpn]:
            self._orbits[kpn][mapping] = self._calculate_orbit(kpn, mapping)
        return self._orbits[kpn][mapping]

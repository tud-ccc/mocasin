# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.representations import SymmetryRepresentation

from itertools import count
from threading import Lock


class OrbitLookupEntry:
    """Orbit lookup entry.

    This class contains information about the mapping orbit, and stores
    oreviously found orbits in a cache. To iterate the values the class return
    the generator obect, which first yields the previously found mappings, then
    it generates new mappings.
    """

    def __init__(self, platform, graph, mapping, only_support=True):
        self.platform = platform
        self.graph = graph
        self.mapping = mapping
        self._lock = Lock()
        self._representation = SymmetryRepresentation(graph, platform)
        self._cached_mappings = []
        self._orbit_generator = self._representation.allEquivalent(
            mapping, only_support=only_support
        )

    def _at(self, i):
        with self._lock:
            cache_size = len(self._cached_mappings)
            if i < cache_size:
                return self._cached_mappings[i]
            if i > cache_size:
                raise RuntimeError(
                    f"Trying to access mapping#{i} while only {cache_size} were"
                    " generated. Mapping must be accessed in-order."
                )
            try:
                m = next(self._orbit_generator)
                self._cached_mappings.append(m)
            except StopIteration:
                m = None
            return m

    def get_generator(self):
        for i in count():
            m = self._at(i)
            if m is None:
                break
            yield m


class OrbitLookupManager:
    """Orbit lookup manager.

    Calculating the orbit takes much time. This class is needed to reduce such
    overhead by caching the already calculated orbits.
    """

    def __init__(self, platform, only_support=True):
        self.platform = platform
        self._only_support = only_support
        self._entries = {}

    def get_orbit_entry(self, graph, mapping):
        """Lookups the orbits, if not existed, calculates the orbit."""
        if graph not in self._entries:
            self._entries[graph] = {}
        if mapping not in self._entries[graph]:
            self._entries[graph][mapping] = OrbitLookupEntry(
                self.platform, graph, mapping, only_support=self._only_support
            )
        return self._entries[graph][mapping]

    def remove_graph_orbit_entries(self, graph):
        """Remove graph's orbits entries."""
        self._entries.pop(graph, None)

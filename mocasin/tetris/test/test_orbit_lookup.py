# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.tetris.orbit_lookup import OrbitLookupManager


def test_orbit_generator(platform, graph, mapping):
    orbit_lookup_manager = OrbitLookupManager(platform, only_support=False)
    orbit_entry = orbit_lookup_manager.get_orbit_entry(graph, mapping)

    gen1 = orbit_entry.get_generator()
    gen2 = orbit_entry.get_generator()

    # No cashed mappings
    assert len(orbit_entry._cached_mappings) == 0

    # First mapping should be the same as original:
    m = next(gen1)
    assert m.to_list() == mapping.to_list()
    m = next(gen2)
    assert m.to_list() == mapping.to_list()
    assert len(orbit_entry._cached_mappings) == 1

    # Check that the mapping is not added twice to the cashed list
    gen2_m = next(gen2)
    gen1_m = next(gen1)
    assert len(orbit_entry._cached_mappings) == 2
    assert gen1_m == gen2_m

    # Get more values
    gen1_m_3 = next(gen1)
    next(gen1)
    next(gen1)
    next(gen1)
    assert len(orbit_entry._cached_mappings) == 6

    # Check the total size of the orbit
    orbit_list = [x for x in orbit_entry.get_generator()]
    assert len(orbit_entry._cached_mappings) == 12
    assert len(orbit_list) == 12

    # check that the old generator still produce correct value
    gen2_m_3 = next(gen2)
    assert gen1_m_3 == gen2_m_3


def test_orbit_support_generator(platform, graph, mapping):
    orbit_lookup_manager = OrbitLookupManager(platform, only_support=True)
    orbit_entry = orbit_lookup_manager.get_orbit_entry(graph, mapping)

    # Check the total size of the orbit
    orbit_list = [x for x in orbit_entry.get_generator()]
    assert len(orbit_entry._cached_mappings) == 6
    assert len(orbit_list) == 6

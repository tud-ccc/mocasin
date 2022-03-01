# Copyright (C) 2022 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.mapper.pareto import mark_pareto_front, filter_pareto_front
from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper


def test_filter_pareto_front(graph, platform_odroid):
    com_mapper = ComFullMapper(graph, platform_odroid)
    mapper = ProcPartialMapper(graph, platform_odroid, com_mapper)

    mappings = []

    mapping = mapper.generate_mapping([0, 0])
    mapping.metadata.exec_time = 10.2
    mapping.metadata.energy = 21.45
    mappings.append(mapping)

    mapping = mapper.generate_mapping([0, 0])
    mapping.metadata.exec_time = 20
    mapping.metadata.energy = 31.45
    mappings.append(mapping)

    mapping = mapper.generate_mapping([1, 1])
    mapping.metadata.exec_time = 30
    mapping.metadata.energy = 50
    mappings.append(mapping)

    mapping = mapper.generate_mapping([0, 1])
    mapping.metadata.exec_time = 5.2
    mapping.metadata.energy = 31.15
    mappings.append(mapping)

    flags = mark_pareto_front(mappings)
    assert flags == [True, False, True, True]

    pareto = filter_pareto_front(mappings)
    assert len(pareto) == sum(flags)

    pareto_iter = iter(pareto)
    for m, f in zip(mappings, flags):
        if not f:
            continue
        pm = next(pareto_iter)
        assert pm is m

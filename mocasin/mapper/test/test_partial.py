# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.mapper.partial import InputTupleFullMapper


def test_input_tuple_full_mapper(graph, platform, trace, representation):
    mapper = InputTupleFullMapper(platform, [1, 0])

    mapping = mapper.generate_mapping(
        graph, trace=trace, representation=representation
    )

    processes = sorted(graph.processes(), key=lambda process: process.name)
    assert mapping.process_info(processes[0]).affinity.name == "processor1"
    assert mapping.process_info(processes[1]).affinity.name == "processor0"

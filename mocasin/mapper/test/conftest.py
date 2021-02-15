# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import pytest

from mocasin.common.graph import DataflowProcess, DataflowGraph
from mocasin.common.platform import Platform, Processor, Scheduler

from mocasin.representations import SimpleVectorRepresentation
from mocasin.common.trace import EmptyTrace


@pytest.fixture
def num_procs():
    return 7


@pytest.fixture
def graph():
    k = DataflowGraph("a")
    k.add_process(DataflowProcess("a"))
    k.add_process(DataflowProcess("b"))
    return k


@pytest.fixture
def platform(num_procs, mocker):
    p = Platform("platform")
    procs = []
    for i in range(num_procs):
        proc = Processor(
            ("processor" + str(i)), "proctype", mocker.Mock(), mocker.Mock()
        )
        procs.append(proc)
        p.add_processor(proc)
    policies = [mocker.Mock()]
    sched = Scheduler("name", procs, policies)
    p.add_scheduler(sched)
    return p


@pytest.fixture
def representation(graph, platform):
    return SimpleVectorRepresentation(graph, platform)


@pytest.fixture
def representation_pbc(graph, platform):
    return SimpleVectorRepresentation(
        graph, platform, periodic_boundary_conditions=True
    )


@pytest.fixture
def trace():
    return EmptyTrace()

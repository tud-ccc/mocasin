# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from mocasin.representations import SimpleVectorRepresentation


def test_crossover_exchanges_both_parents(mocker):
    mocker.patch("mocasin.representations.random.sample", return_value=[1])
    representation = object.__new__(SimpleVectorRepresentation)
    first = [0, 0]
    second = [1, 1]

    representation._crossover(first, second, 1)

    assert first == [0, 1]
    assert second == [1, 0]

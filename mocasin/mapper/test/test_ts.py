# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from itertools import product

import pytest

from mocasin.mapper.tabu_search import TabuSearchMapper
from mocasin.mapper.test.mock_cache import MockMappingCache


@pytest.fixture
def mapper(platform, simres_evaluation_function, mocker):
    m = TabuSearchMapper(
        platform, 42, False, 100, 10, 10, 10, 2, False, 10, False, True, 4
    )
    m._simulation_manager = MockMappingCache(simres_evaluation_function, mocker)
    return m


def test_ts(mapper, graph, trace, representation, evaluation_function):
    result_mapper = mapper.generate_mapping(
        graph, trace=trace, representation=representation
    )
    results = [
        (evaluation_function([x, y]), x, y)
        for x, y in product(range(7), range(7))
    ]
    expected = set([(x, y) for (_, x, y) in sorted(results)[:3]])

    # result is top 3 best
    assert tuple(result_mapper.to_list()) in expected


def test_update_candidate_moves(mapper, graph, trace, representation):
    mapper.update_candidate_moves(graph, trace, representation, [3, 3])
    moves = [move for (move, _) in mapper.moves]
    # fmt: off
    expected = {
        (0, 1), (0, 0), (1, 0), (-1, 1), (1, 1), (0, -2), (-2, 0), (1, -1),
        (2, 0), (0, 2), (0, -1), (-1, 0), (-1, -1), (-1, -2), (-1, 2), (1, 2),
        (1, -2), (-2, -1), (-2, 1), (2, 1), (2, -1),
    }
    # fmt: on

    assert set(moves).issubset(expected)

    mapper.update_candidate_moves(graph, trace, representation, [0, 0])
    moves = [move for (move, _) in mapper.moves]
    expected = {(0, 1), (0, 0), (1, 0), (1, 1), (2, 0), (0, 2), (1, 2), (2, 1)}

    assert set(moves).issubset(expected)

    mapper.update_candidate_moves(graph, trace, representation, [6, 6])
    moves = [move for (move, _) in mapper.moves]
    # fmt: off
    expected = {
        (0, -1), (0, 0), (-1, 0), (-1, -1),
        (-2, 0), (0, -2), (-1, -2), (-2, -1),
    }
    # fmt: on

    assert set(moves).issubset(expected)


def test_move(mapper):
    mapper.moves = [((0, 1), 115), ((1, 0), 110), ((-1, 0), 90)]
    mapper.tabu_moves = {(-1, 0): 1, (1, 0): 2}

    # if tabu es better than best, choose inspite of tabu
    assert mapper.move(100) == ((-1, 0), 90)

    mapper.moves = [((0, 1), 115), ((1, 0), 110), ((1, 1), 120)]

    # (0,1) still in tabu, should not be chosen
    assert mapper.move(100) == ((0, 1), 115)

    # now (1,0) not in tabu anymore (instantiated with tenure 2)
    assert mapper.move(100) == ((1, 0), 110)

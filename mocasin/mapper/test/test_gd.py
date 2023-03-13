# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from itertools import product

import pytest
import numpy as np

from mocasin.mapper.gradient_descent import GradientDescentMapper
from mocasin.mapper.test.mock_cache import MockMappingCache


@pytest.fixture
def evaluation_function_gradient():
    return lambda m: [
        np.sin(1 - 2 * m[1]) * np.sin(m[0] - m[1]),
        1 / 2 * (3 * np.cos(1 + m[0] - 3 * m[1]) + np.cos(1 - m[0] - m[1])),
    ]


@pytest.fixture
def mapper(platform, simres_evaluation_function, mocker):
    m = GradientDescentMapper(
        platform, 100, 2, 42, False, False, 10, False, True, 4
    )
    m._simulation_manager = MockMappingCache(simres_evaluation_function, mocker)
    return m


def test_gd(mapper, graph, trace, representation_pbc, evaluation_function):
    result_mapper = mapper.generate_mapping(
        graph, trace=trace, representation=representation_pbc
    )
    results = [
        (evaluation_function([x, y]), x, y)
        for x, y in product(range(7), range(7))
    ]
    expected = set([(x, y) for (_, x, y) in sorted(results)[:3]])

    # result is top 3 best
    assert tuple(result_mapper.to_list()) in expected


def test_gradient(
    graph,
    trace,
    representation,
    mapper,
    evaluation_function,
    evaluation_function_gradient,
):
    mapper.dim = 2
    good = 0
    bad = 0

    for x, y in product(range(1, 6), range(1, 6)):
        # > max(evaluation_function)
        mapper.best_exec_time = 3
        mapper.best_mapping = np.zeros(mapper.dim)
        actual_grad = np.array(evaluation_function_gradient([x, y]))
        calculated_grad = mapper.calculate_gradient(
            graph, trace, representation, [x, y], evaluation_function([x, y])
        )

        if not np.allclose(actual_grad, np.zeros(mapper.dim)):
            actual_grad_normed = actual_grad * 1 / np.linalg.norm(actual_grad)
        else:
            actual_grad_normed = actual_grad

        if not np.allclose(calculated_grad, np.zeros(mapper.dim)):
            calculated_grad_normed = (
                calculated_grad * 1 / np.linalg.norm(calculated_grad)
            )
        else:
            calculated_grad_normed = calculated_grad

        if np.allclose(actual_grad_normed, calculated_grad_normed, atol=0.4):
            good += 1
        else:
            bad += 1

    assert good > bad

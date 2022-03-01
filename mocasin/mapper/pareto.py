# Copyright (C) 2022 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import numpy as np


def _is_pareto_efficient(costs):
    """Find the Pareto-efficient points.

    Args:
        costs: An (n_points, n_costs) array

    Returns:
        A (n_points, ) boolean array, indicating whether each point is Pareto
            efficient
    """
    # Taken from
    # https://stackoverflow.com/questions/32791911/fast-calculation-of-pareto-front-in-python # noqa
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            # Keep any point with a lower cost
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)
            # And keep self
            is_efficient[i] = True
    return is_efficient


def mark_pareto_front(mappings):
    """Find Pareto-efficient mappings.

    Each mapping is characterized with the following costs:
    * processor costs - 0-1 value for each processor
    * execution time - a float value
    * energy consumotion - a float value

    Note that this function does not transform mappings into canonical form.

    Args:
        mappings: a list of mappings

    Returns:
        A boolean list, indicating whether each mapping is Paretor efficient.
    """
    if not mappings:
        return []

    processors = mappings[0].platform.processors()
    costs = np.empty((0, len(processors) + 2), float)
    for m in mappings:
        lm = [0] * len(processors)
        procs = m.get_used_processors()
        for i, p in enumerate(processors):
            if p in procs:
                lm[i] = 1
        lm.append(m.metadata.exec_time)
        lm.append(m.metadata.energy)
        costs = np.append(costs, [lm], axis=0)
    flags = _is_pareto_efficient(costs)
    return list(flags)


def filter_pareto_front(mappings):
    """Filter Pareto-efficient mappings.

    Each mapping is characterized with the following costs:
    * processor costs - 0-1 value for each processor
    * execution time - a float value
    * energy consumotion - a float value

    Note that this function does not transform mappings into canonical form.

    Args:
        mappings: a list of mappings

    Returns:
        A list of mappings forming the Pareto front.
    """
    flags = mark_pareto_front(mappings)
    res = [m for m, f in zip(mappings, flags) if f]
    return res

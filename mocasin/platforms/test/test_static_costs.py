# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens

import pytest

@pytest.xfail("There is a bug in NoCs produced by the platform designer")
def test_static_costs(platform):
    sizes = [1, 8, 64, 1024]
    for prim in platform.primitives():
        for src in prim.producers:
            for tgt in prim.consumers:
                static_costs = [
                    prim.static_costs(src, tgt, token_size=size)
                    for size in sizes
                ]
                for i in range(len(sizes) - 1):
                    # costs don't decrease for larger tokens
                    assert static_costs[i] <= static_costs[i + 1]

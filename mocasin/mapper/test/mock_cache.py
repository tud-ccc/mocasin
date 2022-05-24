# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens

from mocasin.mapper.utils import Statistics


class MockMappingCache:
    def __init__(self, simres_evaluation_function, mocker):
        self.simulate = lambda g, t, r, x: list(
            map(simres_evaluation_function, x)
        )
        self.statistics = Statistics(mocker.Mock())

    def reset_statistics(self):
        pass

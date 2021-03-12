# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

from mocasin.mapper.genetic import Objectives

import pytest


def test_objectives():
    flags = Objectives.from_string("exec_time;energy")

    assert Objectives.EXEC_TIME in flags
    assert Objectives.ENERGY in flags
    assert Objectives.RESOURCES not in flags

    flags = Objectives.from_string("resources")

    assert Objectives.EXEC_TIME not in flags
    assert Objectives.ENERGY not in flags
    assert Objectives.RESOURCES in flags


@pytest.mark.raises(exception=RuntimeError)
def test_objectives_raise():
    flags = Objectives.from_string("dumb")

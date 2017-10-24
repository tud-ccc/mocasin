# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import simpy

import pytest


@pytest.fixture
def env():
    return simpy.Environment()

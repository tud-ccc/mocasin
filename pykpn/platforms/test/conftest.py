# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
from pykpn.platforms.platformDesigner import platformDesigner
from pykpn.common.platform import Platform

@pytest.fixture
def DAG():
    return {0 : [1,2],
            1 : [3,4],
            2 : [5,6],
            3 : [7],
            4 : [9],
            5 : [],
            6 : [],
            7 : [],
            8 : [],
            9 : [8]}
    
@pytest.fixture
def cyclicGraph():
    return {0 : [1,4,7],
            1 : [0,2,4],
            2 : [1,3,7],
            3 : [2,6,8],
            4 : [0,1,5,7],
            5 : [4,6,8],
            6 : [3,5],
            7 : [0,2,4,8],
            8 : [3,5,7,9],
            9 : [8]}
    
@pytest.fixture
def designer():
    platformObject = Platform('test')
    designer = platformDesigner(platformObject)
    designer.setSchedulingPolicy('TestPolicy', 1000)
    return designer




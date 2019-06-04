# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
import random as rnd

from pykpn.gui import dataTemplates


@pytest.fixture
def simpleList(length):
    result = []
    for i in range(0, length):
        result.append(rnd.randint(0, 1000))
    return result

@pytest.fixture
def nestedList(depth):
    length = rnd.randint(0, 100)
    
    result = []
    
    for i in range(0, length):
        result.append(rnd.randint(0, 1000))
    
    for i in range(0, depth):
        tmpList = []
        for j in range(0, length):
                tmpList.append(result)
        result = tmpList
        
    return result

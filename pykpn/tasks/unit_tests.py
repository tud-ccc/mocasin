# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
import os

def unit_tests(cfg):
    print(os.getcwd())
    pytest.main(["../../../pykpn/",])
    
    
if __name__ == "__main__":
    unit_tests(None)
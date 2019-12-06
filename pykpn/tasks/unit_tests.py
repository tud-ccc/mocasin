# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import pytest
import os

def unit_tests(cfg):
    pytest.main()
    
if __name__ == "__main__":
    print(os.getcwd())
    unit_tests(None)
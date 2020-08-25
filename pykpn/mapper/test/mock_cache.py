from unittest.mock import Mock
from pykpn.mapper.utils import Statistics

class MockMappingCache():
    def __init__(self,evaluation_function):
        self.simulate = (lambda x: list(map(evaluation_function,x)))
        self.statistics = Statistics(Mock(),0,False)



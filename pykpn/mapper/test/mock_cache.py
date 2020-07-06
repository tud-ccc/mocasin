from unittest.mock import Mock
from pykpn.mapper.utils import Statistics

class MockMappingCache():
    def __init__(self,evaluation_function):
        self.evaluate_mapping = evaluation_function
        self.statistics = Statistics(Mock(),0,False)



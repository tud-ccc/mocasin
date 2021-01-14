from mocasin.mapper.utils import Statistics

class MockMappingCache():
    def __init__(self,evaluation_function, mocker):
        self.simulate = (lambda x: list(map(evaluation_function,x)))
        self.statistics = Statistics(mocker.Mock(),0,False)



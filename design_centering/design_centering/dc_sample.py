import dc_volume

class Sample(object):
    
    def __init__(self):
        print("init sample")
        self.feasible = False
    
    def gen_random_sample(self):
        print("generate random sample")

    def gen_sample_in_vol(self, vol):
        print("generate random sample from vol")

    def print2tuple(self):
        return (1,2)

    def uniform_distibution(self):
        pass
    
    def gaussian_distibution(self):
        pass

class SampleSet(object):

    def add_sample(self, sample):
        pass
    
    def get_feasible(self):
        print("is feasible?")
        return 0

    def get_infeasible(self):
        print("is infeasible?")

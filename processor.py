import simpy

class Processor(simpy.resources.resource.Resource):
    """
    A SimPy resource that represents a processor in the target platform.
    """

    def __init__(self, env, name, type, frequency):
        """
        Constructor

        :param env the SimPy environment
        :param name the processor name
        :param type the processor type
        :param frequency the processor frequency
        """
        self.name = name
        self.type = type
        self.frequency = frequency

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

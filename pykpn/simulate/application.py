class RuntimeApplication:
    '''
    Represents an instance of a kpn application at runtime.
    '''

    def __init__(self, name, kpn_graph, mapping, trace_readers,
                 start_at_tick=0):
        '''
        Initialize a RuntimeApplication.
        :param name:          name of the application
        :param kpn_graph:     the corresponding KpnGraph object
        :param mapping:       the corresponding Mapping object
        :param trace_readers: a dictionary of process names and TraceReader
                              objects
        '''
        self.name = name
        self.kpn_graph = kpn_graph
        self.mapping = mapping
        self.trace_readers = trace_readers
        self.start_at_tick = start_at_tick

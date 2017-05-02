class Application:
    def __init__(self, name, graph, mapping, traceReaders, ini_time):
        self.name = name
        self.graph = graph
        self.mapping = mapping
        self.traceReaders = traceReaders
        self.ini_time=ini_time

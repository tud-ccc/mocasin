class Application:
    def __init__(self, name, graph, mapping, traceReaders, start_time):
        self.name = name
        self.graph = graph
        self.mapping = mapping
        self.traceReaders = traceReaders
        self.start_time=start_time

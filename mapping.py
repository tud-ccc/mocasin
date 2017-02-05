class ChannelInfo:
    name = None
    capacity = None
    fromProcessor = None
    toProcessor = None
    viaMemory = None
    primitive = None


class SchedulerInfo:
    name = None
    policy = None
    processNames = None
    processorNames = None


class Mapping:
    schedulers = []
    channels = []

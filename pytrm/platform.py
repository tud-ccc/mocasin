# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from enum import Enum
import parser


class Memory:

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.endpoint = None


class Processor:

    def __init__(self, name, type, frequency):
        self.name = name
        self.type = type
        self.frequency = frequency
        self.endpoint = None

    def cyclesToTicks(self, cycles):
        tmp = float(cycles) * 1000000000000 / float(self.frequency)
        return int(tmp)


class Endpoint:

    def __init__(self, processor, memory):
        assert processor.endpoint is None
        assert memory.endpoint is None

        self.processor = processor
        self.memory = memory

        processor.endpoint = self
        memory.endpoint = self

        self.outgoing_link = None
        self.incoming_link = None


class Router:
    outgoing_links = []
    incoming_links = []


class XYRouter(Router):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def hop(self, target):
        """
        Do one hop into the direction of the target.
        """

        assert isinstance(target, Endpoint)
        assert target.incoming_link is not None
        assert isinstance(target.incoming_link._from, XYRouter)

        targetRouter = target.incoming_link._from

        if self.x == targetRouter.x and self.y == targetRouter.y:
            return target.incoming_link

        for link in self.outgoing_links:
            if link.link_type == LinkType.RouterToRouter:
                if ((self.x < targetRouter.x and link._to.x == self.x + 1 and
                     link._to.y == self.y) or
                    (self.x > targetRouter.x and link._to.x == self.x - 1 and
                     link._to.y == self.y) or
                    (self.x == targetRouter.x and self.y < targetRouter.y and
                     link._to.y == self.y + 1 and link._to.x == self.x) or
                    (self.x == targetRouter.x and self.y > targetRouter.y and
                     link._to.y == self.y - 1 and link._to.x == self.x)):
                    return link

        assert False, "Did not find a valid route!"


class LinkType(Enum):
    RouterToRouter = 0
    RouterToEndpoint = 1
    EndpointToRouter = 2


class Link:

    def __init__(self, bandwidth):
        self._to = None
        self._from = None
        self.link_type = None
        self.bandwidth = bandwidth

    def connect(self, _from, _to):
        assert self._from is None and self._to is None and \
            self.link_type is None, "link is alreay connected!"

        self._from = _from
        self._to = _to

        if isinstance(_from, Router) and isinstance(_to, Router):
            self.link_type = LinkType.RouterToRouter
            _from.outgoing_links.append(self)
            _to.incoming_links.append(self)
        elif isinstance(_from, Endpoint) and isinstance(_to, Router):
            self.link_type = LinkType.EndpointToRouter
            assert _from.outgoing_link is None, \
                "Endpoint is already connected!"
            _from.outgoing_link = self
            _to.incoming_links.append(self)
        elif isinstance(_from, Router) and isinstance(_to, Endpoint):
            self.link_type = LinkType.RouterToEndpoint
            assert _to.incoming_link is None, "Endpoint is already connected!"
            _to.incoming_link = self
            _from.outgoing_links.append(self)
        else:
            assert False, "Atempted to connect some unsopported objects!"


class Primitive:

    def __init__(self, typename, _from, _to, _via, f_consume, f_transport,
                 f_produce):
        self.typename = typename
        self._from = _from
        self._to = _to
        self._via = _via
        self.f_produce = parser.expr(f_produce).compile()
        self.f_consume = parser.expr(f_consume).compile()
        self.f_transport = parser.expr(f_transport).compile()

    def getConsumeCosts(self, x):
        return eval(self.f_consume)

    def getTransportCosts(self, x):
        return eval(self.f_transport)

    def getProduceCosts(self, x):
        return eval(self.f_produce)


class NocPrimitive(Primitive):

    def __init__(self, typename, _from, _to, _via, f_consume, f_transport,
                 f_produce, consumeHops, consumeBandwidth, transportHops,
                 transportBandwidth, produceHops, produceBandwidth):
        Primitive.__init__(self, typename, _from, _to, _via, f_consume,
                           f_transport, f_produce)
        self.consumeHops = consumeHops
        self.consumeBandwidth = consumeBandwidth
        self.produceHops = produceHops
        self.produceBandwidth = produceBandwidth
        self.transportHops = transportHops
        self.transportBandwidth = transportBandwidth

    def getConsumeCosts(self, x):
        hops = self.consumeHops
        bw = self.consumeBandwidth
        return eval(self.f_consume)

    def getTransportCosts(self, x):
        hops = self.transportHops
        bw = self.transportBandwidth
        return eval(self.f_transport)

    def getProduceCosts(self, x):
        hops = self.produceHops
        bw = self.produceBandwidth
        return eval(self.f_produce)


class Platform(object):
    routers = []
    links = []
    processors = []
    memories = []
    endpoints = []
    primitives = []

    def find_route(self, _from, _to):
        assert isinstance(_from, Endpoint)
        assert isinstance(_to, Endpoint)

        current_pos = _from
        target_pos = _to

        if current_pos is target_pos:
            return []

        hops = [current_pos.outgoing_link]
        current_pos = current_pos.outgoing_link._to

        while current_pos is not target_pos:
            link = current_pos.hop(target_pos)
            hops.append(link)
            current_pos = link._to

        return hops

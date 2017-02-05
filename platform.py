# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from enum import Enum


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

    def __init__(self, platform, typename, _from, _to, _via,
                 f_produce, f_consume, f_transport):
        self.typename = typename
        self._from = _from
        self._to = _to
        self._via = _via
        self.f_produce = f_produce
        self.f_consume = f_consume
        self.f_transport = f_transport

        self.route_to_mem = platform.find_route(_from.endpoint, _via.endpoint)
        self.route_from_mem = platform.find_route(_via.endpoint, _to.endpoint)

        pass


# Primitive = namedtuple("Primitive", "name from_processor to_processor
# via_memory f_produce f_consume f_transport")


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

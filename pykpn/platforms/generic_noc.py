# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from ..common import CommunicationPhase
from ..common import CommunicationResource
from ..common import FrequencyDomain
from ..common import Platform
from ..common import Primitive
from ..common import Processor
from ..common import MeshNoc
from ..common import TorusNoc
from ..common import Scheduler
from ..common import Storage


class GenericNocPlatform(Platform):

    def createConsumerPrimitive(self, noc, pe_from, pe_to, mem):
        p = Primitive('consumer_cp', pe_from, mem, pe_to)

        links = noc.get_route(pe_from.name, pe_to.name)

        prepare = CommunicationPhase('prepare_remote_produce',
                                     [self.remote_fifo_access],
                                     'write')
        transport = CommunicationPhase('transport', links, 'write',
                                       ignore_latency=True)
        consume = CommunicationPhase('local_comsume',
                                     [self.local_fifo_access],
                                     'read')

        p.produce.append(prepare)
        p.produce.append(transport)
        p.consume.append(consume)

        return p

    def createProducerPrimitive(self, noc, pe_from, pe_to, mem):
        p = Primitive('producer_cp', pe_from, mem, pe_to)

        request_links = noc.get_route(pe_to.name, pe_from.name)
        transport_links = noc.get_route(pe_from.name, pe_to.name)

        produce = CommunicationPhase('local_produce',
                                     [self.local_fifo_access],
                                     'write')

        prepare = CommunicationPhase('prepare_remote_consume',
                                     [self.remote_fifo_access],
                                     'read')
        request = CommunicationPhase('read_request',
                                     [request_links[0], request_links[-1]],
                                     'read',
                                     size=0)
        transport = CommunicationPhase('transport',
                                       transport_links,
                                       'read')

        p.produce.append(produce)
        p.consume.append(prepare)
        p.consume.append(request)
        p.consume.append(transport)

        return p

    def __init__(self, architecture, x, y, endpoints_per_router=2):
        Platform.__init__(self)

        self.frequency_domain = FrequencyDomain('fd_sys', 200000000)
        self.local_fifo_access = CommunicationResource('local_fifo_access',
                                                       self.frequency_domain,
                                                       164,  # read latency,
                                                       205)  # write latency
        self.remote_fifo_access = CommunicationResource('remote_fifo_access',
                                                        self.frequency_domain,
                                                        242,  # read latency,
                                                        299)  # write latency

        noc = None
        if architecture == 'mesh':
            noc = MeshNoc(self.frequency_domain, 8, 8, "yx", x, y)
        elif architecture == 'torus':
            noc = TorusNoc(self.frequency_domain, 8, 8, "yx", x, y)
        else:
            raise ValueError('specified architecture does not exist')

        z = 0  # id of current pe
        for i in range(x):
            for j in range(y):
                for k in range(endpoints_per_router):
                    processor = Processor("PE" + str(z), 'RISC',
                                          self.frequency_domain, 1000, 1000)
                    self.processors.append(processor)

                    memory = Storage("sp" + str(z), self.frequency_domain,
                                     1, 1, 8, 8, False)
                    self.communication_resources.append(memory)

                    noc.create_ni([memory, processor], i, j)

                    # define a scheduler per PE, the scheduling delay is
                    # arbitrarily chosen
                    scheduler = Scheduler("SchedulerForProcessor(PE" + str(z) +
                                          ")",
                                          [processor],
                                          {'FIFO': 100, 'RoundRobin': 200})
                    self.schedulers.append(scheduler)
                    z += 1

        num_pes = x * y * endpoints_per_router
        for i in range(num_pes):
            for j in range(num_pes):
                pi = self.findProcessor('PE%d' % i)
                pj = self.findProcessor('PE%d' % j)
                mi = self.findCommunicationResource('sp%d' % i)
                mj = self.findCommunicationResource('sp%d' % j)

                cp = self.createConsumerPrimitive(noc, pi, pj, mj)
                pp = self.createProducerPrimitive(noc, pi, pj, mi)

                self.primitives.append(cp)
                self.primitives.append(pp)

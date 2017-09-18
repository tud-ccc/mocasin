# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from ..common import CommunicationPhase
from ..common import CommunicationResource
from ..common import FrequencyDomain
from ..common import MeshNoc
from ..common import Platform
from ..common import Primitive
from ..common import Processor
from ..common import Scheduler
from ..common import Storage


class Tomahawk2Platform(Platform):

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

    def __init__(self):
        Platform.__init__(self)

        self.frequency_domain = FrequencyDomain('fd_sys', 200000000)
        self.local_fifo_access = CommunicationResource('local_fifo_access',
                                                       self.frequency_domain,
                                                       164,  # read latency,
                                                       205)  # write latency
        self.remote_fifo_access = CommunicationResource('remote_fifo_access',
                                                        self.frequency_domain,
                                                        234,  # read latency,
                                                        299)  # write latency

        noc = MeshNoc(self.frequency_domain, 8, 8, "yx", 2, 2)

        for i in range(0, 8):
            processor = Processor("PE" + str(i), 'RISC', self.frequency_domain,
                                  1000, 1000)
            self.processors.append(processor)

            memory = Storage("sp" + str(i), self.frequency_domain,
                             1, 1, 8, 8, False)
            self.communication_resources.append(memory)

            noc.create_ni([memory, processor], int(i / 4), int(i / 4))

            # Scheduling on the Tomahawk2 is currently not possible.
            scheduler = Scheduler("SchedulerForProcessor(PE" + str(i) + ")",
                                  [processor],
                                  {'None': 0})
            self.schedulers.append(scheduler)

        for i in range(0, 8):
            for j in range(0, 8):
                pi = self.findProcessor('PE%d' % i)
                pj = self.findProcessor('PE%d' % j)
                mi = self.findCommunicationResource('sp%d' % i)
                mj = self.findCommunicationResource('sp%d' % j)

                cp = self.createConsumerPrimitive(noc, pi, pj, mj)
                pp = self.createProducerPrimitive(noc, pi, pj, mi)

                self.primitives.append(cp)
                self.primitives.append(pp)

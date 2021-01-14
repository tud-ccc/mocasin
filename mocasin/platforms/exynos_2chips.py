# Copyright (C) 2018 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from mocasin.common.platform import FrequencyDomain, Platform, Processor, \
    SchedulingPolicy, Scheduler, Storage, CommunicationPhase, Primitive


class Exynos2Chips(Platform):

    def __init__(self):
        super(Exynos2Chips, self).__init__("Exynos2Chips")

        # Frequency domains
        fd_a7 = FrequencyDomain('fd_a7', 1400000000)
        fd_a15 = FrequencyDomain('fd_a15', 2000000000)
        fd_l3 = FrequencyDomain('fd_l3', 1400000000)
        fd_ram = FrequencyDomain('fd_ram', 933000000)

        # Processors
        for i in range(0, 4):
            self.add_processor(
                Processor('PE%02d' % i, 'ARM_CORTEX_A7', fd_a7))
        for i in range(4, 8):
            self.add_processor(
                Processor('PE%02d' % i, 'ARM_CORTEX_A15', fd_a15))
        for i in range(8, 12):
            self.add_processor(
                Processor('PE%02d' % i, 'ARM_CORTEX_A7', fd_a7))
        for i in range(12, 16):
            self.add_processor(
                Processor('PE%02d' % i, 'ARM_CORTEX_A15', fd_a15))

        # Schedulers
        sp = SchedulingPolicy('FIFO', 1000)
        for i in range(0, 16):
            self.add_scheduler(
                Scheduler('sched%02d' % i,
                          [self.find_processor('PE%02d' % i)], [sp]))

        # L1 Caches
        for i in range(0, 4):
            self.add_communication_resource(
                Storage('L1_PE%02d' % i, fd_a7,
                        read_latency=1, write_latency=4,
                        read_throughput=8, write_throughput=8))
        for i in range(4, 8):
            self.add_communication_resource(
                Storage('L1_PE%02d' % i, fd_a15,
                        read_latency=1, write_latency=4,
                        read_throughput=8, write_throughput=8))
        for i in range(8, 12):
            self.add_communication_resource(
                Storage('L1_PE%02d' % i, fd_a7,
                        read_latency=1, write_latency=4,
                        read_throughput=8, write_throughput=8))
        for i in range(12, 16):
            self.add_communication_resource(
                Storage('L1_PE%02d' % i, fd_a15,
                        read_latency=1, write_latency=4,
                        read_throughput=8, write_throughput=8))

        # L1 Primitives
        for i in range(0, 16):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)
            produce = CommunicationPhase('produce', [l1], 'write')
            consume = CommunicationPhase('consume', [l1], 'read')

            prim = Primitive('prim_L1_PE%02d' % i)
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
            self.add_primitive(prim)

        # L2 Caches
        l2_C0_A7 = Storage('L2_C0_A7', fd_a7,
                           read_latency=16, write_latency=21,
                           read_throughput=8, write_throughput=8)
        l2_C0_A15 = Storage('L2_C0_A15', fd_a15,
                            read_latency=16, write_latency=21,
                            read_throughput=8, write_throughput=8)
        l2_C1_A7 = Storage('L2_C1_A7', fd_a7,
                           read_latency=16, write_latency=21,
                           read_throughput=8, write_throughput=8)
        l2_C1_A15 = Storage('L2_C1_A15', fd_a15,
                            read_latency=16, write_latency=21,
                            read_throughput=8, write_throughput=8)
        self.add_communication_resource(l2_C0_A7)
        self.add_communication_resource(l2_C0_A15)
        self.add_communication_resource(l2_C1_A7)
        self.add_communication_resource(l2_C1_A15)

        # L2 Primitives
        prim = Primitive('prim_L2_C0_A7')
        for i in range(0, 4):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C0_A7], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C0_A7], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

        prim = Primitive('prim_L2_C0_A15')
        for i in range(4, 8):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C0_A15], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C0_A15], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

        prim = Primitive('prim_L2_C1_A7')
        for i in range(8, 12):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C1_A7], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C1_A7], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

        prim = Primitive('prim_L2_C1_A15')
        for i in range(12, 16):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C1_A15], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C1_A15], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

        # L3 Caches
        l3_C0 = Storage('L3_C0', fd_l3,
                        read_latency=30, write_latency=21,
                        read_throughput=8, write_throughput=8)
        l3_C1 = Storage('L3_C1', fd_l3,
                        read_latency=40, write_latency=21,
                        read_throughput=8, write_throughput=8)
        self.add_communication_resource(l3_C0)
        self.add_communication_resource(l3_C1)

        # L3 Primitives
        prim = Primitive('prim_L3_C0')
        for i in range(0, 4):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C0_A7, l3_C0], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C0_A7, l3_C0], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        for i in range(4, 8):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C0_A15, l3_C0], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C0_A15, l3_C0], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

        prim = Primitive('prim_L3_C1')
        for i in range(8, 12):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C1_A7, l3_C1], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C1_A7, l3_C1], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        for i in range(12, 16):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C1_A15, l3_C1], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C1_A15, l3_C1], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

        # RAM
        ram = Storage('RAM', fd_ram,
                      read_latency=120, write_latency=120,
                      read_throughput=8, write_throughput=8)
        self.add_communication_resource(ram)

        prim = Primitive('prim_RAM')
        for i in range(0, 4):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C0_A7, l3_C0, ram], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C0_A7, l3_C0, ram], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        for i in range(4, 8):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C0_A15, l3_C0, ram], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C0_A15, l3_C0, ram], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        for i in range(8, 12):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C1_A7, l3_C1, ram], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C1_A7, l3_C1, ram], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        for i in range(12, 16):
            pe = self.find_processor('PE%02d' % i)
            l1 = self.find_communication_resource('L1_PE%02d' % i)

            produce = CommunicationPhase('produce', [l1, l2_C1_A15, l3_C1, ram], 'write')
            consume = CommunicationPhase('consume', [l1, l2_C1_A15, l3_C1, ram], 'read')
            prim.add_producer(pe, [produce])
            prim.add_consumer(pe, [consume])
        self.add_primitive(prim)

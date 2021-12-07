# Copyright (C) 2018 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


from mocasin.common.platform import (
    FrequencyDomain,
    Platform,
    Processor,
    SchedulingPolicy,
    Scheduler,
    Storage,
    CommunicationPhase,
    Primitive,
)
from mocasin.platforms.platformDesigner import PlatformDesigner

class Exynos2Chips(Platform):
    def __init__(self):
        super(Exynos2Chips, self).__init__("Exynos2Chips")

        designer = PlatformDesigner(self)
        exynos2chips = designer.addCluster("exynos2chips")

        # Frequency domains
        fd_a7 = FrequencyDomain("fd_a7", 1400000000)
        fd_a15 = FrequencyDomain("fd_a15", 2000000000)
        fd_l3 = FrequencyDomain("fd_l3", 1400000000)
        fd_ram = FrequencyDomain("fd_ram", 933000000)

        # Schedulers
        designer.setSchedulingPolicy("FIFO", 1000)

        # Processors
        processor_a7 = Processor("PE0", "ARM_CORTEX_A7", fd_a7, None)
        processor_a15 = Processor("PE1", "ARM_CORTEX_A15", fd_a15, None)

        num_chips = 2
        num_clusters = 2
        num_pes = 4

        chips = list()
        clusters = list()
        l3_list = list()

        for i in range(num_chips):
            chip = designer.addCluster(f"chip{i}", exynos2chips)

            l2_list = list()
            for j in range(num_clusters):
                cluster = designer.addCluster(f"cluster{j}_chip{i}", chip)
                print(j % num_clusters)
                if not j % num_clusters:
                    pe_base = processor_a7
                    fd = fd_a7
                else:
                    pe_base = processor_a15
                    fd = fd_a15

                l1_list = list()
                for k in range(num_pes):
                    print(pe_base.name)
                    # Processors
                    pe = designer.addPeToCluster(
                        cluster,
                        f"processor{k}_cluster{j}_chip{i}",
                        pe_base.type,
                        pe_base.frequency_domain,
                        pe_base.power_model,
                        pe_base.context_load_cycles,
                        pe_base.context_store_cycles,
                    )

                    # L1 Caches
                    l1 = designer.addStorage(
                        f"l1_{k}_cluster{j}_chip{i}",
                        cluster,
                        readLatency=1,
                        writeLatency=4,
                        readThroughput=8,
                        writeThroughput=8,
                        frequency=fd.frequency,
                    )

                    # L1 Primitives
                    designer.connectPeToCom(pe, l1)
                    l1_list.append(l1)

                # L2 Caches
                l2 = designer.addStorage(
                    f"l2_cluster{j}_chip{i}",
                    cluster,
                    readLatency=16,
                    writeLatency=21,
                    readThroughput=8,
                    writeThroughput=8,
                    frequency=fd.frequency,
                )

                # L2 Primitives
                for l1 in l1_list:
                    designer.connectStorageLevels(l1, l2)
                l2_list.append(l2)
                clusters.append(cluster)

            # L3 Caches
            if i == 0:
                readLatency = 30
            elif i == 1:
                readLatency = 40

            l3 = designer.addStorage(
                f"l3_chip{i}",
                chip,
                readLatency=readLatency,
                writeLatency=21,
                readThroughput=8,
                writeThroughput=8,
                frequency=fd_l3.frequency,
            )

            # L3 Primitives
            for l2 in l2_list:
                designer.connectStorageLevels(l2, l3)
            l3_list.append(l3)
            chips.append(chip)

        # RAM
        RAM = designer.addStorage(
            "RAM",
            exynos2chips,
            readLatency=120,
            writeLatency=120,
            readThroughput=8,
            writeThroughput=8,
            frequency=fd_ram.frequency,
        )
        for l3 in l3_list:
            designer.connectStorageLevels(l3, RAM)

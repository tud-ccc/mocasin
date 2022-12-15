# Copyright (C) 2018 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Julian Robledo


from mocasin.common.platform import FrequencyDomain, Platform, Processor
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster


class Exynos2Chips(Platform):
    def __init__(self):
        super(Exynos2Chips, self).__init__("Exynos2Chips")

        # Start platform designer
        designer = PlatformDesigner(self)
        exynos2chips = cluster("exynos2chips", designer)

        # Schedulers
        designer.setSchedulingPolicy("FIFO", 1000)

        # make exynos chips
        exynos1 = makeExynos("exynos1", designer, 30)
        exynos2 = makeExynos("exynos2", designer, 40)
        exynos2chips.addCluster(exynos1)
        exynos2chips.addCluster(exynos2)

        # RAM
        l3_exynos1 = exynos1.findComRes("l3")
        l3_exynos2 = exynos2.findComRes("l3")
        RAM = exynos2chips.addStorage("RAM", 120, 120, 8, 8, 933000000)
        designer.connectComponents(l3_exynos1, RAM)
        designer.connectComponents(l3_exynos2, RAM)

        self.generate_all_primitives()


class makeExynos(cluster):
    def __init__(self, name, designer, l3_latency):
        super(makeExynos, self).__init__(name, designer)

        # reference processors
        fd_a7 = FrequencyDomain("fd_a7", 1400000000)
        fd_a15 = FrequencyDomain("fd_a15", 2000000000)
        processor_a7 = Processor("PE0", "ARM_CORTEX_A7", fd_a7, None)
        processor_a15 = Processor("PE1", "ARM_CORTEX_A15", fd_a15, None)
        peA7 = (*self.peParams(processor_a7),)
        peA15 = (*self.peParams(processor_a15),)

        num_pes = 4
        a7cluster = makeCluster(f"clusterA7_{name}", designer, peA7, num_pes)
        a15cluster = makeCluster(f"clusterA15_{name}", designer, peA15, num_pes)
        self.addCluster(a7cluster)
        self.addCluster(a15cluster)

        l2_cluster1 = a7cluster.findComRes("l2")
        l2_cluster2 = a15cluster.findComRes("l2")
        l3 = self.addStorage(f"l3", l3_latency, 21, 8, 8, 1400000000)
        designer.connectComponents(l2_cluster1, l3)
        designer.connectComponents(l2_cluster2, l3)

    # get parameters for pes
    def peParams(self, processor):
        return (
            processor.type,
            processor.frequency_domain,
            processor.power_model,
            processor.context_load_cycles,
            processor.context_store_cycles,
            processor.n_threads,
        )


class makeCluster(cluster):
    def __init__(self, name, designer, processor, num_pes):
        super(makeCluster, self).__init__(name, designer)

        freq = processor[1].frequency
        l2 = self.addStorage(f"l2", 16, 21, 8, 8, freq)
        for k in range(num_pes):
            pe = self.addPeToCluster(f"pe{k}", *processor)
            l1 = self.addStorage(f"l1_{k}", 1, 4, 8, 8, freq)
            designer.connectComponents(pe, l1)
            designer.connectComponents(l1, l2)

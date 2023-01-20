# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

from mocasin.common.platform import Platform
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster
from hydra.utils import instantiate
from mocasin.common.platform import Processor


class DesignerPlatformExynos990(Platform):
    def __init__(
        self,
        processor_0,
        processor_1,
        processor_2,
        processor_3,
        name="exynos-990",
        symmetries_json=None,
        embedding_json=None,
    ):
        super(DesignerPlatformExynos990, self).__init__(
            name, symmetries_json, embedding_json
        )
        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1, Processor):
            processor_1 = instantiate(processor_1)
        if not isinstance(processor_2, Processor):
            processor_2 = instantiate(processor_2)
        if not isinstance(processor_3, Processor):
            processor_3 = instantiate(processor_3)

        # get parameters for components
        pe0Params = self.peParams(processor_0)
        pe1Params = self.peParams(processor_1)
        pe2Params = self.peParams(processor_2)
        pe3Params = self.peParams(processor_3)
        l1c0Params = self.l1c0Params()
        l2c0Params = self.l2c0Params()
        l1c1Params = self.l1c1Params()
        l2c1Params = self.l2c1Params()
        l1c2Params = self.l1c2Params()
        l2c2Params = self.l2c2Params()
        l1c3Params = self.l1c3Params()
        dramParams = self.dramParams()
        busParams = self.busParams()

        # Start platform designer
        designer = PlatformDesigner(self)
        exynos990 = cluster("exynos990", designer)

        # Schedulers
        designer.setSchedulingPolicy("FIFO", 1000)

        # clusters with l2 cache
        cluster0 = makeCluster(
            "cluster_0", designer, pe0Params, l1c0Params, l2c0Params, 2
        )
        cluster1 = makeCluster(
            "cluster_1", designer, pe1Params, l1c1Params, l2c1Params, 2
        )
        cluster2 = makeCluster(
            "cluster_2", designer, pe2Params, l1c2Params, l2c2Params, 4
        )
        # single GPU
        cluster3 = makeCluster("cluster_3", designer, pe3Params, l1c3Params)

        # add clusters to exynos
        exynos990.addCluster(cluster0)
        exynos990.addCluster(cluster1)
        exynos990.addCluster(cluster2)
        exynos990.addCluster(cluster3)

        # add ram
        ram = exynos990.addStorage("RAM", *dramParams)
        l2c0 = cluster0.findComRes("l2")
        l2c1 = cluster1.findComRes("l2")
        l2c2 = cluster2.findComRes("l2")
        designer.connectComponents(l2c0, ram)
        designer.connectComponents(l2c1, ram)
        designer.connectComponents(l2c2, ram)

        # another memory, simulating BUS
        l1c3 = cluster3.findComRes("l1_0")
        bus = exynos990.addCommunicationResource("BUS", *busParams)
        designer.connectComponents(ram, bus)
        designer.connectComponents(l1c3, bus)

        self.generate_all_primitives()

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

    # returns (readLatency, writeLatency, readThroughput, writeThroughput, freq)
    def l1c0Params(self):
        return (5, 7, float("inf"), float("inf"), 6000000.0)

    def l2c0Params(self):
        return (225, 300, float("inf"), float("inf"), 600000000.0)

    def l1c1Params(self):
        return (5, 7, float("inf"), float("inf"), 6670000.0)

    def l2c1Params(self):
        return (225, 300, float("inf"), float("inf"), 667000000.0)

    def l1c2Params(self):
        return (5, 7, float("inf"), float("inf"), 6670000.0)

    def l2c2Params(self):
        return (225, 300, float("inf"), float("inf"), 667000000.0)

    def l1c3Params(self):
        return (5, 7, float("inf"), float("inf"), 6670000.0)

    def dramParams(self):
        return (800, 2000, float("inf"), float("inf"), 6000000.0)

    def busParams(self):
        return (2000, 6000, float("inf"), float("inf"), 4000000.0)


class makeCluster(cluster):
    def __init__(
        self, name, designer, peParams, l1Params, l2Params=None, num_pes=1
    ):
        super(makeCluster, self).__init__(name, designer)

        if l2Params:
            l2c0 = self.addStorage("l2", *l2Params)
        for i in range(num_pes):
            pe = self.addPeToCluster(f"pe{i}", *peParams)
            l1 = self.addStorage(f"l1_{i}", *l1Params)
            designer.connectComponents(pe, l1)
            if l2Params:
                designer.connectComponents(l1, l2c0)

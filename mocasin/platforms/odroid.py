# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

import logging

log = logging.getLogger(__name__)

from mocasin.common.platform import (
    Platform,
    Processor,
)
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster
from hydra.utils import instantiate


class DesignerPlatformOdroid(Platform):
    def __init__(
        self,
        processor_0,
        processor_1,
        num_big=4,
        num_little=4,
        name="odroid",
        peripheral_static_power=None,
        **kwargs,
    ):
        # workaraound for Hydra < 1.1
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1, Processor):
            processor_1 = instantiate(processor_1)
        super(DesignerPlatformOdroid, self).__init__(
            name,
            kwargs.get("symmetries_json", None),
            kwargs.get("embedding_json", None),
        )

        # Start platform designer
        designer = PlatformDesigner(self)
        exynos5422 = makeOdroid(
            name,
            designer,
            processor_0,
            processor_1,
            peripheral_static_power,
            num_little,
            num_big,
        )


class makeOdroid(cluster):
    def __init__(
        self,
        name,
        designer,
        processor_0,
        processor_1,
        peripheral_static_power,
        num_little,
        num_big,
    ):
        super(makeOdroid, self).__init__(name, designer)

        # get parameters for components
        pe0Params = peParams(processor_0)
        pe1Params = peParams(processor_1)
        l1a7Params = l1Params(processor_0.frequency_domain.frequency)
        l2a7Params = l2Params(processor_0.frequency_domain.frequency)
        l1a15Params = l1Params(processor_1.frequency_domain.frequency)
        l2a15Params = l2Params(processor_1.frequency_domain.frequency)
        ramParams = dramParams()

        # Schedulers
        designer.setSchedulingPolicy("FIFO", 1000)

        # cluster 0 with l2 cache
        cluster_a7 = cluster(f"cluster_a7_{name}", designer)
        self.addCluster(cluster_a7)

        L2_A7 = cluster_a7.addStorage("L2_A7", *l2a7Params)
        for i in range(num_little):
            pe = cluster_a7.addPeToCluster(f"pe{i:02d}", *pe0Params)
            l1 = cluster_a7.addStorage("L1_" + f"pe{i:02d}", *l1a7Params)
            designer.connectComponents(pe, l1)
            designer.generatePrimitivesForStorage(l1)
            # designer.printPrimitives()
            designer.connectComponents(l1, L2_A7)
        designer.generatePrimitivesForStorage(L2_A7)

        # cluster 1, with l2 cache
        cluster_a15 = cluster(f"cluster_a15_{name}", designer)
        self.addCluster(cluster_a15)

        L2_A15 = cluster_a15.addStorage("L2_A15", *l2a15Params)
        for i in range(num_big):
            pe = cluster_a15.addPeToCluster(f"pe{i:02d}", *pe1Params)
            l1 = cluster_a15.addStorage("L1_" + f"pe{i:02d}", *l1a15Params)
            designer.connectComponents(pe, l1)
            designer.generatePrimitivesForStorage(l1)
            designer.connectComponents(l1, L2_A15)
        designer.generatePrimitivesForStorage(L2_A15)

        # RAM connecting all clusters
        DRAM = self.addStorage("DRAM", *ramParams)
        designer.connectComponents(L2_A7, DRAM)
        designer.connectComponents(L2_A15, DRAM)
        designer.generatePrimitivesForStorage(DRAM)

        # Set peripheral static power of the platform.
        designer.setPeripheralStaticPower(peripheral_static_power)


# get parameters for pes
def peParams(processor):
    return (
        processor.type,
        processor.frequency_domain,
        processor.power_model,
        processor.context_load_cycles,
        processor.context_store_cycles,
        processor.n_threads,
    )


# returns (readLatency, writeLatency, readThroughput, writeThroughput, freq)
def l1Params(freq):
    return (1, 1, 8, 8, freq)


def l2Params(freq):
    return (21, 21, 8, 8, freq)


def dramParams():
    return (120, 120, 8, 8, 933000000.0)

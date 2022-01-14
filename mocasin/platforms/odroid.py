# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

import logging

log = logging.getLogger(__name__)

from mocasin.common.platform import (
    Platform,
    Processor,
    CommunicationResourceType,
)
from mocasin.platforms.platformDesigner import PlatformDesigner
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

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        exynos5422 = designer.addCluster("exynos5422")

        # cluster 0 with l2 cache
        cluster_a7 = designer.addCluster("cluster_a7", exynos5422)
        L1_list = list()
        for i in range(num_little):
            pe = designer.addPeToCluster(
                cluster_a7,
                f"A7_{i:02d}",
                processor_0.type,
                processor_0.frequency_domain,
                processor_0.power_model,
                processor_0.context_load_cycles,
                processor_0.context_store_cycles,
            )

            L1 = designer.addCommunicationResource(
                "L1_" + pe.name,
                cluster_a7,
                readLatency=1,
                writeLatency=1,
                readThroughput=8,
                writeThroughput=8,
                resourceType=CommunicationResourceType.Storage,
                frequency=processor_0.frequency_domain.frequency,
            )
            designer.connectPeToCom(pe, L1)
            L1_list.append(L1)

        L2_A7 = designer.addCommunicationResource(
            "L2_A7",
            cluster_a7,
            readLatency=21,
            writeLatency=21,
            readThroughput=8,
            writeThroughput=8,
            frequency=processor_0.frequency_domain.frequency,
        )
        for l1 in L1_list:
            designer.connectStorageLevels(l1, L2_A7)

        # cluster 1, with l2 cache
        cluster_a15 = designer.addCluster("cluster_a15", exynos5422)
        L1_list = list()
        for i in range(num_big):
            pe = designer.addPeToCluster(
                cluster_a15,
                f"A15_{i:02d}",
                processor_1.type,
                processor_1.frequency_domain,
                processor_1.power_model,
                processor_1.context_load_cycles,
                processor_1.context_store_cycles,
            )

            L1 = designer.addCommunicationResource(
                "L1_" + pe.name,
                cluster_a15,
                readLatency=1,
                writeLatency=1,
                readThroughput=8,
                writeThroughput=8,
                resourceType=CommunicationResourceType.Storage,
                frequency=processor_1.frequency_domain.frequency,
            )
            designer.connectPeToCom(pe, L1)
            L1_list.append(L1)

        # L2 latency is L1 latency plus 21 cycles
        L2_A15 = designer.addCommunicationResource(
            "L2_A15",
            cluster_a15,
            readLatency=21,
            writeLatency=21,
            readThroughput=8,
            writeThroughput=8,
            frequency=processor_1.frequency_domain.frequency,
        )
        for l1 in L1_list:
            designer.connectStorageLevels(l1, L2_A15)

        # RAM connecting all clusters
        # RAM latency is L2 latency plus 120 cycles
        DRAM = designer.addCommunicationResource(
            "DRAM",
            exynos5422,
            readLatency=120,
            writeLatency=120,
            readThroughput=8,
            writeThroughput=8,
            frequency=933000000.0,
        )
        designer.connectStorageLevels(L2_A7, DRAM)
        designer.connectStorageLevels(L2_A15, DRAM)

        # Set peripheral static power of the platform.
        designer.setPeripheralStaticPower(peripheral_static_power)

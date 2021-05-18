# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import logging

log = logging.getLogger(__name__)

from mocasin.common.platform import Platform, FrequencyDomain, Processor
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
            name, kwargs.get("symmetries_json", None)
        )

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        designer.newElement("exynos5422")

        # cluster 0 with l2 cache
        pe_names = [f"A7_{i:02d}" for i in range(num_little)]
        designer.addPeClusterForProcessor(
            "cluster_a7", processor_0, num_little, processor_names=pe_names
        )
        # Add L1/L2 caches
        designer.addCacheForPEs(
            "cluster_a7",
            readLatency=1,
            writeLatency=1,
            readThroughput=8,
            writeThroughput=8,
            frequencyDomain=processor_0.frequency_domain.frequency,
            name="L1_A7",
        )
        designer.addCommunicationResource(
            name="L2_A7",
            clusterIds=["cluster_a7"],
            readLatency=21,
            writeLatency=21,
            readThroughput=8,
            writeThroughput=8,
            frequencyDomain=processor_0.frequency_domain.frequency,
        )

        # cluster 1, with l2 cache
        pe_names = [f"A15_{i:02d}" for i in range(num_big)]
        designer.addPeClusterForProcessor(
            "cluster_a15", processor_1, num_big, processor_names=pe_names
        )
        # Add L1/L2 caches
        designer.addCacheForPEs(
            "cluster_a15",
            readLatency=1,
            writeLatency=1,
            readThroughput=8,
            writeThroughput=8,
            frequencyDomain=processor_1.frequency_domain.frequency,
            name="L1_A15",
        )
        # L2 latency is L1 latency plus 21 cycles
        designer.addCommunicationResource(
            "L2_A15",
            ["cluster_a15"],
            readLatency=22,
            writeLatency=22,
            readThroughput=8,
            writeThroughput=8,
            frequencyDomain=processor_1.frequency_domain.frequency,
        )

        # RAM connecting all clusters
        # RAM latency is L2 latency plus 120 cycles
        designer.addCommunicationResource(
            "DRAM",
            ["cluster_a7", "cluster_a15"],
            readLatency=142,
            writeLatency=142,
            readThroughput=8,
            writeThroughput=8,
            frequencyDomain=933000000.0,
        )

        # Set peripheral static power of the platform.
        designer.setPeripheralStaticPower(peripheral_static_power)

        designer.finishElement()

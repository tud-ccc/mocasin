# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.common.platform import Platform
from mocasin.platforms.platformDesigner import PlatformDesigner
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

        designer = PlatformDesigner(self)
        exynos990 = designer.addCluster("exynos990")

        # Schedulers
        designer.setSchedulingPolicy("FIFO", 1000)

        clusters = list()

        # cluster 0 with l2 cache
        l1_list = list()
        l2_list = list()
        cluster0 = designer.addCluster("cluster_0", exynos990)
        for i in range(2):
            # Processors
            pe = designer.addPeToCluster(
                cluster0,
                f"processor{i}_cluster0",
                processor_0.type,
                processor_0.frequency_domain,
                processor_0.power_model,
                processor_0.context_load_cycles,
                processor_0.context_store_cycles,
            )

            # L1 Caches
            l1 = designer.addStorage(
                f"l1_{i}_cluster0",
                cluster0,
                readLatency=5,
                writeLatency=7,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=6000000.0,
            )

            # L1 Primitives
            designer.connectPeToCom(pe, l1)
            l1_list.append(l1)

        # L2 caches
        l2 = designer.addStorage(
            "l2_cluster0",
            cluster0,
            readLatency=225,
            writeLatency=300,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=600000000.0,
        )

        # L2 Primitives
        for l1 in l1_list:
            designer.connectStorageLevels(l1, l2)
        l2_list.append(l2)
        clusters.append(cluster0)


        # cluster 1, with l2 cache
        l1_list = list()
        cluster1 = designer.addCluster("cluster_1", exynos990)
        for i in range(2):
            # Processors
            pe = designer.addPeToCluster(
                cluster1,
                f"processor{i}_cluster1",
                processor_1.type,
                processor_1.frequency_domain,
                processor_1.power_model,
                processor_1.context_load_cycles,
                processor_1.context_store_cycles,
            )

            # L1 Caches
            l1 = designer.addStorage(
                f"l1_{i}_cluster1",
                cluster1,
                readLatency=5,
                writeLatency=7,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=6670000.0,
            )

            # L1 Primitives
            designer.connectPeToCom(pe, l1)
            l1_list.append(l1)

        # L2 caches
        l2 = designer.addStorage(
            "l2_cluster1",
            cluster1,
            readLatency=225,
            writeLatency=300,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=667000000.0,
        )

        # L2 Primitives
        for l1 in l1_list:
            designer.connectStorageLevels(l1, l2)
        l2_list.append(l2)
        clusters.append(cluster1)


        # cluster 2, with l2 cache
        l1_list = list()
        cluster2 = designer.addCluster("cluster_2", exynos990)
        for i in range(4):
            # Processors
            pe = designer.addPeToCluster(
                cluster2,
                f"processor{i}_cluster2",
                processor_2.type,
                processor_2.frequency_domain,
                processor_2.power_model,
                processor_2.context_load_cycles,
                processor_2.context_store_cycles,
            )

            # L1 Caches
            l1 = designer.addStorage(
                f"l1_{i}_cluster2",
                cluster2,
                readLatency=5,
                writeLatency=7,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=6670000.0,
            )

            # L1 Primitives
            designer.connectPeToCom(pe, l1)
            l1_list.append(l1)

        # L2 caches
        l2 = designer.addStorage(
            "l2_cluster2",
            cluster2,
            readLatency=225,
            writeLatency=300,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=667000000.0,
        )

        # L2 Primitives
        for l1 in l1_list:
            designer.connectStorageLevels(l1, l2)
        l2_list.append(l2)
        clusters.append(cluster2)

        # RAM connecting all clusters
        RAM = designer.addStorage(
            "RAM",
            exynos990,
            readLatency=800,
            writeLatency=2000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=6000000.0,
        )
        for l2 in l2_list:
            designer.connectStorageLevels(l2, RAM)


        # single GPU
        cluster3 = designer.addCluster("cluster_3", exynos990)
        # Processors
        pe = designer.addPeToCluster(
            cluster3,
            "GPU",
            processor_3.type,
            processor_3.frequency_domain,
            processor_3.power_model,
            processor_3.context_load_cycles,
            processor_3.context_store_cycles,
        )

        # L1 Caches
        l1 = designer.addStorage(
            "l1_cluster3",
            cluster3,
            readLatency=5,
            writeLatency=7,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=6670000.0,
        )

        # L1 Primitives
        designer.connectPeToCom(pe, l1)


        # another memory, simulating BUS
        BUS = designer.addCommunicationResource(
            "BUS",
            exynos990,
            readLatency=2000,
            writeLatency=6000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=4000000.0,
        )
        # BUS Primitives
        designer.connectStorageLevels(RAM, BUS)
        designer.connectStorageLevels(l1, BUS)


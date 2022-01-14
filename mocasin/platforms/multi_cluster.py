# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.common.platform import Platform, Processor
from mocasin.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate


class DesignerPlatformMultiCluster(Platform):
    def __init__(
        self,
        processor_0,
        processor_1,
        name="multi_cluster",
        symmetries_json=None,
        embedding_json=None,
    ):
        super(DesignerPlatformMultiCluster, self).__init__(
            name, symmetries_json, embedding_json
        )

        # woraround for Hydra < 1.1
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1, Processor):
            processor_1 = instantiate(processor_1)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        multi_cluster = designer.addCluster("multi_cluster")

        # add first cluster with L2 cache
        cluster_0 = designer.addCluster("cluster_0", multi_cluster)
        pe_list = list()
        for i in range(2):
            pe = designer.addPeToCluster(
                cluster_0,
                f"processor_{i:02d}_0",
                processor_0.type,
                processor_0.frequency_domain,
                processor_0.power_model,
                processor_0.context_load_cycles,
                processor_0.context_store_cycles,
            )
            pe_list.append(pe)

        cl0_l2 = designer.addStorage(
            "cl0_l2",
            cluster_0,
            readLatency=100,
            writeLatency=100,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=10000,
        )
        for pe in pe_list:
            designer.connectPeToCom(pe, cl0_l2)

        # add second cluster with L2 cache
        cluster_1 = designer.addCluster("cluster_1", multi_cluster)
        pe_list = list()
        for i in range(2):
            pe = designer.addPeToCluster(
                cluster_1,
                f"processor_{i:02d}_1",
                processor_1.type,
                processor_1.frequency_domain,
                processor_1.power_model,
                processor_1.context_load_cycles,
                processor_1.context_store_cycles,
            )
            pe_list.append(pe)

        cl1_l2 = designer.addStorage(
            "cl1_l2",
            cluster_1,
            readLatency=100,
            writeLatency=100,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=10000,
        )
        for pe in pe_list:
            designer.connectPeToCom(pe, cl1_l2)

        # RAM connecting all clusters
        ram = designer.addStorage(
            "RAM",
            multi_cluster,
            1000,
            1000,
            float("inf"),
            float("inf"),
            frequency=1000,
        )
        designer.connectStorageLevels(cl0_l2, ram)
        designer.connectStorageLevels(cl1_l2, ram)

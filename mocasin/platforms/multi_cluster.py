# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.common.platform import Platform, Processor
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster
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
        multi_cluster = cluster("multi_cluster", designer)

        # add first cluster with L2 cache
        cluster_0 = makeCluster("cluster_0", designer, processor_0, 2)
        cluster_1 = makeCluster("cluster_1", designer, processor_1, 2)
        multi_cluster.addCluster(cluster_0)
        multi_cluster.addCluster(cluster_1)

        # RAM connecting all clusters
        ram = multi_cluster.addStorage(
            "RAM",
            1000,
            1000,
            float("inf"),
            float("inf"),
            frequency=1000,
        )
        cl0_l2 = cluster_0.findComRes("l2")
        cl1_l2 = cluster_1.findComRes("l2")
        designer.connectComponents(cl0_l2, ram)
        designer.connectComponents(cl1_l2, ram)

        self.generate_all_primitives()

class makeCluster(cluster):
    def __init__(self, name, designer, processor, num_pes):
        super(makeCluster, self).__init__(name, designer)

        pe_list = list()
        for i in range(num_pes):
            pe = self.addPeToCluster(
                f"processor_{i:02d}",
                processor.type,
                processor.frequency_domain,
                processor.power_model,
                processor.context_load_cycles,
                processor.context_store_cycles,
            )
            pe_list.append(pe)

        l2 = self.addStorage(
            "l2",
            readLatency=100,
            writeLatency=100,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=10000,
        )
        for pe in pe_list:
            designer.connectComponents(pe, l2)
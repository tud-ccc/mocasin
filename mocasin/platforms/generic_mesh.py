# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.platforms.topologies import meshTopology
from mocasin.platforms.utils import simpleDijkstra as sd
from mocasin.common.platform import Platform, Processor
from mocasin.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate


class DesignerPlatformMesh(Platform):
    def __init__(
        self,
        processor_0,
        processor_1,
        name="parallella-styled",
        symmetries_json=None,
        embedding_json=None,
    ):
        super(DesignerPlatformMesh, self).__init__(
            name, symmetries_json, embedding_json
        )
        # This is a workaround until Hydra 1.1 (with recursive instantiaton!)
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1, Processor):
            processor_1 = instantiate(processor_1)
        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        designer.newElement("test_chip")

        designer.addPeClusterForProcessor("cluster_0", processor_0, 16)
        topology = meshTopology(
            [
                "processor_0000",
                "processor_0001",
                "processor_0002",
                "processor_0003",
                "processor_0004",
                "processor_0005",
                "processor_0006",
                "processor_0007",
                "processor_0008",
                "processor_0009",
                "processor_0010",
                "processor_0011",
                "processor_0012",
                "processor_0013",
                "processor_0014",
                "processor_0015",
            ]
        )
        designer.createNetworkForCluster(
            "cluster_0", "testNet", topology, sd, 6000000.0, 100, 150, 100, 60
        )

        designer.addPeClusterForProcessor("cluster_1", processor_1, 2)
        designer.addCommunicationResource(
            "lvl2_cl1",
            ["cluster_1"],
            500,
            1000,
            float("inf"),
            float("inf"),
            frequencyDomain=600000000.0,
        )

        designer.addCommunicationResource(
            "RAM",
            ["cluster_0", "cluster_1"],
            1000,
            3000,
            float("inf"),
            float("inf"),
            frequencyDomain=6000000.0,
        )
        designer.finishElement()

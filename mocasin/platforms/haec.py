# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.common.platform import Platform, Processor
from mocasin.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate
from mocasin.platforms.topologies import meshTopology
from mocasin.platforms.utils import simpleDijkstra as sd


class DesignerPlatformHAEC(Platform):
    def __init__(
        self,
        processor_0,
        name="haec-like",
        symmetries_json=None,
        embedding_json=None,
    ):
        super(DesignerPlatformHAEC, self).__init__(
            name, symmetries_json, embedding_json
        )

        # woraround for Hydra < 1.1
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        designer.newElement("haec_like")
        for i in range(4):
            designer.addPeClusterForProcessor(f"cluster_{i}", processor_0, 16)
            processors = [
                f"processor_{j:04d}" for j in range(i * 16, (i + 1) * 16)
            ]
            topology = meshTopology(processors)
            designer.createNetworkForCluster(
                f"cluster_{i}",
                "optic",
                topology,
                sd,
                6000000.0,
                100,
                150,
                100,
                60,
            )

        for i in range(4 - 1):
            designer.addCommunicationResource(
                f"wireless_{i}",
                [f"cluster_{i}", f"cluster_{i+1}"],
                200,
                300,
                float("inf"),
                float("inf"),
                frequencyDomain=6000000.0,
            )

        designer.addCommunicationResource(
            f"RAM",
            [f"cluster_{i}" for i in range(4)],
            2000,
            3000,
            float("inf"),
            float("inf"),
            frequencyDomain=6000000.0,
        )
        designer.finishElement()

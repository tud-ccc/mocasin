# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

from mocasin.common.platform import Platform, Processor, FrequencyDomain, CommunicationResource, CommunicationResourceType
from mocasin.platforms.topologies import fullyConnectedTopology
from mocasin.platforms.platformDesigner import PlatformDesigner
from mocasin.platforms.utils import simpleDijkstra as sd
from hydra.utils import instantiate


class DesignerPlatformCoolidge(Platform):
    # The topology and latency numbers (!) of this should come from the MPPA3 Coolidge
    # sheet published by Kalray
    def __init__(
        self,
        processor_0,
        processor_1,
        name="coolidge",
        symmetries_json=None,
        embedding_json=None,
    ):
        super(DesignerPlatformCoolidge, self).__init__(
            name, symmetries_json, embedding_json
        )

        # workaround until Hydra 1.1
        if not isinstance(processor_0, Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1, Processor):
            processor_1 = instantiate(processor_1)

        designer = PlatformDesigner(self)
        designer.setSchedulingPolicy("FIFO", 1000)
        coolidge = designer.addCluster("coolidge")

        fd = FrequencyDomain("fd_electric", 6000000.0)
        pl = CommunicationResource(
            "electric",
            fd,
            CommunicationResourceType.PhysicalLink,
            100,
            150,
            100,
            60
        )

        # create five chips with 16 cores, NoC, +Security Core
        l2_list = list()
        for i in range(5):
            cluster = designer.addCluster(f"cluster_{i}", coolidge)
            cluster_0 = designer.addCluster(f"cluster_{i}_0", cluster)
            nocList = list()
            l1_list = list()
            for j in range(16):
                pe = designer.addPeToCluster(
                    cluster_0,
                    f"processor0_{(j+i*16):04d}",
                    processor_0.type,
                    processor_0.frequency_domain,
                    processor_0.power_model,
                    processor_0.context_load_cycles,
                    processor_0.context_store_cycles,
                )
                noc = designer.addRouter(
                    f"noc_{(j+i*16):04d}",
                    cluster_0,
                    readLatency=100,
                    writeLatency=150,
                    readThroughput=100,
                    writeThroughput=60,
                    frequency=40000.0,
                )
                # workaround to connect pes in cluster to an external memory
                l1_0 = designer.addStorage(
                    f"l1_{(j+i*16):04d}_0",
                    cluster_0,
                    readLatency=0,
                    writeLatency=0,
                    readThroughput=float("inf"),
                    writeThroughput=float("inf"),
                    frequency=600000.0,
                )
                designer.connectPeToCom(pe, noc)
                designer.connectPeToCom(pe, l1_0)
                nocList.append(noc)
                l1_list.append(l1_0)

            topology = fullyConnectedTopology(nocList)
            designer.createNetworkForRouters(
                f"noc_{i}",
                nocList,
                topology,
                sd,
                pl
            )

            cluster_1 = designer.addCluster(f"cluster_{i}_1", cluster)
            pe = designer.addPeToCluster(
                cluster_1,
                f"processor1_{i}",
                processor_1.type,
                processor_1.frequency_domain,
                processor_1.power_model,
                processor_1.context_load_cycles,
                processor_1.context_store_cycles,
            )
            # workaround to connect pes in cluster to an external memory
            l1_1 = designer.addStorage(
                f"l1_{i:04d}_1",
                cluster_1,
                readLatency=0,
                writeLatency=0,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=600000.0,
            )
            designer.connectPeToCom(pe, l1_1)

            # L2 memory
            l2 = designer.addCommunicationResource(
                f"L2_{i}",
                cluster,
                readLatency=500,
                writeLatency=1500,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=600000.0,
            )
            for l1_0 in l1_list:
                designer.connectStorageLevels(l1_0, l2)
            designer.connectStorageLevels(l1_1, l2)
            l2_list.append(l2)

        # RAM
        ram = designer.addCommunicationResource(
            "RAM",
            coolidge,
            1000,
            3000,
            float("inf"),
            float("inf"),
            frequency=10000,
        )
        for l2 in l2_list:
            designer.connectStorageLevels(l2, ram)


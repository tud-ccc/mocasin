# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

from mocasin.common.platform import (
    Platform,
    Processor,
    CommunicationResourceType,
    CommunicationResource,
    FrequencyDomain)
from mocasin.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate
from mocasin.platforms.topologies import meshTopology, fullyConnectedTopology
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
        haec = designer.addCluster("haec_like")

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

        clusters = list()
        for i in range(4):
            cluster = designer.addCluster(f"cluster_{i}", haec)
            nocList = []
            for j in range(16):
                pe = designer.addPeToCluster(
                    cluster,
                    f"processor_{(j+i*16):04d}",
                    processor_0.type,
                    processor_0.frequency_domain,
                    processor_0.power_model,
                    processor_0.context_load_cycles,
                    processor_0.context_store_cycles,
                )
                noc = designer.addRouter(
                    f"noc_{(j+i*16):04d}",
                    cluster,
                    readLatency=100,
                    writeLatency=150,
                    readThroughput=100,
                    writeThroughput=60,
                    frequency=6000000.0,
                )
                designer.connectPeToCom(pe, noc)
                nocList.append(noc)

            topology = meshTopology(nocList)
            designer.createNetworkForRouters(
                "electric",
                nocList,
                topology,
                sd,
                pl
            )
            clusters.append(cluster)

        wirelessList = list()
        for i in range(4):
            wireless = designer.addRouter(
                f"wireless_{i}",
                clusters[i],
                readLatency=200,
                writeLatency=300,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=6000000.0,
            )

            processors = designer.getPesInCluster(clusters[i])
            for pe in processors:
                designer.connectPeToCom(pe, wireless)
            wirelessList.append(wireless)

        pl = CommunicationResource(
            "wireless",
            fd,
            CommunicationResourceType.PhysicalLink,
            200,
            300,
            float("inf"),
            float("inf"),
        )
        topology = fullyConnectedTopology(wirelessList)
        designer.createNetworkForRouters(
            "optic",
            wirelessList,
            topology,
            sd,
            pl
        )

        ram = designer.addStorage(
            "RAM",
            haec,
            readLatency=2000,
            writeLatency=3000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=6000000.0,
        )

        for i in range(4):
            cache = designer.addStorage(
                f"cache_{i}",
                clusters[i],
                readLatency=0,
                writeLatency=0,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=6000000.0,
            )
            processors = designer.getPesInCluster(clusters[i])
            for pe in processors:
                designer.connectPeToCom(pe, cache)
            designer.connectStorageLevels(cache, ram)

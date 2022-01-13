# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.platforms.topologies import meshTopology
from mocasin.platforms.utils import yxRouting as yx
from mocasin.common.platform import (
    Platform,
    Processor,
    FrequencyDomain,
    CommunicationResource,
    CommunicationResourceType)
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
        test_chip = designer.addCluster("test_chip")

        # define communication resource to be used as reference to build
        # the NoC network
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

        # cluster 0
        cluster_0 = designer.addCluster("cluster_0", test_chip)
        noc_list = list()
        pes_cluster_0 = list()
        l1_list = list()
        for i in range(16):
            pe = designer.addPeToCluster(
                cluster_0,
                f"processor0_{i:04d}",
                processor_0.type,
                processor_0.frequency_domain,
                processor_0.power_model,
                processor_0.context_load_cycles,
                processor_0.context_store_cycles,
            )
            noc = designer.addRouter(
                f"noc_{i:04d}",
                cluster_0,
                readLatency=100,
                writeLatency=150,
                readThroughput=100,
                writeThroughput=60,
                frequency=6000000.0,
            )

            # workaround to connect pes in cluster to an external memory
            l1 = designer.addStorage(
                f"l1_{i:04d}",
                cluster_0,
                readLatency=0,
                writeLatency=0,
                readThroughput=float("inf"),
                writeThroughput=float("inf"),
                frequency=6000000.0,
            )
            designer.connectPeToCom(pe, noc)
            designer.connectPeToCom(pe, l1)
            noc_list.append(noc)
            pes_cluster_0.append(pe)
            l1_list.append(l1)

        topology = meshTopology(noc_list)
        designer.createNetworkForRouters(
            "electric",
            noc_list,
            topology,
            yx,
            pl
        )

        # cluster 1
        cluster_1 = designer.addCluster("cluster_1", test_chip)
        pes_cluster_1 = list()
        for i in range(2):
            pe = designer.addPeToCluster(
                cluster_1,
                f"processor1_{i:04d}",
                processor_1.type,
                processor_1.frequency_domain,
                processor_1.power_model,
                processor_1.context_load_cycles,
                processor_1.context_store_cycles,
            )
            pes_cluster_1.append(pe)

        lvl2_cl1 = designer.addStorage(
            "lvl2_cl1",
            cluster_1,
            readLatency=500,
            writeLatency=1000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=600000000.0,
        )
        for pe in pes_cluster_1:
            designer.connectPeToCom(pe, lvl2_cl1)

        # RAM
        ram = designer.addStorage(
            "RAM",
            test_chip,
            readLatency=1000,
            writeLatency=3000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=6000000.0,
        )

        designer.connectStorageLevels(lvl2_cl1, ram)
        for l1 in l1_list:
            designer.connectStorageLevels(l1, ram)


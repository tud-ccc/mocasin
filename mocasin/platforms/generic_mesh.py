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
    CommunicationResourceType,
)
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster
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
        test_chip = cluster("test_chip", designer)

        # cluster 0
        cluster0 = makeCluster0("cluster0", designer, processor_0)
        test_chip.addCluster(cluster0)

        # cluster 1
        cluster1 = makeCluster1("cluster1", designer, processor_1)
        test_chip.addCluster(cluster1)

        # RAM
        ram = test_chip.addStorage(
            "RAM",
            readLatency=1000,
            writeLatency=3000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=6000000.0,
        )

        pes = cluster0.getProcessors()
        l2 = cluster1.getCommunicationResources()
        for component in pes + l2:
            designer.connectComponents(component, ram)

        self.generate_all_primitives()


class makeCluster0(cluster):
    def __init__(self, name, designer, pe0):
        super(makeCluster0, self).__init__(name, designer)

        noc_list = list()
        routerParams = (
            100,
            150,
            100,
            60,
            6000000.0,
        )
        for i in range(16):
            pe = self.addPeToCluster(f"processor0_{i:04d}", *peParams(pe0))
            noc = self.addRouter(f"noc_{i:04d}", *routerParams)
            designer.connectComponents(pe, noc)
            noc_list.append(noc)

        # physical link
        fd = FrequencyDomain("fd_electric", 6000000.0)
        pl = CommunicationResource(
            "electric",
            fd,
            CommunicationResourceType.PhysicalLink,
            100,
            150,
            100,
            60,
        )

        # create network
        designer.createNetwork("electric", noc_list, meshTopology, pl)


class makeCluster1(cluster):
    def __init__(self, name, designer, pe1):
        super(makeCluster1, self).__init__(name, designer)

        l1 = self.addStorage(
            "l1",
            readLatency=500,
            writeLatency=1000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=600000000.0,
        )
        for i in range(2):
            pe = self.addPeToCluster(f"processor1_{i:04d}", *peParams(pe1))
            designer.connectComponents(pe, l1)


# get parameters for pes
def peParams(processor):
    return (
        processor.type,
        processor.frequency_domain,
        processor.power_model,
        processor.context_load_cycles,
        processor.context_store_cycles,
        processor.n_threads
    )

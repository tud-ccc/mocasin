# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

from mocasin.common.platform import (
    Platform,
    Processor,
    FrequencyDomain,
    CommunicationResource,
    CommunicationResourceType,
)
from mocasin.platforms.topologies import fullyConnectedTopology
from mocasin.platforms.platformDesigner import PlatformDesigner
from mocasin.platforms.platformDesigner import cluster as cl
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
        coolidge = cl("coolidge", designer)

        # create five chips with 16 cores, NoC, +Security Core
        l2_list = list()
        for i in range(5):
            chip = makeChip(f"chip{i}", designer, processor_0, processor_1)
            l2_list = l2_list + chip.getCommunicationResources()

        # RAM
        ram = coolidge.addStorage("RAM", *ramParams())
        for l2 in l2_list:
            designer.connectComponents(l2, ram)

        self.generate_all_primitives()


class makeChip(cl):
    def __init__(self, name, designer, pe0, pe1):
        super(makeChip, self).__init__(name, designer)

        pe0 = peParams(pe0)
        pe1 = peParams(pe1)
        router = routerParams()

        cluster_0 = makeCluster0(f"cluster0_{name}", designer, pe0, router)
        cluster_1 = makeCluster1(f"cluster1_{name}", designer, pe1)
        self.addCluster(cluster_0)
        self.addCluster(cluster_1)

        # L2 memory
        l2 = self.addStorage("l2", *l2Params())
        pe0_list = cluster_0.getProcessors()
        pe1_list = cluster_1.getProcessors()
        pes = pe0_list + pe1_list
        for pe in pes:
            designer.connectComponents(pe, l2)


class makeCluster0(cl):
    def __init__(self, name, designer, pe0, router):
        super(makeCluster0, self).__init__(name, designer)

        nocList = list()
        for j in range(16):
            pe = self.addPeToCluster(f"pe_{(j):04d}", *pe0)
            noc = self.addRouter(f"noc_{(j):04d}", *router)

            # connect pes to routers and l1s
            designer.connectComponents(pe, noc)
            nocList.append(noc)

        fd = FrequencyDomain("fd_electric", 6000000.0)
        pl = CommunicationResource("pl", *plParams(fd))
        designer.createNetwork(f"noc", nocList, fullyConnectedTopology, pl)


class makeCluster1(cl):
    def __init__(self, name, designer, pe1):
        super(makeCluster1, self).__init__(name, designer)

        self.addPeToCluster("pe", *pe1)


# get parameters for pes
def peParams(processor):
    return (
        processor.type,
        processor.frequency_domain,
        processor.power_model,
        processor.context_load_cycles,
        processor.context_store_cycles,
    )


# readLatency, writeLatency, readThroughput, writeThroughput. frequency
def routerParams():
    return (
        100,
        150,
        100,
        60,
        40000.0,
    )


def l2Params():
    return (
        500,
        1500,
        float("inf"),
        float("inf"),
        600000.0,
    )


def ramParams():
    return (
        1000,
        3000,
        float("inf"),
        float("inf"),
        10000.0,
    )


def plParams(fd):
    return (
        "electric",
        fd,
        CommunicationResourceType.PhysicalLink,
        100,
        150,
        100,
        60,
    )

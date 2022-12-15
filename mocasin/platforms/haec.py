# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Julian Robledo

from mocasin.common.platform import (
    Platform,
    Processor,
    CommunicationResourceType,
    CommunicationResource,
    FrequencyDomain,
)
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster
from hydra.utils import instantiate
from mocasin.platforms.topologies import meshTopology, fullyConnectedTopology


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
        haec = cluster("haec_like", designer)
        ram = haec.addStorage(
            "RAM",
            readLatency=2000,
            writeLatency=3000,
            readThroughput=float("inf"),
            writeThroughput=float("inf"),
            frequency=6000000.0,
        )

        pe0 = peParams(processor_0)
        wirelessList = list()
        for i in range(4):
            cluster_i = makeCluster(f"cluster{i}", designer, pe0)
            pes = cluster_i.getProcessors()
            haec.addCluster(cluster_i)
            wirelessList.append(cluster_i.getWirelessRouter())
            for pe in pes:
                designer.connectComponents(pe, ram)

        designer.createNetwork(
            "optic", wirelessList, fullyConnectedTopology, getPlForWireless()
        )
        self.generate_all_primitives()


class makeCluster(cluster):
    def __init__(self, name, designer, pe0):
        super(makeCluster, self).__init__(name, designer)

        nocList = []
        self.wireless = self.addRouter(f"wireless", *nocWireless())
        for j in range(16):
            pe = self.addPeToCluster(f"processor_{j:04d}", *pe0)
            noc = self.addRouter(f"noc_{j:04d}", *nocRouter())
            designer.connectComponents(pe, noc)
            designer.connectComponents(pe, self.wireless)
            nocList.append(noc)

        pl = getPlForRouter()
        designer.createNetwork(f"electric_{name}", nocList, meshTopology, pl)

    def getWirelessRouter(self):
        return self.wireless


class makeWireless(cluster):
    def __init__(self, name, designer, pe0, router):
        super(makeCluster, self).__init__(name, designer)


def peParams(processor):
    return (
        processor.type,
        processor.frequency_domain,
        processor.power_model,
        processor.context_load_cycles,
        processor.context_store_cycles,
        processor.n_threads,
    )


def nocRouter():
    return (
        100,
        150,
        100,
        60,
        6000000.0,
    )


def nocWireless():
    return (
        200,
        300,
        float("inf"),
        float("inf"),
        6000000.0,
    )


def getPlForRouter():
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
    return pl


def getPlForWireless():
    fd = FrequencyDomain("fd_wireless", 6000000.0)
    pl = CommunicationResource(
        "wireless",
        fd,
        CommunicationResourceType.PhysicalLink,
        200,
        300,
        float("inf"),
        float("inf"),
    )
    return pl

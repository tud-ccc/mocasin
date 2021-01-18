# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

from mocasin.platforms.utils import simpleDijkstra


class TestPlatformDesigner(object):
    def test_singleCluster(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "TestCluster", 4, 1000)
        designer.addCommunicationResource("RAM", [0], 1000, 1000, 1000, 1000)
        designer.finishElement()

        platform = designer.getPlatform()

        assert len(platform.processors()) == 4
        assert len(platform.primitives()) == 1

        for primitive in platform.primitives():
            assert len(primitive.consumers) == len(primitive.producers) == 4

    def test_doubleCluster(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "cluster_0", 4, 1000)
        designer.addPeCluster(1, "cluster_1", 4, 1000)
        designer.addCommunicationResource(
            "L2Cache_0", [0], 1000, 1000, 1000, 1000
        )
        designer.addCommunicationResource(
            "L2Cache_1", [1], 1000, 1000, 1000, 1000
        )
        designer.addCommunicationResource("RAM", [0, 1], 1000, 1000, 1000, 1000)
        designer.finishElement()

        platform = designer.getPlatform()

        assert len(platform.processors()) == 8
        i = 0
        for element in platform.primitives():
            i += 1
        assert i == 3

        l2caches = 0
        RAM = 0
        for primitive in platform.primitives():
            if primitive.name == "prim_chip_RAM_1":
                RAM += 1
                assert len(primitive.consumers) == len(primitive.producers) == 8
            else:
                l2caches += 1
                assert len(primitive.consumers) == len(primitive.producers) == 4
        assert l2caches == 2
        assert RAM == 1

    def test_doubleClusterL1(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "cluster_0", 4, 1000)
        designer.addPeCluster(1, "cluster_1", 4, 1000)
        designer.addCacheForPEs(0, 1000, 1000, 1000, 1000)
        designer.addCacheForPEs(1, 1000, 1000, 1000, 1000)
        designer.addCommunicationResource(
            "L2Cache_0", [0], 1000, 1000, 1000, 1000
        )
        designer.addCommunicationResource(
            "L2Cache_1", [1], 1000, 1000, 1000, 1000
        )
        designer.addCommunicationResource("RAM", [0, 1], 1000, 1000, 1000, 1000)
        designer.finishElement()

        platform = designer.getPlatform()

        assert len(platform.processors()) == 8
        i = 0
        for element in platform.primitives():
            i += 1
        assert i == 11

        l1caches = 0
        l2caches = 0
        RAM = 0
        for primitive in platform.primitives():
            if primitive.name == "prim_chip_RAM_1":
                RAM += 1
                assert len(primitive.consumers) == len(primitive.producers) == 8
            elif primitive.name.split("_")[1] == "L1":
                l1caches += 1
            else:
                l2caches += 1
                assert len(primitive.consumers) == len(primitive.producers) == 4

        assert l1caches == 8
        assert l2caches == 2
        assert RAM == 1

    def test_networkOnChip(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "cluster_0", 4, 1000)
        designer.addPeCluster(1, "cluster_1", 4, 1000)
        designer.createNetworkForCluster(
            0,
            "testNet",
            {
                "PE00": ["PE01", "PE02"],
                "PE01": ["PE00", "PE03"],
                "PE02": ["PE00", "PE03"],
                "PE03": ["PE01", "PE02"],
            },
            simpleDijkstra,
            1000,
            1000,
            1000,
            1000,
            1000,
        )

        designer.addCommunicationResource(
            "L2Cache_1", [1], 1000, 1000, 1000, 1000
        )
        designer.addCommunicationResource("RAM", [0, 1], 1000, 1000, 1000, 1000)
        designer.finishElement()

        platform = designer.getPlatform()
        assert len(platform.processors()) == 8
        i = 0
        for element in platform.primitives():
            i += 1
        assert i == 6

        for prim in platform.primitives():
            if prim.name.split("_")[0] == "testNet":
                assert len(prim.producers) == 4
                assert len(prim.consumers) == 4
                assert len(prim.consume_phases) == 4
                assert len(prim.produce_phases) == 4

    def test_NetworkOfChips(self, designer):
        designer.newElement("chip_0")
        designer.addPeCluster(0, "cluster_0", 4, 1000)
        designer.addCacheForPEs(0, 1000, 1000, 1000, 1000)
        designer.addCommunicationResource("L2_0", [0], 1000, 1000, 1000, 1000)
        designer.finishElement()

        designer.newElement("chip_1")
        designer.addPeCluster(1, "cluster_1", 4, 1000)
        designer.addCacheForPEs(1, 1000, 1000, 1000, 1000)
        designer.addCommunicationResource("L2_1", [1], 1000, 1000, 1000, 1000)
        designer.finishElement()

        designer.newElement("chip_2")
        designer.addPeCluster(2, "cluster_2", 4, 1000)
        designer.addCacheForPEs(2, 1000, 1000, 1000, 1000)
        designer.addCommunicationResource("L2_2", [2], 1000, 1000, 1000, 1000)
        designer.finishElement()

        designer.newElement("chip_3")
        designer.addPeCluster(3, "cluster_3", 4, 1000)
        designer.addCacheForPEs(3, 1000, 1000, 1000, 1000)
        designer.addCommunicationResource("L2_3", [3], 1000, 1000, 1000, 1000)
        designer.finishElement()

        designer.createNetworkForChips(
            "testNet",
            {
                "chip_0": ["chip_1", "chip_2"],
                "chip_1": ["chip_0", "chip_3"],
                "chip_2": ["chip_0", "chip_3"],
                "chip_3": ["chip_1", "chip_2"],
            },
            simpleDijkstra,
            1000,
            1000,
            1000,
            1000,
            1000,
        )

        platform = designer.getPlatform()

        assert len(platform.processors()) == 16
        assert len(platform.primitives()) == 36

        l1Caches = 0
        l2Caches = 0
        netPrim = 0

        for prim in platform.primitives():
            name = prim.name.split("_")

            if name[1] == "testNet":
                netPrim += 1
                assert len(prim.producers) == 16
                assert len(prim.consumers) == 16
                assert len(prim.consume_phases) == 16
                assert len(prim.produce_phases) == 16
            elif name[1] == "L1":
                l1Caches += 1
            elif name[3] == "L2":
                l2Caches += 1
            else:
                assert False

        assert l1Caches == 16
        assert l2Caches == 4
        assert netPrim == 16

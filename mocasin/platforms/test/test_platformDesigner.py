# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

from mocasin.platforms.utils import simpleDijkstra


class TestPlatformDesigner(object):
    def test_singleCluster(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "TestCluster", 4, 1000)
        designer.addCommunicationResource(
            "RAM", [0], 100, 200, 16, 8, frequencyDomain=100000000  # 100 MHz
        )
        designer.finishElement()

        platform = designer.getPlatform()

        assert len(platform.processors()) == 4
        assert len(platform.primitives()) == 1

        assert len(platform.primitives()) == 1
        ram_prim = platform.find_primitive("prim_chip_RAM_1")
        assert len(ram_prim.consumers) == len(ram_prim.producers) == 4

        for src, sink in zip(platform.processors(), platform.processors()):
            assert ram_prim.static_consume_costs(sink, 0) == 1000000  # 1 us
            assert ram_prim.static_produce_costs(src, 0) == 2000000  # 2 us

            assert ram_prim.static_consume_costs(sink, 1024) == 1640000
            assert ram_prim.static_produce_costs(src, 1024) == 3280000

            assert ram_prim.static_costs(src, sink, 0) == 3000000
            assert ram_prim.static_costs(src, sink, 8) == 3015000
            assert ram_prim.static_costs(src, sink, 1024) == 4920000

    def test_doubleCluster(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "cluster_0", 4, 1000)
        designer.addPeCluster(1, "cluster_1", 4, 1000)
        designer.addCommunicationResource(
            "L2Cache_0", [0], 8, 8, 32, 32, frequencyDomain=1000000000  # 1 GHz
        )
        designer.addCommunicationResource(
            "L2Cache_1", [1], 8, 8, 32, 32, frequencyDomain=1000000000  # 1 GHz
        )
        designer.addCommunicationResource(
            "RAM", [0, 1], 100, 200, 16, 8, frequencyDomain=100000000  # 100 MHz
        )
        designer.finishElement()

        platform = designer.getPlatform()

        assert len(platform.processors()) == 8
        assert len(platform.primitives()) == 3

        prim_ram = platform.find_primitive("prim_chip_RAM_1")
        prim_l2_0 = platform.find_primitive("prim_chip_L2Cache_0_1")
        prim_l2_1 = platform.find_primitive("prim_chip_L2Cache_1_1")

        assert len(prim_ram.consumers) == len(prim_ram.producers) == 8
        assert len(prim_l2_0.consumers) == len(prim_l2_0.producers) == 4
        assert len(prim_l2_1.consumers) == len(prim_l2_1.producers) == 4

        for src in platform.processors():
            for sink in platform.processors():
                assert prim_ram.static_consume_costs(sink, 0) == 1000000  # 1 us
                assert prim_ram.static_produce_costs(src, 0) == 2000000  # 2 us

                assert prim_ram.static_consume_costs(sink, 1024) == 1640000
                assert prim_ram.static_produce_costs(src, 1024) == 3280000

                assert prim_ram.static_costs(src, sink, 0) == 3000000
                assert prim_ram.static_costs(src, sink, 8) == 3015000
                assert prim_ram.static_costs(src, sink, 1024) == 4920000

        for prim in [prim_l2_0, prim_l2_1]:
            for src in prim.producers:
                for sink in prim.consumers:
                    assert prim.static_consume_costs(sink, 0) == 8000  # 8 ns
                    assert prim.static_produce_costs(src, 0) == 8000  # 8 ns

                    assert prim.static_consume_costs(sink, 1024) == 40000
                    assert prim.static_produce_costs(src, 1024) == 40000

                    assert prim.static_costs(src, sink, 0) == 16000
                    assert prim.static_costs(src, sink, 8) == 16500
                    assert prim.static_costs(src, sink, 1024) == 80000

    def test_doubleClusterL1(self, designer):
        designer.newElement("chip")
        designer.addPeCluster(0, "cluster_0", 4, 1000)
        designer.addPeCluster(1, "cluster_1", 4, 1000)
        designer.addCacheForPEs(
            0, 1, 1, 64, 64, frequencyDomain=1000000000  # 1 GHz
        )
        designer.addCacheForPEs(
            1, 1, 1, 64, 64, frequencyDomain=1000000000  # 1 GHz
        )
        designer.addCommunicationResource(
            "L2Cache_0", [0], 8, 8, 32, 32, frequencyDomain=1000000000  # 1 GHz
        )
        designer.addCommunicationResource(
            "L2Cache_1", [1], 8, 8, 32, 32, frequencyDomain=1000000000  # 1 GHz
        )
        designer.addCommunicationResource(
            "RAM", [0, 1], 100, 200, 16, 8, frequencyDomain=100000000  # 100 MHz
        )
        designer.finishElement()

        platform = designer.getPlatform()

        assert len(platform.processors()) == 8
        assert len(platform.primitives()) == 11

        prim_ram = platform.find_primitive("prim_chip_RAM_1")
        prim_l2_0 = platform.find_primitive("prim_chip_L2Cache_0_1")
        prim_l2_1 = platform.find_primitive("prim_chip_L2Cache_1_1")
        prim_l1 = [
            platform.find_primitive(f"prim_L1_PE0{i}") for i in range(0, 8)
        ]

        for src in platform.processors():
            for sink in platform.processors():
                assert prim_ram.static_consume_costs(sink, 0) == 1000000  # 1 us
                assert prim_ram.static_produce_costs(src, 0) == 2000000  # 2 us

                assert prim_ram.static_consume_costs(sink, 1024) == 1640000
                assert prim_ram.static_produce_costs(src, 1024) == 3280000

                assert prim_ram.static_costs(src, sink, 0) == 3000000
                assert prim_ram.static_costs(src, sink, 8) == 3015000
                assert prim_ram.static_costs(src, sink, 1024) == 4920000

        for prim in [prim_l2_0, prim_l2_1]:
            assert len(prim.consumers) == len(prim.producers) == 4
            for src in prim.producers:
                for sink in prim.consumers:
                    assert prim.static_consume_costs(sink, 0) == 8000  # 8 ns
                    assert prim.static_produce_costs(src, 0) == 8000  # 8 ns

                    assert prim.static_consume_costs(sink, 1024) == 40000
                    assert prim.static_produce_costs(src, 1024) == 40000

                    assert prim.static_costs(src, sink, 0) == 16000
                    assert prim.static_costs(src, sink, 8) == 16500
                    assert prim.static_costs(src, sink, 1024) == 80000

        for prim in prim_l1:
            assert len(prim.consumers) == len(prim.producers) == 1
            src = prim.producers[0]
            sink = prim.consumers[0]
            assert prim.static_consume_costs(sink, 0) == 1000  # 1 ns
            assert prim.static_produce_costs(src, 0) == 1000  # 1 ns

            assert prim.static_consume_costs(sink, 1024) == 17000  # 25 ns
            assert prim.static_produce_costs(src, 1024) == 17000  # 25 ns

            assert prim.static_costs(src, sink, 0) == 2000
            assert prim.static_costs(src, sink, 8) == 2250
            assert prim.static_costs(src, sink, 1024) == 34000

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

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

from mocasin.platforms.utils import simpleDijkstra
from mocasin.platforms.platformDesigner import cluster, genericProcessor
from mocasin.platforms.topologies import meshTopology


class TestPlatformDesigner(object):
    def test_singleCluster(self, designer):
        processor = genericProcessor("TestCluster", 1000)
        chip = cluster("chip", designer)
        ram = chip.addStorage("RAM", 100, 200, 16, 8, 100000000)
        for i in range(4):
            pe = chip.addPeToCluster(
                f"pe{i}",
                processor.type,
                processor.frequency_domain,
                processor.power_model,
                processor.context_load_cycles,
                processor.context_store_cycles,
            )
            designer.connectComponents(pe, ram)

        platform = designer.getPlatform()
        platform.generate_all_primitives()

        num_processors = len(platform.processors())
        assert num_processors == 4
        assert len(platform.primitives()) == num_processors * num_processors

        for src, sink in zip(platform.processors(), platform.processors()):
            prim = platform.find_primitive(f"prim_{src}_{sink}")
            assert prim.static_consume_costs(sink, 0) == 1000000  # 1 us
            assert prim.static_produce_costs(src, 0) == 2000000  # 2 us

            assert prim.static_consume_costs(sink, 1024) == 1640000
            assert prim.static_produce_costs(src, 1024) == 3280000

            assert prim.static_costs(src, sink, 0) == 3000000
            assert prim.static_costs(src, sink, 8) == 3015000
            assert prim.static_costs(src, sink, 1024) == 4920000

    def test_doubleCluster(self, designer):
        processor = genericProcessor("TestCluster", 1000)
        chip = cluster("chip", designer)
        cluster0 = cluster("cluster_0", designer)
        cluster1 = cluster("cluster_1", designer)
        chip.addCluster(cluster0)
        chip.addCluster(cluster1)

        L2Cache_0 = cluster0.addStorage(
            "L2Cache_0", 8, 8, 32, 32, 1000000000  # 1 GHz
        )
        for i in range(4):
            pe = cluster0.addPeToCluster(
                f"pe{i}",
                processor.type,
                processor.frequency_domain,
                processor.power_model,
                processor.context_load_cycles,
                processor.context_store_cycles,
            )
            designer.connectComponents(pe, L2Cache_0)

        L2Cache_1 = cluster1.addStorage(
            "L2Cache_1", 8, 8, 32, 32, 1000000000  # 1 GHz
        )
        for i in range(4):
            pe = cluster1.addPeToCluster(
                f"pe{i}",
                processor.type,
                processor.frequency_domain,
                processor.power_model,
                processor.context_load_cycles,
                processor.context_store_cycles,
            )
            designer.connectComponents(pe, L2Cache_1)

        ram = chip.addStorage("RAM", 100, 200, 16, 8, 100000000)  # 100 MHz
        designer.connectComponents(L2Cache_0, ram)
        designer.connectComponents(L2Cache_1, ram)

        platform = designer.getPlatform()
        platform.generate_all_primitives()

        num_processors = len(platform.processors())
        assert num_processors == 8
        assert len(platform.primitives()) == num_processors * num_processors

        for src in platform.processors():
            for sink in platform.processors():
                if designer.getClusterForComponent(
                    src
                ) != designer.getClusterForComponent(sink):
                    prim = platform.find_primitive(f"prim_{src}_{sink}")
                    assert prim.static_consume_costs(sink, 0) == 1000000  # 1 us
                    assert prim.static_produce_costs(src, 0) == 2000000  # 2 us

                    assert prim.static_consume_costs(sink, 1024) == 1640000
                    assert prim.static_produce_costs(src, 1024) == 3280000

                    assert prim.static_costs(src, sink, 0) == 3000000
                    assert prim.static_costs(src, sink, 8) == 3015000
                    assert prim.static_costs(src, sink, 1024) == 4920000

        for pes in [cluster0.getProcessors(), cluster1.getProcessors()]:
            for src in pes:
                for sink in pes:
                    prim = platform.find_primitive(f"prim_{src}_{sink}")
                    assert prim.static_consume_costs(sink, 0) == 8000  # 8 ns
                    assert prim.static_produce_costs(src, 0) == 8000  # 8 ns

                    assert prim.static_consume_costs(sink, 1024) == 40000
                    assert prim.static_produce_costs(src, 1024) == 40000

                    assert prim.static_costs(src, sink, 0) == 16000
                    assert prim.static_costs(src, sink, 8) == 16500
                    assert prim.static_costs(src, sink, 1024) == 80000


    def test_networkOnChip(self, designer):
        processor = genericProcessor("TestCluster", 1000)
        chip = cluster("chip", designer)
        cluster0 = cluster("cluster_0", designer)
        chip.addCluster(cluster0)

        noc0 = list()
        for i in range(4):
            pe = cluster0.addPeToCluster(
                f"pe{i}",
                processor.type,
                processor.frequency_domain,
                processor.power_model,
                processor.context_load_cycles,
                processor.context_store_cycles,
            )
            router = cluster0.addRouter(
                f"router{i}",
                1000,
                1000,
                1000,
                1000,
                1000,
            )
            designer.connectComponents(pe, router)
            noc0.append(router)

        designer.createNetwork(
            "noc0",
            noc0,
            meshTopology,
        )

        platform = designer.getPlatform()
        platform.generate_all_primitives()

        num_processors = len(platform.processors())
        assert num_processors == 4
        assert len(platform.primitives()) == num_processors * num_processors

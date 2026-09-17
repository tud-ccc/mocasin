# Copyright (C) 2026 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

"""Performance model of the AMD Kria KV260 starter kit.

The programmable logic is intentionally represented as one processing unit.
"""

from mocasin.common.platform import (
    CommunicationPhase,
    FrequencyDomain,
    Platform,
    Primitive,
)
from mocasin.platforms.platformDesigner import PlatformDesigner, cluster


class DesignerPlatformKriaKV260(Platform):
    """Model a KV260 as four Cortex-A53 cores and one FPGA processing unit.

    Each Cortex-A53 core has a private L1 cache and all four cores share an L2
    cache. The Cortex-A53 cluster and the programmable logic communicate via
    DDR4. The PS interconnect and the PL's AXI path are folded into the DDR4
    communication costs rather than represented as separate resources.
    """

    def __init__(
        self,
        name="kria_kv260",
        a53_frequency=1_333_000_000,
        pl_frequency=100_000_000,
        l1_read_latency=1,  # placeholder
        l1_write_latency=1,  # placeholder
        l1_read_throughput=8,  # placeholder
        l1_write_throughput=8,  # placeholder
        l2_read_latency=21,  # placeholder
        l2_write_latency=21,  # placeholder
        l2_read_throughput=8,  # placeholder
        l2_write_throughput=8,  # placeholder
        pl_local_read_latency=1,  # placeholder
        pl_local_write_latency=1,  # placeholder
        pl_local_read_throughput=4,  # placeholder
        pl_local_write_throughput=4,  # placeholder
        memory_frequency=1_200_000_000,  # placeholder
        memory_read_latency=120,  # placeholder
        memory_write_latency=120,  # placeholder
        memory_read_throughput=16,  # placeholder
        memory_write_throughput=16,  # placeholder
        a53_scheduling_cycles=1000,  # placeholder
        pl_scheduling_cycles=0,
        symmetries_json=None,
    ):
        super().__init__(name, symmetries_json=symmetries_json)

        designer = PlatformDesigner(self)
        kv260 = cluster(name, designer)
        a53_cluster = cluster("a53_cluster", designer)
        kv260.addCluster(a53_cluster)

        # Cortex-A53 cache hierarchy.
        designer.setSchedulingPolicy("FIFO", a53_scheduling_cycles)
        a53_domain = FrequencyDomain("fd_cortex_a53", a53_frequency)
        l2 = a53_cluster.addStorage(
            "l2",
            l2_read_latency,
            l2_write_latency,
            l2_read_throughput,
            l2_write_throughput,
            a53_frequency,
        )
        cpu_paths = {}
        for index in range(4):
            processor = a53_cluster.addPeToCluster(
                f"cortex_a53_{index}",
                "CortexA53",
                a53_domain,
                None,
                0,
                0,
            )
            l1 = a53_cluster.addStorage(
                f"l1_{index}",
                l1_read_latency,
                l1_write_latency,
                l1_read_throughput,
                l1_write_throughput,
                a53_frequency,
            )
            designer.connectComponents(processor, l1)
            designer.generatePrimitivesForStorage(l1)
            designer.connectComponents(l1, l2)
            cpu_paths[processor] = [l1, l2]
        designer.generatePrimitivesForStorage(l2)

        # The FPGA is a single, non-preemptive processing unit in this model.
        designer.setSchedulingPolicy("FIFO", pl_scheduling_cycles)
        pl_domain = FrequencyDomain("fd_k26_pl", pl_frequency)
        fpga = kv260.addPeToCluster(
            "fpga",
            "K26_PL",
            pl_domain,
            None,
            0,
            0,
        )
        pl_local = kv260.addStorage(
            "pl_local",
            pl_local_read_latency,
            pl_local_write_latency,
            pl_local_read_throughput,
            pl_local_write_throughput,
            pl_frequency,
        )
        designer.connectComponents(fpga, pl_local)

        # DDR4 path, including the PS interconnect and PL AXI path.
        memory = kv260.addStorage(
            "ddr4",
            memory_read_latency,
            memory_write_latency,
            memory_read_throughput,
            memory_write_throughput,
            memory_frequency,
        )
        designer.connectComponents(l2, memory)
        designer.connectComponents(fpga, memory)

        # Local FPGA communication. This is the only primitive that supports
        # K26_PL-to-K26_PL channels, so they cannot accidentally use DDR4.
        pl_local_primitive = Primitive("prim_pl_local")
        pl_local_primitive.add_producer(
            fpga,
            [CommunicationPhase("produce", [pl_local], "write")],
        )
        pl_local_primitive.add_consumer(
            fpga,
            [CommunicationPhase("consume", [pl_local], "read")],
        )
        self.add_primitive(pl_local_primitive)

        # CPU-only access to DDR4. Cross-domain transfers use separate
        # directional primitives below.
        cpu_ddr_primitive = Primitive("prim_cpu_ddr")
        for processor, cache_path in cpu_paths.items():
            cpu_ddr_primitive.add_producer(
                processor,
                [CommunicationPhase("produce", cache_path + [memory], "write")],
            )
            cpu_ddr_primitive.add_consumer(
                processor,
                [
                    CommunicationPhase(
                        "consume",
                        [memory] + list(reversed(cache_path)),
                        "read",
                    )
                ],
            )
        self.add_primitive(cpu_ddr_primitive)

        cpu_to_pl_primitive = Primitive("prim_cpu_to_pl")
        for processor, cache_path in cpu_paths.items():
            cpu_to_pl_primitive.add_producer(
                processor,
                [CommunicationPhase("produce", cache_path + [memory], "write")],
            )
        cpu_to_pl_primitive.add_consumer(
            fpga,
            [CommunicationPhase("consume", [memory], "read")],
        )
        self.add_primitive(cpu_to_pl_primitive)

        pl_to_cpu_primitive = Primitive("prim_pl_to_cpu")
        pl_to_cpu_primitive.add_producer(
            fpga,
            [CommunicationPhase("produce", [memory], "write")],
        )
        for processor, cache_path in cpu_paths.items():
            pl_to_cpu_primitive.add_consumer(
                processor,
                [
                    CommunicationPhase(
                        "consume",
                        [memory] + list(reversed(cache_path)),
                        "read",
                    )
                ],
            )
        self.add_primitive(pl_to_cpu_primitive)

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens
import logging
log = logging.getLogger(__name__)

from pykpn.common.platform import Platform, FrequencyDomain
from pykpn.platforms.platformDesigner import PlatformDesigner

class DesignerPlatformOdroid(Platform):
    def __init__(self, processor_1, processor_2, name="odroid"):
        super(DesignerPlatformOdroid, self).__init__(name)
        processor1 = processor_1.to_pykpn_processor()
        if processor1.frequency_domain.frequency != 1400000000.0:
            log.warning(f"Rescaling processor {processor_1.name} to fit Odroid frequency")
            fd_a7 = FrequencyDomain('fd_a7', 1400000000.0)
            processor1.frequency_domain = fd_a7

        processor2 = processor_2.to_pykpn_processor()
        designer = PlatformDesigner(self)
        if processor2.frequency_domain.frequency != 2000000000.0:
            log.warning(f"Rescaling processor {processor_2.name} to fit Odroid frequency")
            fd_a15 = FrequencyDomain('fd_a15', 2000000000.0)
            processor2.frequency_domain = fd_a15

        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("exynos5422")

        # cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_a7",
                                          processor1,
                                          4)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_a7", 1, 0, 8.0, float('inf'), frequencyDomain=1400000000.0, name='L1_A7')
        designer.addCommunicationResource("L2_A7",
                                          ["cluster_a7"],
                                          250,
                                          250,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=1400000000.0)

        # cluster 1, with l2 cache
        designer.addPeClusterForProcessor("cluster_a15",
                                          processor2,
                                          4)
        # Add L1/L2 caches
        designer.addCacheForPEs("cluster_a15", 1, 4, 8.0, 8.0, frequencyDomain=2000000000.0, name='L1_A15')
        designer.addCommunicationResource("L2_A15",
                                          ["cluster_a15"],
                                          250,
                                          250,
                                          float('inf'),
                                          float('inf'),
                                          frequencyDomain=2000000000.0)

        # RAM connecting all clusters
        designer.addCommunicationResource("DRAM",
                                          ["cluster_a7", "cluster_a15"],
                                          120,
                                          120,
                                          8.0,
                                          8.0,
                                          frequencyDomain=933000000.0)
        designer.finishElement()

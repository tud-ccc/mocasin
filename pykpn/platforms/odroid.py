# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens
import logging
log = logging.getLogger(__name__)

from pykpn.common.platform import Platform, FrequencyDomain, Processor
from pykpn.platforms.platformDesigner import PlatformDesigner
from hydra.utils import instantiate

class DesignerPlatformOdroid(Platform):
    def __init__(self, processor_0, processor_1, num_big=4, num_little=4,name="odroid",**kwargs):

        #workaraound for Hydra < 1.1
        if not isinstance(processor_0,Processor):
            processor_0 = instantiate(processor_0)
        if not isinstance(processor_1,Processor):
            processor_1 = instantiate(processor_1)
        super(DesignerPlatformOdroid, self).__init__(name,kwargs.get('symmetries_json',None))
        if processor_0.frequency_domain.frequency != 1400000000.0:
            log.warning(f"Rescaling processor {processor_0.name} to fit Odroid frequency")
            fd_a7 = FrequencyDomain('fd_a7', 1400000000.0)
            processor_0.frequency_domain = fd_a7

        designer = PlatformDesigner(self)
        if processor_1.frequency_domain.frequency != 2000000000.0:
            log.warning(f"Rescaling processor {processor_1.name} to fit Odroid frequency")
            fd_a15 = FrequencyDomain('fd_a15', 2000000000.0)
            processor_1.frequency_domain = fd_a15

        designer.setSchedulingPolicy('FIFO', 1000)
        designer.newElement("exynos5422")

        # cluster 0 with l2 cache
        designer.addPeClusterForProcessor("cluster_a7",
                                          processor_0,
                                          num_little)
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
                                          processor_1,
                                          num_big)
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

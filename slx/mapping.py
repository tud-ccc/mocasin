# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import xml.etree.ElementTree as ET
import logging

from pytrm import Mapping
from pytrm import SchedulerInfo
from pytrm import ChannelInfo
from pytrm import SchedulingPolicy

log = logging.getLogger(__name__)


class SlxMapping(Mapping):

    def __init__(self, mapping_file):
        Mapping.__init__(self)
        tree = ET.parse(mapping_file)
        self.xmlroot = tree.getroot()

        # parse the scheduler descriptors
        for desc in self.xmlroot.findall('SingleSchedulerDesc'):
            s = SchedulerInfo()
            id = desc.get('ID')
            s.name = desc.get('Name')
            s.policy = SchedulingPolicy[desc.get('SchedulingPolicy')]
            s.processNames = []
            for p in desc.iter('Process'):
                s.processNames.append(p.get('Name'))
            s.processorNames = []
            for s2g in self.xmlroot.iter('Scheduler2Group'):
                if id == s2g.get('SchedulerID'):
                    groupID = s2g.get('GroupID')
                    for group in self.xmlroot.iter('PeGroup'):
                        if groupID == group.get('GroupId'):
                            l = group.get('Processors').split(' ')
                            s.processorNames = l
            self.schedulers.append(s)

        # parse the channel descriptors
        for bound in self.xmlroot.iter('FifoBound'):
            c = ChannelInfo()
            c.name = bound.get('Fifo')
            c.capacity = int(bound.get('Bound'))

            for mapping in self.xmlroot.iter('ChannelMapping'):
                if c.name == mapping.get('PnChannel'):
                    c.primitive = mapping.get('CommPrimitive')
                    c.processorFrom = mapping.get('ProcessorFrom')
                    c.viaMemory = mapping.get('Memory')
                    c.processorTo = mapping.get('ProcessorTo')
            self.channels.append(c)

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import xml.etree.ElementTree as ET
import logging

from ..common import Mapping
from ..common import ChannelMappingInfo
from ..common import ProcessMappingInfo

log = logging.getLogger(__name__)


class SlxMapping(Mapping):

    def __init__(self, kpn, platform, mapping_file):
        Mapping.__init__(self, kpn, platform)

        tree = ET.parse(mapping_file)
        xmlroot = tree.getroot()

        log.info('Start parsing the SLX mapping ' + mapping_file)

        # parse the scheduler descriptors
        for desc in xmlroot.findall('SingleSchedulerDesc'):
            schedulerName = desc.get('Name')
            log.debug('  Found a scheduling descriptor for ' + schedulerName)

            scheduler = platform.findScheduler(schedulerName)
            if scheduler is None:
                raise RuntimeError('The scheduler ' + schedulerName +
                                   'is not defined by the platform')

            policy = desc.get('SchedulingPolicy')
            log.debug('    It uses the ' + policy + ' policy')
            if policy not in scheduler.policies:
                fallback = list(scheduler.policies.keys())[0]
                log.warn('The scheduler ' + schedulerName + ' does not ' +
                         'support the requested scheduling policy. Falling '
                         'back to ' + fallback)
                policy = fallback

            log.debug('    and schedules the following processes:')

            for p in desc.iter('Process'):
                processName = p.get('Name')
                log.debug('      * ' + processName)
                kpnProcess = kpn.findProcess(processName)
                log.debug('    Found the process ' + processName + ' policy')
                if kpnProcess is None:
                    raise RuntimeError('The process ' + processName +
                                       ' is not defined by the KPN graph')

                self.processMappings.append(ProcessMappingInfo(kpnProcess,
                                                               scheduler,
                                                               policy))
        # parse the channel descriptors
        for bound in xmlroot.iter('FifoBound'):
            channelName = bound.get('Fifo')
            capacity = int(bound.get('Bound'))

            mapping = self.findChannelMapping(xmlroot, channelName)
            assert mapping is not None

            log.debug('  Found a channel descriptor for ' + channelName)
            log.debug('    It is bound to ' + str(capacity) + ' tokens')

            kpnChannel = kpn.findChannel(channelName)
            if kpnChannel is None:
                raise RuntimeError('The channel ' + channelName +
                                   ' is not defined by the KPN graph')
            processorNameFrom = mapping.get('ProcessorFrom')
            processorNameTo = mapping.get('ProcessorTo')
            viaMemoryName = mapping.get('Memory')
            primitiveType = mapping.get('CommPrimitive')

            primitiveString = ''.join([primitiveType,
                                       ': ',
                                       processorNameFrom,
                                       ' -> ',
                                       viaMemoryName,
                                       ' -> ',
                                       processorNameTo])
            log.debug('    and uses this primitive: ' + primitiveString)

            processorFrom = platform.findProcessor(processorNameFrom)
            processorTo = platform.findProcessor(processorNameTo)
            viaMemory = platform.findStorageDevice(viaMemoryName)

            if processorFrom is None:
                raise RuntimeError('The processor ' + processorNameFrom +
                                   ' is not defined by the platform')
            if processorTo is None:
                raise RuntimeError('The processor ' + processorNameTo +
                                   ' is not defined by the platform')
            if viaMemory is None:
                raise RuntimeError('The memory ' + viaMemory +
                                   ' is not defined by the platform')

            primitive = platform.findPrimitive(primitiveType,
                                               processorFrom,
                                               processorTo,
                                               viaMemory)
            if primitive is None:
                raise RuntimeError('The primitive ' + primitiveString +
                                   ' is not defined by the platform')

            self.channelMappings.append(ChannelMappingInfo(kpnChannel,
                                                           capacity,
                                                           primitive))

        log.info('Done parsing the SLX mapping')

    def findChannelMapping(self, xmlroot, name):
        for mapping in xmlroot.iter('ChannelMapping'):
            if name == mapping.get('PnChannel'):
                return mapping
        return None

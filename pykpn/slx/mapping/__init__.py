# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import pint

from pykpn.common import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)


log = logging.getLogger(__name__)


_ur = pint.UnitRegistry()


class SlxMapping(Mapping):

    def __init__(self, kpn, platform, mapping_file, version='2017.10'):
        super().__init__(kpn, platform)

        self._slx_version = version

        log.info('Start parsing the SLX mapping ' + mapping_file)

        # load the xml
        with open(mapping_file) as mf:
            if (version == '2017.10'):
                from ._2017_10 import slxmapping
                xml_mapping = slxmapping.CreateFromDocument(mf.read())
            elif (version == '2017.04'):
                from ._2017_04 import slxmapping
                xml_mapping = slxmapping.CreateFromDocument(mf.read())
            else:
                raise ValueError('SLX version %s is not supported!' % version)

        # keep track of the mapping process->scheduler
        process_scheduler = {}
        # parse schedulers
        for xs in xml_mapping.Scheduler:
            name = xs.id
            scheduler = platform.find_scheduler(name)

            # the policy mechanism differs depending on the version
            if (version == '2017.10'):
                policy = scheduler.policies[0]
                param = None
                log.warn('2017.10 mapping descriptors do not specify the '
                         'scheduling policy. -> Set the policy for %s to the '
                         'first policy specified by the platform (%s)' %
                         (name, policy.name))
            elif (version == '2017.04'):
                if xs.timeSliceValue is not None:
                    time_slice = _ur(str(xs.timeSliceValue) + xs.timeSliceUnit)
                    param = time_slice.to('ps').magnitude
                else:
                    param = None
                policy = scheduler.find_policy(xs.policy)
            else:
                raise NotImplementedError(
                    'policy parsing not implemented for version %s!' % version)

            for pref in xs.ProcessRef:
                pname = pref.process
                process_scheduler[pname] = scheduler
            info = SchedulerMappingInfo(policy, param)
            self.add_scheduler_info(scheduler, info)
            log.debug('configure scheduler %s to use policy %s' %
                      (name, policy.name))

        # parse processes
        for xp in xml_mapping.Process:
            name = xp.id
            p_name = xp.ProcessorAffinityRef[0].processor
            processor = platform.find_processor(p_name)
            priority = int(xp.priority)
            info = ProcessMappingInfo(process_scheduler[name], processor,
                                      priority)
            self._process_info[name] = info
            log.debug('map process %s to scheduler %s and affinity %s '
                      '(priority: %d)' % (name, process_scheduler[name].name,
                                          p_name, priority))

        # parse channels
        for xc in xml_mapping.Channel:
            capacity = int(xc.bound)
            prim = platform.find_primitive(xc.commPrimitive)
            info = ChannelMappingInfo(prim, capacity)
            self._channel_info[xc.id] = info
            log.debug('map channel %s to primitive %s and bound to %s tokens'
                      % (xc.id, prim.name, capacity))

        log.info('Done parsing the SLX mapping')

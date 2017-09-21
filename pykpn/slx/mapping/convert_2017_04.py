# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
from ..platform.convert_2017_04 import get_value_in_unit


from ...common import ChannelMappingInfo
from ...common import ProcessMappingInfo
from ...common import SchedulerMappingInfo

log = logging.getLogger(__name__)


def convert(mapping, xml_mapping):
    platform = mapping._platform
    kpn = mapping._kpn

    # keep track of the mapping process->scheduler while parsing the schedulers
    process_scheduler = {}
    # parse schedulers
    for xs in xml_mapping.get_Scheduler():
        name = xs.get_id()
        scheduler = platform.find_scheduler(name, True)
        policy = scheduler.find_policy(xs.get_policy())
        param = get_value_in_unit(xs, 'timeSlice', 'ps', None)
        processes = []
        for pref in xs.get_ProcessRef():
            pname = pref.get_process()
            process_scheduler[pname] = scheduler
            processes.append(kpn.find_process(pname))
        info = SchedulerMappingInfo(None, policy, param)
        mapping._scheduler_info[name] = info

    # parse processes
    for xp in xml_mapping.get_Process():
        name = xp.get_id()
        affinity_ref = xp.get_ProcessorAffinityRef()
        processor = affinity_ref[0].get_processor()
        info = ProcessMappingInfo(process_scheduler[name], processor)
        mapping._process_info[name] = info

    # parse channels
    for xc in xml_mapping.get_Channel():
        name = xc.get_id()
        capacity = int(xc.get_bound())
        prim_type = xc.get_commPrimitive()
        info = ChannelMappingInfo(prim_type, capacity)
        mapping._channel_info[name] = info

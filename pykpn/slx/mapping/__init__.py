# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


import pint

from pykpn.util import logging
from pykpn.common.mapping import (ChannelMappingInfo, Mapping,
    ProcessMappingInfo, SchedulerMappingInfo)


log = logging.getLogger(__name__)


_ur = pint.UnitRegistry()


class SlxMapper:
    """
    Reads a SLX mapping from a file. The actual mapping is returned when
    calling the generate_mapping method.  This implements the common mapper
    interface.
    """
    def __init__(self, kpn, platform, cfg, mapping_xml=None, slx_version=None):
        self.mapping = SlxMapping(kpn, platform, mapping_xml, slx_version)

    def generate_mapping(self):
        return self.mapping


class SlxMapping(Mapping):

    #config parameter is not needed but still added to remain the interface of other mappings types in order
    #to ensure instantiation via hydra
    def __init__(self, kpn, platform, mapping_xml=None, slx_version=None):
        super().__init__(kpn, platform)

        log.info('Start parsing the SLX mapping ' + mapping_xml)

        # load the xml
        with open(mapping_xml) as mf:
            if (slx_version == '2017.10'):
                from ._2017_10 import slxmapping
                xml_mapping = slxmapping.CreateFromDocument(mf.read())
            elif (slx_version == '2017.04'):
                from ._2017_04 import slxmapping
                xml_mapping = slxmapping.CreateFromDocument(mf.read())
            else:
                raise ValueError('SLX version %s is not supported!' % slx_version)

        # keep track of the mapping process->scheduler
        process_scheduler = {}
        # parse schedulers
        for xs in xml_mapping.Scheduler:
            name = xs.id
            scheduler = platform.find_scheduler(name)

            # the policy mechanism differs depending on the version
            if (slx_version == '2017.10'):
                policy = scheduler.policies[0]
                param = None
                log.warning('2017.10 mapping descriptors do not specify the '
                            'scheduling policy. -> Set the policy for %s to the '
                            'first policy specified by the platform (%s)' %
                            (name, policy.name))
            elif (slx_version == '2017.04'):
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

    def export(self, file_name, version):
        export_slx_mapping(self, file_name, version)


def export_slx_mapping(mapping, file_name, version):
    if (version == '2017.10'):
        from ._2017_10 import slxmapping
    elif (version == '2017.04'):
        from ._2017_04 import slxmapping
    else:
        raise ValueError('SLX version %s is not supported!' % version)

    xml_mapping = slxmapping.MappingType()
    xml_mapping.version = '1.0'
    xml_mapping.platformName = mapping.kpn.name
    xml_mapping.applicationName = mapping.platform.name

    used_processors = []
    used_primitives = []

    # export processes
    for name, info in mapping._process_info.items():
        xml_process = slxmapping.ProcessType()
        xml_process.id = name
        xml_process.priority = info.priority

        xml_affinity = slxmapping.ProcessorRefType()
        xml_affinity.processor = info.affinity.name
        xml_process.ProcessorAffinityRef.append(xml_affinity)
        used_processors.append(info.affinity)

        xml_mapping.Process.append(xml_process)

    # export channels
    for name, info in mapping._channel_info.items():
        xml_channel = slxmapping.ChannelType()
        xml_channel.id = name
        xml_channel.bound = info.capacity
        xml_channel.commPrimitive = info.primitive.name
        channel = mapping.kpn.find_channel(name)
        xml_channel.processWriter = channel.source.name
        used_primitives.append(info.primitive)

        for sink in channel.sinks:
            xml_reader = slxmapping.ProcessRefType()
            xml_reader.process = sink.name
            xml_channel.ProcessReaderRef.append(xml_reader)

        xml_mapping.Channel.append(xml_channel)

    # export processors
    for p in used_processors:
        xml_processor = slxmapping.ProcessorType()
        xml_processor.id = p.name
        xml_processor.type = p.type

        xml_mapping.Processor.append(xml_processor)

    # export primitives
    for p in used_primitives:
        xml_primitive = slxmapping.CommPrimitiveType()
        xml_primitive.id = p.name

        xml_mapping.CommPrimitive.append(xml_primitive)

    # export schedulers
    for name, info in mapping._scheduler_info.items():
        xml_scheduler = slxmapping.SchedulerType()
        xml_scheduler.id = name

        scheduler = mapping.platform.find_scheduler(name)
        for p in scheduler.processors:
            xml_processor_ref = slxmapping.ProcessorRefType()
            xml_processor_ref.processor = p.name
            xml_scheduler.ProcessorRef.append(xml_processor_ref)

        for p in mapping.scheduler_processes(scheduler):
            xml_process_ref = slxmapping.ProcessRefType()
            xml_process_ref.process = p.name
            xml_scheduler.ProcessRef.append(xml_process_ref)

        if version == '2017.10':
            log.warning('slx 2017.10 mapping descriptors do not support '
                        'scheduling policies -> truncate while exporting')
        elif version == '2017.04':
            xml_scheduler.policy = info.policy.name
            # has param?
            if info.param is not None:
                if isinstance(info.param, int):
                    # interpret it as the time slice value
                    xml_scheduler.timeSliceValue = info.param
                    xml_scheduler.timeSliceUnit = 'ps'
                else:
                    log.warning('found a unknown scheduler parameter '
                                '-> ignore it during export')

        xml_mapping.Scheduler.append(xml_scheduler)

    with open(file_name, 'w+') as f:
        dom = xml_mapping.toDOM(element_name='slxmapping:Mapping')
        f.write(dom.toprettyxml())
        log.info('wrote %s', file_name)

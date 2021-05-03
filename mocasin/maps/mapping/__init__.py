# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import logging
import pint

from hydra.utils import to_absolute_path

from mocasin.common.mapping import (
    ChannelMappingInfo,
    Mapping,
    ProcessMappingInfo,
)
from mocasin.maps.mapping import mapsmapping


log = logging.getLogger(__name__)


_ur = pint.UnitRegistry()


class MapsMapper:
    """
    Reads a MAPS mapping from a file. The actual mapping is returned when
    calling the generate_mapping method.  This implements the common mapper
    interface.
    """

    def __init__(self, graph, platform, trace, representation, xml_file=None):
        self.mapping = MapsMapping(graph, platform, xml_file)

    def generate_mapping(self):
        return self.mapping


class MapsMapping(Mapping):
    def __init__(self, graph, platform, xml_file):
        super().__init__(graph, platform)

        log.info("Start parsing the MAPS mapping " + xml_file)

        # load the xml
        with open(to_absolute_path(xml_file)) as f:
            xml_mapping = mapsmapping.CreateFromDocument(f.read())

        # keep track of the mapping process->scheduler
        process_scheduler = {}
        # parse schedulers
        for xs in xml_mapping.Scheduler:
            name = xs.id
            scheduler = platform.find_scheduler(name)
            for pref in xs.ProcessRef:
                pname = pref.process
                process_scheduler[pname] = scheduler

        for xp in xml_mapping.Process:
            name = xp.id
            p_name = xp.ProcessorAffinityRef[0].processor
            processor = platform.find_processor(p_name)
            priority = int(xp.priority)
            info = ProcessMappingInfo(
                process_scheduler[name], processor, priority
            )
            self._process_info[name] = info
            log.debug(
                "map process %s to scheduler %s and affinity %s "
                "(priority: %d)"
                % (name, process_scheduler[name].name, p_name, priority)
            )

        # parse channels
        for xc in xml_mapping.Channel:
            capacity = int(xc.bound)
            prim = platform.find_primitive(xc.commPrimitive)
            info = ChannelMappingInfo(prim, capacity)
            self._channel_info[xc.id] = info
            log.debug(
                "map channel %s to primitive %s and bound to %s tokens"
                % (xc.id, prim.name, capacity)
            )

        log.info("Done parsing the MAPS mapping")

    def export(self, file_name):
        export_maps_mapping(self, file_name)


def export_maps_mapping(mapping, file_name):
    xml_mapping = mapsmapping.MappingType()
    xml_mapping.version = "1.0"
    xml_mapping.platformName = mapping.graph.name
    xml_mapping.applicationName = mapping.platform.name

    used_processors = []
    used_primitives = []

    # export processes
    for name, info in mapping._process_info.items():
        xml_process = mapsmapping.ProcessType()
        xml_process.id = name
        xml_process.priority = info.priority

        xml_affinity = mapsmapping.ProcessorRefType()
        xml_affinity.processor = info.affinity.name
        xml_process.ProcessorAffinityRef.append(xml_affinity)
        used_processors.append(info.affinity)

        xml_mapping.Process.append(xml_process)

    # export channels
    for name, info in mapping._channel_info.items():
        xml_channel = mapsmapping.ChannelType()
        xml_channel.id = name
        xml_channel.bound = info.capacity
        xml_channel.commPrimitive = info.primitive.name
        channel = mapping.graph.find_channel(name)
        xml_channel.processWriter = channel.source.name
        used_primitives.append(info.primitive)

        for sink in channel.sinks:
            xml_reader = mapsmapping.ProcessRefType()
            xml_reader.process = sink.name
            xml_channel.ProcessReaderRef.append(xml_reader)

        xml_mapping.Channel.append(xml_channel)

    # export processors
    for p in used_processors:
        xml_processor = mapsmapping.ProcessorType()
        xml_processor.id = p.name
        xml_processor.type = p.type

        xml_mapping.Processor.append(xml_processor)

    # export primitives
    for p in used_primitives:
        xml_primitive = mapsmapping.CommPrimitiveType()
        xml_primitive.id = p.name

        xml_mapping.CommPrimitive.append(xml_primitive)

    # export schedulers
    for scheduler in mapping.platform.schedulers():
        xml_scheduler = mapsmapping.SchedulerType()
        xml_scheduler.id = scheduler.name

        for p in scheduler.processors:
            xml_processor_ref = mapsmapping.ProcessorRefType()
            xml_processor_ref.processor = p.name
            xml_scheduler.ProcessorRef.append(xml_processor_ref)

        for p in mapping.scheduler_processes(scheduler):
            xml_process_ref = mapsmapping.ProcessRefType()
            xml_process_ref.process = p.name
            xml_scheduler.ProcessRef.append(xml_process_ref)

        xml_mapping.Scheduler.append(xml_scheduler)

    with open(file_name, "w+") as f:
        dom = xml_mapping.toDOM(element_name="mapsmapping:Mapping")
        f.write(dom.toprettyxml())
        log.info("wrote %s", file_name)

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
from pint import UnitRegistry

from ...common import CommunicationPhase
from ...common import CommunicationResource
from ...common import FrequencyDomain
from ...common import Primitive
from ...common import Processor
from ...common import Scheduler
from ...common import SchedulingPolicy


ur = UnitRegistry()
log = logging.getLogger(__name__)


def create_policy_list(xml_platform, list_ref):
    policies = []
    for pl in xml_platform.get_SchedulingPolicyList():
        if pl.get_id() == list_ref:
            for p in pl.get_SchedulingPolicy():
                name = p.get_schedulingAlgorithm()
                # there is no scheduling delay in slx
                cycles = 0
                # 1 tick == 1 ps
                param = get_value_in_unit(p, 'timeSlice', 'ps', None)
                policies.append(SchedulingPolicy(name, cycles, param))
            return policies
    raise RuntimeError('Could not find the SchedulingPolicyList %s', list_ref)


def get_value_in_unit(obj, value_name, unit, default=None):
    """
    Read an objects value converted to a unit from the parsed xml.
    :param obj: the object who's value should be read
    :param value_name: name of the value to be read
    :param unit: the unit to  convert to
    :param default: value returned if the value is not defined in the xml
    """

    get_value = getattr(obj, 'get_%sValue' % value_name)
    get_unit = getattr(obj, 'get_%sUnit' % value_name)
    if get_value() is not None:
        return ur(get_value() + get_unit()).to(unit).magnitude
    return default


def get_value_in_cycles(obj, value_name, default=None):
    return get_value_in_unit(obj, value_name, 'cycle', default)


def get_value_in_byte_per_cycle(obj, value_name, default=None):
    return get_value_in_unit(obj, value_name, 'byte / cycle', default)


def find_elem(xml_platform, type_name, elem_name):
    """
    Find an element of a certain type in the platform.
    :param xml_platform: platform to search in
    :param type_name:    type of the element to be found
    :param elem_name:    name of the element to be found
    """
    get_type_elems = getattr(xml_platform, 'get_' + type_name)
    for elem in get_type_elems():
        if elem.get_id() == elem_name:
            return elem
    raise RuntimeError('%s %s was not defined', type_name, elem_name)


def convert(platform, xml_platform):
    # keep a map of scheduler names to processors, this helps when creating
    # scheduler objects
    schedulers_to_processors = {}
    for s in xml_platform.get_Scheduler():
        schedulers_to_processors[s.get_id()] = []

    # TODO implement scheduling delays correctly
    log.warn('SLX platforms do not specify scheduling delays! -> assume 0')

    # Collect all frequency domains
    frequency_domains = {}
    for fd in xml_platform.get_FrequencyDomain():
        name = fd.get_id()
        # we set the frequency to None. It will be set to the correct value
        # when read the mapping is read.
        frequency_domains[name] = FrequencyDomain(name, None)
        log.debug('Found frequency domain %s', name)

    # Initialize all Processors
    for xp in xml_platform.get_Processor():
        name = xp.get_id()
        type = xp.get_core()
        fd = frequency_domains[xp.get_frequencyDomain()]
        context_load = get_value_in_cycles(xp, 'contextLoad', 0)
        context_store = get_value_in_cycles(xp, 'contextStore', 0)
        p = Processor(name, type, fd, context_load, context_store)
        schedulers_to_processors[xp.get_scheduler()].append(p)
        platform.processors.append(p)
        log.debug('Found processor %s of type %s', name, type)

    # Initialize all Schedulers
    for xs in xml_platform.get_Scheduler():
        name = xs.get_id()
        policies = create_policy_list(xml_platform,
                                      xs.get_schedulingPolicyList())
        s = Scheduler(name, schedulers_to_processors[name], policies)
        log.debug('Found scheduler %s for %s supporting %s',
                  name, schedulers_to_processors[name], policies)

    # Initialize all Memories, Caches, and Fifos as CommunicationResources
    for xm in xml_platform.get_Memory():
        name = xm.get_id()
        read_latency = get_value_in_cycles(xm, 'readLatency', 0)
        write_latency = get_value_in_cycles(xm, 'writeLatency', 0)
        read_throughput = get_value_in_byte_per_cycle(
            xm, 'readThroughput', float('inf'))
        write_throughput = get_value_in_byte_per_cycle(
            xm, 'writeThroughput', float('inf'))
        fd = frequency_domains[xm.get_frequencyDomain()]
        mem = CommunicationResource(name, fd, read_latency, write_latency,
                                    read_throughput, write_throughput)
        platform.communication_resources.append(mem)
        log.debug('Found memory %s', name)

    for xc in xml_platform.get_Cache():
        name = xc.get_id()
        # XXX we assume 100% cache hit rate (This is also what Silexica does)
        read_latency = get_value_in_cycles(xm, 'readHitLatency', 0)
        write_latency = get_value_in_cycles(xm, 'writeHitLatency', 0)
        read_throughput = get_value_in_byte_per_cycle(
            xm, 'readHitThroughput', float('inf'))
        write_throughput = get_value_in_byte_per_cycle(
            xm, 'writeHitThroughput', float('inf'))
        fd = frequency_domains[xc.get_frequencyDomain()]
        cache = CommunicationResource(name, fd, read_latency, write_latency,
                                      read_throughput, write_throughput)
        platform.communication_resources.append(cache)
        log.debug('Found cache %s', name)

    for xf in xml_platform.get_Fifo():
        name = xf.get_id()
        read_latency = get_value_in_cycles(xm, 'readLatency', 0)
        write_latency = get_value_in_cycles(xm, 'writeLatency', 0)
        read_throughput = get_value_in_byte_per_cycle(
            xm, 'readThroughput', float('inf'))
        write_throughput = get_value_in_byte_per_cycle(
            xm, 'writeThroughput', float('inf'))
        fd = frequency_domains[xf.get_frequencyDomain()]
        fifo = CommunicationResource(name, fd, read_latency, write_latency,
                                     read_throughput, write_throughput)
        platform.communication_resources.append(fifo)
        log.debug('Found FIFO %s', name)

    # We also need to collect all the physical links, logical links and dma
    # controllers
    for ll in (xml_platform.get_LogicalLink() +
               xml_platform.get_PhysicalLink() +
               xml_platform.get_DMAController()):
        name = ll.get_id()
        latency = get_value_in_cycles(ll, 'latency', 0)
        throughput = get_value_in_byte_per_cycle(
            ll, 'throughput', float('inf'))
        fd = frequency_domains[ll.get_frequencyDomain()]
        link = CommunicationResource(name, fd, latency, latency, throughput,
                                     throughput)
        platform.communication_resources.append(link)
        log.debug('Found link or DMA %s', name)

    # Initialize all Communication Primitives
    for xcom in xml_platform.get_Communication():
        name = xcom.get_id()
        xbuf = xcom.get_Buffer()

        via_name = None
        xmem = xbuf.get_MemoryRef()
        xfifo = xbuf.get_FifoRef()
        xcache = xbuf.get_CacheRef()

        # TODO we should do more sanity checks here
        if len(xmem) > 0:
            via_name = xmem[0].get_memory()
        elif len(xfifo) > 0:
            via_name = xfifo[0].get_fifo()
        elif len(xcache) > 0:
            via_name = xcache[0].get_cache()
        else:
            raise RuntimeError('No buffer set for primitive %s!', name)

        producers = {}
        consumers = {}

        # Read the Producers
        for xp in xcom.get_Producer():
            pn = xp.get_processor()

            # TODO implement passive producing costs
            if xp.get_Passive() is not None:
                log.warn('Passive producing costs are not supported'
                         ' -> ignore passive phase of primitive %s', name)

            # We create a single phase for each producer
            active = CommunicationPhase(
                'Produce Active',
                resources_from_access(xp.get_Active(), platform),
                'write')
            producers[pn] = [active]

        # Read the Consumers
        for xc in xcom.get_Consumer():
            cn = xc.get_processor()

            # TODO implement passive producing costs
            if xc.get_Passive() is not None:
                log.warn('Passive consuming costs are not supported'
                         ' -> ignore passive phase of primitive %s', name)

            # We create a single phase for each producer
            active = CommunicationPhase(
                'Consume Active',
                resources_from_access(xp.get_Active(), platform),
                'read')
            consumers[cn] = [active]

        # Create a Primitive for each combination of producer and consumer
        for pn in producers:
            for cn in consumers:
                p = Primitive(name,
                              platform.find_processor(pn),
                              platform.find_communication_resource(via_name),
                              platform.find_processor(cn))
                log.debug('Found communication primitive %s: %s -> %s -> %s',
                          name, pn, via_name, cn)
                platform.primitives.append(p)


def find_resource(platform, id):
    '''
    Search for a resource in a platform and raise an error if the resource is
    not found.
    :param platform: The Platform object to search in
    :param id: Name of the resource to search for
    '''
    resource = platform.find_communication_resource(id)
    if resource is None:
        raise RuntimeError('Resource %s is not in the platform' % id)
    return resource


def resources_from_access(access_list, platform):
    """
    Parse a list of accesses and references from the xml and convert it to a
    list of communication resources. This is required for creating
    communication primitives
    """
    resources = []
    for acc in access_list.get_CacheAccess():
        assert('write' == acc.get_access())
        resources.append(find_resource(platform, acc.get_cache()))
    for acc in access_list.get_FifoAccess():
        assert('write' == acc.get_access())
        resources.append(find_resource(platform, acc.get_fifo()))
    for acc in access_list.get_MemoryAccess():
        assert('write' == acc.get_access())
        resources.append(find_resource(platform, acc.get_memory()))
    for ref in access_list.get_DMAControllerRef():
        resources.append(find_resource(platform, ref.get_dmaController()))
    for ref in access_list.get_PhysicalLinkRef():
        resources.append(find_resource(platform, ref.get_physicalLink()))
    for ref in access_list.get_LogicalLinkRef():
        resources.append(find_resource(platform, ref.get_logicalLink()))
    return resources

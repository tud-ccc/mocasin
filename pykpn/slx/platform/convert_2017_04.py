# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
from pint import UnitRegistry

from ...common import CommunicationResource
from ...common import FrequencyDomain
from ...common import Primitive
from ...common import Processor
from ...common import Scheduler


ur = UnitRegistry()
log = logging.getLogger(__name__)


def get_policy_list(xml_platform, ref):
    l = []
    for pl in xml_platform.get_SchedulingPolicyList():
        if pl.get_id() == ref:
            for p in pl.get_SchedulingPolicy():
                l.append(p.get_schedulingAlgorithm())
            return l

    raise RuntimeError('Could not find the SchedulingPolicyList %s', ref)


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

    # TODO implement support for frequency domains
    log.warn('Pykpn does not support frequency domains. We always use the '
             'processor frequency for delay calculation. Use with care!')

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
        p = Processor(name, type, fd, 0, 0)
        # TODO we need to set the switching delays per scheduling policy, not
        #      per processor
        schedulers_to_processors[xp.get_scheduler()].append(p)
        platform.processors.append(p)
        log.debug('Found processor %s of type %s', name, type)

    # Initialize all Schedulers
    for xs in xml_platform.get_Scheduler():
        name = xs.get_id()
        policies = get_policy_list(xml_platform, xs.get_schedulingPolicyList())
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
        platform.storage_devices.append(mem)
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
        platform.storage_devices.append(cache)
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
        platform.storage_devices.append(fifo)
        log.debug('Found FIFO %s', name)

    # We also need to collect all the physical and logical links
    platform_links = []
    for ll in xml_platform.get_LogicalLink() + xml_platform.get_PhysicalLink():
        name = ll.get_id()
        latency = get_value_in_cycles(ll, 'latency', 0)
        throughput = get_value_in_byte_per_cycle(
            ll, 'throughput', float('inf'))
        fd = frequency_domains[ll.get_frequencyDomain()]
        link = CommunicationResource(name, fd, latency, latency, throughput,
                                     throughput)
        platform_links.append(link)
        log.debug('Found link %s', name)

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

            if xp.get_Passive() is not None:
                log.warn('Passive producing costs are not supported'
                         ' -> ignore (%s)', name)

            producers[pn] = get_active_produce_cost_func(xml_platform,
                                                         xp.get_Active())

        # Read the Consumers
        for xc in xcom.get_Consumer():
            cn = xc.get_processor()

            if xc.get_Passive() is not None:
                log.warn('Passive consuming costs are not supported'
                         ' -> ignore (%s)', name)

            consumers[cn] = get_active_consume_cost_func(xml_platform,
                                                         xc.get_Active())

        # Create a Primitive for each combination of producer and consumer
        for pn in producers:
            for cn in consumers:
                p = Primitive(name,
                              platform.findProcessor(pn),
                              platform.findStorageDevice(via_name),
                              platform.findProcessor(cn))
                log.debug('Found communication primitive %s: %s -> %s -> %s'
                          ', produce(x)=%s, consume(x)=%s', name,
                          pn, via_name, cn, producers[pn], consumers[cn])


def get_active_produce_cost_func(xml_platform, active):
    latency = 0
    min_throughput = float('inf')

    for cache_acc in active.get_CacheAccess():
        assert('write' == cache_acc.get_access())
        cache_name = cache_acc.get_cache()
        cache = find_elem(xml_platform, 'Cache', cache_name)
        # XXX We assume a 100% Cache Hit rate, Silexca is doing the same...
        latency += get_value_in_cycles(cache, 'writeHitLatency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            cache, 'writeHitThroughput', float('inf')))

    for fifo_acc in active.get_FifoAccess():
        assert('write' == fifo_acc.get_access())
        fifo_name = fifo_acc.get_fifo()
        fifo = find_elem(xml_platform, 'Fifo', fifo_name)
        latency += get_value_in_cycles(fifo, 'writeLatency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            fifo, 'writeThroughput', float('inf')))

    for memory_acc in active.get_MemoryAccess():
        assert('write' == memory_acc.get_access())
        memory_name = memory_acc.get_memory()
        memory = find_elem(xml_platform, 'Memory', memory_name)
        latency += get_value_in_cycles(memory, 'writeLatency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            memory, 'writeThroughput', float('inf')))

    for dma_ref in active.get_DMAControllerRef():
        dma_name = dma_ref.get_dmaController()
        dma = find_elem(xml_platform, 'DMAController', dma_name)
        latency += get_value_in_cycles(dma, 'latency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            dma, 'throughput', float('inf')))

    for ll_ref in active.get_LogicalLinkRef():
        ll_name = ll_ref.get_logicalLink()
        ll = find_elem(xml_platform, 'LogicalLink', ll_name)
        latency += get_value_in_cycles(ll, 'latency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            ll, 'throughput', float('inf')))

    for pl_ref in active.get_PhysicalLinkRef():
        pl_name = pl_ref.get_physicalLink()
        pl = find_elem(xml_platform, 'PhysicalLink', pl_name)
        latency += get_value_in_cycles(pl, 'latency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            pl, 'throughput', float('inf')))

    return str(latency) + ' + x * ' + str(1/min_throughput)


def get_active_consume_cost_func(xml_platform, active):
    latency = ur('0 cycles')
    min_throughput = float('inf') * ur('byte / cycle')

    # TODO handle frequency domains!

    for cache_acc in active.get_CacheAccess():
        assert('read' == cache_acc.get_access())
        cache_name = cache_acc.get_cache()
        cache = find_elem(xml_platform, 'Cache', cache_name)
        # XXX We assume a 100% Cache Hit rate, Silexca is doing the same...
        latency += get_value_in_cycles(cache, 'readHitLatency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            cache, 'readHitThroughput', float('inf')))

    for fifo_acc in active.get_FifoAccess():
        assert('read' == fifo_acc.get_access())
        fifo_name = fifo_acc.get_fifo()
        fifo = find_elem(xml_platform, 'Fifo', fifo_name)
        latency += get_value_in_cycles(fifo, 'readLatency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            fifo, 'readThroughput', float('inf')))

    for memory_acc in active.get_MemoryAccess():
        assert('read' == memory_acc.get_access())
        memory_name = memory_acc.get_memory()
        memory = find_elem(xml_platform, 'Memory', memory_name)
        latency += get_value_in_cycles(memory, 'readLatency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            memory, 'readThroughput', float('inf')))

    for dma_ref in active.get_DMAControllerRef():
        dma_name = dma_ref.get_dmaController()
        dma = find_elem(xml_platform, 'DMAController', dma_name)
        latency += get_value_in_cycles(dma, 'latency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            dma, 'throughput', float('inf')))

    for ll_ref in active.get_LogicalLinkRef():
        ll_name = ll_ref.get_logicalLink()
        ll = find_elem(xml_platform, 'LogicalLink', ll_name)
        latency += get_value_in_cycles(ll, 'latency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            ll, 'throughput', float('inf')))

    for pl_ref in active.get_PhysicalLinkRef():
        pl_name = pl_ref.get_physicalLink()
        pl = find_elem(xml_platform, 'PhysicalLink', pl_name)
        latency += get_value_in_cycles(pl, 'latency', 0)
        min_throughput = min(min_throughput, get_value_in_byte_per_cycle(
            pl, 'throughput', float('inf')))

    return str(latency) + ' + x * ' + str(1/min_throughput)

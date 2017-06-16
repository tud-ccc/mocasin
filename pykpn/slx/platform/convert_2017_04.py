# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
from pint import UnitRegistry

from ...common import Primitive
from ...common import Processor
from ...common import Scheduler


ur = UnitRegistry()
log = logging.getLogger(__name__)


def get_frequency(xml_platform, domain):
    '''
    Search for a given frequency domain and return the first frequency.
    '''
    for fd in xml_platform.get_FrequencyDomain():
        if fd.get_id() == domain:
            frequencies = fd.get_Frequency()
            if (len(frequencies) > 1):
                log.warn('FrequencyDomain %s has multiple frequencies set. '
                         'Frequency switching is not yet supported'
                         ' -> use first frequency' % domain)
            f = frequencies[0]
            return ur(f.get_value() + f.get_unit()).to(ur.Hz).magnitude

    raise RuntimeError('Could not find the FrequencyDomain %s', domain)


def get_policy_list(xml_platform, ref):
    l = []
    for pl in xml_platform.get_SchedulingPolicyList():
        if pl.get_id() == ref:
            for p in pl.get_SchedulingPolicy():
                l.append(p.get_schedulingAlgorithm())
            return l

    raise RuntimeError('Could not find the SchedulingPolicyList %s', ref)


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

    # Initialize all Processors
    for xp in xml_platform.get_Processor():
        name = xp.get_id()
        type = xp.get_core()
        f = int(get_frequency(xml_platform, xp.get_frequencyDomain()))
        p = Processor(name, type, f, 0, 0)
        # TODO we need to set the switching delays per scheduling policy, not
        #      per processor
        schedulers_to_processors[xp.get_scheduler()].append(p)
        platform.processors.append(p)
        log.debug('Found processor %s of type %s running at %d Hz',
                  name, type, f)

    # Initialize all Schedulers
    for xs in xml_platform.get_Scheduler():
        name = xs.get_id()
        policies = get_policy_list(xml_platform, xs.get_schedulingPolicyList())
        s = Scheduler(name, schedulers_to_processors[name], policies)
        log.debug('Found scheduler %s for %s supporting %s',
                  name, schedulers_to_processors[name], policies)

    # Initialize all Memories, Caches, and Fifos as Memories
    # TODO implement real support for HW Fifos and Caches
    for xm in xml_platform.get_Memory():
        name = xm.get_id()
        size = ur(xm.get_sizeValue() + xm.get_sizeUnit()).to(ur.byte).magnitude
        m = Memory(name, size)
        platform.memories.append(m)
        log.debug('Found memory %s that is %d bytes large', name, size)

    for xc in xml_platform.get_Cache():
        name = xc.get_id()
        size = ur(xc.get_sizeValue() + xc.get_sizeUnit()).to(ur.byte).magnitude
        m = Memory(name, size)
        platform.memories.append(m)
        log.debug('Found cache %s that is %d bytes large', name, size)
        log.warn('Caches are not supported! -> Treat %s as a memory', name)

    for xf in xml_platform.get_Fifo():
        name = xf.get_id()
        m = Memory(name, 0)
        platform.memories.append(m)
        log.debug('Found Fifo %s', name)
        log.warn('Hardware Fifos are not supported! -> Treat %s as a memory',
                 name)

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
                              platform.findMemory(via_name),
                              platform.findProcessor(cn))
                log.debug('Found communication primitive %s: %s -> %s -> %s'
                          ', produce(x)=%s, consume(x)=%s', name,
                          pn, via_name, cn, producers[pn], consumers[cn])


def find_cache(xml_platform, name):
    for c in xml_platform.get_Cache():
        if c.get_id() == name:
            return c
    raise RuntimeError('Cache %s was not defined', name)


def find_fifo(xml_platform, name):
    for c in xml_platform.get_Fifo():
        if c.get_id() == name:
            return c
    raise RuntimeError('FIFO %s was not defined', name)


def find_memory(xml_platform, name):
    for c in xml_platform.get_Memory():
        if c.get_id() == name:
            return c
    raise RuntimeError('Memory %s was not defined', name)


def find_dma(xml_platform, name):
    for c in xml_platform.get_DMAController():
        if c.get_id() == name:
            return c
    raise RuntimeError('DMAController %s was not defined', name)


def find_logical_link(xml_platform, name):
    for c in xml_platform.get_LogicalLink():
        if c.get_id() == name:
            return c
    raise RuntimeError('LogicalLink %s was not defined', name)


def find_physical_link(xml_platform, name):
    for c in xml_platform.get_PhysicalLink():
        if c.get_id() == name:
            return c
    raise RuntimeError('PhysicalLink %s was not defined', name)


def get_active_produce_cost_func(xml_platform, active):
    latency = ur('0 cycles')
    min_throughput = float('inf') * ur('byte / cycle')

    for cache_acc in active.get_CacheAccess():
        assert('write' == cache_acc.get_access())
        cache_name = cache_acc.get_cache()
        cache = find_cache(xml_platform, cache_name)

        # XXX We assume a 100% Cache Hit rate, Silexca is doing the same...
        lv = cache.get_writeHitLatencyValue()
        lu = cache.get_writeHitLatencyUnit()
        latency += ur(lv + lu)

        tv = cache.get_writeHitThroughputValue()
        tu = cache.get_writeHitThroughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for fifo_acc in active.get_FifoAccess():
        assert('write' == fifo_acc.get_access())
        fifo_name = fifo_acc.get_fifo()
        fifo = find_fifo(xml_platform, fifo_name)

        lv = fifo.get_writeLatencyValue()
        lu = fifo.get_writeLatencyUnit()
        latency += ur(lv + lu)

        tv = fifo.get_writeThroughputValue()
        tu = fifo.get_writeThroughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for memory_acc in active.get_MemoryAccess():
        assert('write' == memory_acc.get_access())
        memory_name = memory_acc.get_memory()
        memory = find_memory(xml_platform, memory_name)

        lv = memory.get_writeLatencyValue()
        lu = memory.get_writeLatencyUnit()
        latency += ur(lv + lu)

        tv = memory.get_writeThroughputValue()
        tu = memory.get_writeThroughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for dma_ref in active.get_DMAControllerRef():
        dma_name = dma_ref.get_dmaController()
        dma = find_dma(xml_platform, dma_name)

        lv = dma.get_latencyValue()
        lu = dma.get_latencyUnit()
        latency += ur(lv + lu)

        tv = dma.get_throughputValue()
        tu = dma.get_throughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for ll_ref in active.get_LogicalLinkRef():
        ll_name = ll_ref.get_logicalLink()
        ll = find_logical_link(xml_platform, ll_name)

        lv = ll.get_latencyValue()
        lu = ll.get_latencyUnit()
        latency += ur(lv + lu)

        tv = ll.get_throughputValue()
        tu = ll.get_throughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for pl_ref in active.get_PhysicalLinkRef():
        pl_name = pl_ref.get_physicalLink()
        pl = find_physical_link(xml_platform, pl_name)

        lv = pl.get_latencyValue()
        lu = pl.get_latencyUnit()
        latency += ur(lv + lu)

        tv = pl.get_throughputValue()
        tu = pl.get_throughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    return str(latency.to('cycle').magnitude) + ' + x * ' + \
        str((1/min_throughput).to('cycle/byte').magnitude)


def get_active_consume_cost_func(xml_platform, active):
    latency = ur('0 cycles')
    min_throughput = float('inf') * ur('byte / cycle')

    # TODO handle frequency domains!

    for cache_acc in active.get_CacheAccess():
        assert('read' == cache_acc.get_access())
        cache_name = cache_acc.get_cache()
        cache = find_cache(xml_platform, cache_name)

        # XXX We assume a 100% Cache Hit rate, Silexca is doing the same...
        lv = cache.get_readHitLatencyValue()
        lu = cache.get_readHitLatencyUnit()
        latency += ur(lv + lu)

        tv = cache.get_readHitThroughputValue()
        tu = cache.get_readHitThroughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for fifo_acc in active.get_FifoAccess():
        assert('read' == fifo_acc.get_access())
        fifo_name = fifo_acc.get_fifo()
        fifo = find_fifo(xml_platform, fifo_name)

        lv = fifo.get_readLatencyValue()
        lu = fifo.get_readLatencyUnit()
        latency += ur(lv + lu)

        tv = fifo.get_readThroughputValue()
        tu = fifo.get_readThroughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for memory_acc in active.get_MemoryAccess():
        assert('read' == memory_acc.get_access())
        memory_name = memory_acc.get_memory()
        memory = find_memory(xml_platform, memory_name)

        lv = memory.get_readLatencyValue()
        lu = memory.get_readLatencyUnit()
        latency += ur(lv + lu)

        tv = memory.get_readThroughputValue()
        tu = memory.get_readThroughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for dma_ref in active.get_DMAControllerRef():
        dma_name = dma_ref.get_dmaController()
        dma = find_dma(xml_platform, dma_name)

        lv = dma.get_latencyValue()
        lu = dma.get_latencyUnit()
        latency += ur(lv + lu)

        tv = dma.get_throughputValue()
        tu = dma.get_throughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for ll_ref in active.get_LogicalLinkRef():
        ll_name = ll_ref.get_logicalLink()
        ll = find_logical_link(xml_platform, ll_name)

        lv = ll.get_latencyValue()
        lu = ll.get_latencyUnit()
        latency += ur(lv + lu)

        tv = ll.get_throughputValue()
        tu = ll.get_throughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    for pl_ref in active.get_PhysicalLinkRef():
        pl_name = pl_ref.get_physicalLink()
        pl = find_physical_link(xml_platform, pl_name)

        lv = pl.get_latencyValue()
        lu = pl.get_latencyUnit()
        latency += ur(lv + lu)

        tv = pl.get_throughputValue()
        tu = pl.get_throughputUnit()
        if tv is not None:
            min_throughput = min(min_throughput, ur(tv + tu))

    return str(latency.to('cycle').magnitude) + ' + x * ' + \
        str((1/min_throughput).to('cycle/byte').magnitude)

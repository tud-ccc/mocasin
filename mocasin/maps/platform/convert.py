# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


import logging

from pint import UnitRegistry

from mocasin.common.platform import (
    CommunicationPhase,
    CommunicationResource,
    CommunicationResourceType,
    FrequencyDomain,
    Primitive,
    Processor,
    ProcessorPowerModel,
    Scheduler,
    SchedulingPolicy,
    Storage,
)


ur = UnitRegistry()
log = logging.getLogger(__name__)


def create_policy(xml_platform, list_ref, scheduler_cycles):
    if scheduler_cycles is None:
        log.warning(
            "MAPS platforms do not define scheduling delays. "
            "-> default to 0. You can override this defult by setting "
            "'platform.scheduler_cycles'"
        )
        scheduler_cycles = 0
    policies = []
    for pl in xml_platform.get_SchedulingPolicyList():
        if pl.get_id() == list_ref:
            for p in pl.get_SchedulingPolicy():
                name = p.get_schedulingAlgorithm()
                # there is no scheduling delay in maps
                time_slice = get_value_in_unit(p, "timeSlice", "ps", None)
                policies.append(
                    SchedulingPolicy(
                        name, scheduler_cycles, time_slice=time_slice
                    )
                )
            if len(policies) == 0:
                raise RuntimeError(
                    f"The SchedulingPolicyList {list_ref} does "
                    "not define any policies!"
                )
            elif len(policies) > 1:
                raise RuntimeError(
                    f"The SchedulingPolicyList {list_ref} "
                    "defines multiple policies!"
                )
            return policies[0]
    raise RuntimeError("Could not find the SchedulingPolicyList %s", list_ref)


# TODO this should be placed somewhere more central
def get_value_in_unit(obj, value_name, unit, default=None):
    """
    Read an objects value converted to a unit from the parsed xml.
    :param obj: the object who's value should be read
    :param value_name: name of the value to be read
    :param unit: the unit to  convert to
    :param default: value returned if the value is not defined in the xml
    """

    get_value = getattr(obj, "get_%sValue" % value_name)
    get_unit = getattr(obj, "get_%sUnit" % value_name)
    if get_value() is not None:
        return ur(get_value() + get_unit()).to(unit).magnitude
    return default


def get_value_in_cycles(obj, value_name, default=None):
    return get_value_in_unit(obj, value_name, "cycle", default)


def get_value_in_byte_per_cycle(obj, value_name, default=None):
    return get_value_in_unit(obj, value_name, "byte / cycle", default)


def find_elem(xml_platform, type_name, elem_name):
    """
    Find an element of a certain type in the platform.
    :param xml_platform: platform to search in
    :param type_name:    type of the element to be found
    :param elem_name:    name of the element to be found
    """
    get_type_elems = getattr(xml_platform, "get_" + type_name)
    for elem in get_type_elems():
        if elem.get_id() == elem_name:
            return elem
    raise RuntimeError("%s %s was not defined", type_name, elem_name)


def convert(platform, xml_platform, scheduler_cycles=None, fd_frequencies=None):
    # keep a map of scheduler names to processors, this helps when creating
    # scheduler objects
    schedulers_to_processors = {}
    for s in xml_platform.get_Scheduler():
        schedulers_to_processors[s.get_id()] = []

    # Check the fd_frequencies defined the frequencies of only known domains
    if fd_frequencies is not None:
        for fd in fd_frequencies:
            fd_names = map(
                lambda x: x.get_id(), xml_platform.get_FrequencyDomain()
            )
            if fd not in fd_names:
                log.warning(
                    f"The fd_frequencies defines the frequency of "
                    f"an unknown domain {fd}"
                )

    # Collect all frequency and voltage domains
    frequency_domains = {}
    # We do not save voltage domains by their names defined in MAPS XML files,
    # instead we save under the same names as frequency domains
    fd_voltage = {}
    for fd in xml_platform.get_FrequencyDomain():
        name = fd.get_id()
        max_frequency = 0
        supported_frequency_voltage_pairs = []
        for f in fd.get_Frequency():
            voltage_domain_conds = f.get_VoltageDomainCondition()
            if len(voltage_domain_conds) > 1:
                raise RuntimeError(
                    f"The xml defines multiple voltages for the frequency domain "
                    f"{name} at {f.get_value()}{f.get_unit()}."
                )
            for v in voltage_domain_conds:
                voltage = ur(v.get_value() + v.get_unit()).to("V").magnitude
            frequency = ur(f.get_value() + f.get_unit()).to("Hz").magnitude
            supported_frequency_voltage_pairs.append(
                tuple((frequency, voltage))
            )
        if fd_frequencies is not None and name in fd_frequencies:
            frequency = fd_frequencies[name]
            voltage = 0
            found = False
            for f, v in supported_frequency_voltage_pairs:
                if frequency != f:
                    continue
                voltage = v
                found = True
            if not found:
                log.warning(
                    f"The fd_frequencies sets the frequency of the domain {name} "
                    f"to {frequency} Hz, which is not defined in the xml. "
                    f"Setting power to 0 V."
                )
        else:
            frequency, voltage = max(supported_frequency_voltage_pairs)
            if len(fd.get_Frequency()) > 1:
                log.warning(
                    "The xml defines multiple frequencies for the domain "
                    "%s. -> Select Maximum",
                    name,
                )
        frequency_domains[name] = FrequencyDomain(name, frequency)
        fd_voltage[name] = voltage
        log.debug(
            "Found frequency domain %s (%d Hz), voltage %f V.",
            name,
            frequency,
            voltage,
        )

    # Collect processor power model parameters
    processor_power_params = {}

    for ppm in xml_platform.get_ProcessorPowerModel():
        name = ppm.get_id()
        leakage_current = (
            ur(ppm.get_leakageCurrentValue() + ppm.get_leakageCurrentUnit())
            .to("A")
            .magnitude
        )
        switched_capacitance = (
            ur(
                ppm.get_switchedCapacitanceValue()
                + ppm.get_switchedCapacitanceUnit()
            )
            .to("F")
            .magnitude
        )
        processor_power_params[name] = {
            "leakage_current": leakage_current,
            "switched_capacitance": switched_capacitance,
        }

    processor_power_models = {}

    # Initialize all Processors
    for xp in xml_platform.get_Processor():
        name = xp.get_id()
        type = xp.get_core()
        fd_name = xp.get_frequencyDomain()
        fd = frequency_domains[fd_name]

        # Initialize a processor power model
        ppm_name = xp.get_processorPowerModel()
        if ppm_name not in processor_power_models:
            voltage = fd_voltage[fd_name]
            power_idle = (
                processor_power_params[ppm_name]["leakage_current"] * voltage
            )
            power_active = (
                power_idle
                + processor_power_params[ppm_name]["switched_capacitance"]
                * voltage
                * voltage
                * fd.frequency
            )
            ppm = ProcessorPowerModel(ppm_name, power_active, power_idle)
            processor_power_models[ppm_name] = ppm
        ppm = processor_power_models[ppm_name]

        context_load = get_value_in_cycles(xp, "contextLoad", 0)
        context_store = get_value_in_cycles(xp, "contextStore", 0)
        p = Processor(name, type, fd, ppm, context_load, context_store)
        schedulers_to_processors[xp.get_scheduler()].append(p)
        platform.add_processor(p)
        log.debug("Found processor %s of type %s", name, type)

    # Initialize all Schedulers
    for xs in xml_platform.get_Scheduler():
        name = xs.get_id()
        policy = create_policy(
            xml_platform, xs.get_schedulingPolicyList(), scheduler_cycles
        )
        s = Scheduler(name, schedulers_to_processors[name], policy)
        log.debug(
            "Found scheduler %s for %s supporting %s",
            name,
            schedulers_to_processors[name],
            policy.name,
        )
        platform.add_scheduler(s)

    # Initialize all Memories, Caches, and Fifos as CommunicationResources
    for xm in xml_platform.get_Memory():
        name = xm.get_id()
        read_latency = get_value_in_cycles(xm, "readLatency", 0)
        write_latency = get_value_in_cycles(xm, "writeLatency", 0)
        read_throughput = get_value_in_byte_per_cycle(
            xm, "readThroughput", float("inf")
        )
        write_throughput = get_value_in_byte_per_cycle(
            xm, "writeThroughput", float("inf")
        )
        fd = frequency_domains[xm.get_frequencyDomain()]
        mem = Storage(
            name,
            fd,
            read_latency,
            write_latency,
            read_throughput,
            write_throughput,
        )
        platform.add_communication_resource(mem)
        log.debug("Found memory %s", name)

    for xc in xml_platform.get_Cache():
        name = xc.get_id()
        # XXX we assume 100% cache hit rate
        read_latency = get_value_in_cycles(xc, "readHitLatency", 0)
        write_latency = get_value_in_cycles(xc, "writeHitLatency", 0)
        read_throughput = get_value_in_byte_per_cycle(
            xc, "readHitThroughput", float("inf")
        )
        write_throughput = get_value_in_byte_per_cycle(
            xc, "writeHitThroughput", float("inf")
        )
        fd = frequency_domains[xc.get_frequencyDomain()]
        cache = Storage(
            name,
            fd,
            read_latency,
            write_latency,
            read_throughput,
            write_throughput,
        )
        platform.add_communication_resource(cache)
        log.debug("Found cache %s", name)

    for xf in xml_platform.get_Fifo():
        name = xf.get_id()
        read_latency = get_value_in_cycles(xf, "readLatency", 0)
        write_latency = get_value_in_cycles(xf, "writeLatency", 0)
        read_throughput = get_value_in_byte_per_cycle(
            xf, "readThroughput", float("inf")
        )
        write_throughput = get_value_in_byte_per_cycle(
            xf, "writeThroughput", float("inf")
        )
        fd = frequency_domains[xf.get_frequencyDomain()]
        fifo = Storage(
            name,
            fd,
            read_latency,
            write_latency,
            read_throughput,
            write_throughput,
        )
        platform.add_communication_resource(fifo)
        log.debug("Found FIFO %s", name)

    # We also need to collect all the physical links, logical links and dma
    # controllers

    # modified by Felix Teweleit 10.08.2018

    for ll in xml_platform.get_PhysicalLink():
        name = ll.get_id()
        latency = get_value_in_cycles(ll, "latency", 0)
        throughput = get_value_in_byte_per_cycle(ll, "throughput", float("inf"))
        fd = frequency_domains[ll.get_frequencyDomain()]
        link = CommunicationResource(
            name,
            fd,
            CommunicationResourceType.PhysicalLink,
            latency,
            latency,
            throughput,
            throughput,
        )
        platform.add_communication_resource(link)
        log.debug("Found link or DMA %s", name)

    for ll in xml_platform.get_LogicalLink():
        name = ll.get_id()
        latency = get_value_in_cycles(ll, "latency", 0)
        throughput = get_value_in_byte_per_cycle(ll, "throughput", float("inf"))
        fd = frequency_domains[ll.get_frequencyDomain()]
        link = CommunicationResource(
            name,
            fd,
            CommunicationResourceType.LogicalLink,
            latency,
            latency,
            throughput,
            throughput,
        )
        platform.add_communication_resource(link)
        log.debug("Found link or DMA %s", name)

    for ll in xml_platform.get_DMAController():
        name = ll.get_id()
        latency = get_value_in_cycles(ll, "latency", 0)
        throughput = get_value_in_byte_per_cycle(ll, "throughput", float("inf"))
        fd = frequency_domains[ll.get_frequencyDomain()]
        link = CommunicationResource(
            name,
            fd,
            CommunicationResourceType.DMAController,
            latency,
            latency,
            throughput,
            throughput,
        )
        platform.add_communication_resource(link)
        log.debug("Found link or DMA %s", name)

    # end of modified code

    # Initialize all Communication Primitives
    for xcom in xml_platform.get_Communication():
        name = xcom.get_id()

        producers = {}
        consumers = {}

        # Read the Producers
        for xp in xcom.get_Producer():
            pn = xp.get_processor()

            # TODO implement passive producing costs
            if xp.get_Passive() is not None:
                log.warning(
                    "Passive producing costs are not supported"
                    " -> ignore passive phase of primitive %s",
                    name,
                )

            # We create a single phase for each producer
            active = CommunicationPhase(
                "Produce Active",
                resources_from_access(xp.get_Active(), platform),
                "write",
            )
            producers[pn] = [active]

        # Read the Consumers
        for xc in xcom.get_Consumer():
            cn = xc.get_processor()

            # TODO implement passive producing costs
            if xc.get_Passive() is not None:
                log.warning(
                    "Passive consuming costs are not supported"
                    " -> ignore passive phase of primitive %s",
                    name,
                )

            # We create a single phase for each producer
            active = CommunicationPhase(
                "Consume Active",
                resources_from_access(xc.get_Active(), platform),
                "read",
            )
            consumers[cn] = [active]

        # Create a Primitive for each combination of producer and consumer
        primitive = Primitive(name)

        for pn in producers:
            primitive.add_producer(platform.find_processor(pn), producers[pn])
        for cn in consumers:
            primitive.add_consumer(platform.find_processor(cn), consumers[cn])

        log.debug(
            "Found the communication primitive %s: %s -> %s"
            % (name, str(producers.keys()), str(consumers.keys()))
        )

        platform.add_primitive(primitive)


def find_resource(platform, id):
    """
    Search for a resource in a platform and raise an error if the resource is
    not found.
    :param platform: The Platform object to search in
    :param id: Name of the resource to search for
    """
    resource = platform.find_communication_resource(id)
    if resource is None:
        raise RuntimeError("Resource %s is not in the platform" % id)
    return resource


def resources_from_access(access_list, platform):
    """
    Parse a list of accesses and references from the xml and convert it to a
    list of communication resources. This is required for creating
    communication primitives
    """
    resources = []
    for acc in access_list.get_CacheAccess():
        resources.append(find_resource(platform, acc.get_cache()))
    for acc in access_list.get_FifoAccess():
        resources.append(find_resource(platform, acc.get_fifo()))
    for acc in access_list.get_MemoryAccess():
        resources.append(find_resource(platform, acc.get_memory()))
    for ref in access_list.get_DMAControllerRef():
        resources.append(find_resource(platform, ref.get_dmaController()))
    for ref in access_list.get_PhysicalLinkRef():
        resources.append(find_resource(platform, ref.get_physicalLink()))
    for ref in access_list.get_LogicalLinkRef():
        resources.append(find_resource(platform, ref.get_logicalLink()))
    return resources

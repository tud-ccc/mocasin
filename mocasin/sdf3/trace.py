# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import logging
import numpy as np
import pint

from dataclasses import dataclass, field
from fractions import Fraction as frac
from hydra.utils import to_absolute_path

from mocasin.sdf3 import _sdf_parser
from mocasin.common.trace import (
    DataflowTrace,
    ComputeSegment,
    ReadTokenSegment,
    WriteTokenSegment,
)

log = logging.getLogger(__name__)
ureg = pint.UnitRegistry()


@dataclass
class _SdfFiringRule:
    """Helper class defining the firing rules of an SDF actor"""

    reads: dict = field(default_factory=dict)
    writes: dict = field(default_factory=dict)
    initial_writes: dict = field(default_factory=dict)


class _ProcessorType:
    """Helper class for managing processor types.

    This class is used to convert the execution times defined for each
    SDF3 processor type to cycle counts for processor types.
    """

    def __init__(self, sdf3_type, frequency, scale):
        self.sdf3_type = sdf3_type
        self.frequency = ureg(frequency)
        self.scale = ureg(scale)
        if not isinstance(self.frequency, pint.Quantity):
            raise ValueError("Provided frequency without a unit.")
        if not self.frequency.check("[frequency]"):
            raise ValueError(
                "Provided frequency with wrong dimension (expected frequency)"
            )
        if not isinstance(self.scale, pint.Quantity):
            raise ValueError("Provided scale without a unit.")
        if not self.scale.check("[time]"):
            raise ValueError(
                "Provided scale with wrong dimension (expected time)"
            )


class Sdf3Trace(DataflowTrace):
    """Represents the  behavior of an SDF3 application

    See `~DataflowTrace`.

    Args:
        xml_file (str): a SDF3 file to read from
        procesor_types (dict(str, dict(str, str))): a dictionary defining a
            mapping from mocasin processor types to SDF3 processor types
        repetitions (int): a number indicating how many times the execution of
            the entire SDF graph should repeat
    """

    def __init__(self, xml_file, processor_types, repetitions=1):
        self._firing_rules = {}
        self._repetition_vector = {}
        self._trace_segments = {}
        self._trace_iterators = {}
        self._actor_processor_cylces = {}
        self._repetitions = repetitions

        log.info("Start parsing the SDF3 trace")
        # load the xml
        with open(to_absolute_path(xml_file)) as f:
            sdf3 = _sdf_parser.CreateFromDocument(f.read())
            if sdf3.type != "sdf":
                raise RuntimeError(
                    f"Cannot parse {sdf3.type} graphs. "
                    "Only SDF graphs are supported."
                )
            graph = sdf3.applicationGraph

        self.__init_firing_rules(graph)
        self.__init_repetition_vector(graph)
        self.__init_trace_segments(graph, repetitions)
        self.__init_cycle_counts(graph, processor_types)

        self.reset()
        log.info("Done parsing the SDF3 trace")

    def __init_firing_rules(self, graph):
        """Collect all firing rules from the graph.

        Initializes the attribute _firing_rules to store firing rules for all
        actors in the graph. This is just for convenience so that the graph
        does not need to be traversed every time we need the firing rates of an
        actor.
        """
        # collect firing rules
        for actor in graph.sdf.actor:
            rule = _SdfFiringRule()
            for port in actor.port:
                if port.type == "out":
                    channel = None
                    for c in graph.sdf.channel:
                        if c.srcActor == actor.name and c.srcPort == port.name:
                            channel = c
                            break
                    if channel is None:
                        raise RuntimeError(
                            "Did not find a channel that is connected to "
                            f"output port {port.name} of actor {actor.name}"
                        )
                    rule.writes[channel.name] = int(port.rate)
                    log.debug(
                        f"{actor.name} writes {port.rate} tokens to channel "
                        f"{channel.name}"
                    )
                    if channel.initialTokens is not None:
                        log.debug(
                            f"{actor.name} writes {channel.initialTokens} "
                            f"initial tokens to channel {channel.name}"
                        )
                        rule.initial_writes[channel.name] = int(
                            channel.initialTokens
                        )
                else:
                    channel = None
                    for c in graph.sdf.channel:
                        if c.dstActor == actor.name and c.dstPort == port.name:
                            channel = c
                            break
                    if channel is None:
                        raise RuntimeError(
                            "Did not find a channel that is connected to "
                            f"input port {port.name} of actor {actor.name}"
                        )
                    rule.reads[channel.name] = int(port.rate)
                    log.debug(
                        f"{actor.name} reads {port.rate} tokens from channel "
                        f"{channel.name}"
                    )
            self._firing_rules[actor.name] = rule

    def __init_repetition_vector(self, graph):
        """Calculate the repetition vector

        Calculates the repetition vector of the graph and stores it in the
        attribute _repetition_vector. The repetition vector is needed in order
        to determine how many repetitions of the actor kernel the generated
        trace needs to contain.
        """
        # initialize repetition vector with None
        for actor in graph.sdf.actor:
            self._repetition_vector[actor.name] = None

        # keep a cache of all ports and rates
        rates = {}
        for actor in graph.sdf.actor:
            actor_rates = {}
            for port in actor.port:
                actor_rates[port.name] = int(port.rate)
            rates[actor.name] = actor_rates

        # a recursive method for traversing the graph
        def visit_node(node):
            assert self._repetition_vector[node] is not None

            # look at all edges
            for channel in graph.sdf.channel:
                if channel.srcActor == node:  # outgoing connections
                    production_rate = rates[channel.srcActor][channel.srcPort]
                    consumption_rate = rates[channel.dstActor][channel.dstPort]
                    factor = frac(production_rate, consumption_rate)
                    src_rate = self._repetition_vector[channel.srcActor]
                    dst_rate = src_rate * factor
                    if self._repetition_vector[channel.dstActor] is None:
                        self._repetition_vector[channel.dstActor] = dst_rate
                        # recursive traversal
                        visit_node(channel.dstActor)
                    elif self._repetition_vector[channel.dstActor] != dst_rate:
                        raise RuntimeError("SDF graph is not consistent!")
                elif channel.dstActor == node:  # incoming connections
                    production_rate = rates[channel.srcActor][channel.srcPort]
                    consumption_rate = rates[channel.dstActor][channel.dstPort]
                    factor = frac(production_rate, consumption_rate)
                    dst_rate = self._repetition_vector[channel.dstActor]
                    src_rate = dst_rate / factor
                    if self._repetition_vector[channel.srcActor] is None:
                        self._repetition_vector[channel.srcActor] = src_rate
                        # recursive traversal
                        visit_node(channel.srcActor)
                    elif self._repetition_vector[channel.srcActor] != src_rate:
                        raise RuntimeError("SDF graph is not consistent!")

        # start traversing the graph at a random node (first node in the dict)
        start_node = next(iter(self._repetition_vector.keys()))
        self._repetition_vector[start_node] = frac(1, 1)
        visit_node(start_node)

        # check that all nodes where visited
        for rate in self._repetition_vector.values():
            if rate is None:
                raise RuntimeError(
                    "SDF graph contains nodes that are not reachable!"
                )

        # find the least common denominator
        lcm = np.lcm.reduce(
            [x.denominator for x in self._repetition_vector.values()]
        )

        # normalize the vector
        for node, rate in self._repetition_vector.items():
            self._repetition_vector[node] = int(rate * lcm)

        log.debug(
            f"The repetition vector for SDF graph {graph.sdf.name} is "
            f"{self._repetition_vector}"
        )

    def __init_cycle_counts(self, graph, processor_types):
        """Collects cycle counts for all actors and defined processor types.

        Converts the time values, given in the actor properties for each SDF3
        processor type, to a cycle count for mocasin's processor types.
        The resulting values are stored in :obj:`~_actor_processor_cycles`
        """
        # initialize processor_types using the _ProcessorType class
        processor_types = {
            k: _ProcessorType(**v) for k, v in processor_types.items()
        }

        for actor in graph.sdf.actor:
            # find actor properties
            a_props = None
            for props in graph.sdfProperties.actorProperties:
                if props.actor == actor.name:
                    a_props = props
            if a_props is None:
                raise RuntimeError(
                    f"Did not find actor properties for {actor.name}"
                )

            # read execution times from the actor properties
            exec_times = {}
            for proc in a_props.processor:
                exec_times[proc.type] = int(proc.executionTime.time)
            assert (
                len(exec_times) > 0
            ), f"Did not find any execution times for actor {actor.name}"

            proc_cycles = {}
            for proc_name, proc_type in processor_types.items():
                try:
                    cycles = (
                        proc_type.scale
                        * proc_type.frequency
                        * exec_times[proc_type.sdf3_type]
                    ).to_reduced_units()
                except KeyError:
                    raise RuntimeError(
                        f"Execution time for actor {actor.name} is not defined"
                        f" for processor type {proc_type.sdf3_type}"
                    )
                assert cycles.check("[]")
                proc_cycles[proc_name] = cycles.magnitude
            self._actor_processor_cylces[actor.name] = proc_cycles

    def get_trace(self, process):
        """Get the trace for a specific actor in the SDF3 application

        Args:
            process (str): Name of the actor to get a trace for

        Yields:
            ComputeSegment, ReadTokenSegment, or WriteTokenSegment: The next
                segement in the process trace
        """
        firings = self._firing_rules[process]

        # place all initial tokens (also called delays)
        for channel, count in firings.initial_writes.items():
            yield WriteTokenSegment(channel=channel, num_tokens=count)

        total_reps = self._repetition_vector[process] * self._repetitions
        for _ in range(0, total_reps):
            # read tokens
            for channel, count in firings.reads.items():
                yield ReadTokenSegment(channel=channel, num_tokens=count)

            # compute
            yield ComputeSegment(
                processor_cycles=self._actor_processor_cycles[process]
            )

            # write tokens
            for channel, count in firings.writes.items():
                yield WriteTokenSegment(channel=channel, num_tokens=count)

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging
import numpy as np

from dataclasses import dataclass, field
from fractions import Fraction as frac

from pykpn.sdf3 import _sdf_parser
from pykpn.common.trace import TraceGenerator, TraceSegment

log = logging.getLogger(__name__)


@dataclass
class _SdfFiringRule:
    reads: dict = field(default_factory=dict)
    writes: dict = field(default_factory=dict)
    initial_writes: dict = field(default_factory=dict)


class Sdf3TraceGenerator(TraceGenerator):
    _firing_rules = {}
    _repetition_vector = {}
    _trace_segments = {}

    _trace_iterators = {}

    def __init__(self, xml_file, repetitions=1):
        log.info("Start parsing the SDF3 trace")
        # load the xml
        with open(xml_file) as f:
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

    def __init_trace_segments(self, graph, repetitions):
        """Generate and store the actual trace segments

        Generates trace segments for all nodes in the graph and stores them in
        the attribute _trace_segments
        """
        for actor in graph.sdf.actor:
            segments = []
            firings = self._firing_rules[actor.name]

            # place all initial tokens (also called delays)
            for channel, count in firings.initial_writes.items():
                s = TraceSegment(write_to_channel=channel, n_tokens=count)
                segments.append(s)

            total_reps = self._repetition_vector[actor.name] * repetitions
            for _ in range(0, total_reps):
                # read tokens
                for channel, count in firings.reads.items():
                    s = TraceSegment(read_from_channel=channel, n_tokens=count)
                    segments.append(s)

                # process
                segments.append(TraceSegment(process_cycles=1000))

                # write tokens
                for channel, count in firings.writes.items():
                    s = TraceSegment(write_to_channel=channel, n_tokens=count)
                    segments.append(s)

            # terminate
            segments.append(TraceSegment(terminate=True))

            # store the trace
            self._trace_segments[actor.name] = segments

    def reset(self):
        """Resets the generator.

        See :meth:`~TraceGenerator.reset`.
        """
        for name, segments in self._trace_segments.items():
            self._trace_iterators[name] = iter(segments)

    def next_segment(self, process_name, processor_type):
        """Return the next trace segment.

        See :meth:`~TraceGenerator.next_segment`.
        """
        return next(self._trace_iterators[process_name])

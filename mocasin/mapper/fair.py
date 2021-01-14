# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import random
import numpy as np
from sortedcontainers import SortedList
import hydra

from mocasin.common.mapping import Mapping, ProcessMappingInfo
from mocasin.util import logging
from mocasin.mapper.random import RandomPartialMapper
from mocasin.mapper.partial import ComPartialMapper
from mocasin.mapper.utils import Statistics


log = logging.getLogger(__name__)


def gen_trace_summary(kpn, platform, trace):
    summary = {}
    p_types = set()
    for p in platform.processors():
        p_types = p_types.union(set([p.type]))
    for p_type in p_types:
        trace.reset()
        for proc in kpn.processes():
            tot = 0
            seg = trace.next_segment(proc.name, p_type)
            while not seg.terminate:
                if seg.processing_cycles is not None:
                    tot += seg.processing_cycles
                seg = trace.next_segment(proc.name, p_type)
            summary[(proc, p_type)] = tot
    return summary


class StaticCFS(object):
    """Base class for mapping using a static method similar to the Linux CFS scheduler.
    See: http://people.redhat.com/mingo/cfs-scheduler/sched-design-CFS.txt
    """

    def __init__(self, platform):
        """Generates a full mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        """
        self.platform = platform
        # self.statistics = Statistics()

    def generate_mapping_dict(
        self, kpns, trace_summary, load=None, restricted=None
    ):
        """Generates a full mapping using a static algorithm
        inspired by Linux' GBM
        """
        core_types = dict(self.platform.get_processor_types())
        processes = {}
        mappings = {}
        if restricted is None:
            restricted = []
        if load is None:
            load = []

        for type in core_types:
            processes[type] = SortedList()
            # use best time at first and update depending on the proc. that is next
            for kpn in kpns:
                for p in kpn.processes():
                    processes[type].add(
                        (trace_summary[(p, type)], kpn.name + p.name)
                    )

        finished = False  # to avoid converting the lists every time
        while not finished:
            # round robin
            for core in self.platform.processors():
                if core.name in restricted:
                    continue
                _, pr = processes[core.type].pop()
                process = None
                for kpn in kpns:
                    for proc in kpn.processes():
                        if kpn.name + proc.name == pr:
                            process = proc
                            break
                    if process is not None:
                        break

                # map process to core
                mappings[process] = core

                # remove process from the other lists
                for type in core_types:
                    if core.type == type:
                        continue
                    to_remove = [
                        (time, p) for (time, p) in processes[type] if p == pr
                    ]
                    assert (len(to_remove)) == 1
                    processes[type].remove(to_remove[0])

                if len(processes[core.type]) == 0:
                    finished = True
                    break

        # finish mapping
        return mappings

    def map_to_core(self, mapping, process, core):
        scheduler = list(self.platform.schedulers())[0]
        affinity = core
        priority = 0
        info = ProcessMappingInfo(scheduler, affinity, priority)
        mapping.add_process_info(process, info)


class StaticCFSMapper(StaticCFS):
    """
    Generates a full mapping by using the static CFS method.
    """

    def __init__(self, kpn, platform, trace, representation):
        super().__init__(platform)
        self.full_mapper = True  # flag indicating the mapper type
        self.kpn = kpn
        self.trace = trace
        self.randMapGen = RandomPartialMapper(self.kpn, self.platform)
        self.comMapGen = ComPartialMapper(
            self.kpn, self.platform, self.randMapGen
        )

    def generate_mapping(self, load=None, restricted=None):
        trace_generator = self.trace
        trace_summary = gen_trace_summary(
            self.kpn, self.platform, trace_generator
        )
        trace_generator.reset()
        mapping = Mapping(self.kpn, self.platform)
        mapping_dict = self.generate_mapping_dict(
            [self.kpn], trace_summary, load=load, restricted=restricted
        )
        for proc in self.kpn.processes():
            self.map_to_core(mapping, proc, mapping_dict[proc])
        return self.comMapGen.generate_mapping(mapping)

    def generate_pareto_front(self):
        pareto = []
        restricted = [[]]
        cores = {}
        all_cores = list(self.platform.processors())
        for core_type, _ in self.platform.get_processor_types().items():
            cores[core_type] = [
                core.name for core in all_cores if core.type == core_type
            ]
        for core_type, _ in self.platform.get_processor_types().items():
            new_res = []
            for r in restricted:
                for i in range(len(cores[core_type])):
                    new_res.append(r + cores[core_type][: i + 1])
            restricted = restricted + new_res
        restricted = restricted[:-1]
        log.debug(f"Length of restricted = {len(restricted)}")
        log.debug(f"{restricted}")
        for res in restricted:
            mapping = self.generate_mapping(restricted=res)
            # num_resources = []
            # for core_type in cores:
            #    tot = 0
            #    for core in res:
            #        if core == cores[core_type]:
            #            tot += 1
            #    num_resources.append(tot)
            pareto.append(mapping)
        return pareto


class StaticCFSMapperMultiApp(StaticCFS):
    def __init__(self, platform):
        super().__init__(platform)

    def generate_mappings(self, kpns, traces, load=None, restricted=None):
        if len(kpns) == 0:
            return []
        else:
            log.info(f"generating fair mapping for {len(kpns)} apps")
        comMapGen = {}
        if len(traces) != len(kpns):
            raise RuntimeError(
                f"Mapper received unbalanced number of traces ({len(traces)}) and applications ({len(kpns)})"
            )
        for kpn in kpns:
            randMapGen = RandomPartialMapper(kpn, self.platform)
            comMapGen[kpn] = ComPartialMapper(kpn, self.platform, randMapGen)

        trace_summaries = {}
        mappings = {}
        for kpn, trace in zip(kpns, traces):
            trace_summaries.update(gen_trace_summary(kpn, self.platform, trace))
            mappings[kpn] = Mapping(kpn, self.platform)
            trace.reset()
        mapping_dict = self.generate_mapping_dict(
            kpns, trace_summaries, load=load, restricted=restricted
        )
        for kpn in kpns:
            for proc in kpn.processes():
                self.map_to_core(mappings[kpn], proc, mapping_dict[proc])

        res = []
        for kpn in mappings:
            res.append(comMapGen[kpn].generate_mapping(mappings[kpn]))
        return res

# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov
"""Segmentized scheduled based on Lagrangian relaxation.

This module implements scheduler with an algorithm from:

S. Wildermann, A. Weichslgartner, and J. Teich, “Design methodology
and run-time management for predictable many-core systems,”
in 2015 IEEE International Symposium on Object/Component/Service-Oriented
Real-Time Distributed Computing Workshops, April 2015, pp. 103–110.
"""
from enum import Enum
import logging
import math

from mocasin.tetris.job_state import Job
from mocasin.tetris.schedule import (
    Schedule,
    MultiJobSegmentMapping,
    SingleJobSegmentMapping,
)
from mocasin.tetris.scheduler import SegmentMapperBase, SegmentedScheduler
from mocasin.tetris.scheduler.lr_solver import LRSolver, LRConstraint

log = logging.getLogger(__name__)


class SegLRSortingKey(Enum):
    MINCOST = 1  # Min config cost (as in [SegLR])
    DEADLINE = 2
    MINCOST_DEADLINE_PRODUCT = 3


class SegLRExploreMode(Enum):
    ALL = 1
    BEST = 2


class SegLRSegmentMapper(SegmentMapperBase):
    """MMKP-based application mapping.

    At the beginning, using Lagrangian relaxation solver we obtain the
    multipliers lambda* and the corresponding selection of operating points x*.
    Then the applications are sorted using the sorting key, and are mapped
    incrementally. Per each application, the configuration points are sorted by
    their cost.

    Args:
        scheduler: A segmentized scheduler
        platform (Platform): Platform
        sortingKey (SortingKey): By which order application are mapped
        allow_local_violations (bool): whethen we allow to choose "slow"
            configurations which can be compensated in a next segment
    """

    def __init__(
        self,
        scheduler,
        platform,
        sorting_key=SegLRSortingKey.MINCOST,
        allow_local_violations=True,
        explore_mode=SegLRExploreMode.ALL,
        lr_constraints=LRConstraint.RESOURCE,
        lr_rounds=1000,
    ):
        super().__init__(scheduler, platform)

        self.__sorting_key = sorting_key
        self.__allow_local_violations = allow_local_violations
        self.__explore_mode = explore_mode

        self.__lr_solver = LRSolver(platform, lr_constraints, lr_rounds)

    def generate_segment(self, jobs, segment_start_time=0.0):
        # Solve Lagrangian relaxation of MMKP
        log.debug("Solving Lagrangian relaxation of MMKP...")
        l, job_mappings = self.__lr_solver.solve(
            jobs, segment_start_time=segment_start_time
        )
        log.debug("Found lambda = {}".format(l))

        for j, m in job_mappings:
            log.debug(
                "Job {}, mapping {} [e:{:.3f}], f = {:.3f}".format(
                    j.to_str(),
                    m.get_used_processor_types(),
                    m.metadata.energy,
                    LRSolver.job_config_cost(j, m, l),
                )
            )

        # Sort applications by a defined sorting key
        if self.__sorting_key == SegLRSortingKey.MINCOST:
            # Sort applications that f(x_i*, lambda*) <= f(x_j*, lambda*), i < j
            job_mappings.sort(
                key=lambda x: (LRSolver.job_config_cost(x[0], x[1], l))
            )
        elif self.__sorting_key == SegLRSortingKey.DEADLINE:
            assert False, "NYI"
            min_configs.sort(key=lambda j: j[0].deadline)
        elif self.__sorting_key == SegLR15SortingKey.MINCOST_DEADLINE_PRODUCT:
            assert False, "NYI"
            min_configs.sort(
                key=lambda j: (
                    LRSolver.job_config_costf(j[0], j[2], l) * j[0].deadline
                )
            )
        else:
            assert False, "Sorting key is not known: {}".format(
                self.__sorting_key
            )

        # Empty resource
        avail_cores = self.platform.get_processor_types()

        # Empty segment mapping
        final_job_mappings = {}

        min_rtime = math.inf

        # Map incrementally jobs
        for job, _ in job_mappings:
            log.debug("Selecting a mapping for {}".format(job.to_str()))
            log.debug("Available resources: {}".format(avail_cores))
            cratio = job.cratio
            rratio = 1.0 - cratio
            # Get all configurations of the job, sort them by f(x_i, lambda)
            cost_mappings = [
                (LRSolver.job_config_cost(job, m, l), m)
                for m in job.request.mappings
            ]
            cost_mappings.sort(key=lambda x: x[0])
            assert self.__explore_mode == SegLRExploreMode.ALL, "NYI"

            added = False
            for cost, mapping in cost_mappings:
                # Check if the current mapping fits resources
                map_cores = mapping.get_used_processor_types()
                log.debug(
                    "... Checking mapping: {}, t*:{:.3f}, e*:{:.3f}, f:{:.3f}".format(
                        map_cores,
                        mapping.metadata.exec_time * rratio,
                        mapping.metadata.energy * rratio,
                        cost,
                    )
                )
                if map_cores | avail_cores != avail_cores:
                    log.debug("....... Not enough resources")
                    continue
                # It is possible to map on the available resources, check
                # whether it satisfies its deadline condition.
                if (
                    mapping.metadata.exec_time * rratio + segment_start_time
                    > job.deadline
                ):
                    # This mapping cannot fit deadline condition.
                    # TODO: test whether it is useful
                    if self.__allow_local_violations:
                        # Check whether we may compensate the rate of job
                        # at the end of the segment
                        if min_rtime + segment_start_time > job.deadline:
                            log.debug("....... Cannot meet deadline")
                            continue
                        # Construct a temporary job_segment
                        job_segment = SingleJobSegmentMapping(
                            job.request,
                            mapping,
                            start_time=segment_start_time,
                            start_cratio=cratio,
                            end_time=segment_start_time + min_rtime,
                        )
                        end_cratio = job_segment.end_cratio
                        bctime = min(
                            [m.metadata.exec_time for m in job.request.mappings]
                        ) * (1.0 - end_cratio)
                        if (
                            min_rtime + bctime + segment_start_time
                            > job.deadline
                        ):
                            # This configuration cannot be compensated
                            log.debug(
                                "....... Cannot meet deadline at the end of the current segment after selecting this mapping"
                            )
                            continue
                        final_job_mappings[job] = mapping
                        log.debug("....... Selected")
                    else:
                        assert False, "NYI"
                        log.debug("....... Cannot meet deadline")
                        continue
                else:
                    # This configuration can fit the deadline
                    final_job_mappings[job] = mapping
                    rtime = mapping.metadata.exec_time * rratio
                    min_rtime = min(min_rtime, rtime)
                    log.debug("....... Selected")
                avail_cores -= map_cores
                added = True
                break

        if all(m is None for m in final_job_mappings):
            return None

        # Calculate segment end time
        jobs_rem_time = [
            m.metadata.exec_time * (1.0 - j.cratio)
            for j, m in final_job_mappings.items()
            if m is not None
        ]
        # TODO: Allow MAX_END_GAP at the end of the segment
        # * Make sure that min_rtime also includes such MAX_END_GAP
        # segment_duration = max(
        #     [t for t in jobs_rem_time if t < min(jobs_rem_time) + MAX_END_GAP])
        segment_duration = min(jobs_rem_time)
        segment_end_time = segment_duration + segment_start_time

        # Construct the job_mappings
        job_segments = []
        for j, m in final_job_mappings.items():
            if m is None:
                assert False, "NYI"
                continue
            ssm = SingleJobSegmentMapping(
                j.request,
                m,
                start_time=segment_start_time,
                start_cratio=j.cratio,
                end_time=segment_end_time,
            )
            job_segments.append(ssm)

        # Construct a schedule segment
        new_segment = MultiJobSegmentMapping(self.platform, job_segments)
        new_segment.verify(only_counters=not self.scheduler.rotations)
        # Check that idle jobs do not miss deadline
        for j, m in final_job_mappings.items():
            if m is not None:
                continue
            if j.deadline < shortest_end_time:
                assert False, "NYI"
                return None

        # Generate the job states at the end of the segment
        new_jobs = [
            x
            for x in Job.from_schedule(
                Schedule(self.platform, [new_segment]), jobs
            )
            if not x.is_terminated()
        ]

        log.debug("Generated segment: {}".format(new_segment.to_str()))
        return new_segment, new_jobs


class SegLRScheduler(SegmentedScheduler):
    def __init__(self, platform, **kwargs):
        sorting_arg = kwargs["seg_lr_sorting"]
        if sorting_arg == "COST":
            self.__sorting_key = SegLRSortingKey.MINCOST
        elif sorting_arg == "DEADLINE":
            self.__sorting_key = SegLRSortingKey.DEADLINE
        elif sorting_arg == "CDP":
            self.__sorting_key = SegLRSortingKey.CDP
        else:
            assert False, "Unknown sorting key"

        explore_arg = kwargs["seg_lr_explore"]
        if explore_arg == "ALL":
            self.__explore_mode = SegLRExploreMode.ALL
        elif explore_arg == "BEST":
            assert False, "NYI"
            self.__explore_mode = SegLRExploreMode.BEST
        else:
            assert False, "Unknown explore mode"

        lr_constraints_arg = kwargs["seg_lr_constraints"]
        if len(lr_constraints_arg) == 0:
            lr_constraints_arg.append("R")
        self.__lr_constraints = LRConstraint.NULL
        if "R" in lr_constraints_arg:
            self.__lr_constraints |= LRConstraint.RESOURCE
        if "D" in lr_constraints_arg:
            self.__lr_constraints |= LRConstraint.DELAY
        if "RDP" in lr_constraints_arg:
            self.__lr_constraints |= LRConstraint.RDP

        self.__lr_rounds = kwargs["seg_lr_iters"]
        segment_mapper = SegLRSegmentMapper(
            self,
            platform,
            sorting_key=self.__sorting_key,
            explore_mode=self.__explore_mode,
            lr_constraints=self.__lr_constraints,
            lr_rounds=self.__lr_rounds,
        )
        super().__init__(platform, segment_mapper)

        self.__name = self.__generate_name()

    def __generate_name(self):
        res = "Segmented LR (sorting="
        if self.__sorting_key == SegLRSortingKey.MINCOST:
            res += "C"
        elif self.__sorting_key == SegLRSortingKey.DEADLINE:
            res += "D"
        elif self.__sorting_key == SegLRSortingKey.CDP:
            res += "CDP"
        else:
            assert False, "Unknown sorting key"
        res += ", explore="
        if self.__explore_mode == SegLRExploreMode.ALL:
            res += "EA"
        elif self.__explore_mode == SegLRExploreMode.BEST:
            res += "EB"
        else:
            assert False, "Unknown explore mode"
        res += ", constraints="
        if bool(self.__lr_constraints & LRConstraint.RESOURCE):
            res += "R"
        if bool(self.__lr_constraints & LRConstraint.DELAY):
            res += "D"
        if bool(self.__lr_constraints & LRConstraint.RDP):
            res += "P"
        res += ", rounds="
        res += "{})".format(self.__lr_rounds)

        return res

    @property
    def name(self):
        return self.__name

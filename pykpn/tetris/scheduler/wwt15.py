"""This module implements scheduler with an algorithm from:

S. Wildermann, A. Weichslgartner, and J. Teich, “Design methodology
and run-time management for predictable many-core systems,”
in 2015 IEEE International Symposium on Object/Component/Service-Oriented
Real-Time Distributed Computing Workshops, April 2015, pp. 103–110.
"""

from pykpn.tetris.scheduler.base import (SingleVariantSegmentMapper,
                                         SingleVariantSegmentizedScheduler)
from pykpn.tetris.scheduler.lr_solver import LRSolver, LRConstraint
from pykpn.common.platform import Platform
from pykpn.tetris.job import Job, JobTable
from pykpn.tetris.mapping import SegmentMapping, JobSegmentMapping
from pykpn.tetris.extra import NamedDimensionalNumber

import math
from enum import Enum

import logging
log = logging.getLogger(__name__)


class WWT15SortingKey(Enum):
    MINCOST = 1  # Min config cost (as in [WWT15])
    DEADLINE = 2
    MINCOST_DEADLINE_PRODUCT = 3


class WWT15ExploreMode(Enum):
    ALL = 1
    BEST = 2


class WWT15SegmentMapper(SingleVariantSegmentMapper):
    """ MMKP-based application mapping.

    At the beginning, using Lagrangian relaxation solver we obtain the
    multipliers lambda* and the corresponding selection of operating points x*.
    Then the applications are sorted using the sorting key, and are mapped
    incrementally. Per each application, the configuration points are sorted by
    their cost.

    Args:
        parent_scheduler: A segmentized scheduler
        platform (Platform): Platform
        sortingKey (SortingKey): By which order application are mapped
        allow_local_violations (bool): whethen we allow to choose "slow"
            configurations which can be compensated in a next segment
    """
    def __init__(self, parent_scheduler, platform,
                 sorting_key=WWT15SortingKey.MINCOST,
                 allow_local_violations=True,
                 explore_mode=WWT15ExploreMode.ALL,
                 lr_constraints=LRConstraint.RESOURCE, lr_rounds=1000):

        super().__init__(parent_scheduler, platform)

        self.__sorting_key = sorting_key
        self.__allow_local_violations = allow_local_violations
        self.__explore_mode = explore_mode

        self.__lr_solver = LRSolver(platform, lr_constraints, lr_rounds)

    def schedule(self, jobs):

        # Solve Lagrangian relaxation of MMKP
        l, min_configs = self.__lr_solver.solve(jobs)

        assert isinstance(l, tuple)

        for j in min_configs:
            log.debug("Job rid = {}, config = {}[{}], f = {}".format(
                j[0].rid, j[1], j[2].core_types,
                LRSolver.job_config_cost(j[0], j[2], l)))

        # Sort applications by a defined sorting key
        if self.__sorting_key == WWT15SortingKey.MINCOST:
            # Sort applications that f(x_i*, lambda*) <= f(x_j*, lambda*), i < j
            min_configs.sort(
                key=lambda j: (LRSolver.job_config_cost(j[0], j[2], l)))
        elif self.__sorting_key == WWT15SortingKey.DEADLINE:
            min_configs.sort(key=lambda j: j[0].deadline)
        elif self.__sorting_key == WWT1515SortingKey.MINCOST_DEADLINE_PRODUCT:
            min_configs.sort(key=lambda j: (LRSolver.job_config_costf(
                j[0], j[2], l) * j[0].deadline))
        else:
            assert False, "Sorting key is not known: {}".format(
                self.__sorting_key)

        # Empty resource
        resources = NamedDimensionalNumber(self.platform.core_types(),
                                           init_only_names=True)

        # Empty segment mapping
        segment_mapping = SegmentMapping(self.platform)

        shortest_end_time = None

        # Map incrementally jobs
        for jc in min_configs:
            job = jc[0]
            app = job.app
            cratio = job.cratio
            # Get all configurations of the job, sort them by f(x_i, lambda)
            clist = [(name, can_mapping,
                      LRSolver.job_config_cost(job, can_mapping, l))
                     for name, can_mapping in job.app.mappings.items()
                     if name != "__idle__"]
            clist.sort(key=lambda x: x[2])

            assert self.__explore_mode == WWT15ExploreMode.ALL, "NYI"

            added = False
            for cm_id, can_mapping, _ in clist:
                # Try to map in this order
                if (resources + can_mapping.core_types <=
                        NamedDimensionalNumber(self.platform.core_types())):
                    # It is possible to map on the available resources, check
                    # whether it satisfies its deadline condition.
                    if can_mapping.time(start_cratio=cratio) > job.deadline:
                        # This mapping cannot fit deadline condition.
                        if self.__allow_local_violations:
                            # Check whether we may compensate the rate of job
                            # at the end of the segment
                            if shortest_end_time is None:
                                # There is no running jobs yet, do not map
                                continue
                            if shortest_end_time > job.deadline:
                                continue
                            # Construct a temporary job_segment
                            job_segment = JobSegmentMapping(
                                job.rid, cm_id, start_time=jobs.time,
                                start_cratio=cratio,
                                end_time=shortest_end_time)
                            end_cratio = job_segment.end_cratio
                            if (shortest_end_time +
                                    app.best_case_time(start_cratio=end_cratio)
                                    > job.abs_deadline):
                                # This configuration cannot be compensated
                                continue
                        else:
                            continue
                    else:
                        # This configuration can fit the deadline
                        job_segment = JobSegmentMapping(
                            job.rid, cm_id, start_time=jobs.time,
                            start_cratio=job.cratio, finished=True)
                    segment_mapping.append_job(job_segment,
                                               expand_time_range=True)
                    if shortest_end_time is None:
                        shortest_end_time = job_segment.end_time
                    else:
                        if job_segment.end_time < shortest_end_time:
                            shortest_end_time = job_segment.end_time
                    resources = resources + can_mapping.core_types
                    added = True
                    break

            if not added:
                # Add idle mapping
                # TODO: Special care of idle jobs
                job_segment = JobSegmentMapping(job.rid, "__idle__",
                                                start_time=jobs.time,
                                                start_cratio=job.cratio,
                                                end_time=math.inf)
                segment_mapping.append_job(job_segment, expand_time_range=True)

        if shortest_end_time is None:
            # No running jobs were added
            return None

        # Cut at the shortest mapping
        segment_mapping = segment_mapping.max_full_subsegment_from_start()

        # Check that idle jobs do not miss deadline
        for jm in segment_mapping:
            if not jm.idle:
                continue
            job = jobs.find_by_rid(jm.rid)
            if job.abs_deadline < shortest_end_time:
                return None

        log.debug("Generated segment: {}".format(segment_mapping.legacy_str()))
        return segment_mapping


class WWT15Scheduler(SingleVariantSegmentizedScheduler):
    def __init__(self, app_table, platform, config):
        sorting_arg = config["wwt15_sorting"]
        if sorting_arg == "COST":
            self.__sorting_key = WWT15SortingKey.MINCOST
        elif sorting_arg == "DEADLINE":
            self.__sorting_key = WWT15SortingKey.DEADLINE
        elif sorting_arg == "CDP":
            self.__sorting_key = WWT15SortingKey.CDP
        else:
            assert False, "Unknown sorting key"

        explore_arg = config["wwt15_seg_explore"]
        if explore_arg == "ALL":
            self.__explore_mode = WWT15ExploreMode.ALL
        elif explore_arg == "BEST":
            self.__explore_mode = WWT15ExploreMode.BEST
        else:
            assert False, "Unknown explore mode"

        lr_constraints_arg = config["wwt15_lr"]
        if len(lr_constraints_arg) == 0:
            lr_constraints_arg.append("R")
        self.__lr_constraints = LRConstraint.NULL
        if "R" in lr_constraints_arg:
            self.__lr_constraints |= LRConstraint.RESOURCE
        if "D" in lr_constraints_arg:
            self.__lr_constraints |= LRConstraint.DELAY
        if "RDP" in lr_constraints_arg:
            self.__lr_constraints |= LRConstraint.RDP

        self.__lr_rounds = config["wwt15_lr_rounds"]
        segment_mapper = WWT15SegmentMapper(
            self, platform, sorting_key=self.__sorting_key,
            explore_mode=self.__explore_mode,
            lr_constraints=self.__lr_constraints, lr_rounds=self.__lr_rounds)
        super().__init__(app_table, platform, segment_mapper)

        self.__name = self.__generate_name()

    def __generate_name(self):
        res = "WWT15-SEG-"
        if self.__sorting_key == WWT15SortingKey.MINCOST:
            res += "C-"
        elif self.__sorting_key == WWT15SortingKey.DEADLINE:
            res += "D-"
        elif self.__sorting_key == WWT15SortingKey.CDP:
            res += "CDP-"
        else:
            assert False, "Unknown sorting key"
        if self.__explore_mode == WWT15ExploreMode.ALL:
            res += "EA-"
        elif self.__explore_mode == WWT15ExploreMode.BEST:
            res += "EB-"
        else:
            assert False, "Unknown explore mode"
        res += "LR"
        if bool(self.__lr_constraints & LRConstraint.RESOURCE):
            res += "R"
        if bool(self.__lr_constraints & LRConstraint.DELAY):
            res += "D"
        if bool(self.__lr_constraints & LRConstraint.RDP):
            res += "P"
        res += "-"
        res += "R{}".format(self.__lr_rounds)

        return res

    @property
    def name(self):
        return self.__name

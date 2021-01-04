#!/usr/bin/env python3

from pykpn.tetris.context import Context
from pykpn.tetris.mapping import SegmentMapping, JobSegmentMapping
from pykpn.tetris.scheduler.base import (SingleVariantSegmentMapper,
                                         SingleVariantSegmentizedScheduler)
from pykpn.tetris.extra import NamedDimensionalNumber
import math
import logging

log = logging.getLogger(__name__)

FINISH_MAX_DIFF = 0.5


class FastSegmentMapper(SingleVariantSegmentMapper):
    """ TODO: Add a description"""
    def __init__(self, parent_scheduler, platform):

        super().__init__(parent_scheduler, platform)

    def __select_app_mappings_fit_deadline_resources(self, app, deadline,
                                                     avl_core_types,
                                                     completion=0.0):
        res = []
        for mid, mapping in app.mappings.items():
            if mid == '__idle__':
                continue
            rem_time = (1.0-completion) * mapping.time()
            if rem_time > deadline:
                continue
            if not (mapping.core_types <= avl_core_types):
                continue

            rem_energy = (1.0-completion) * mapping.energy()
            res.append((mid, rem_energy))
        res.sort(key=lambda tup: tup[1])
        return res

    def __create_mapping_from_list(self, clist):
        full_mapping_list = []

        # Calculate estimated end time
        for ts, m in zip(self.__job_table, clist):
            single_job_mapping = JobSegmentMapping(
                ts.rid, m, start_time=self.__start_time,
                start_cratio=ts.cratio, finished=True)
            full_mapping_list.append(single_job_mapping)

        segment_mapping_list = []
        min_finish_time = min([x.end_time for x in full_mapping_list])
        stop_jobs = [
            x for x in full_mapping_list
            if x.end_time < min_finish_time + FINISH_MAX_DIFF
        ]
        segment_end_time = max([x.end_time for x in stop_jobs])
        for fsm in full_mapping_list:
            ssm = JobSegmentMapping(fsm.rid, fsm.can_mapping_id,
                                    start_time=fsm.start_time,
                                    start_cratio=fsm.start_cratio,
                                    end_time=segment_end_time)
            segment_mapping_list.append(ssm)

        # Check if the scheduling meets deadlines
        segment_meets_deadline = True
        finished = True
        for ssm in segment_mapping_list:
            rid = ssm.rid
            ts = self.__job_table.find_by_rid(rid)
            d = ts.abs_deadline
            if not ssm.finished:
                finished = False
            if ssm.end_time > d:
                segment_meets_deadline = False
            app = ts.app
            min_time_left = app.best_case_time(start_cratio=ssm.end_cratio)
            if min_time_left + ssm.end_time > d:
                segment_meets_deadline = False

        cur_energy = sum([x.energy for x in segment_mapping_list])

        new_segment = SegmentMapping(
            self.platform, segment_mapping_list,
            time_range=(self.__start_time, segment_end_time))
        return (segment_meets_deadline, new_segment)

    def schedule(self, job_table):
        assert len(job_table) != 0
        self.__job_table = job_table
        self.__start_time = job_table.time

        mapping = [None] * len(self.__job_table)
        avl_core_types = NamedDimensionalNumber(
            dict(self.platform.get_processor_types()))

        while None in mapping:
            # List of mappings to finish the applications
            to_finish = [None] * len(self.__job_table)
            i_max_diff, diff = None, -math.inf
            for i, r in enumerate(mapping):
                if r is not None:
                    continue
                rid = self.__job_table[i].rid
                d = Context().req_table[rid].deadline()
                c = self.__job_table[i].cratio
                app = Context().req_table[rid].app()
                to_finish[i] = (
                    self.__select_app_mappings_fit_deadline_resources(
                        app, d - self.__start_time, avl_core_types,
                        completion=c))
                log.debug("to_finish[{}]: {}".format(i, to_finish[i]))
                if len(to_finish[i]) == 0:
                    mapping[i] = '__idle__'
                    continue
                if len(to_finish[i]) == 1:
                    diff = math.inf
                    i_max_diff = i
                    continue
                if to_finish[i][1][1] - to_finish[i][0][1] > diff:
                    diff = to_finish[i][1][1] - to_finish[i][0][1]
                    i_max_diff = i
            log.debug("Choose {}".format(i_max_diff))
            if i_max_diff is None:
                return None
            # On Odroid XU-4, the check that it can be scheduled is simple.
            # All mappings in to_finish are valid.
            rid = self.__job_table[i_max_diff].rid
            a = Context().req_table[rid].app()
            mid = to_finish[i_max_diff][0][0]
            m = a.mappings[mid]
            avl_core_types -= m.core_types
            mapping[i_max_diff] = mid
        log.debug('Mapping: {}'.format(mapping))
        res, segment = self.__create_mapping_from_list(mapping)
        if res:
            return segment
        else:
            return None


class FastScheduler(SingleVariantSegmentizedScheduler):
    def __init__(self, app_table, platform):
        """Fast scheduler.

        :param app_table: a table with applications
        :type app_table: AppTable
        :param platform: a platform
        :type platform: Platform
        """
        segment_mapper = FastSegmentMapper(self, platform)
        super().__init__(app_table, platform, segment_mapper)

    @property
    def name(self):
        return "FAST"

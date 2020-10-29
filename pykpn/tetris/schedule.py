# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov
"""
This module implements schedule structure.
Schedule is represented as list of segments, each segment includes the mappings
of each particular job.

Todo:
    1) Add verification of the schedules
    2) Compact printing
"""

from pykpn.tetris.job_request import JobRequestInfo

from pykpn.common.mapping import Mapping
from pykpn.common.platform import Platform

from collections import Counter
from functools import reduce
import logging
import math
import sys

EPS = 0.00001
MAX_END_GAP = 0.5

log = logging.getLogger(__name__)


class JobSegmentMapping:
    """A mapping of a single job on a time segment.

    Each mapping is defined by the job request, time segment and the completion
    ratios of the application at both ends of the time segment.

    Note: the constructor require that only one condition is satisfied
        1) end_time is not None
        2) end_cratio is not None
        3) finished is True

    Args:
        job_request (JobRequestInfo): a job request
        mapping (Mapping): a mapping
        start_time (float): start time of a segment
        start_cratio (float): a completion ratio at the beginning of the segment
        end_time (float): an end time of a segment
        end_cratio (float): a completion ratio at the end of the segment
        finished (bool): Whether application finished its execution during this
            segment.
    """
    def __init__(self, job_request, mapping, start_time=0.0, start_cratio=0.0,
                 end_time=None, end_cratio=None, finished=False):
        assert isinstance(job_request, JobRequestInfo)
        assert isinstance(mapping, Mapping)
        assert isinstance(start_time, (int, float)), (
            "Start_time is of type {}, but must be float or int".format(
                type(start_time)))
        assert isinstance(start_cratio, float)

        self.__request = job_request
        self.__mapping = mapping

        self.__start_time = start_time
        self.__start_cratio = start_cratio

        self.__end_time = None
        self.__end_cratio = None
        self.__finished = None
        self.__energy = None

        if end_time is not None:
            assert end_cratio is None and not finished, (
                "Only one argument must be set: end_time, end_cratio, finished"
            )
            self.__init_by_end_time(end_time)
        elif end_cratio is not None:
            assert end_time is None and not finished, (
                "Only one argument must be set: end_time, end_cratio, finished"
            )
            self.__init_by_end_cratio(end_cratio)
        elif finished:
            assert end_cratio is None and end_time is None, (
                "Only one argument must be set: end_time, end_cratio, finished"
            )
            self.__init_finished()

    def __init_by_end_time(self, end_time):
        assert end_time >= self.__start_time, (
            "end_time ({}) must be greater or equal then start_time ({})"
            .format(end_time, self.__start_time))
        full_rem_time = self.mapping.metadata.exec_time * (1. -
                                                           self.__start_cratio)
        segment_time = end_time - self.__start_time
        if full_rem_time <= segment_time + EPS:
            self.__end_time = self.__start_time + full_rem_time
            self.__end_cratio = 1.0
            self.__finished = True
        else:
            self.__end_time = end_time
            self.__end_cratio = (
                self.__start_cratio +
                segment_time / self.mapping.metadata.exec_time)
            self.__finished = False
        cratio = self.__end_cratio - self.__start_cratio
        self.__energy = self.mapping.metadata.energy * cratio

    def __init_by_end_cratio(self, end_cratio):
        assert end_cratio >= self.__start_cratio
        cratio = end_cratio - self.__start_cratio
        rem_time = self.mapping.exec_time * cratio
        self.__end_time = self.__start_time + rem_time
        self.__end_cratio = end_cratio
        self.__finished = (end_cratio == 1.0)
        self.__energy = self.mapping.energy * cratio

    def __init_finished(self):
        cratio = 1.0 - self.__start_cratio
        rem_time = self.mapping.metadata.exec_time * cratio
        self.__end_time = self.__start_time + rem_time
        self.__end_cratio = 1.0
        self.__finished = True
        self.__energy = self.mapping.metadata.energy * cratio

    @property
    def request(self):
        """JobRequestInfo: The request."""
        return self.__request

    @property
    def app(self):
        """KpnGraph: The kpn graph."""
        return self.__request.app

    @property
    def mapping(self):
        """Mapping: the mapping."""
        return self.__mapping

    @property
    def start_time(self):
        """float: The start time of the single mapping."""
        return self.__start_time

    @property
    def start_cratio(self):
        """float: Returns the start completion ratio of the mapping.

        Todo:
            * Consider changing to functions `start_state()`
        """
        return self.__start_cratio

    @property
    def end_time(self):
        """float: Returns the end time of the single mapping."""
        return self.__end_time

    @property
    def end_cratio(self):
        """float: Returns the end completion ratio of the single mapping.abs

        Todo:
            * Consider changing to functions `end_state()`
        """
        return self.__end_cratio

    @property
    def finished(self):
        """bool: Whether application is finished at the end of the segment."""
        return self.__finished

    @property
    def energy(self):
        """float: Returns the consumed energy."""
        return self.__energy

    def verify(self):
        """ Verify that the object in a consistent state."""
        assert self.__end_time is not None
        assert self.__end_cratio is not None
        assert self.__end_cratio <= 1.0
        assert self.__end_cratio >= self.__start_cratio
        assert self.__finished is not None
        assert self.__energy is not None

        if self.finished and self.end_cratio < 1.0:
            log.critical(
                "Inconsistent finished ({}) and end_cratio values ({})".format(
                    self.finished, self.end_cratio))
            assert False

    def to_str(self):
        cores = self.mapping.get_used_processors()
        core_types = self.mapping.get_used_processor_types()
        print(core_types)
        core_types_str = ", ".join(
            ["{}: {}".format(ty, count) for ty, count in core_types.items()])
        job_str = "Job: {} ".format(self.app.name)
        mapping_str = "mapping: {}[{}, EU: {{exec_time={:.3f} energy={:.3f}}}]".format(
            cores, core_types_str, self.mapping.metadata.exec_time, self.mapping.metadata.energy)
        start_str = "start = {0:.3f} [{1:.2f}]".format(self.start_time,
                                                       self.start_cratio)
        if self.finished:
            f_str = "F"
        else:
            f_str = ""
        end_str = "end = {:.3f} [{:.2f}{}]".format(self.end_time,
                                                   self.end_cratio, f_str)
        energy_str = "energy = {:.3f}".format(self.energy)
        res_str = "{}, {}, {}, {}, {}".format(job_str, mapping_str, start_str,
                                              end_str, energy_str)
        return res_str


class ScheduleSegment:
    """ Job mappings defined on a single time segment

    Args:
        platform (Platform): The platform model
        jobs (:obj:`list` of :obj:`SingleJobMapping`): A list of
            JobSegmentMapping objects
    """
    def __init__(self, platform, jobs=[]):
        self.platform = platform
        self.__time_range = (None, None)
        self.__jobs = []

        for j in jobs:
            self.append_job(j)

    @property
    def start_time(self):
        """float: The start time of the segment"""
        return self.__time_range[0]

    @property
    def end_time(self):
        """float: The end time of the segment"""
        return self.__time_range[1]

    @property
    def duration(self):
        """float: The duration of the segment."""
        return self.end_time - self.start_time

    @property
    def energy(self):
        """float: The consumed energy."""
        return sum([x.energy for x in self.__jobs])

    def jobs(self):
        """list(JobSegmentMapping): Returns a shallow copy of job mappings."""
        return self.__jobs.copy()

    @property
    def finished(self):
        """bool: Whether all active jobs are finished during the current
        segment.
        """
        res = True
        for jm in self.__jobs:
            res = res and jm.finished
        return res

    def verify(self):
        """ Verify that ScheduleSegment in a consistent stay.
        """
        failed = False
        # All JobSegmentMappings should have the same time range
        for j in self.__jobs:
            j.verify()
            if abs(self.start_time - j.start_time) > EPS:
                log.error(
                    "Job start_time does not equal segment start_time: {}"
                    .format(j.to_str()))
                failed = True
            if (self.end_time - j.end_time > MAX_END_GAP
                    or j.end_time - self.end_time > EPS):
                log.error(
                    "Job start_time does not equal segment start_time: {}"
                    .format(j.to_str()))
                failed = True

        # Check that there are enough processors
        cores_used = self.get_used_processor_types()
        cores_total = self.platform.get_processor_types()
        if (cores_used | cores_total) != cores_total:
            log.error("Not enough available processors for a schedule segment")
            failed = True

        if failed:
            log.error("Some errors found in a segment schedule: {}".format(
                self.to_str()))
            assert False

    def __iter__(self):
        yield from self.__jobs

    def __len__(self):
        return len(self.__jobs)

    def append_job(self, job):
        """Add a new job mapping to the current object."""
        assert job is not None
        assert isinstance(job, JobSegmentMapping)

        self.__jobs.append(job)

        if self.start_time is None:
            new_start_time, new_end_time = job.start_time, job.end_time
        else:
            new_start_time = min(self.start_time, job.start_time)
            new_end_time = max(self.end_time, job.end_time)
        self.__time_range = (new_start_time, new_end_time)

    def get_used_processors(self):
        """ Returns the set of used processors. """
        return reduce(set.union,
                      [x.mapping.get_used_processors() for x in self.jobs()])

    def get_used_processor_types(self):
        """Counter: Number of used cores per type."""
        used_procs = reduce(
            (lambda x, y: x + y),
            [x.mapping.get_used_processor_types() for x in self.jobs()],
            Counter())
        return used_procs

    def split(self, time):
        """Split the current segment at time time.

        Args:
            time (float): Time to split the segment.

        Returns:
            A tupple with two mapping segment split at time `time`.
        """
        assert time < self.end_time and self.start_time < time, (
            "Trying to split a segment at time {}, which is outside of"
            " the segment time range [{}, {})".format(time, self.start_time,
                                                      self.end_time))

        m1 = ScheduleSegment(self.platform)
        m2 = ScheduleSegment(self.platform)
        for jm in self:
            jm1 = JobSegmentMapping(jm.request, jm.mapping,
                                    start_time=jm.start_time,
                                    start_cratio=jm.start_cratio,
                                    end_time=time)
            m1.append_job(jm1)
            if jm1.finished:
                continue
            jm2 = JobSegmentMapping(jm.request, jm.mapping, start_time=time,
                                    start_cratio=jm1.end_cratio,
                                    end_time=jm.end_time)
            m2.append_job(jm2)
        return m1, m2

    def to_str(self):
        res = ("Schedule segment: [{:.3f}, {:.3f}), energy: {:.3f}".format(
            self.start_time, self.end_time, self.energy) + "\n")
        for sm in self:
            res += "  " + sm.to_str() + "\n"
        return res


class Schedule:
    """A multi-applicaiton schedule.

    The schedule is represented as a list of schedule segments, which in turn
    are represented as the list of individual job mappings.
    """
    def __init__(self, platform, segments=[]):
        assert isinstance(platform, Platform)
        self.platform = platform
        self.__segments = []

        # yapf: disable
        assert isinstance(segments, (list, ScheduleSegment)), (
                "segments must be a list or a ScheduleSegment, but it is {}"
                .format(type(segments)))
        # yapf: enable

        if isinstance(segments, ScheduleSegment):
            segments = [segments]

        for s in segments:
            self.append_segment(s)

    @property
    def start_time(self):
        """float: The start time of the schedule."""
        if self.first is None:
            return None
        return self.first.start_time

    @property
    def end_time(self):
        """float: The end time of the schedule."""
        if self.last is None:
            return None
        return self.last.end_time

    @property
    def energy(self):
        """float: The energy consumption of the schedule"""
        return sum([x.energy for x in self.__segments], 0.0)

    @property
    def first(self):
        """ScheduleSegment: the first schedule segment"""
        if len(self.__segments) == 0:
            return None
        return self.__segments[0]

    @property
    def last(self):
        """ScheduleSegment: the last schedule segment"""
        if len(self.__segments) == 0:
            return None
        return self.__segments[-1]

    def segments(self):
        """list(ScheduleSegment): Returns a shallow copy of schedule segments"""
        return self.__segments.copy()

    def copy(self):
        """Schedule: Returns a copy of the schedule segments"""
        copy_segments = []
        for segment in self.__segments:
            copy_segments.append(
                ScheduleSegment(segment.platform, segment.jobs()))

        return Schedule(self.platform, copy_segments)

    def append_segment(self, segment):
        self.__segments.append(segment)

    def insert_segment(self, index, segment):
        """Insert a segment into mapping.

        Args:
            index (int): The position where a segment needs to be inserted
            segment (ScheduleSegment): The segment to insert.
        """
        self.__segments.insert(index, segment)

    def remove_segment(self, index):
        """Remove a segment by index.

        Args:
            index (int): The position of a segment to remove.
        """
        del self.__segments[index]

    def __len__(self):
        return len(self.__segments)

    def __iter__(self):
        yield from self.__segments

    def verify(self):
        for segment in self:
            segment.verify()

    def to_str(self):
        """Compact representation of the schedule.

        Format:
        Schedule t:(<start_time>, <end_time>), e:<energy>
            [t:(<start_time>, <end_time>) <n> job(s), PEs: <cores_used>, e:<energy> ]
        where the format of <cores_used>: (<type>: <count>, ...)
        """
        res = "Schedule t:({}, {}), e:{:.3f}\n".format(self.start_time,
                                                       self.end_time,
                                                       self.energy)
        for segment in self:
            res += "    [t:({:.3f}, {:.3f}), ".format(segment.start_time,
                                                      segment.end_time)
            res += "{} job".format(len(segment))
            if len(segment) > 1:
                res += "s"
            res += ", PEs: {}, e:{:.3f}]\n".format(
                segment.get_used_processor_types(), segment.energy)
        return res

    def count_finished_jobs(self):
        return sum([ms[-1].finished for _, ms in self.per_requests().items()])

    def per_requests(self, none_as_idle=False):
        """ Returns a dict of 'JobRequestInfo' objects involved in the schedule
        with the list of 'JobSegmentMapping' objects. If 'none_as_idle' is true,
        add None values for the segment where the job was idle or finished.
        """
        res = {}
        for i, segment in enumerate(self):
            for j in segment:
                if j.request not in res:
                    if none_as_idle:
                        res[j.request] = [None] * i
                    else:
                        res[j.request] = []
                res[j.request].append(j)
            if none_as_idle:
                for k, v in res.items():
                    if len(v) == i:
                        res[k].append(None)
                    assert len(v) == i + 1
        return res

    def find_request_segments(self, request):
        """Returns a list of job segment mappings for of specific job request.
        """
        res = []
        for segment in self:
            for j in segment:
                if j.request == request:
                    res.append(j)
        return res

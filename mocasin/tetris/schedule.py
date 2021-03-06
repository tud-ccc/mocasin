# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
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

from mocasin.tetris.job_request import JobRequestInfo

from mocasin.common.mapping import Mapping
from mocasin.common.platform import Platform
from mocasin.representations import SimpleVectorRepresentation

from collections import Counter
from functools import reduce
import itertools
import logging

ENERGY_EPS = 0.00001
TIME_EPS = 0.00001
CRATIO_EPS = 0.00001
# TODO: Make this parameter be read from the config
MAX_END_GAP = 0.5

log = logging.getLogger(__name__)


class SingleJobSegmentMapping:
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

    def __init__(
        self,
        job_request,
        mapping,
        start_time=0.0,
        start_cratio=0.0,
        end_time=None,
        end_cratio=None,
        finished=False,
    ):
        assert isinstance(job_request, JobRequestInfo)
        assert isinstance(mapping, Mapping)
        assert isinstance(
            start_time, (int, float)
        ), "Start_time is of type {}, but must be float or int".format(
            type(start_time)
        )
        assert isinstance(start_cratio, float)

        self.__request = job_request
        self.__mapping = mapping

        self.__start_time = start_time  # in ms
        self.__start_cratio = start_cratio

        self.__end_time = None
        self.__end_cratio = None
        self.__finished = None
        self.__energy = None

        if end_time is not None:
            assert (
                end_cratio is None and not finished
            ), "Only one argument must be set: end_time, end_cratio, finished"
            self.__init_by_end_time(end_time)
        elif end_cratio is not None:
            assert (
                end_time is None and not finished
            ), "Only one argument must be set: end_time, end_cratio, finished"
            self.__init_by_end_cratio(end_cratio)
        elif finished:
            assert (
                end_cratio is None and end_time is None
            ), "Only one argument must be set: end_time, end_cratio, finished"
            self.__init_finished()

    def __init_by_end_time(self, end_time):
        assert (
            end_time >= self.__start_time
        ), "end_time ({}) must be greater or equal then start_time ({})".format(
            end_time, self.__start_time
        )
        full_rem_time = self.mapping.metadata.exec_time * (
            1.0 - self.__start_cratio
        )
        segment_time = end_time - self.__start_time
        if full_rem_time <= segment_time + TIME_EPS:
            self.__end_time = self.__start_time + full_rem_time
            self.__end_cratio = 1.0
            self.__finished = True
        else:
            self.__end_time = end_time
            self.__end_cratio = (
                self.__start_cratio
                + segment_time / self.mapping.metadata.exec_time
            )
            self.__finished = False
        cratio = self.__end_cratio - self.__start_cratio
        self.__energy = self.mapping.metadata.energy * cratio

    def __init_by_end_cratio(self, end_cratio):
        assert end_cratio >= self.__start_cratio
        cratio = end_cratio - self.__start_cratio
        rem_time = self.mapping.metadata.exec_time * cratio
        self.__end_time = self.__start_time + rem_time
        self.__end_cratio = end_cratio
        self.__finished = end_cratio == 1.0
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
        """DataflowGraph: The dataflow graph."""
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
    def duration(self):
        """float: The duration of the job segment."""
        return self.end_time - self.start_time

    @property
    def finished(self):
        """bool: Whether application is finished at the end of the segment."""
        return self.__finished

    @property
    def energy(self):
        """float: Returns the consumed energy."""
        return self.__energy

    def verify(self):
        """Verify that the object in a consistent state."""
        assert self.__end_time is not None
        assert self.__end_cratio is not None
        assert self.__end_cratio <= 1.0
        assert self.__end_cratio >= self.__start_cratio
        assert self.__finished is not None
        assert self.__energy is not None

        if self.finished and self.end_cratio < 1.0:
            log.critical(
                "Inconsistent finished ({}) and end_cratio values ({})".format(
                    self.finished, self.end_cratio
                )
            )
            assert False

    def to_str(self):
        cores = self.mapping.get_used_processors()
        cores_str = "{{{}}}".format(", ".join(sorted([x.name for x in cores])))
        core_types = self.mapping.get_used_processor_types()
        core_types_str = ", ".join(
            [
                "{}: {}".format(ty, count)
                for ty, count in sorted(core_types.items())
            ]
        )
        job_str = "Job: {} ".format(self.app.name)
        mapping_str = "mapping: {} [{} | t={:.3f} e={:.3f}]".format(
            cores_str,
            core_types_str,
            self.mapping.metadata.exec_time,
            self.mapping.metadata.energy,
        )
        start_str = "start = {0:.3f} [{1:.2f}]".format(
            self.start_time, self.start_cratio
        )
        if self.finished:
            f_str = "F"
        else:
            f_str = ""
        end_str = "end = {:.3f} [{:.2f}{}]".format(
            self.end_time, self.end_cratio, f_str
        )
        energy_str = "energy = {:.3f}".format(self.energy)
        res_str = "{}, {}, {}, {}, {}".format(
            job_str, start_str, end_str, energy_str, mapping_str
        )
        return res_str


class MultiJobSegmentMapping:
    """Multiple Job Segment Mapping.

    This class contains the job's mappings active in a schedule segment.

    Args:
        platform (Platform): The platform model
        jobs (:obj:`list` of :obj:`SingleJobSegmentMapping`): A list of
            SingleJobSegmentMapping objects
    """

    def __init__(self, platform, jobs=[]):
        self.platform = platform
        self._start_time = None  # in ms
        self._end_time = None  # in ms
        self._jobs = []

        for j in jobs:
            self.append_job(j)

    @property
    def start_time(self):
        """float: The start time of the segment"""
        return self._start_time

    @property
    def end_time(self):
        """float: The end time of the segment"""
        return self._end_time

    @property
    def duration(self):
        """float: The duration of the segment."""
        return self.end_time - self.start_time

    @property
    def energy(self):
        """float: The consumed energy."""
        return sum([x.energy for x in self._jobs])

    def jobs(self):
        """list(SingleJobSegmentMapping): Returns a shallow copy of
        single job segment mappings.
        """
        return self._jobs.copy()

    def verify(self, only_counters=False):
        """Verify that MultiJobSegmentMapping in a consistent stay."""
        failed = False
        # All JobSegmentMappings should have the same time range
        for j in self._jobs:
            j.verify()
            if abs(self.start_time - j.start_time) > TIME_EPS:
                log.error(
                    "Job start_time does not equal segment start_time: "
                    f"{j.to_str()}"
                )
                failed = True
            if (
                self.end_time - j.end_time > MAX_END_GAP
                or j.end_time - self.end_time > TIME_EPS
            ):
                log.error(
                    "Job start_time does not equal segment start_time: {}".format(
                        j.to_str()
                    )
                )
                failed = True

        # Check that there are enough processors
        if only_counters:
            cores_used = self.get_used_processor_types()
            cores_total = self.platform.get_processor_types()
            if (cores_used | cores_total) != cores_total:
                log.error(
                    "Not enough available processors for a schedule segment"
                )
                failed = True
        else:
            for j1, j2 in itertools.combinations(self._jobs, r=2):
                j1_cores = j1.mapping.get_used_processors()
                j2_cores = j2.mapping.get_used_processors()
                if j1_cores.intersection(j2_cores):
                    log.error(
                        f"Some jobs share the jobs: {j1_cores}, {j2_cores}"
                    )
                    failed = True

        if failed:
            log.error(
                "Some errors found in a segment schedule: {}".format(
                    self.to_str()
                )
            )
            assert False

    def find_job_segment(self, request):
        """Find a job segment by the request."""
        for job_segment in self._jobs:
            if job_segment.request != request:
                continue
            return job_segment
        return None

    def append_job(self, job):
        """Add a new job mapping to the current object."""
        assert job is not None
        assert isinstance(job, SingleJobSegmentMapping)

        self._jobs.append(job)

        if self.start_time is None:
            new_start_time, new_end_time = job.start_time, job.end_time
        else:
            new_start_time = min(self.start_time, job.start_time)
            new_end_time = max(self.end_time, job.end_time)
        self._start_time, self._end_time = new_start_time, new_end_time

    def remove_job(self, job):
        """Remove a job from the MultiJobSegmentMapping."""
        assert job in self._jobs
        self._jobs.remove(job)

    def get_requests(self):
        """Get active requests in the segment."""
        res = set()
        for job in self._jobs:
            res.add(job.request)
        return res

    def get_used_processors(self):
        """Returns the set of used processors."""
        return reduce(
            set.union, [x.mapping.get_used_processors() for x in self._jobs]
        )

    def get_used_processor_types(self):
        """Counter: Number of used cores per type."""
        used_procs = reduce(
            (lambda x, y: x + y),
            [x.mapping.get_used_processor_types() for x in self._jobs],
            Counter(),
        )
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
            " the segment time range [{}, {})".format(
                time, self.start_time, self.end_time
            )
        )

        m1 = MultiJobSegmentMapping(self.platform)
        m2 = MultiJobSegmentMapping(self.platform)
        for jm in self._jobs:
            jm1 = SingleJobSegmentMapping(
                jm.request,
                jm.mapping,
                start_time=jm.start_time,
                start_cratio=jm.start_cratio,
                end_time=time,
            )
            m1.append_job(jm1)
            if jm1.finished:
                continue
            jm2 = SingleJobSegmentMapping(
                jm.request,
                jm.mapping,
                start_time=time,
                start_cratio=jm1.end_cratio,
                end_time=jm.end_time,
            )
            m2.append_job(jm2)
        return m1, m2

    def to_str(self):
        res = (
            "Schedule segment: [{:.3f}, {:.3f}), energy: {:.3f}".format(
                self.start_time, self.end_time, self.energy
            )
            + "\n"
        )
        for sm in self._jobs:
            res += "  " + sm.to_str() + "\n"
        return res


class Schedule:
    """A multi-applicaiton schedule.

    The schedule is represented as a list of schedule segments, which in turn
    are represented as the list of individual job mappings.
    """

    def __init__(self, platform, segments=None):
        assert isinstance(platform, Platform)
        self.platform = platform
        self._segments = []

        if segments:
            for s in segments:
                self.add_segment(s)

    @property
    def start_time(self):
        """float: The start time of the schedule."""
        if self.is_empty():
            return None
        return self._segments[0].start_time

    @property
    def end_time(self):
        """float: The end time of the schedule."""
        if self.is_empty():
            return None
        return self._segments[-1].end_time

    @property
    def energy(self):
        """float: The energy consumption of the schedule"""
        return sum([x.energy for x in self._segments], 0.0)

    def is_empty(self):
        """Returns if the schedule is empty."""
        return len(self._segments) == 0

    def segments(self):
        """list(MultiJobSegmentMapping): Returns a shallow copy of
        multi job segment mappings.
        """
        return self._segments.copy()

    def copy(self):
        """Schedule: Returns a copy of the schedule segments"""
        copy_segments = []
        for segment in self._segments:
            copy_segments.append(
                MultiJobSegmentMapping(segment.platform, segment.jobs())
            )

        return Schedule(self.platform, copy_segments)

    def _find_segment_overlap(self, new_segment):
        """Returns a segment which overlaps with a new segment."""
        start_time = new_segment.start_time
        end_time = new_segment.end_time
        assert start_time is not None and end_time is not None

        for segment in self._segments:
            if segment.start_time <= start_time < segment.end_time - TIME_EPS:
                return segment
            if segment.start_time + TIME_EPS < end_time <= segment.end_time:
                return segment
            if start_time <= segment.start_time < end_time - TIME_EPS:
                return segment
            if start_time + TIME_EPS < segment.end_time <= end_time:
                return segment
        return None

    def add_segment(self, new_segment):
        """Add segment to the schedule.

        The segments could be added in any order to the schedule, however, it
        must not overlap with any already added segments. The new segment is
        inserted to the correct place, so all segments are chronologically
        ordered.
        """
        # Check that new segment does not overlap with any already added
        overlap = self._find_segment_overlap(new_segment)
        start_time = new_segment.start_time
        end_time = new_segment.end_time
        if overlap:
            raise RuntimeError(
                f"New segment ({start_time}, {end_time}) overlaps with another "
                f"segment ({overlap.start_time}, {overlap.end_time})"
            )

        if self.is_empty():
            self._segments.append(new_segment)
            return

        # Find a right position to insert the segment
        idx = None
        for i, segment in enumerate(self._segments):
            if segment.start_time >= new_segment.start_time:
                idx = i
                break

        if idx is None:
            self._segments.append(new_segment)
            return

        self._segments.insert(idx, new_segment)

    def remove_segment(self, segment):
        """Remove the segment.

        Args:
            segment (MultiJobSegmentMapping): The segment to remove.
        """
        if segment not in self._segments:
            raise RuntimeError("Segment not found")
        self._segments.remove(segment)

    def pop_front(self):
        """Remove a first segment from the schedule."""
        return self._segments.pop(0)

    def verify(self, only_counters=False):
        # Verify segments
        for segment in self._segments:
            segment.verify(only_counters=only_counters)

        failed = False

        # Verify the segment borders
        s0, s1 = itertools.tee(self._segments)
        next(s1, None)
        for left, right in zip(s0, s1):
            if abs(left.end_time - right.start_time) > TIME_EPS:
                failed = True
                log.error(
                    "The segment is not aligned with the end of "
                    "the previous segment:\n{}\n{}".format(
                        left.to_str(), right.to_str()
                    )
                )

        if failed:
            log.error(
                "Some errors found in a segment schedule: {}".format(
                    self.to_str()
                )
            )
            assert False

    def to_str(self, verbose=False):
        """Compact representation of the schedule.

        Format:
        Schedule t:(<start_time>, <end_time>), e:<energy>
            [t:(<start_time>, <end_time>) <n> job(s), PEs: <cores_used>, e:<energy> ]
        where the format of <cores_used>: (<type>: <count>, ...)

        If verbose is True, it also returns the information of job segment mappings.
        """
        if self.is_empty():
            return "Schedule <Empty>"
        res = (
            f"Schedule t:({self.start_time:.3f}, {self.end_time:.3f}), "
            f"e:{self.energy:.3f}\n"
        )
        for segment in self._segments:
            res += f"    [t:({segment.start_time:.3f}, {segment.end_time:.3f}),"
            res += f" {len(segment.jobs())} job"
            if len(segment.jobs()) > 1:
                res += "s"
            core_types_str = ", ".join(
                [
                    f"{ty}: {count}"
                    for ty, count in sorted(
                        segment.get_used_processor_types().items()
                    )
                ]
            )
            res += f", PEs: [{core_types_str}], e:{segment.energy:.3f}]\n"
            if verbose:
                for job in segment.jobs():
                    res += f"        {job.to_str()}\n"
        return res

    def count_finished_jobs(self):
        return sum([ms[-1].finished for _, ms in self.per_requests().items()])

    def per_requests(self, none_as_idle=False):
        """Returns a dict of 'JobRequestInfo' objects involved in the schedule
        with the list of 'SingleJobSegmentMapping' objects. If 'none_as_idle' is
        true, add None values for the segment where the job was idle or finished.
        """
        res = {}
        for i, segment in enumerate(self._segments):
            for j in segment.jobs():
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
        """Returns a list of job segment mappings for of specific job request."""
        res = []
        for segment in self._segments:
            for j in segment.jobs():
                if j.request == request:
                    res.append(j)
        return res

    def get_requests(self):
        """Get active requests in the schedule."""
        res = set()
        for segment in self._segments:
            res.update(segment.get_requests())
        return res

    def is_request_completed(self, request):
        """Returns whether the request comleted in the current schedule."""
        for segment in self._segments:
            for j in segment.jobs():
                if j.request == request and j.finished:
                    return True
        return False

    def is_any_request_migrated(self):
        """Returns whether any job migrates in the schedule."""
        job_schedules = self.per_requests()
        for job, segments in job_schedules.items():
            rep = SimpleVectorRepresentation(job.app, self.platform)
            start_mapping_list = rep.toRepresentation(segments[0].mapping)
            itersegments = iter(segments)
            next(itersegments)
            for jm in itersegments:
                # Compare mappings here
                segment_mapping_list = rep.toRepresentation(jm.mapping)
                if start_mapping_list != segment_mapping_list:
                    return True
        return False

    def get_job_mappings(self):
        """Returns the pairs of jobs and used mappings during the schedule.

        The mappings are given without time ranges, and duplications. The order
        of the mappings is undefined, though implemented in the order appeared
        in the schedule.

        Returns: a dict of job and list of mappings.
        """
        job_schedules = self.per_requests()
        rdict = {}
        for job, segments in job_schedules.items():
            rep = SimpleVectorRepresentation(job.app, self.platform)
            job_mapping_list = []
            for segment in segments:
                mapping_vect = rep.toRepresentation(segment.mapping)
                # Check that it is not already included:
                already_included = any(
                    rep.toRepresentation(m) == mapping_vect
                    for m in job_mapping_list
                )
                if already_included:
                    continue
                job_mapping_list.append(segment.mapping)
            rdict[job] = job_mapping_list
        return rdict

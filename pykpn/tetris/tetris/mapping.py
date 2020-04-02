"""
This module implements mappings.
Mapping is represented as list of segments, each segment includes the mappings of each particular job.

Todo:
    1) Add verification of the mappings
    2) Compact printing
"""
import sys
import math

from functools import reduce

from pykpn.tetris.tetris.context import Context
from pykpn.tetris.tetris.tplatform import Platform

EPS = 0.00001

class JobSegmentMapping:
    """A mapping of a single job on a time segment.

    Each mapping is defined by the request id, time segment and the completion rates of the application at both ends of the time segment.

    Note: the constructor require that only one condition is satisfied
        1) end_time is not None
        2) end_cratio is not None
        3) finished is True

    Args:
        rid (int): Request id
        can_mapping_id (str): An id of canonical mapping
        start_time (float): Start time of a segment
        start_cratio (float): Completion rate at the beginning of the segment
        end_time (float): End time of a segment
        end_cratio (float): Completion rate at the end of the segment
        finished (bool): Whether application finished its execution during this segment.
    """
    def __init__(self, rid, can_mapping_id, start_time = 0.0, start_cratio = 0.0,
            end_time = None, end_cratio = None, finished = False):
        assert isinstance(rid, int)
        assert isinstance(start_time, (int, float)), "Start_time is of type {}, but must be float or int".format(type(start_time))
        assert isinstance(start_cratio, float)

        self.__rid = rid
        assert can_mapping_id is not None
        # Next two fields can be derived from each other
        self.__can_mapping_id = can_mapping_id

        self.__start_time = start_time
        self.__start_cratio = start_cratio

        self.__end_time = None
        self.__end_cratio = None
        self.__finished = None
        self.__energy = None

        if end_time is not None:
            assert end_cratio is None and not finished, "Only one argument must be set: end_time, end_cratio, finished"
            self.__init_by_end_time(end_time)
        elif end_cratio is not None:
            assert end_time is None and not finished, "Only one argument must be set: end_time, end_cratio, finished"
            self.__init_by_end_cratio(end_cratio)
        elif finished:
            assert end_cratio is None and end_time is None, "Only one argument must be set: end_time, end_cratio, finished"
            self.__init_finished()

        assert self.__end_time is not None
        assert self.__end_cratio is not None
        assert self.__end_cratio <= 1.0
        assert self.__end_cratio >= self.__start_cratio
        assert self.__finished is not None
        assert self.__energy is not None

    def __init_by_end_time(self, end_time):
        assert end_time >= self.__start_time, "end_time ({}) must be greater or equal then start_time ({})".format(end_time, self.__start_time)
        full_rem_time = self.can_mapping.time(
                start_cratio = self.__start_cratio)
        segment_time = end_time - self.__start_time
        if full_rem_time <= segment_time + EPS:
            self.__end_time = self.__start_time + full_rem_time
            self.__end_cratio = 1.0
            self.__finished = True
        else:
            self.__end_time = end_time
            self.__end_cratio = self.__start_cratio + segment_time / self.can_mapping.time()
            self.__finished = False
        self.__energy = self.can_mapping.energy(
                start_cratio = self.__start_cratio,
                end_cratio = self.__end_cratio)

    def __init_by_end_cratio(self, end_cratio):
        assert end_cratio >= self.__start_cratio
        rem_time = self.__can_mapping.time(
                start_cratio = self.__start_cratio,
                end_cratio = end_cratio)
        self.__end_time = self.__start_time + rem_time
        self.__end_cratio = end_cratio
        self.__finished = (end_cratio == 1.0)
        self.__energy = self.__can_mapping.energy(
                start_cratio = self.__start_cratio,
                end_cratio = end_cratio)

    def __init_finished(self):
        rem_time = self.can_mapping.time(
                start_cratio = self.__start_cratio)
        self.__end_time = self.__start_time + rem_time
        self.__end_cratio = 1.0
        self.__finished = True
        self.__energy = self.can_mapping.energy(
                start_cratio = self.__start_cratio)

    @property
    def rid(self):
        """int: The request id."""
        return self.__rid

    @property
    def request(self):
        """Request: The request."""
        return Context().req_table[self.__rid]

    @property
    def app(self):
        """Application: The application."""
        return Context().req_table[self.__rid].app()

    @property
    def can_mapping_id(self):
        """int: the id of canonical mapping."""
        return self.__can_mapping_id

    @property
    def can_mapping(self):
        """CanonicalMapping: the canonical mapping."""
        return Context().req_table[self.rid].app().mappings[self.can_mapping_id]

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

    @property
    def idle(self):
        """Returns whether the job is idle."""
        return self.__can_mapping_id == "__idle__"

    def __str__(self):
        core_types = self.can_mapping.core_types
        core_types_str = ", ".join(["{}: {}".format(ty, count) for ty,count in core_types])
        job_str = "Job: {} [{}]".format(self.rid, self.app.name)
        mapping_str = "mapping: {} [{}]".format(self.can_mapping_id, core_types_str)
        start_str = "start = {0:.3f} [{1:.2f}]".format(self.start_time, self.start_cratio)
        if self.finished:
            f_str = "F"
        else:
            f_str = ""
        end_str = "end = {:.3f} [{:.2f}{}]".format(self.end_time, self.end_cratio, f_str)
        energy_str = "energy = {:.3f}".format(self.energy)
        if self.idle:
            res_str = "{}, __idle__".format(job_str)
        else:
            res_str = "{}, {}, {}, {}, {}".format(job_str, mapping_str, start_str, end_str, energy_str)
        return res_str

    def dump_str(self, prefix = ""):
        return prefix + str(self)


class SegmentMapping:
    """All job mappings on a time segment.

    Mappings for different jobs are defined by SingleJobMapping objects.

    Args:
        platform (Platform): The platform model
        jobs (:obj:`list` of :obj:`SingleJobMapping`): A list of JobSegmentMapping objects
        time_range: Time range of the mapping
    """
    def __init__(self, platform, jobs = [], time_range = None):
        assert isinstance(platform, Platform)
        self.__platform = platform
        self.__time_range = time_range
        self.__jobs = []

        if len(jobs) > 0:
            # Initialized with a list of jobs' segment mappings

            # Identify the time range bounds
            min_start_time = min([x.start_time for x in jobs])
            max_end_time = max([x.end_time for x in jobs])
            if time_range is None:
                self.__set_time_range((min_start_time, max_end_time))
            else:
                assert min_start_time >= time_range[0] - EPS
                assert max_end_time <= time_range[1] + EPS
                self.__set_time_range(time_range)

            for jm in jobs:
                self.append_job(jm)
        elif time_range is not None:
            self.__set_time_range(time_range)

    def __set_time_range(self, t):
        assert isinstance(t, tuple)
        assert len(t) == 2
        assert isinstance(t[0], (int, float)) and isinstance(t[1], (int, float)), "Each element of tuple must be a type of int or float, but they are {} and {}".format(type(t[0]), type(t[1]))
        assert t[0] < t[1]
        self.__time_range = t

    @property
    def start_time(self):
        """float: The start time of the segment"""
        if self.__time_range is None:
            return None
        return self.__time_range[0]

    @property
    def end_time(self):
        """float: The end time of the segment"""
        if self.__time_range is None:
            return None
        return self.__time_range[1]

    @property
    def duration(self):
        """float: The duration of the segment."""
        return self.end_time - self.start_time

    @property
    def energy(self):
        """float: The consumed energy."""
        return sum([x.energy for x in self.__jobs])

    @property
    def used_core_types(self):
        """NamedDimensionalNumber: Number of used cores per type."""
        cores_used = reduce((lambda x, y: x + y),
                            [x.can_mapping.core_types for x in self.jobs()],
                            self.__platform.core_types(only_types = True))
        return cores_used

    def jobs(self):
        """list(JobSegmentMapping): Returns a shallow copy of job mappings."""
        return self.__jobs.copy()

    @property
    def finished(self):
        """bool: Whether all active jobs are finished during the current segment."""
        res = True
        for jm in self.__jobs:
            res = res and jm.finished
        return res

    def __iter__(self):
        yield from self.__jobs

    def __len__(self):
        return len(self.__jobs)

    def append_job(self, job, expand_time_range = False):
        """Add a new job mapping to the current object."""
        assert job is not None
        assert isinstance(job, JobSegmentMapping)

        cores_used = self.used_core_types + job.can_mapping.core_types

        ctr = self.__time_range
        if expand_time_range:
            # Update time range
            if ctr is None:
                new_start_time, new_end_time = job.start_time, job.end_time
            else:
                new_start_time = min(self.start_time, job.start_time)
                new_end_time = max(self.end_time, job.end_time)
            self.__set_time_range((new_start_time, new_end_time))
        else:
            # Check that time range is not violated
            assert job.start_time + EPS >= self.start_time
            assert job.end_time <= self.end_time + EPS, "Job's end_time ({}) must be not larger than the segment's end_time ({})".format(job.end_time, self.end_time)


        if cores_used <= self.__platform.core_types():
            self.__jobs.append(job)
        else:
            #print([ str(x) for x in self.__job_mappings])
            #print(job_mapping)
            assert False, "Cannot add a job mapping, not enough free resources"
        pass


    def split_at_time(self, time):
        """Split the current segment at time time.

        Args:
            time (float): Time to split the segment.

        Returns:
            A tupple with two mapping segment split at time `time`.
        """
        assert time < self.end_time and self.start_time < time, "Trying to split a segment at time {}, which is outside of the segment time range [{}, {})".format(time, self.start_time, self.end_time)
        m1 = SegmentMapping(self.__platform, time_range = (self.start_time, time))
        m2 = SegmentMapping(self.__platform, time_range = (time, self.end_time))
        for jm in self:
            jm1 = JobSegmentMapping(jm.rid, jm.can_mapping_id,
                start_time = jm.start_time,
                start_cratio = jm.start_cratio,
                end_time = time)
            m1.append_job(jm1)
            if jm1.finished:
                continue
            jm2 = JobSegmentMapping(jm.rid, jm.can_mapping_id,
                start_time = time,
                start_cratio = jm1.end_cratio,
                end_time = jm.end_time)
            m2.append_job(jm2)
        return m1, m2

    def max_full_subsegment_from_start(self):
        """Create a new mapping segment based on the current one, where the end_time is set to the shortest job."""
        shortest_end_time = min([x.end_time for x in self if not x.idle])
        m = SegmentMapping(self.__platform, time_range = (self.start_time, shortest_end_time))

        for jm in self:
            jm_new = JobSegmentMapping(jm.rid, jm.can_mapping_id,
                    start_time = jm.start_time,
                    start_cratio = jm.start_cratio,
                    end_time = shortest_end_time)
            m.append_job(jm_new)
        return m

    def legacy_str(self):
        res = "Time window: [{:.3f}, {:.3f}), Energy (Total): {:.3f} (MISSED)".format(
                self.start_time, self.end_time, self.energy) + "\n"
        for sm in self:
            res += "  " + str(sm) + "\n"
        return res

    def legacy_dump_str(self, prefix = ""):
        lines = self.legacy_str()
        return ''.join([prefix + x for x in lines.splitlines(True)])


class Mapping:
    """Application mapping.

    Describes the mapping application over time.
    """
    def __init__(self, segments = []):
        self.__segments = []

        assert isinstance(segments, list), "segments should be a type of list, but it is {}".format(type(segments))

        for s in segments:
            self.append_segment(s)

    @property
    def start_time(self):
        """float: The start time of the mapping."""
        if self.first is None:
            return None
        return self.first.start_time

    @property
    def end_time(self):
        """float: The end time of the mapping."""
        if self.last is None:
            return None
        return self.last.end_time

    @property
    def energy(self):
        """float: The energy consumption of the mapping"""
        return sum([x.energy for x in self.__segments], 0.0)

    @property
    def first(self):
        """SegmentMapping: the first segment mapping"""
        if len(self.__segments) == 0:
            return None
        return self.__segments[0]

    @property
    def last(self):
        """SegmentMapping: the last segment mapping"""
        if len(self.__segments) == 0:
            return None
        return self.__segments[-1]

    def segments(self):
        """list(SegmentMapping): Returns a shallow copy of mapping segments"""
        return self.__segments.copy()

    def copy(self):
        """Mapping: Returns a shallow copy of the mapping"""
        return Mapping(self.__segments)

    def append_segment(self, segment):
        self.__segments.append(segment)

    def insert_segment(self, index, segment):
        """Insert a segment into mapping.

        Args:
            index (int): The position where a segment needs to be inserted
            segment (SegmentMapping): The segment to insert.
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

    @staticmethod
    def __str_jobs(job_list, segment, end = False):
        finished_jobs = []
        # Collect all jobs into a list
        for job in segment:
            jstr = "{}(".format(job.rid)
            if not end:
                if job.idle:
                    jstr += 'idle,'
                else:
                    jstr += '{},'.format(job.can_mapping_id)
                if job.start_cratio < EPS:
                    jstr += 'S)'
                else:
                    jstr += '{0:.2f})'.format(job.start_cratio)
            else:
                if job.finished:
                    jstr += 'F)'
                else:
                    jstr += '{0:.2f})'.format(job.end_cratio)
            job_list.append(tuple((job.rid, jstr)))
            if job.finished:
                fstr = "{}(F)".format(job.rid)
                finished_jobs.append(tuple((job.rid, fstr)))
        return job_list, finished_jobs


    def __str__(self):
        """Compact representation of the scheduling.

        Format:
        Scheduling e:<energy_value> [t:<timestamp> RID(mapping,cratio) .. ] -> .. -> [t:<timestamp> RID(F) ..]
        - If the job is finished, print RID(F), where RID is a request id
        - All jobs are sorted by their RID
        """
        res = "Scheduling e:{0:.3f}".format(self.energy)
        finished_jobs = []
        for idx, segment in enumerate(self):
            if idx != 0:
                res += " ->"
            res += " [t:{0:.2f} ".format(segment.start_time)
            # Copy a list of finished jobs into new list
            sjl = finished_jobs.copy()
            sjl, finished_jobs = Mapping.__str_jobs(sjl, segment)
            sjl.sort(key=lambda x: x[0])
            res += " ".join([x[1] for x in sjl])
            res += ']'

        # process the end of the last segment
        res += " -> [t:{0:.2f} ".format(segment.end_time)
        sjl, _  = Mapping.__str_jobs([], self.last, end=True)
        sjl.sort(key=lambda x: x[0])
        res += " ".join([x[1] for x in sjl])
        res += ']'
        return res

    def legacy_str(self):
        assert self.last is not None
        res = self.last.legacy_str()
        return res

    def legacy_dump_str(self, prefix = ""):
        res = ""
        for segment in self:
            res += segment.legacy_dump_str(prefix = prefix) + '\n'
        return res.strip()

    def legacy_dump(self, outf = sys.stdout, prefix = ""):
        print(self.legacy_dump_str(prefix=prefix), file=outf)

    def get_job_end_cratio(self, rid):
        """Returns the job cratio."""
        for segment in reversed(self.__segments):
            for j in segment:
                if j.rid == rid:
                    return j.end_cratio
        return None


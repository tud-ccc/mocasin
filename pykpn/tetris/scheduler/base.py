# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import Schedule

from abc import ABC, abstractmethod


class SegmentSchedulerBase(ABC):
    def __init__(self, parent_scheduler, platform):
        assert isinstance(parent_scheduler, SchedulerBase)
        self.__parent_scheduler = parent_scheduler
        self.__platform = platform

    @property
    def platform(self):
        return self.__platform

    @abstractmethod
    def schedule(self, jobs):
        pass


class SchedulerBase(ABC):
    def __init__(self, platform, migrations=True, preemptions=True):
        """A base class for tetris scheduler

        Args:
            platform (Platform): a platform
            migrations (bool): whether scheduler can migrate processes
            preemptions (bool): whether scheduler can preempt processes
        """
        self.__platform = platform
        self.__migrations = migrations
        self.__preemptions = preemptions
        super().__init__()

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def platform(self):
        return self.__platform

    @property
    def migrations(self):
        return self.__migrations

    @property
    def preemptions(self):
        return self.__preemptions

    @abstractmethod
    def schedule(self, jobs, scheduling_start_time=0.0):
        """ Schedule jobs.

        Args:
            jobs (list[JobState]): input jobs
            scheduling_start_time (float): a start time
        """
        pass


class SingleVariantSegmentScheduler(SegmentSchedulerBase):
    def __init__(self, parent_scheduler, platform):
        assert isinstance(parent_scheduler, SingleVariantSegmentizedScheduler)
        super().__init__(parent_scheduler, platform)


class SingleVariantSegmentizedScheduler(SchedulerBase):
    """Greedy scheduler.

    The scheduler generates a schedule iteratively from schedule segments by
    invocating a segment scheduler.

    Args:
        platform (Platform): A platform
        segment_scheduler: A segment scheduler
    """
    def __init__(self, platform, segment_scheduler):
        super().__init__(platform)
        assert isinstance(segment_scheduler, SingleVariantSegmentScheduler)
        self.__segment_scheduler = segment_scheduler

    @property
    def segment_scheduler(self):
        return self.__segment_scheduler

    def schedule(self, jobs, scheduling_start_time=0.0):
        """Run a segmentized scheduler"""

        # Init mapping
        schedule = Schedule(self.platform)
        cjobs = jobs.copy()
        ctime = scheduling_start_time

        while cjobs is not None and len(cjobs) > 0:
            res_segment = self.segment_scheduler.schedule(
                cjobs, segment_start_time=ctime)
            if res_segment is None:
                # No feasible segment found
                cjobs = None
                break
            new_segment, cjobs = res_segment
            schedule.append_segment(new_segment)
            ctime = schedule.end_time

        if cjobs is not None:
            return schedule
        return None

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.job_state import Job
from pykpn.tetris.orbit_lookup import OrbitLookupManager
from pykpn.tetris.schedule import Schedule

from abc import ABC, abstractmethod


class SegmentSchedulerBase(ABC):
    def __init__(self, scheduler, platform):
        assert isinstance(scheduler, SchedulerBase)
        self.scheduler = scheduler
        self.platform = platform

    @abstractmethod
    def schedule(self, jobs):
        pass


class SchedulerBase(ABC):
    def __init__(self, platform, orbit_lookup_manager=None, migrations=True,
                 preemptions=True, rotations=False):
        """A base class for tetris scheduler

        If rotations is False, the scheduler does not rotate the mappings. In
        the final scheduler it is only checked that total number of used cores
        of corresponding type does not exceed the number of cores in the
        platform.

        If orbit_lookup is None, then a new orbit lookup manager will be
        constructed. Otherwise, it will use one supplied, which is useful in
        case jobs scheduled several times.

        Args:
            platform (Platform): a platform
            orbit_lookup (OrbitLookupManager): an orbit lookup manager
            migrations (bool): whether scheduler can migrate processes
            preemptions (bool): whether scheduler can preempt processes
            rotations (bool): whether the scheduler rotate the mappings
        """
        self.__platform = platform
        self.__migrations = migrations
        self.__preemptions = preemptions
        self.__rotations = rotations
        if orbit_lookup_manager is None:
            orbit_lookup_manager = OrbitLookupManager(self.platform)
        self.__orbit_lookup_manager = orbit_lookup_manager

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

    @property
    def rotations(self):
        return self.__rotations

    @property
    def orbit_lookup_manager(self):
        return self.__orbit_lookup_manager

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

# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

from abc import ABC, abstractmethod

from mocasin.tetris.job_state import Job
from mocasin.tetris.orbit_lookup import OrbitLookupManager
from mocasin.tetris.schedule import Schedule
from mocasin.tetris.variant import CounterVariantSelector


class SegmentMapperBase(ABC):
    def __init__(self, scheduler, platform):
        """Segment Mapper base class.

        This class generates a multi job segment mapping.
        """
        assert isinstance(scheduler, SchedulerBase)
        self.scheduler = scheduler
        self.platform = platform

    @abstractmethod
    def generate_segment(self, jobs):
        """Generate a multi job segment mapping."""
        pass


class SchedulerBase(ABC):
    def __init__(
        self,
        platform,
        orbit_lookup_manager=None,
        migrations=True,
        preemptions=True,
        rotations=False,
        **kwargs
    ):
        """A base class for tetris scheduler.

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
        super().__init__()
        self.platform = platform
        self._migrations = migrations
        self._preemptions = preemptions
        self._rotations = rotations
        if orbit_lookup_manager is None:
            orbit_lookup_manager = OrbitLookupManager(self.platform)
        self._orbit_lookup_manager = orbit_lookup_manager
        self.variant_selector = CounterVariantSelector(self.platform)

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def migrations(self):
        return self._migrations

    @property
    def preemptions(self):
        return self._preemptions

    @property
    def rotations(self):
        return self._rotations

    @property
    def orbit_lookup_manager(self):
        return self._orbit_lookup_manager

    @abstractmethod
    def schedule(self, jobs, scheduling_start_time=0.0):
        """Schedule jobs.

        Args:
            jobs (list[JobState]): input jobs
            scheduling_start_time (float): a start time
        """
        pass


class SegmentedScheduler(SchedulerBase):
    """Single Variant Segmented scheduler.

    The scheduler generates a schedule iteratively from schedule segments by
    invocating a segment mapper.

    Args:
        platform (Platform): A platform
        segment_mapper: A segment scheduler
    """

    def __init__(self, platform, segment_mapper):
        super().__init__(platform)
        assert isinstance(segment_mapper, SegmentMapperBase)
        self.segment_mapper = segment_mapper

    def schedule(self, jobs, scheduling_start_time=0.0):
        """Run a segmentized scheduler"""

        # Init mapping
        schedule = Schedule(self.platform)
        cjobs = jobs.copy()
        ctime = scheduling_start_time

        while cjobs is not None and len(cjobs) > 0:
            res_segment = self.segment_mapper.generate_segment(
                cjobs, segment_start_time=ctime
            )
            if res_segment is None:
                # No feasible segment found
                cjobs = None
                break
            new_segment, cjobs = res_segment
            schedule.add_segment(new_segment)
            ctime = schedule.end_time

        if cjobs is not None:
            return schedule
        return None

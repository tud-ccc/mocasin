from pykpn.common.platform import Platform
from pykpn.tetris.apptable import AppTable
from pykpn.tetris.job import JobTable
from pykpn.tetris.mapping import Mapping, SegmentMapping

import abc


class SegmentMapperBase(abc.ABC):
    def __init__(self, parent_scheduler, platform):
        assert isinstance(parent_scheduler, SchedulerBase)
        assert isinstance(platform, Platform)
        self.__parent_scheduler = parent_scheduler
        self.__platform = platform

    @property
    def platform(self):
        return self.__platform

    @abc.abstractmethod
    def schedule(self, jobs):
        pass


class SchedulerBase(abc.ABC):
    def __init__(self, app_table, platform):
        """Generates a schedule.

        :param app_table: a table with applications
        :type app_table: AppTable
        :param platform: a platform
        :type platform: Platform
        """
        assert isinstance(app_table, AppTable)
        assert isinstance(platform, Platform)
        self.__platform = platform
        self.__app_table = app_table
        super().__init__()

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    def platform(self):
        return self.__platform

    @abc.abstractmethod
    def schedule(self, jobs):
        pass


class SingleVariantSegmentMapper(SegmentMapperBase):
    def __init__(self, parent_scheduler, platform):
        assert isinstance(parent_scheduler, SingleVariantSegmentizedScheduler)
        super().__init__(parent_scheduler, platform)


class SingleVariantSegmentizedScheduler(SchedulerBase):
    """Greedy scheduler.

    The scheduler generates the mapping segment by segment by invocating
    a segment mapper. The segment mapper returns a single mapping segment.

    Args:
        platform (Platform): A platform
        segment_mapper: A segment mapper
    """
    def __init__(self, app_table, platform, segment_mapper):
        super().__init__(app_table, platform)
        assert isinstance(segment_mapper, SingleVariantSegmentMapper)
        self.__segment_mapper = segment_mapper

    def schedule(self, start_jobs):
        """Run a segmentized scheduler"""

        # Init mapping
        scheduling = Mapping()
        finished = False

        while not finished:
            # While there is at least one non-finished job

            # Initialize job table
            if len(scheduling) > 0:
                jobs = JobTable.from_mapping(scheduling)
            else:
                jobs = start_jobs.copy()

            # Generate a new segment
            new_segment = self.__segment_mapper.schedule(jobs)

            if new_segment is None:
                # No feasible segment found
                finished = True
                feasible = False
                break

            assert isinstance(new_segment, SegmentMapping)
            scheduling.append_segment(new_segment)

            if new_segment.finished:
                # All jobs finished
                finished = True
                feasible = True

        assert finished

        if not feasible:
            return False, None, True
        else:
            return True, scheduling, True

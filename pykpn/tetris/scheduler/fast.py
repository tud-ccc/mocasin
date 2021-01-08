# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

from pykpn.tetris.job_state import Job
from pykpn.tetris.schedule import (Schedule, ScheduleSegment,
                                   JobSegmentMapping, MAX_END_GAP)
from pykpn.tetris.scheduler.base import (SingleVariantSegmentScheduler,
                                         SingleVariantSegmentizedScheduler)

import logging
import math

log = logging.getLogger(__name__)


class FastSegmentScheduler(SingleVariantSegmentScheduler):
    """ TODO: Add a description"""
    def __init__(self, scheduler, platform):

        super().__init__(scheduler, platform)

    def _filter_job_mappings_by_deadline_resources(self, job, free_cores):
        """ Filters mappings which can feet deadline resources.

        Args:
            job (Job): a job
            free_cores (Counter): a counter of available core types

        Returns: a list of mappings satisfying deadline and resources
        conditions.
        """
        # TODO: This function is similar to Medf?
        res = []
        rratio = 1.0 - job.cratio
        rdeadline = job.request.deadline - self.__segment_start_time
        for m in job.request.mappings:
            m_cores = m.get_used_processor_types()
            # filter by deadline
            rtime = rratio * m.metadata.exec_time
            if rtime > rdeadline:
                continue
            # filter by resources
            if (m_cores | free_cores) != free_cores:
                continue
            res.append(m)
        return res

    def _form_schedule_segment(self, job_mappings):
        # TODO: This function is very similar to one in Bruteforce.
        # Consider placing it in a base class
        """ Generate a schedule segment out of job_mappings.

        Args:
            job_mappings (dict): a dict of job mappings
        """

        # Skip mappings with all idle jobs
        if all(m is None for m in job_mappings.values()):
            return None

        # Calculate segment end time
        jobs_rem_time = [
            m.metadata.exec_time * (1.0 - j.cratio)
            for j, m in job_mappings.items() if m is not None
        ]
        segment_duration = max(
            [t for t in jobs_rem_time if t < min(jobs_rem_time) + MAX_END_GAP])
        segment_end_time = segment_duration + self.__segment_start_time

        # Construct JobSegmentMapping objects
        job_segments = []
        for j, m in job_mappings.items():
            if m is not None:
                ssm = JobSegmentMapping(j.request, m,
                                        start_time=self.__segment_start_time,
                                        start_cratio=j.cratio,
                                        end_time=segment_end_time)
                job_segments.append(ssm)

        # Construct a schedule segment
        new_segment = ScheduleSegment(self.platform, job_segments)
        new_segment.verify(only_counters=not self.scheduler.rotations)
        return new_segment

    def schedule(self, jobs, segment_start_time=0.0):
        self.__segment_start_time = segment_start_time

        job_mappings = {}
        avl_core_types = self.platform.get_processor_types()

        while any(j not in job_mappings for j in jobs):
            log.debug("Free cores: {}".format(avl_core_types))
            # List of mappings to finish the applications
            to_finish = {}
            diff = (-math.inf, None)
            for job in jobs:
                # Skip jobs with found mappings
                if job in job_mappings:
                    continue
                to_finish[job] = (
                    self._filter_job_mappings_by_deadline_resources(
                        job, avl_core_types))
                to_finish[job].sort(key=lambda m: m.metadata.energy)
                log.debug("to_finish[{}]: {}".format(job.to_str(), [
                    m.metadata.energy * (1.0 - job.cratio)
                    for m in to_finish[job]
                ]))
                if len(to_finish[job]) == 0:
                    job_mappings[job] = None
                    continue
                if len(to_finish[job]) == 1:
                    diff = (math.inf, job)
                    continue
                # Check energy difference between first two mappings
                cdiff = (1.0 -
                         job.cratio) * (to_finish[job][1].metadata.energy -
                                        to_finish[job][0].metadata.energy)
                if cdiff > diff[0]:
                    diff = (cdiff, job)
            _, job_d = diff
            if job_d is None:
                return None
            log.debug("Choose {}".format(job_d.to_str()))
            # On Odroid XU-4, the check that it can be scheduled is simple.
            # All mappings in to_finish are valid.
            m = to_finish[job_d][0]
            avl_core_types -= m.get_used_processor_types()
            job_mappings[job_d] = m
            log.debug('Job_mappings: {}'.format([
                (j.to_str(), m.get_used_processor_types(),
                 m.metadata.energy * (1.0 - j.cratio)) if m is not None else
                (j.to_str(), None) for j, m in job_mappings.items()
            ]))

        segment = self._form_schedule_segment(job_mappings)
        # TODO: this is copied from bruteforce, put it in a separate functions
        if segment is None:
            return None

        # Check that all jobs meet dealines
        for js in segment:
            if js.end_time > js.request.deadline:
                return None

        # Generate the job states at the end of the segment
        new_jobs = [
            x
            for x in Job.from_schedule(Schedule(self.platform, segment), jobs)
            if not x.is_terminated()
        ]

        # Check whether all remaining jobs still meet deadlines
        if not all(j.can_meet_deadline(segment.end_time) for j in new_jobs):
            return None

        return segment, new_jobs


class FastScheduler(SingleVariantSegmentizedScheduler):
    def __init__(self, platform, **kwargs):
        """Fast scheduler.

        :param platform: a platform
        :type platform: Platform
        """
        segment_mapper = FastSegmentScheduler(self, platform)
        super().__init__(platform, segment_mapper)

    @property
    def name(self):
        return "FAST"

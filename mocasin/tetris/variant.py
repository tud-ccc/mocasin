# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import copy

from mocasin.representations import SimpleVectorRepresentation
from mocasin.tetris.schedule import (
    Schedule,
    MultiJobSegmentMapping,
    SingleJobSegmentMapping,
)


class BaseVariantSelector:
    """Base Variant Selector class.

    Finalize the schedule by selecting non-overlapped mapping variants in each
    segment.
    """

    def __init__(self, platform):
        self.platform = platform

    def finalize_schedule(self, schedule):
        """Finalize the schedule.

        This method takes the schedule consisting of the canonical mappings.
        The output returns the schedule, where no mappings overlap in the same
        segment, and each transformed mapping is equivalent to the original one.
        """
        raise NotImplementedError(
            "This method needs to be overridden by a subclass"
        )


def _update_job_segment_mapping(job, mapping):
    """Copy a job segment with the new mapping."""
    return SingleJobSegmentMapping(
        job.request,
        mapping,
        start_time=job.start_time,
        start_cratio=job.start_cratio,
        end_time=job.end_time,
    )


class CounterVariantSelector(BaseVariantSelector):
    """Counter-based Variant Selector.

    Finalize the schedule by selecting non-overlapped mapping variants in each
    segment. In this version, the mapping variant is selected by choosing the
    first available cores in the list. If the preselected operating point for
    the application is the same during subsequent segments, the variant selector
    selects a single variant on these segments.
    """

    def __init__(self, platform):
        super().__init__(platform)
        self._processor_id = {}
        for index, processor in enumerate(sorted(platform.processors())):
            self._processor_id[processor] = index

    def finalize_schedule(self, schedule):
        """Finalize the schedule.

        This method takes the schedule consisting of the canonical mappings.
        The output returns the schedule, where no mappings overlap in the same
        segment, and each transformed mapping is equivalent to the original one.
        """
        if not schedule:
            return None
        # TODO: Check that the transformed mapping is equivalent. (Check that
        # SymmetryRepresentation does not create the whole orbit for that.)
        rotated_schedule = Schedule(self.platform)
        prev_segment = None
        prev_rotated = None
        for segment in schedule.segments():
            rotated_segment = self._finalize_segment(
                segment, prev=prev_segment, prev_rotated=prev_rotated
            )
            rotated_schedule.add_segment(rotated_segment)
            prev_segment = segment
            prev_rotated = rotated_segment
        return rotated_schedule

    def _finalize_segment(self, segment, prev=None, prev_rotated=None):
        """Rotate mappings in the segment.

        This method is called during the schedule finalization.

        Args:
            segment (MultiJobSegmentMapping): a segment to be transformed
            prev (MultiJobSegmentMapping): a previous segment in the original
                schedule
            prev_rotated (MultiJobSegmentMapping): a rotated segment variant of
                `prev`.
        """
        rotated_segment = MultiJobSegmentMapping(self.platform)

        processors = set(self.platform.processors())
        # Find jobs with equal mappings as in previous one
        keep_mapping = self._find_keeping_mappings(segment, prev)

        for job in keep_mapping:
            prev_job = prev_rotated.find_job_segment(job.request)
            rotated_job = _update_job_segment_mapping(job, prev_job.mapping)
            rotated_segment.append_job(rotated_job)
            # update available processors
            processors = processors - prev_job.mapping.get_used_processors()

        for job in segment.jobs():
            if job in keep_mapping:
                continue
            rotated_mapping = self._adjust_mapping_to_processors(
                job.mapping, processors
            )
            rotated_job = _update_job_segment_mapping(job, rotated_mapping)
            rotated_segment.append_job(rotated_job)
            # update available processors
            processors = processors - rotated_mapping.get_used_processors()
        return rotated_segment

    def _adjust_mapping_to_processors(self, mapping, processors):
        """Adjust mapping to the given processors."""
        mapping_pes = mapping.get_used_processors()

        # If the current mapping fits the given processor list, use it.
        if mapping_pes.issubset(processors):
            return mapping

        available_pe_dict = {}
        for pe in sorted(processors):
            if pe.type not in available_pe_dict:
                available_pe_dict[pe.type] = []
            available_pe_dict[pe.type].append(pe)

        mapping_pe_dict = {}
        for pe in mapping_pes:
            if pe.type not in mapping_pe_dict:
                mapping_pe_dict[pe.type] = []
            mapping_pe_dict[pe.type].append(pe)

        perm = {}
        for ptype, cores in mapping_pe_dict.items():
            available = available_pe_dict[ptype]
            if len(cores) > len(available):
                raise RuntimeError(
                    f"Not enough available processors of the type {ptype}"
                )
            for in_core, out_core in zip(cores, available):
                perm[in_core] = out_core

        return self._permutate_mapping(mapping, perm)

    def _permutate_mapping(self, mapping, perm):
        # This custom permutation is probably better to implement in one of
        # the representations. TODO: Consider it
        rep = SimpleVectorRepresentation(mapping.graph, self.platform)
        mapping_list = rep.toRepresentation(mapping)

        _perm = {}
        for k, v in perm.items():
            _perm[self._processor_id[k]] = self._processor_id[v]

        rotated_list = list(map(lambda x: _perm[x], mapping_list))
        rotated_mapping = rep.fromRepresentation(rotated_list)
        rotated_mapping.metadata = copy.copy(mapping.metadata)
        return rotated_mapping

    def _find_keeping_mappings(self, segment, prev):
        """Find jobs which use the same mapping as in a previous segment."""
        res = []
        if not prev:
            return res

        for job in segment.jobs():
            job_prev = prev.find_job_segment(job.request)
            if not job_prev:
                continue
            if job.mapping == job_prev.mapping:
                res.append(job)
        return res

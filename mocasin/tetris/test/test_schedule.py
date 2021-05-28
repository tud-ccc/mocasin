# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Robert Khasanov

import pytest

from mocasin.tetris.schedule import MultiJobSegmentMapping, Schedule


class TestSchedule:
    def setUp(self, platform):
        pass

    def tearDown(self):
        pass

    def test_create(self, platform):
        schedule = Schedule(platform)
        assert not schedule.segments()

    def test_create_segments(self, platform, mocker):
        segment = mocker.Mock(spec=MultiJobSegmentMapping)
        segment.start_time = 0
        segment.end_time = 10
        schedule = Schedule(platform, [segment])
        assert len(schedule.segments()) == 1

    def test_add_segment(self, platform, mocker):
        segment1 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment1.start_time = 0
        segment1.end_time = 10
        segment2 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment2.start_time = 10
        segment2.end_time = 20
        segment3 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment3.start_time = 20
        segment3.end_time = 30
        schedule = Schedule(platform)
        # insert the segment in the arbitrary order
        # in the end the segments should be ordered
        schedule.add_segment(segment1)
        assert len(schedule.segments()) == 1
        schedule.add_segment(segment3)
        assert len(schedule.segments()) == 2
        schedule.add_segment(segment2)
        assert len(schedule.segments()) == 3
        assert schedule._segments[0] == segment1
        assert schedule._segments[1] == segment2
        assert schedule._segments[2] == segment3

    def test_add_segment_overlap(self, platform, mocker):
        segment = mocker.Mock(spec=MultiJobSegmentMapping)
        segment.start_time = 10
        segment.end_time = 20
        segment1 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment1.start_time = 19
        segment1.end_time = 21
        segment2 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment2.start_time = 9
        segment2.end_time = 11
        segment3 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment3.start_time = 14
        segment3.end_time = 16
        segment4 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment4.start_time = 5
        segment4.end_time = 25
        segment5 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment5.start_time = 10
        segment5.end_time = 20
        segment6 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment6.start_time = 10
        segment6.end_time = 25

        schedule = Schedule(platform)
        schedule.add_segment(segment)

        with pytest.raises(RuntimeError):
            schedule.add_segment(segment1)
        with pytest.raises(RuntimeError):
            schedule.add_segment(segment2)
        with pytest.raises(RuntimeError):
            schedule.add_segment(segment3)
        with pytest.raises(RuntimeError):
            schedule.add_segment(segment4)
        with pytest.raises(RuntimeError):
            schedule.add_segment(segment5)
        with pytest.raises(RuntimeError):
            schedule.add_segment(segment6)

    def test_remove_segment(self, platform, mocker):
        segment1 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment1.start_time = 0
        segment1.end_time = 10
        segment2 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment2.start_time = 10
        segment2.end_time = 20
        schedule = Schedule(platform)
        schedule.add_segment(segment1)
        schedule.add_segment(segment2)
        assert len(schedule.segments()) == 2
        schedule.remove_segment(segment1)
        assert len(schedule.segments()) == 1
        schedule.remove_segment(segment2)
        assert len(schedule.segments()) == 0

    def test_remove_segment_raises(self, platform, mocker):
        segment1 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment1.start_time = 0
        segment1.end_time = 10
        segment2 = mocker.Mock(spec=MultiJobSegmentMapping)
        segment2.start_time = 10
        segment2.end_time = 20
        schedule = Schedule(platform)
        schedule.add_segment(segment1)
        with pytest.raises(RuntimeError):
            schedule.remove_segment(segment2)
        schedule.remove_segment(segment1)
        with pytest.raises(RuntimeError):
            schedule.remove_segment(segment1)
